"""
Enhanced Supabase adapter for 3D graph visualization
Designed for the new graph-oriented schema
"""

import json
import uuid
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from scrapers.common import AITool
from supabase import create_client, Client
from dotenv import load_dotenv


class SupabaseGraphAdapter:
    """Enhanced Supabase adapter for graph database operations"""
    
    def __init__(self):
        load_dotenv()
        
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        
        self.supabase: Client = create_client(self.url, self.key)
        print(f"✅ Connected to Supabase: {self.url}")
    
    def insert_tool(self, tool: AITool, content_hash: str) -> Optional[str]:
        """Insert a new tool and return its UUID"""
        try:
            tool_data = {
                'ext_id': tool.ext_id,
                'source': tool.source,
                'name': tool.name,
                'description': tool.description,
                'url': tool.url,
                'logo_url': tool.logo_url,
                'price': tool.price,
                'pricing_model': self._detect_pricing_model(tool.price),
                'popularity': tool.popularity,
                'rank': tool.rank,
                'upvotes': tool.upvotes,
                'monthly_users': tool.monthly_users,
                'editor_score': tool.editor_score,
                'categories': tool.categories or [],
                'macro_domain': tool.macro_domain,
                'maturity': tool.maturity,
                'platform': tool.platform or [],
                'features': tool.features or {},
                'tags': self._extract_tags(tool),
                'node_color': self._get_domain_color(tool.macro_domain),
                'node_size': self._calculate_node_size(tool.popularity),
                'content_hash': content_hash,
                'last_scraped': tool.last_scraped.isoformat() if tool.last_scraped else None,
                'scrape_source_data': self._create_scrape_metadata(tool)
            }
            
            response = self.supabase.table('ai_tool').insert(tool_data).execute()
            
            if response.data:
                tool_id = response.data[0]['id']
                
                # Auto-create categories and relationships
                self._ensure_categories_exist(tool.categories or [])
                self._link_tool_to_categories(tool_id, tool.categories or [])
                
                return tool_id
            
            return None
            
        except Exception as e:
            print(f"❌ Error inserting tool {tool.name}: {e}")
            return None
    
    def update_tool(self, tool_id: str, tool: AITool, content_hash: str) -> bool:
        """Update an existing tool"""
        try:
            tool_data = {
                'name': tool.name,
                'description': tool.description,
                'url': tool.url,
                'logo_url': tool.logo_url,
                'price': tool.price,
                'pricing_model': self._detect_pricing_model(tool.price),
                'popularity': tool.popularity,
                'rank': tool.rank,
                'upvotes': tool.upvotes,
                'monthly_users': tool.monthly_users,
                'editor_score': tool.editor_score,
                'categories': tool.categories or [],
                'macro_domain': tool.macro_domain,
                'maturity': tool.maturity,
                'platform': tool.platform or [],
                'features': tool.features or {},
                'tags': self._extract_tags(tool),
                'node_color': self._get_domain_color(tool.macro_domain),
                'node_size': self._calculate_node_size(tool.popularity),
                'content_hash': content_hash,
                'last_scraped': tool.last_scraped.isoformat() if tool.last_scraped else None,
                'scrape_source_data': self._create_scrape_metadata(tool),
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('ai_tool').update(tool_data).eq('id', tool_id).execute()
            
            if response.data:
                # Update category links
                self._ensure_categories_exist(tool.categories or [])
                self._update_tool_categories(tool_id, tool.categories or [])
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error updating tool: {e}")
            return False
    
    def find_duplicate_tool(self, tool: AITool) -> Optional[Dict[str, Any]]:
        """Find duplicate tool by URL or name"""
        try:
            # Search by URL first (most specific)
            if tool.url:
                response = self.supabase.table('ai_tool').select('*').ilike('url', tool.url).limit(1).execute()
                if response.data:
                    return response.data[0]
            
            # Search by name if no URL match
            if tool.name:
                response = self.supabase.table('ai_tool').select('*').ilike('name', tool.name).limit(1).execute()
                if response.data:
                    return response.data[0]
            
            return None
            
        except Exception as e:
            print(f"❌ Error finding duplicate: {e}")
            return None
    
    def generate_similarity_relationships(self, similarity_threshold: float = 0.7) -> int:
        """Generate tool relationships based on similarity"""
        try:
            response = self.supabase.rpc('generate_similarity_relationships', {
                'similarity_threshold': similarity_threshold
            }).execute()
            
            if response.data:
                count = response.data
                print(f"✅ Generated {count} similarity relationships")
                return count
            
            return 0
            
        except Exception as e:
            print(f"❌ Error generating relationships: {e}")
            return 0
    
    def create_manual_relationship(self, source_tool_id: str, target_tool_id: str, 
                                 relationship_type: str, strength: float = 1.0,
                                 description: str = None) -> bool:
        """Create a manual relationship between tools"""
        try:
            relationship_data = {
                'source_tool_id': source_tool_id,
                'target_tool_id': target_tool_id,
                'relationship_type': relationship_type,
                'strength': strength,
                'confidence': 1.0,  # Manual relationships have high confidence
                'description': description,
                'auto_detected': False,
                'verified': True
            }
            
            response = self.supabase.table('tool_relationship').insert(relationship_data).execute()
            return bool(response.data)
            
        except Exception as e:
            print(f"❌ Error creating relationship: {e}")
            return False
    
    def get_graph_data(self, limit: int = 1000) -> Dict[str, Any]:
        """Get graph data for 3D visualization"""
        try:
            # Get nodes (tools)
            nodes_response = self.supabase.table('ai_tool').select(
                'id, name, popularity, macro_domain, categories, url, logo_url, '
                'node_color, node_size, graph_position, monthly_users, editor_score'
            ).limit(limit).execute()
            
            # Get edges (relationships)
            edges_response = self.supabase.table('tool_relationship').select(
                'source_tool_id, target_tool_id, relationship_type, strength, '
                'edge_color, edge_width, description'
            ).execute()
            
            # Get categories for clustering
            categories_response = self.supabase.table('category').select(
                'id, name, cluster_color, cluster_position, tool_count'
            ).execute()
            
            return {
                'nodes': nodes_response.data or [],
                'edges': edges_response.data or [],
                'categories': categories_response.data or [],
                'metadata': {
                    'total_nodes': len(nodes_response.data or []),
                    'total_edges': len(edges_response.data or []),
                    'generated_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"❌ Error getting graph data: {e}")
            return {'nodes': [], 'edges': [], 'categories': [], 'error': str(e)}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            # Basic counts
            tools_count = self.supabase.table('ai_tool').select('id', count='exact').execute().count
            relationships_count = self.supabase.table('tool_relationship').select('id', count='exact').execute().count
            categories_count = self.supabase.table('category').select('id', count='exact').execute().count
            
            # Tools by domain
            domains_response = self.supabase.table('ai_tool').select(
                'macro_domain', count='exact'
            ).execute()
            
            domains_data = {}
            for item in domains_response.data:
                domain = item['macro_domain']
                domains_data[domain] = domains_data.get(domain, 0) + 1
            
            # Tools by source
            sources_response = self.supabase.table('ai_tool').select(
                'source', count='exact'
            ).execute()
            
            sources_data = {}
            for item in sources_response.data:
                source = item['source']
                sources_data[source] = sources_data.get(source, 0) + 1
            
            # Network statistics
            network_stats = self.supabase.table('tool_network').select(
                'connection_count'
            ).execute()
            
            connection_counts = [item['connection_count'] for item in network_stats.data]
            avg_connections = sum(connection_counts) / len(connection_counts) if connection_counts else 0
            
            return {
                'total_tools': tools_count,
                'total_relationships': relationships_count,
                'total_categories': categories_count,
                'by_domain': domains_data,
                'by_source': sources_data,
                'network': {
                    'avg_connections_per_tool': round(avg_connections, 2),
                    'max_connections': max(connection_counts) if connection_counts else 0,
                    'total_network_density': round(relationships_count / (tools_count * (tools_count - 1)) * 2, 4) if tools_count > 1 else 0
                },
                'database_type': 'Supabase Graph',
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {'error': str(e)}
    
    def refresh_materialized_views(self) -> bool:
        """Refresh materialized views for better performance"""
        try:
            self.supabase.rpc('refresh_all_materialized_views').execute()
            print("✅ Materialized views refreshed")
            return True
        except Exception as e:
            print(f"❌ Error refreshing views: {e}")
            return False
    
    def _detect_pricing_model(self, price_str: str) -> str:
        """Detect pricing model from price string"""
        if not price_str:
            return 'unknown'
        
        price_lower = price_str.lower()
        
        if 'free' in price_lower and 'trial' not in price_lower:
            return 'free'
        elif 'freemium' in price_lower:
            return 'freemium'
        elif 'trial' in price_lower:
            return 'free_trial'
        elif any(term in price_lower for term in ['month', 'year', 'subscription']):
            return 'subscription'
        elif 'enterprise' in price_lower:
            return 'enterprise'
        elif '$' in price_str and 'month' not in price_lower and 'year' not in price_lower:
            return 'one_time'
        else:
            return 'unknown'
    
    def _get_domain_color(self, domain: str) -> str:
        """Get color for domain visualization"""
        domain_colors = {
            'NLP': '#3B82F6',           # Blue
            'COMPUTER_VISION': '#10B981', # Green
            'AUDIO': '#EF4444',         # Red
            'VIDEO': '#F59E0B',         # Orange
            'GENERATIVE_AI': '#8B5CF6', # Purple
            'ML_FRAMEWORKS': '#06B6D4', # Cyan
            'DATA_ANALYSIS': '#84CC16', # Lime
            'AUTOMATION': '#F97316',    # Orange
            'DESIGN': '#EC4899',        # Pink
            'CODING': '#6366F1',        # Indigo
            'BUSINESS': '#14B8A6',      # Teal
            'OTHER': '#6B7280'          # Gray
        }
        return domain_colors.get(domain, '#6B7280')
    
    def _calculate_node_size(self, popularity: float) -> float:
        """Calculate node size based on popularity"""
        if not popularity:
            return 1.0
        
        # Scale from 0.5 to 3.0 based on popularity
        return 0.5 + (popularity / 100) * 2.5
    
    def _extract_tags(self, tool: AITool) -> List[str]:
        """Extract tags from tool for better searchability"""
        tags = []
        
        # Add categories as tags
        if tool.categories:
            tags.extend(tool.categories)
        
        # Add platforms as tags
        if tool.platform:
            tags.extend(tool.platform)
        
        # Add domain as tag
        if tool.macro_domain:
            tags.append(tool.macro_domain.lower())
        
        # Add pricing info as tag
        if tool.price:
            if 'free' in tool.price.lower():
                tags.append('free')
            if '$' in tool.price:
                tags.append('paid')
        
        # Remove duplicates and return
        return list(set(tags))
    
    def _create_scrape_metadata(self, tool: AITool) -> Dict[str, Any]:
        """Create metadata about the scraping process"""
        return {
            'scraped_at': datetime.now().isoformat(),
            'source': tool.source,
            'original_ext_id': tool.ext_id,
            'has_logo': bool(tool.logo_url),
            'has_metrics': bool(tool.monthly_users or tool.upvotes),
            'feature_count': len(tool.features) if tool.features else 0,
            'platform_count': len(tool.platform) if tool.platform else 0
        }
    
    def _ensure_categories_exist(self, categories: List[str]):
        """Ensure categories exist in the database"""
        for category_name in categories:
            try:
                # Check if category exists
                existing = self.supabase.table('category').select('id').eq('name', category_name).execute()
                
                if not existing.data:
                    # Create new category
                    slug = category_name.lower().replace(' ', '-').replace('_', '-')
                    category_data = {
                        'name': category_name,
                        'slug': slug,
                        'description': f'Auto-generated category for {category_name}',
                        'cluster_color': self._get_category_color(category_name)
                    }
                    
                    self.supabase.table('category').insert(category_data).execute()
                    
            except Exception as e:
                print(f"⚠️ Error ensuring category {category_name}: {e}")
    
    def _link_tool_to_categories(self, tool_id: str, categories: List[str]):
        """Link tool to categories"""
        for category_name in categories:
            try:
                # Get category ID
                category_response = self.supabase.table('category').select('id').eq('name', category_name).execute()
                
                if category_response.data:
                    category_id = category_response.data[0]['id']
                    
                    # Create link
                    link_data = {
                        'tool_id': tool_id,
                        'category_id': category_id,
                        'confidence': 1.0,
                        'auto_assigned': True
                    }
                    
                    self.supabase.table('tool_category').insert(link_data).execute()
                    
            except Exception as e:
                print(f"⚠️ Error linking tool to category {category_name}: {e}")
    
    def _update_tool_categories(self, tool_id: str, categories: List[str]):
        """Update tool category associations"""
        try:
            # Remove existing links
            self.supabase.table('tool_category').delete().eq('tool_id', tool_id).execute()
            
            # Add new links
            self._link_tool_to_categories(tool_id, categories)
            
        except Exception as e:
            print(f"⚠️ Error updating tool categories: {e}")
    
    def _get_category_color(self, category_name: str) -> str:
        """Get color for category based on name"""
        category_colors = {
            'ai': '#3B82F6',
            'nlp': '#10B981',
            'image': '#F59E0B',
            'video': '#EF4444',
            'audio': '#8B5CF6',
            'productivity': '#06B6D4',
            'business': '#14B8A6',
            'coding': '#6366F1',
            'design': '#EC4899'
        }
        
        # Try to match partial category names
        category_lower = category_name.lower()
        for key, color in category_colors.items():
            if key in category_lower:
                return color
        
        # Default color
        return '#6B7280'


# Convenience functions for easy integration
def create_graph_adapter() -> SupabaseGraphAdapter:
    """Create a new Supabase graph adapter"""
    return SupabaseGraphAdapter()


def test_graph_connection() -> bool:
    """Test the graph database connection"""
    try:
        adapter = SupabaseGraphAdapter()
        stats = adapter.get_statistics()
        print(f"✅ Graph database connected: {stats.get('total_tools', 0)} tools")
        return True
    except Exception as e:
        print(f"❌ Graph database connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Supabase Graph Adapter\n")
    
    # Test connection
    if test_graph_connection():
        print("\n💡 Graph adapter ready for 3D visualization!")
        print("🚀 Use create_graph_adapter() to get started")
    else:
        print("\n❌ Graph adapter not ready - check Supabase connection")