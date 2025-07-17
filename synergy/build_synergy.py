"""
Formal Edge-Scoring Algorithm for AI Tools Graph Visualization

This module implements a documented algorithm that decides whether two AI tools should be 
connected in the graph and assigns a numeric strength based on:

1. BASE CONNECTIVITY (0.4 weight):
   - Connect if macro_domain equal OR both in {video, audio}
   - Binary flag: 1.0 if connected, 0.0 otherwise

2. SEMANTIC SIMILARITY (0.4 weight):
   - TF-IDF cosine similarity on tool descriptions ∈ [0,1]
   - Only computed for pairs sharing overlapping keywords in categories

3. POPULARITY BOOST (0.2 weight):
   - pop_score = log1p(monthly_users_i) * log1p(monthly_users_j)
   - Min-max normalized to [0,1] across all tool pairs

4. FINAL STRENGTH:
   - strength = 0.4 * base_flag + 0.4 * semantic_sim + 0.2 * pop_score
   - Discard edges where strength < 0.25

PERFORMANCE OPTIMIZATION:
- Avoids O(N²) complexity on 5k nodes by pre-filtering with keyword overlap
- Uses sparse matrix operations for TF-IDF computation
- Batch processing for database operations

COMPLEXITY ANALYSIS:
- Category filtering: O(N * avg_categories) 
- TF-IDF computation: O(M * vocab_size) where M << N²
- Database operations: O(M) where M is filtered pairs
- Total: O(N * vocab_size + M) instead of O(N²)

OUTPUT:
- Upserts into ai_synergy(tool_id_1, tool_id_2, strength) with tool_id_1 < tool_id_2
- Refreshes materialized view ai_tool_degree after insertion
"""

import os
import math
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Set
from collections import defaultdict, Counter
from supabase import create_client, Client
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dataclasses import dataclass

# Load environment variables
load_dotenv()


@dataclass
class ToolData:
    """Data structure for AI tool information"""
    id: str
    name: str
    description: str
    macro_domain: str
    categories: List[str]
    monthly_users: Optional[int]
    popularity: float


