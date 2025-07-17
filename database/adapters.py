"""
Database adapter pattern for SQLite and Supabase
Allows easy switching between local development and production databases
"""

import json
import sqlite3
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from scrapers.common import AITool


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Test database connection"""
        pass
    
    @abstractmethod
    def insert_tool(self, tool: AITool, content_hash: str) -> bool:
        """Insert a new tool"""
        pass
    
    @abstractmethod
    def update_tool(self, tool_id: int, tool: AITool, content_hash: str) -> bool:
        """Update an existing tool"""
        pass
    
    @abstractmethod
    def find_duplicate_tool(self, tool: AITool) -> Optional[Dict[str, Any]]:
        """Find duplicate tool by URL or name"""
        pass
    
    @abstractmethod
    def get_existing_tool(self, ext_id: str, source: str) -> Optional[Dict[str, Any]]:
        """Get tool by ext_id and source"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        pass
    
    @abstractmethod
    def validate_no_duplicates(self) -> Dict[str, Any]:
        """Validate no duplicates exist"""
        pass


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter for local development"""
    
    def __init__(self, db_path: str = "database/ai_tools.db"):
        self.db_path = db_path
        self.connection = None
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Create database and run schema
            conn = sqlite3.connect(self.db_path)
            
            # Read and execute schema
            schema_path = "database/sqlite_schema.sql"
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                    conn.executescript(schema_sql)
            
            conn.close()
            print(f"✅ SQLite database ready at: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Error creating SQLite database: {e}")
    
    def connect(self) -> bool:
        """Test SQLite connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM ai_tool")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ SQLite connected: {count} tools in database")
            return True
        except Exception as e:
            print(f"❌ SQLite connection failed: {e}")
            return False
    
    def _tool_to_dict(self, tool: AITool, content_hash: str) -> Dict[str, Any]:
        """Convert AITool to SQLite-compatible dict"""
        return {
            'ext_id': tool.ext_id,
            'name': tool.name,
            'description': tool.description,
            'price': tool.price,
            'popularity': tool.popularity,
            'categories': json.dumps(tool.categories) if tool.categories else None,
            'source': tool.source,
            'macro_domain': tool.macro_domain,
            'content_hash': content_hash,
            'url': tool.url,
            'logo_url': tool.logo_url,
            'rank': tool.rank,
            'upvotes': tool.upvotes,
            'monthly_users': tool.monthly_users,
            'editor_score': tool.editor_score,
            'maturity': tool.maturity,
            'platform': json.dumps(tool.platform) if tool.platform else None,
            'features': json.dumps(tool.features) if tool.features else None,
            'last_scraped': tool.last_scraped.isoformat() if tool.last_scraped else None
        }
    
    def _dict_to_tool(self, data: Dict[str, Any]) -> AITool:
        """Convert SQLite dict to AITool"""
        return AITool(
            ext_id=data.get('ext_id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            price=data.get('price', ''),
            popularity=data.get('popularity', 0),
            categories=json.loads(data.get('categories', '[]')) if data.get('categories') else [],
            source=data.get('source', ''),
            macro_domain=data.get('macro_domain', 'OTHER'),
            url=data.get('url'),
            logo_url=data.get('logo_url'),
            rank=data.get('rank'),
            upvotes=data.get('upvotes'),
            monthly_users=data.get('monthly_users'),
            editor_score=data.get('editor_score'),
            maturity=data.get('maturity'),
            platform=json.loads(data.get('platform', '[]')) if data.get('platform') else None,
            features=json.loads(data.get('features', '{}')) if data.get('features') else None,
            last_scraped=datetime.fromisoformat(data.get('last_scraped')) if data.get('last_scraped') else None
        )
    
    def insert_tool(self, tool: AITool, content_hash: str) -> bool:
        """Insert a new tool"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            tool_data = self._tool_to_dict(tool, content_hash)
            
            columns = ', '.join(tool_data.keys())
            placeholders = ', '.join(['?' for _ in tool_data])
            
            sql = f"INSERT INTO ai_tool ({columns}) VALUES ({placeholders})"
            conn.execute(sql, list(tool_data.values()))
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ SQLite insert failed: {e}")
            return False
    
    def update_tool(self, tool_id: int, tool: AITool, content_hash: str) -> bool:
        """Update an existing tool"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            tool_data = self._tool_to_dict(tool, content_hash)
            tool_data['updated_at'] = datetime.now().isoformat()
            
            # Remove ext_id and source from update (shouldn't change)
            tool_data.pop('ext_id', None)
            
            set_clause = ', '.join([f"{k} = ?" for k in tool_data.keys()])
            sql = f"UPDATE ai_tool SET {set_clause} WHERE id = ?"
            
            values = list(tool_data.values()) + [tool_id]
            conn.execute(sql, values)
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ SQLite update failed: {e}")
            return False
    
    def find_duplicate_tool(self, tool: AITool) -> Optional[Dict[str, Any]]:
        """Find duplicate tool by URL or name"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Search by URL first (more specific)
            if tool.url:
                cursor = conn.execute(
                    "SELECT * FROM ai_tool WHERE LOWER(url) = LOWER(?) LIMIT 1",
                    (tool.url,)
                )
                result = cursor.fetchone()
                if result:
                    conn.close()
                    return dict(result)
            
            # Search by name if no URL match
            if tool.name:
                cursor = conn.execute(
                    "SELECT * FROM ai_tool WHERE LOWER(name) = LOWER(?) LIMIT 1",
                    (tool.name,)
                )
                result = cursor.fetchone()
                if result:
                    conn.close()
                    return dict(result)
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"❌ SQLite duplicate search failed: {e}")
            return None
    
    def get_existing_tool(self, ext_id: str, source: str) -> Optional[Dict[str, Any]]:
        """Get tool by ext_id and source"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            cursor = conn.execute(
                "SELECT * FROM ai_tool WHERE ext_id = ? AND source = ? LIMIT 1",
                (ext_id, source)
            )
            result = cursor.fetchone()
            conn.close()
            
            return dict(result) if result else None
            
        except Exception as e:
            print(f"❌ SQLite get existing failed: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Total tools
            cursor = conn.execute("SELECT COUNT(*) as count FROM ai_tool")
            total_tools = cursor.fetchone()['count']
            
            # By source
            cursor = conn.execute("""
                SELECT source, COUNT(*) as count 
                FROM ai_tool 
                GROUP BY source 
                ORDER BY count DESC
            """)
            by_source = {row['source']: row['count'] for row in cursor.fetchall()}
            
            # By domain
            cursor = conn.execute("""
                SELECT macro_domain, COUNT(*) as count 
                FROM ai_tool 
                GROUP BY macro_domain 
                ORDER BY count DESC
            """)
            by_domain = {row['macro_domain']: row['count'] for row in cursor.fetchall()}
            
            # Recent activity
            cursor = conn.execute("""
                SELECT DATE(last_scraped) as date, COUNT(*) as count
                FROM ai_tool 
                WHERE last_scraped IS NOT NULL
                GROUP BY DATE(last_scraped)
                ORDER BY date DESC
                LIMIT 7
            """)
            recent_activity = {row['date']: row['count'] for row in cursor.fetchall()}
            
            conn.close()
            
            return {
                'total_tools': total_tools,
                'by_source': by_source,
                'by_domain': by_domain,
                'recent_activity': recent_activity,
                'database_type': 'SQLite',
                'database_path': self.db_path
            }
            
        except Exception as e:
            print(f"❌ SQLite statistics failed: {e}")
            return {'error': str(e)}
    
    def validate_no_duplicates(self) -> Dict[str, Any]:
        """Validate no duplicates exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Check URL duplicates
            cursor = conn.execute("""
                SELECT LOWER(url) as url, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM ai_tool 
                WHERE url IS NOT NULL AND url != ''
                GROUP BY LOWER(url)
                HAVING count > 1
                LIMIT 10
            """)
            url_conflicts = [dict(row) for row in cursor.fetchall()]
            
            # Check name duplicates
            cursor = conn.execute("""
                SELECT LOWER(name) as name, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM ai_tool 
                WHERE name IS NOT NULL AND name != ''
                GROUP BY LOWER(name)
                HAVING count > 1
                LIMIT 10
            """)
            name_conflicts = [dict(row) for row in cursor.fetchall()]
            
            # Total count
            cursor = conn.execute("SELECT COUNT(*) as count FROM ai_tool")
            total_tools = cursor.fetchone()['count']
            
            conn.close()
            
            validation_result = {
                'total_tools': total_tools,
                'url_duplicates': len(url_conflicts),
                'name_duplicates': len(name_conflicts),
                'url_conflicts': url_conflicts,
                'name_conflicts': name_conflicts,
                'is_clean': len(url_conflicts) == 0 and len(name_conflicts) == 0,
                'database_type': 'SQLite'
            }
            
            return validation_result
            
        except Exception as e:
            print(f"❌ SQLite validation failed: {e}")
            return {'error': str(e)}


class SupabaseAdapter(DatabaseAdapter):
    """Supabase database adapter for production"""
    
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.supabase = None
        
        if not self.url or not self.key:
            print("⚠️ Supabase credentials not found in .env")
    
    def connect(self) -> bool:
        """Test Supabase connection"""
        try:
            from supabase import create_client
            self.supabase = create_client(self.url, self.key)
            
            response = self.supabase.table('ai_tool').select('id').limit(1).execute()
            print(f"✅ Supabase connected: {len(response.data)} sample records")
            return True
            
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
            return False
    
    def insert_tool(self, tool: AITool, content_hash: str) -> bool:
        """Insert a new tool"""
        # Placeholder implementation - would use existing SupabaseMerger logic
        print("⚠️ Supabase insert not implemented due to connection issues")
        return False
    
    def update_tool(self, tool_id: int, tool: AITool, content_hash: str) -> bool:
        """Update an existing tool"""
        print("⚠️ Supabase update not implemented due to connection issues")
        return False
    
    def find_duplicate_tool(self, tool: AITool) -> Optional[Dict[str, Any]]:
        """Find duplicate tool by URL or name"""
        print("⚠️ Supabase find_duplicate not implemented due to connection issues")
        return None
    
    def get_existing_tool(self, ext_id: str, source: str) -> Optional[Dict[str, Any]]:
        """Get tool by ext_id and source"""
        print("⚠️ Supabase get_existing not implemented due to connection issues")
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {'error': 'Supabase not available due to connection issues'}
    
    def validate_no_duplicates(self) -> Dict[str, Any]:
        """Validate no duplicates exist"""
        return {'error': 'Supabase not available due to connection issues'}


def create_database_adapter(use_sqlite: bool = True) -> DatabaseAdapter:
    """Factory function to create the appropriate database adapter"""
    
    if use_sqlite:
        print("🔧 Using SQLite adapter for local development")
        return SQLiteAdapter()
    else:
        print("🔧 Using Supabase adapter for production")
        return SupabaseAdapter()


def test_adapters():
    """Test both database adapters"""
    print("🧪 Testing Database Adapters\n")
    
    # Test SQLite
    print("Testing SQLite Adapter:")
    sqlite_adapter = SQLiteAdapter()
    sqlite_works = sqlite_adapter.connect()
    
    if sqlite_works:
        stats = sqlite_adapter.get_statistics()
        print(f"📊 SQLite Stats: {stats.get('total_tools', 0)} tools")
        
        validation = sqlite_adapter.validate_no_duplicates()
        print(f"🔍 Validation: {'✅ Clean' if validation.get('is_clean') else '⚠️ Has duplicates'}")
    
    print(f"SQLite: {'✅ WORKING' if sqlite_works else '❌ BROKEN'}")
    
    # Test Supabase
    print("\nTesting Supabase Adapter:")
    supabase_adapter = SupabaseAdapter()
    supabase_works = supabase_adapter.connect()
    print(f"Supabase: {'✅ WORKING' if supabase_works else '❌ BROKEN'}")
    
    print(f"\n📊 Results:")
    print(f"✅ SQLite: {'Ready' if sqlite_works else 'Failed'}")
    print(f"{'✅' if supabase_works else '❌'} Supabase: {'Ready' if supabase_works else 'Failed'}")
    
    if sqlite_works:
        print(f"\n💡 Recommendation: Use SQLite for development")
        print(f"   Database location: {sqlite_adapter.db_path}")


if __name__ == "__main__":
    test_adapters()