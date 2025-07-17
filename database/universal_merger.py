"""
Universal database merger that works with SQLite or Supabase
Uses the adapter pattern for easy switching between databases
"""

import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
from scrapers.common import AITool
from database.adapters import DatabaseAdapter, create_database_adapter


class UniversalMerger:
    """Universal merger that works with any database adapter"""
    
    def __init__(self, use_sqlite: bool = True):
        self.adapter = create_database_adapter(use_sqlite)
        self.database_type = "SQLite" if use_sqlite else "Supabase"
        
        # Test connection
        if not self.adapter.connect():
            raise ConnectionError(f"Failed to connect to {self.database_type} database")
    
    def merge_and_upsert_tools(self, tools: List[AITool]) -> Dict[str, int]:
        """
        Merge and upsert tools with advanced deduplication
        
        Args:
            tools: List of tools to insert/update
            
        Returns:
            Dict with statistics: {'inserted': n, 'updated': n, 'errors': n, 'merged': n}
        """
        stats = {'inserted': 0, 'updated': 0, 'errors': 0, 'merged': 0}
        
        if not tools:
            print("⚠️ No tools to process")
            return stats
        
        print(f"🔄 Processing {len(tools)} tools with {self.database_type} database...")
        
        # First, deduplicate within the batch
        deduplicated_tools = self._deduplicate_tools_batch(tools)
        print(f"🧹 Internal deduplication: {len(tools)} -> {len(deduplicated_tools)} tools")
        
        for i, tool in enumerate(deduplicated_tools):
            try:
                # Update timestamp
                tool.last_scraped = datetime.now()
                
                # Generate content hash
                content_hash = self._generate_content_hash(tool)
                
                # Look for duplicates in database
                existing_tool = self.adapter.find_duplicate_tool(tool)
                
                if existing_tool:
                    # Merge data intelligently
                    merged_tool = self._merge_tool_data(existing_tool, tool)
                    
                    # Check if there are changes after merge
                    merged_hash = self._generate_content_hash(merged_tool)
                    if existing_tool.get('content_hash') != merged_hash:
                        # Update with merged data
                        if self.adapter.update_tool(existing_tool['id'], merged_tool, merged_hash):
                            stats['updated'] += 1
                            print(f"🔄 [{i+1}/{len(deduplicated_tools)}] Updated (merged): {tool.name}")
                        else:
                            stats['errors'] += 1
                    else:
                        # No content changes, just update timestamp
                        existing_tool['last_scraped'] = datetime.now().isoformat()
                        existing_tool['content_hash'] = merged_hash
                        if self.adapter.update_tool(existing_tool['id'], merged_tool, merged_hash):
                            stats['merged'] += 1
                            print(f"⏭️ [{i+1}/{len(deduplicated_tools)}] Timestamp updated: {tool.name}")
                        else:
                            stats['errors'] += 1
                else:
                    # Insert new tool
                    if self.adapter.insert_tool(tool, content_hash):
                        stats['inserted'] += 1
                        print(f"✅ [{i+1}/{len(deduplicated_tools)}] Inserted: {tool.name}")
                    else:
                        stats['errors'] += 1
                
            except Exception as e:
                stats['errors'] += 1
                print(f"❌ [{i+1}/{len(deduplicated_tools)}] Error processing {tool.name}: {e}")
                continue
        
        print(f"\n📊 Results: {stats['inserted']} inserted, {stats['updated']} updated, {stats['merged']} merged, {stats['errors']} errors")
        return stats
    
    def _deduplicate_tools_batch(self, tools: List[AITool]) -> List[AITool]:
        """Deduplicate tools within the batch by URL or name"""
        seen_tools = {}
        deduplicated = []
        
        for tool in tools:
            # Deduplication keys
            url_key = tool.url.lower().strip() if tool.url else None
            name_key = tool.name.lower().strip() if tool.name else None
            
            # Look for duplicates
            duplicate_key = None
            if url_key and url_key in seen_tools:
                duplicate_key = url_key
            elif name_key and name_key in seen_tools:
                duplicate_key = name_key
            
            if duplicate_key:
                # Merge with existing duplicate
                existing_tool = seen_tools[duplicate_key]
                merged_tool = self._merge_tool_objects(existing_tool, tool)
                seen_tools[duplicate_key] = merged_tool
                
                # Update in deduplicated list
                for j, existing in enumerate(deduplicated):
                    if existing == existing_tool:
                        deduplicated[j] = merged_tool
                        break
            else:
                # Add new tool
                if url_key:
                    seen_tools[url_key] = tool
                if name_key:
                    seen_tools[name_key] = tool
                deduplicated.append(tool)
        
        return deduplicated
    
    def _merge_tool_data(self, existing_dict: Dict[str, Any], new_tool: AITool) -> AITool:
        """Merge existing database record with new tool data"""
        # Convert dict to AITool (handling JSON fields)
        existing_tool = self._dict_to_aitool(existing_dict)
        
        # Merge objects
        return self._merge_tool_objects(existing_tool, new_tool)
    
    def _dict_to_aitool(self, data: Dict[str, Any]) -> AITool:
        """Convert database dict to AITool (handle JSON fields properly)"""
        import json
        
        # Handle JSON fields
        categories = data.get('categories', [])
        if isinstance(categories, str):
            try:
                categories = json.loads(categories)
            except:
                categories = []
        
        platform = data.get('platform', [])
        if isinstance(platform, str):
            try:
                platform = json.loads(platform)
            except:
                platform = []
        
        features = data.get('features')
        if isinstance(features, str):
            try:
                features = json.loads(features)
            except:
                features = None
        
        # Handle datetime
        last_scraped = data.get('last_scraped')
        if isinstance(last_scraped, str):
            try:
                last_scraped = datetime.fromisoformat(last_scraped.replace('Z', '+00:00'))
            except:
                last_scraped = None
        
        return AITool(
            ext_id=data.get('ext_id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            price=data.get('price', ''),
            popularity=data.get('popularity', 0),
            categories=categories,
            source=data.get('source', ''),
            macro_domain=data.get('macro_domain', 'OTHER'),
            url=data.get('url'),
            logo_url=data.get('logo_url'),
            rank=data.get('rank'),
            upvotes=data.get('upvotes'),
            monthly_users=data.get('monthly_users'),
            editor_score=data.get('editor_score'),
            maturity=data.get('maturity'),
            platform=platform,
            features=features,
            last_scraped=last_scraped
        )
    
    def _merge_tool_objects(self, existing: AITool, new: AITool) -> AITool:
        """Merge two AITool objects intelligently"""
        # Keep longer description
        description = new.description if (new.description and len(new.description) > len(existing.description or "")) else existing.description
        
        # Keep larger numeric values (except rank where smaller is better)
        popularity = max(existing.popularity, new.popularity)
        rank = self._min_optional(existing.rank, new.rank)  # Smaller rank is better
        upvotes = self._max_optional(existing.upvotes, new.upvotes)
        monthly_users = self._max_optional(existing.monthly_users, new.monthly_users)
        editor_score = self._max_optional(existing.editor_score, new.editor_score)
        
        # Combine lists
        categories = list(set((existing.categories or []) + (new.categories or [])))
        platform = list(set((existing.platform or []) + (new.platform or [])))
        
        # Combine features
        features = {}
        if existing.features:
            features.update(existing.features)
        if new.features:
            features.update(new.features)
        
        return AITool(
            ext_id=existing.ext_id,  # Keep original ID
            name=new.name or existing.name,
            description=description,
            price=new.price or existing.price,
            popularity=popularity,
            categories=categories,
            source=existing.source,  # Keep original source
            macro_domain=new.macro_domain or existing.macro_domain,
            url=new.url or existing.url,
            logo_url=new.logo_url or existing.logo_url,
            rank=rank,
            upvotes=upvotes,
            monthly_users=monthly_users,
            editor_score=editor_score,
            maturity=new.maturity or existing.maturity,
            platform=platform,
            features=features if features else None,
            last_scraped=new.last_scraped or existing.last_scraped
        )
    
    def _max_optional(self, val1: Optional[int], val2: Optional[int]) -> Optional[int]:
        """Return the larger of two optional values"""
        if val1 is None and val2 is None:
            return None
        if val1 is None:
            return val2
        if val2 is None:
            return val1
        return max(val1, val2)
    
    def _min_optional(self, val1: Optional[int], val2: Optional[int]) -> Optional[int]:
        """Return the smaller of two optional values"""
        if val1 is None and val2 is None:
            return None
        if val1 is None:
            return val2
        if val2 is None:
            return val1
        return min(val1, val2)
    
    def _generate_content_hash(self, tool: AITool) -> str:
        """Generate hash of tool content for change detection"""
        content_parts = [
            tool.name or "",
            tool.description or "",
            tool.price or "",
            str(tool.popularity),
            '|'.join(sorted(tool.categories)),
            tool.url or "",
            tool.logo_url or "",
            str(tool.rank) if tool.rank else "",
            str(tool.upvotes) if tool.upvotes else "",
            str(tool.monthly_users) if tool.monthly_users else "",
            str(tool.editor_score) if tool.editor_score else "",
            tool.maturity or "",
            '|'.join(sorted(tool.platform)) if tool.platform else "",
            str(tool.features) if tool.features else ""
        ]
        content = "|".join(content_parts)
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self.adapter.get_statistics()
    
    def validate_no_duplicates(self) -> Dict[str, Any]:
        """Validate no duplicates exist"""
        return self.adapter.validate_no_duplicates()


# Convenience functions
def merge_tools_to_database(tools: List[AITool], use_sqlite: bool = True) -> Dict[str, int]:
    """
    Convenience function to merge tools to database
    
    Args:
        tools: List of tools to merge
        use_sqlite: True for SQLite, False for Supabase
        
    Returns:
        Dict with operation statistics
    """
    merger = UniversalMerger(use_sqlite)
    return merger.merge_and_upsert_tools(tools)


def get_database_statistics(use_sqlite: bool = True) -> Dict[str, Any]:
    """
    Get database statistics
    
    Args:
        use_sqlite: True for SQLite, False for Supabase
        
    Returns:
        Dict with database statistics
    """
    merger = UniversalMerger(use_sqlite)
    return merger.get_statistics()


def validate_database_integrity(use_sqlite: bool = True) -> Dict[str, Any]:
    """
    Validate database integrity (no duplicates)
    
    Args:
        use_sqlite: True for SQLite, False for Supabase
        
    Returns:
        Dict with validation results
    """
    merger = UniversalMerger(use_sqlite)
    return merger.validate_no_duplicates()


if __name__ == "__main__":
    print("🧪 Testing Universal Database Merger\n")
    
    # Test SQLite
    try:
        print("Testing SQLite:")
        sqlite_merger = UniversalMerger(use_sqlite=True)
        sqlite_stats = sqlite_merger.get_statistics()
        print(f"✅ SQLite: {sqlite_stats.get('total_tools', 0)} tools")
        
        sqlite_validation = sqlite_merger.validate_no_duplicates()
        print(f"🔍 SQLite validation: {'✅ Clean' if sqlite_validation.get('is_clean') else '⚠️ Has duplicates'}")
        
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")
    
    # Test Supabase
    try:
        print("\nTesting Supabase:")
        supabase_merger = UniversalMerger(use_sqlite=False)
        supabase_stats = supabase_merger.get_statistics()
        print(f"✅ Supabase: {supabase_stats.get('total_tools', 0)} tools")
        
    except Exception as e:
        print(f"❌ Supabase test failed: {e}")
    
    print("\n💡 Use UniversalMerger(use_sqlite=True) for local development")
    print("💡 Use UniversalMerger(use_sqlite=False) for production")