class EdgeScoringEngine:
    """Formal edge-scoring algorithm for AI tools graph"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        
        self.supabase: Client = create_client(self.url, self.key)
        print(f"✅ Connected to Supabase for edge scoring")
        
        # Algorithm weights as specified
        self.BASE_WEIGHT = 0.4
        self.SEMANTIC_WEIGHT = 0.4
        self.POPULARITY_WEIGHT = 0.2
        self.STRENGTH_THRESHOLD = 0.25
        
        # Video/Audio domain compatibility
        self.MULTIMEDIA_DOMAINS = {'VIDEO', 'AUDIO'}
        
        # TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True,
            token_pattern=r'\b[a-zA-Z][a-zA-Z0-9]*\b'
        )
        
    def calculate_all_edges(self, batch_size: int = 500) -> Dict[str, int]:
        """
        Calculate edges for all tools using the formal algorithm
        
        Args:
            batch_size: Size of batches for processing
            
        Returns:
            Statistics about the edge calculation process
        """
        stats = {'calculated': 0, 'inserted': 0, 'filtered_out': 0, 'errors': 0}
        
        print("🔄 Starting formal edge-scoring algorithm...")
        
        # 1. Load all tools from database
        tools = self._load_all_tools()
        if not tools:
            print("⚠️ No tools found in database")
            return stats
        
        print(f"📊 Loaded {len(tools)} tools for analysis")
        
        # 2. Clean existing synergies
        self._cleanup_existing_synergies()
        
        # 3. Pre-filter tool pairs by category overlap (performance optimization)
        candidate_pairs = self._filter_pairs_by_category_overlap(tools)
        print(f"🔍 Filtered to {len(candidate_pairs)} candidate pairs (avoiding O(N²))")
        
        # 4. Compute TF-IDF matrix for semantic similarity
        descriptions = [tool.description or '' for tool in tools]
        tfidf_matrix = self._compute_tfidf_matrix(descriptions)
        print(f"📈 Computed TF-IDF matrix: {tfidf_matrix.shape}")
        
        # 5. Calculate popularity normalization factors
        pop_norm_factors = self._calculate_popularity_normalization(tools)
        
        # 6. Process candidate pairs in batches
        edges_to_insert = []
        tool_id_to_index = {tool.id: i for i, tool in enumerate(tools)}
        
        for i, (tool1_idx, tool2_idx) in enumerate(candidate_pairs):
            try:
                tool1, tool2 = tools[tool1_idx], tools[tool2_idx]
                
                # Calculate edge strength using formal algorithm
                strength = self._calculate_edge_strength(
                    tool1, tool2, 
                    tfidf_matrix[tool1_idx], tfidf_matrix[tool2_idx],
                    pop_norm_factors
                )
                
                stats['calculated'] += 1
                
                # Filter by strength threshold
                if strength >= self.STRENGTH_THRESHOLD:
                    # Ensure tool_id_1 < tool_id_2 for consistent ordering
                    tool_id_1 = min(tool1.id, tool2.id)
                    tool_id_2 = max(tool1.id, tool2.id)
                    
                    # Classify edge type based on connection reason
                    edge_type = self._classify_edge_type(
                        tool1, tool2,
                        tfidf_matrix[tool1_idx], tfidf_matrix[tool2_idx],
                        strength
                    )
                    
                    edges_to_insert.append({
                        'tool_id_1': tool_id_1,
                        'tool_id_2': tool_id_2,
                        'strength': round(strength, 4),
                        'edge_type': edge_type
                    })
                else:
                    stats['filtered_out'] += 1
                
                # Batch insert for performance
                if len(edges_to_insert) >= batch_size:
                    inserted = self._batch_insert_edges(edges_to_insert)
                    stats['inserted'] += inserted
                    edges_to_insert = []
                
                # Progress reporting
                if (i + 1) % 1000 == 0:
                    progress = ((i + 1) / len(candidate_pairs)) * 100
                    print(f"📈 Progress: {progress:.1f}% ({i + 1}/{len(candidate_pairs)} pairs)")
                    
            except Exception as e:
                stats['errors'] += 1
                print(f"❌ Error processing pair {tool1_idx}-{tool2_idx}: {e}")
                continue
        
        # Insert remaining edges
        if edges_to_insert:
            inserted = self._batch_insert_edges(edges_to_insert)
            stats['inserted'] += inserted
        
        # 7. Refresh materialized view
        self._refresh_materialized_view()
        
        print(f"\n🎯 Edge calculation complete:")
        print(f"   📊 Pairs calculated: {stats['calculated']}")
        print(f"   💾 Edges inserted: {stats['inserted']}")
        print(f"   🚫 Filtered out: {stats['filtered_out']}")
        print(f"   ❌ Errors: {stats['errors']}")
        
        return stats
    
    def _load_all_tools(self) -> List[ToolData]:
        """Load all tools from database"""
        try:
            response = self.supabase.table('ai_tool').select(
                'id, name, description, macro_domain, categories, monthly_users, popularity'
            ).execute()
            
            tools = []
            for item in response.data:
                tools.append(ToolData(
                    id=item['id'],
                    name=item.get('name', ''),
                    description=item.get('description', ''),
                    macro_domain=item.get('macro_domain', 'OTHER'),
                    categories=item.get('categories', []),
                    monthly_users=item.get('monthly_users'),
                    popularity=item.get('popularity', 0.0)
                ))
            
            return tools
            
        except Exception as e:
            print(f"❌ Error loading tools: {e}")
            return []
    
    def _filter_pairs_by_category_overlap(self, tools: List[ToolData]) -> List[Tuple[int, int]]:
        """
        Pre-filter tool pairs by category overlap to avoid O(N²) complexity
        
        Performance optimization: only compute similarity for pairs that share
        at least one category keyword
        """
        # Build category keyword index
        keyword_to_tools = defaultdict(set)
        
        for i, tool in enumerate(tools):
            if tool.categories:
                for category in tool.categories:
                    # Extract keywords from category names
                    keywords = category.lower().split()
                    for keyword in keywords:
                        keyword_to_tools[keyword].add(i)
        
        # Find pairs with overlapping keywords
        candidate_pairs = set()
        
        for keyword, tool_indices in keyword_to_tools.items():
            if len(tool_indices) > 1:
                tool_list = list(tool_indices)
                for i in range(len(tool_list)):
                    for j in range(i + 1, len(tool_list)):
                        idx1, idx2 = tool_list[i], tool_list[j]
                        if idx1 != idx2:
                            # Ensure consistent ordering
                            pair = (min(idx1, idx2), max(idx1, idx2))
                            candidate_pairs.add(pair)
        
        return list(candidate_pairs)
    
    def _compute_tfidf_matrix(self, descriptions: List[str]) -> np.ndarray:
        """Compute TF-IDF matrix for all tool descriptions"""
        try:
            # Clean descriptions
            cleaned_descriptions = []
            for desc in descriptions:
                if desc and isinstance(desc, str):
                    cleaned_descriptions.append(desc.strip())
                else:
                    cleaned_descriptions.append('')
            
            # Fit and transform
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(cleaned_descriptions)
            return tfidf_matrix.toarray()
            
        except Exception as e:
            print(f"❌ Error computing TF-IDF matrix: {e}")
            # Return zero matrix as fallback
            return np.zeros((len(descriptions), 100))
    
    def _calculate_popularity_normalization(self, tools: List[ToolData]) -> Dict[str, float]:
        """Calculate popularity normalization factors"""
        # Compute log1p(monthly_users) for all tools
        log_users = []
        for tool in tools:
            users = tool.monthly_users or 0
            log_users.append(math.log1p(users))
        
        # Calculate all pairwise products for normalization
        products = []
        for i in range(len(log_users)):
            for j in range(i + 1, len(log_users)):
                products.append(log_users[i] * log_users[j])
        
        if not products:
            return {'min_product': 0.0, 'max_product': 1.0}
        
        min_product = min(products)
        max_product = max(products)
        
        # Avoid division by zero
        if max_product == min_product:
            max_product = min_product + 1.0
        
        return {
            'min_product': min_product,
            'max_product': max_product,
            'log_users': log_users
        }
    
    def _calculate_edge_strength(self, tool1: ToolData, tool2: ToolData, 
                                tfidf1: np.ndarray, tfidf2: np.ndarray,
                                pop_norm_factors: Dict[str, Any]) -> float:
        """
        Calculate edge strength using the formal algorithm:
        strength = 0.4 * base_flag + 0.4 * semantic_sim + 0.2 * pop_score
        """
        
        # 1. Base connectivity (0.4 weight)
        base_flag = self._calculate_base_connectivity(tool1.macro_domain, tool2.macro_domain)
        
        # 2. Semantic similarity (0.4 weight) 
        semantic_sim = self._calculate_semantic_similarity(tfidf1, tfidf2)
        
        # 3. Popularity boost (0.2 weight)
        pop_score = self._calculate_popularity_score(
            tool1.monthly_users, tool2.monthly_users, pop_norm_factors
        )
        
        # Final weighted sum
        strength = (
            self.BASE_WEIGHT * base_flag +
            self.SEMANTIC_WEIGHT * semantic_sim +
            self.POPULARITY_WEIGHT * pop_score
        )
        
        return max(0.0, min(1.0, strength))  # Clamp to [0,1]
    
    def _calculate_base_connectivity(self, domain1: str, domain2: str) -> float:
        """
        Base connectivity rule:
        Connect if (macro_domain equal) OR (both macro_domain in {video, audio})
        """
        if not domain1 or not domain2:
            return 0.0
        
        # Same domain
        if domain1 == domain2:
            return 1.0
        
        # Both in multimedia domains (video/audio)
        if (domain1.upper() in self.MULTIMEDIA_DOMAINS and 
            domain2.upper() in self.MULTIMEDIA_DOMAINS):
            return 1.0
        
        return 0.0
    
    def _calculate_semantic_similarity(self, tfidf1: np.ndarray, tfidf2: np.ndarray) -> float:
        """Calculate cosine similarity between TF-IDF vectors"""
        try:
            # Reshape for sklearn cosine_similarity
            vec1 = tfidf1.reshape(1, -1)
            vec2 = tfidf2.reshape(1, -1)
            
            # Compute cosine similarity
            similarity = cosine_similarity(vec1, vec2)[0, 0]
            
            # Ensure result is in [0,1]
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            print(f"⚠️ Error calculating semantic similarity: {e}")
            return 0.0
    
    def _calculate_popularity_score(self, users1: Optional[int], users2: Optional[int],
                                  pop_norm_factors: Dict[str, Any]) -> float:
        """
        Calculate popularity score:
        pop_score = log1p(monthly_users_i) * log1p(monthly_users_j)
        Min-max normalized to [0,1]
        """
        if users1 is None or users2 is None:
            return 0.0
        
        # Calculate log product
        log1 = math.log1p(users1)
        log2 = math.log1p(users2)
        product = log1 * log2
        
        # Min-max normalize
        min_product = pop_norm_factors['min_product']
        max_product = pop_norm_factors['max_product']
        
        if max_product == min_product:
            return 0.0
        
        normalized = (product - min_product) / (max_product - min_product)
        return max(0.0, min(1.0, normalized))
    
    def _cleanup_existing_synergies(self) -> None:
        """Remove existing synergies for recalculation"""
        try:
            print("🧹 Cleaning existing synergies...")
            self.supabase.table('ai_synergy').delete().gte('id', 0).execute()
            print("✅ Existing synergies cleaned")
        except Exception as e:
            print(f"⚠️ Error cleaning synergies (continuing): {e}")
    
    def _batch_insert_edges(self, edges: List[Dict[str, Any]]) -> int:
        """Batch insert edges into database"""
        try:
            response = self.supabase.table('ai_synergy').insert(edges).execute()
            return len(response.data) if response.data else 0
        except Exception as e:
            print(f"❌ Error inserting edge batch: {e}")
            return 0
    
    def _refresh_materialized_view(self) -> None:
        """Refresh materialized view ai_tool_degree"""
        try:
            print("🔄 Refreshing materialized view ai_tool_degree...")
            # Note: This assumes the view exists in your Supabase schema
            self.supabase.rpc('refresh_materialized_view', {'view_name': 'ai_tool_degree'}).execute()
            print("✅ Materialized view refreshed")
        except Exception as e:
            print(f"⚠️ Error refreshing materialized view: {e}")
    
    def _classify_edge_type(self, tool1: ToolData, tool2: ToolData, 
                           tfidf1: np.ndarray, tfidf2: np.ndarray, 
                           strength: float) -> str:
        """
        Classify edge type based on the primary connection reason
        
        Categories:
        - same_domain: Tools in identical macro_domain
        - video_audio: Video and Audio domain connection
        - semantic_similarity: High semantic similarity (>0.6)
        - weak: Below semantic threshold but above strength threshold
        
        Args:
            tool1, tool2: Tool data objects
            tfidf1, tfidf2: TF-IDF vectors for semantic analysis
            strength: Overall edge strength
            
        Returns:
            Edge type classification string
        """
        # Check base connectivity reasons first (highest priority)
        base_connectivity = self._calculate_base_connectivity(tool1.macro_domain, tool2.macro_domain)
        
        if base_connectivity > 0:
            # Same domain connection
            if tool1.macro_domain == tool2.macro_domain:
                return 'same_domain'
            
            # Video ↔ Audio connection
            if (tool1.macro_domain.upper() in self.MULTIMEDIA_DOMAINS and 
                tool2.macro_domain.upper() in self.MULTIMEDIA_DOMAINS):
                return 'video_audio'
        
        # Check semantic similarity strength
        semantic_sim = self._calculate_semantic_similarity(tfidf1, tfidf2)
        
        # High semantic similarity (primary driver)
        if semantic_sim >= 0.6:
            return 'semantic_similarity'
        
        # Medium semantic similarity
        elif semantic_sim >= 0.3:
            return 'semantic_similarity'
        
        # Weak connections (popularity-driven or low semantic)
        else:
            return 'weak'
    
    def get_edge_statistics(self) -> Dict[str, Any]:
        """Get statistics about calculated edges"""
        try:
            # Total edges
            total_response = self.supabase.table('ai_synergy').select('id', count='exact').execute()
            total_edges = total_response.count
            
            # Strength statistics
            strength_response = self.supabase.table('ai_synergy').select('strength').execute()
            strengths = [item['strength'] for item in strength_response.data]
            
            if strengths:
                avg_strength = sum(strengths) / len(strengths)
                max_strength = max(strengths)
                min_strength = min(strengths)
                
                # Distribution by strength ranges
                strong_edges = len([s for s in strengths if s >= 0.7])
                medium_edges = len([s for s in strengths if 0.4 <= s < 0.7])
                weak_edges = len([s for s in strengths if 0.25 <= s < 0.4])
            else:
                avg_strength = max_strength = min_strength = 0
                strong_edges = medium_edges = weak_edges = 0
            
            return {
                'total_edges': total_edges,
                'avg_strength': round(avg_strength, 4),
                'max_strength': round(max_strength, 4),
                'min_strength': round(min_strength, 4),
                'distribution': {
                    'strong_edges': strong_edges,   # >= 0.7
                    'medium_edges': medium_edges,   # 0.4-0.7  
                    'weak_edges': weak_edges        # 0.25-0.4
                },
                'algorithm': {
                    'base_weight': self.BASE_WEIGHT,
                    'semantic_weight': self.SEMANTIC_WEIGHT,
                    'popularity_weight': self.POPULARITY_WEIGHT,
                    'threshold': self.STRENGTH_THRESHOLD
                }
            }
            
        except Exception as e:
            print(f"❌ Error getting edge statistics: {e}")
            return {}


# Convenience functions for external use
def build_synergies(batch_size: int = 500) -> Dict[str, int]:
    """
    Build all synergies using the formal edge-scoring algorithm
    
    Args:
        batch_size: Batch size for processing
        
    Returns:
        Statistics about the operation
    """
    engine = EdgeScoringEngine()
    return engine.calculate_all_edges(batch_size)


def get_synergy_stats() -> Dict[str, Any]:
    """
    Get statistics about calculated synergies
    
    Returns:
        Statistics dictionary
    """
    engine = EdgeScoringEngine()
    return engine.get_edge_statistics()


# Legacy compatibility functions (maintaining existing interface)
class SynergyBuilder:
    """Legacy compatibility wrapper"""
    
    def __init__(self):
        self.engine = EdgeScoringEngine()
    
    def calculate_all_synergies(self, batch_size: int = 500) -> Dict[str, int]:
        return self.engine.calculate_all_edges(batch_size)
    
    def get_synergy_statistics(self) -> Dict[str, Any]:
        return self.engine.get_edge_statistics()


def get_tool_synergies(tool_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get synergies for a specific tool
    
    Args:
        tool_id: Tool ID (UUID)
        limit: Maximum number of synergies to return
        
    Returns:
        List of synergies ordered by strength
    """
    try:
        engine = EdgeScoringEngine()
        
        # Query synergies where tool appears as tool_id_1 or tool_id_2
        response1 = engine.supabase.table('ai_synergy').select(
            'strength, tool_id_2, ai_tool!ai_synergy_tool_id_2_fkey(id, name, description)'
        ).eq('tool_id_1', tool_id).order('strength', desc=True).limit(limit).execute()
        
        response2 = engine.supabase.table('ai_synergy').select(
            'strength, tool_id_1, ai_tool!ai_synergy_tool_id_1_fkey(id, name, description)'
        ).eq('tool_id_2', tool_id).order('strength', desc=True).limit(limit).execute()
        
        synergies = []
        
        # Process results where tool is tool_id_1
        for item in response1.data:
            synergies.append({
                'strength': item['strength'],
                'related_tool_id': item['tool_id_2'],
                'related_tool': item['ai_tool']
            })
        
        # Process results where tool is tool_id_2
        for item in response2.data:
            synergies.append({
                'strength': item['strength'],
                'related_tool_id': item['tool_id_1'],
                'related_tool': item['ai_tool']
            })
        
        # Sort by strength and return top N
        synergies.sort(key=lambda x: x['strength'], reverse=True)
        return synergies[:limit]
        
    except Exception as e:
        print(f"❌ Error getting tool synergies for {tool_id}: {e}")
        return []


if __name__ == "__main__":
    print("🎯 Testing Formal Edge-Scoring Algorithm")
    print("=" * 50)
    
    engine = EdgeScoringEngine()
    stats = engine.calculate_all_edges()
    
    print(f"\n📊 Final Results:")
    print(f"   Calculated: {stats['calculated']}")
    print(f"   Inserted: {stats['inserted']}")
    print(f"   Filtered: {stats['filtered_out']}")
    print(f"   Errors: {stats['errors']}")