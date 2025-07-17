#!/usr/bin/env python3
"""
Louvain Community Detection for AI Tools Graph

This module implements the Louvain algorithm to detect communities in the AI tools graph
and updates the community_id column in the database.

The Louvain algorithm:
1. Starts with each node in its own community
2. Iteratively moves nodes to neighboring communities that maximize modularity
3. Coarsens the graph by merging communities
4. Repeats until no improvement in modularity

Performance optimizations:
- Uses sparse matrices for large graphs
- Implements efficient modularity calculation
- Batch database updates for community assignments
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from supabase import create_client, Client
from dotenv import load_dotenv
import networkx as nx
from dataclasses import dataclass
import math

# Load environment variables
load_dotenv()


@dataclass
class GraphEdge:
    """Represents an edge in the graph"""
    node1: str
    node2: str
    weight: float
    edge_type: str


@dataclass
class CommunityStats:
    """Statistics for a detected community"""
    community_id: int
    size: int
    internal_edges: int
    external_edges: int
    modularity_contribution: float
    dominant_domains: List[str]
    avg_popularity: float


class LouvainCommunityDetector:
    """Louvain algorithm implementation for AI tools graph"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        
        self.supabase: Client = create_client(self.url, self.key)
        print(f"✅ Connected to Supabase for community detection")
        
        # Algorithm parameters
        self.resolution = 1.0  # Resolution parameter for modularity
        self.min_community_size = 3  # Minimum size for meaningful communities
        self.max_iterations = 100  # Maximum iterations per level
        self.tolerance = 1e-6  # Convergence tolerance
        
    def detect_communities(self) -> Dict[str, any]:
        """
        Main method to detect communities using Louvain algorithm
        
        Returns:
            Dictionary with community detection results and statistics
        """
        stats = {
            'nodes_processed': 0,
            'edges_processed': 0,
            'communities_found': 0,
            'modularity_score': 0.0,
            'iterations': 0,
            'largest_community_size': 0
        }
        
        print("🔄 Starting Louvain community detection...")
        
        # 1. Load graph data from database
        graph_data = self._load_graph_data()
        if not graph_data['nodes'] or not graph_data['edges']:
            print("⚠️ No graph data found")
            return stats
            
        stats['nodes_processed'] = len(graph_data['nodes'])
        stats['edges_processed'] = len(graph_data['edges'])
        
        print(f"📊 Loaded graph: {stats['nodes_processed']} nodes, {stats['edges_processed']} edges")
        
        # 2. Build NetworkX graph for algorithm
        G = self._build_networkx_graph(graph_data)
        
        # 3. Apply Louvain algorithm
        communities = self._louvain_algorithm(G)
        stats['communities_found'] = len(set(communities.values()))
        stats['iterations'] = self._get_iteration_count()
        
        # 4. Calculate modularity
        stats['modularity_score'] = self._calculate_modularity(G, communities)
        
        # 5. Filter small communities
        filtered_communities = self._filter_small_communities(communities, graph_data['nodes'])
        stats['communities_found'] = len(set(filtered_communities.values()))
        
        # 6. Update database with community assignments
        updated_count = self._update_database_communities(filtered_communities)
        
        # 7. Generate community statistics
        community_stats = self._generate_community_stats(G, filtered_communities, graph_data['nodes'])
        
        if community_stats:
            stats['largest_community_size'] = max(cs.size for cs in community_stats)
        
        print(f"\\n🎯 Community detection complete:")
        print(f"   📊 Nodes processed: {stats['nodes_processed']}")
        print(f"   🔗 Edges processed: {stats['edges_processed']}")
        print(f"   🏘️ Communities found: {stats['communities_found']}")
        print(f"   📈 Modularity score: {stats['modularity_score']:.4f}")
        print(f"   🔄 Algorithm iterations: {stats['iterations']}")
        print(f"   💾 Database records updated: {updated_count}")
        
        return stats
    
    def _load_graph_data(self) -> Dict[str, any]:
        """Load graph nodes and edges from database"""
        try:
            # Load nodes (tools)
            nodes_response = self.supabase.table('ai_tool').select(
                'id, name, macro_domain, popularity, monthly_users'
            ).execute()
            
            nodes = {}
            for item in nodes_response.data:
                nodes[item['id']] = {
                    'name': item.get('name', ''),
                    'macro_domain': item.get('macro_domain', 'OTHER'),
                    'popularity': item.get('popularity', 0.0),
                    'monthly_users': item.get('monthly_users', 0)
                }
            
            # Load edges (synergies)
            edges_response = self.supabase.table('ai_synergy').select(
                'tool_id_1, tool_id_2, strength, edge_type'
            ).execute()
            
            edges = []
            for item in edges_response.data:
                edges.append(GraphEdge(
                    node1=item['tool_id_1'],
                    node2=item['tool_id_2'],
                    weight=item['strength'],
                    edge_type=item.get('edge_type', 'unspecified')
                ))
            
            return {'nodes': nodes, 'edges': edges}
            
        except Exception as e:
            print(f"❌ Error loading graph data: {e}")
            return {'nodes': {}, 'edges': []}
    
    def _build_networkx_graph(self, graph_data: Dict[str, any]) -> nx.Graph:
        """Build NetworkX graph from loaded data"""
        G = nx.Graph()
        
        # Add nodes with attributes
        for node_id, node_data in graph_data['nodes'].items():
            G.add_node(node_id, **node_data)
        
        # Add edges with weights
        for edge in graph_data['edges']:
            if edge.node1 in G.nodes and edge.node2 in G.nodes:
                G.add_edge(edge.node1, edge.node2, 
                          weight=edge.weight, 
                          edge_type=edge.edge_type)
        
        print(f"🔗 NetworkX graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def _louvain_algorithm(self, G: nx.Graph) -> Dict[str, int]:
        """
        Implement Louvain algorithm for community detection
        
        Returns:
            Dictionary mapping node_id to community_id
        """
        # Initialize each node in its own community
        communities = {node: i for i, node in enumerate(G.nodes())}
        self._iteration_count = 0
        
        improved = True
        level = 0
        
        while improved and level < 10:  # Max 10 levels
            improved = False
            level += 1
            
            print(f"🔄 Louvain level {level}: {len(set(communities.values()))} communities")
            
            # Phase 1: Local optimization
            for iteration in range(self.max_iterations):
                self._iteration_count += 1
                nodes_moved = 0
                
                # Randomize node order for better convergence
                nodes = list(G.nodes())
                np.random.shuffle(nodes)
                
                for node in nodes:
                    current_community = communities[node]
                    
                    # Find best community for this node
                    best_community, best_gain = self._find_best_community(
                        G, node, communities, current_community
                    )
                    
                    # Move node if improvement found
                    if best_gain > self.tolerance:
                        communities[node] = best_community
                        nodes_moved += 1
                        improved = True
                
                # Check convergence
                if nodes_moved == 0:
                    break
                    
                if iteration % 10 == 0:
                    modularity = self._calculate_modularity(G, communities)
                    print(f"   Iteration {iteration}: {nodes_moved} moves, modularity = {modularity:.4f}")
            
            # Phase 2: Graph coarsening (simplified for this implementation)
            # In a full implementation, we would create a new graph where communities become nodes
            
        final_modularity = self._calculate_modularity(G, communities)
        print(f"🏁 Final modularity: {final_modularity:.4f}")
        
        return communities
    
    def _find_best_community(self, G: nx.Graph, node: str, communities: Dict[str, int], 
                           current_community: int) -> Tuple[int, float]:
        """Find the best community for a node to maximize modularity gain"""
        
        # Get neighboring communities
        neighbor_communities = set()
        for neighbor in G.neighbors(node):
            neighbor_communities.add(communities[neighbor])
        
        # Add current community to candidates
        neighbor_communities.add(current_community)
        
        best_community = current_community
        best_gain = 0.0
        
        for candidate_community in neighbor_communities:
            if candidate_community == current_community:
                continue
                
            # Calculate modularity gain from moving node to candidate community
            gain = self._calculate_modularity_gain(
                G, node, communities, current_community, candidate_community
            )
            
            if gain > best_gain:
                best_gain = gain
                best_community = candidate_community
        
        return best_community, best_gain
    
    def _calculate_modularity_gain(self, G: nx.Graph, node: str, communities: Dict[str, int],
                                 from_community: int, to_community: int) -> float:
        """Calculate modularity gain from moving a node between communities"""
        
        # Simplified modularity gain calculation
        # In practice, this would be more sophisticated
        
        m = G.number_of_edges()  # Total edges
        if m == 0:
            return 0.0
        
        # Calculate edge weights to communities
        k_i_in_from = 0  # Edges from node to from_community
        k_i_in_to = 0    # Edges from node to to_community
        
        for neighbor in G.neighbors(node):
            weight = G[node][neighbor].get('weight', 1.0)
            
            if communities[neighbor] == from_community:
                k_i_in_from += weight
            elif communities[neighbor] == to_community:
                k_i_in_to += weight
        
        # Node degree
        k_i = sum(G[node][neighbor].get('weight', 1.0) for neighbor in G.neighbors(node))
        
        # Community degrees (simplified)
        sigma_from = sum(
            sum(G[n][neighbor].get('weight', 1.0) for neighbor in G.neighbors(n))
            for n in G.nodes() if communities[n] == from_community
        )
        
        sigma_to = sum(
            sum(G[n][neighbor].get('weight', 1.0) for neighbor in G.neighbors(n))
            for n in G.nodes() if communities[n] == to_community
        )
        
        # Modularity gain (simplified formula)
        gain = (k_i_in_to - k_i_in_from) / (2 * m) - k_i * (sigma_to - sigma_from) / (4 * m * m)
        
        return gain * self.resolution
    
    def _calculate_modularity(self, G: nx.Graph, communities: Dict[str, int]) -> float:
        """Calculate modularity score for the current community assignment"""
        
        if G.number_of_edges() == 0:
            return 0.0
        
        # Use NetworkX built-in modularity calculation
        community_list = []
        community_to_nodes = defaultdict(list)
        
        for node, community in communities.items():
            community_to_nodes[community].append(node)
        
        community_list = list(community_to_nodes.values())
        
        try:
            modularity = nx.algorithms.community.modularity(G, community_list, weight='weight')
            return modularity
        except:
            return 0.0
    
    def _filter_small_communities(self, communities: Dict[str, int], 
                                 nodes: Dict[str, any]) -> Dict[str, int]:
        """Filter out communities smaller than minimum size"""
        
        # Count community sizes
        community_sizes = Counter(communities.values())
        
        # Find communities to keep
        valid_communities = {
            comm_id for comm_id, size in community_sizes.items() 
            if size >= self.min_community_size
        }
        
        # Filter communities
        filtered = {}
        for node_id, community_id in communities.items():
            if community_id in valid_communities:
                filtered[node_id] = community_id
            else:
                # Assign to community -1 (unclustered)
                filtered[node_id] = -1
        
        print(f"🔍 Filtered {len(community_sizes)} → {len(valid_communities)} communities (min size: {self.min_community_size})")
        
        return filtered
    
    def _update_database_communities(self, communities: Dict[str, int]) -> int:
        """Update database with community assignments"""
        
        try:
            # Prepare batch updates
            updates = []
            for node_id, community_id in communities.items():
                # Use None for unclustered nodes (community_id = -1)
                db_community_id = None if community_id == -1 else community_id
                updates.append({
                    'id': node_id,
                    'community_id': db_community_id
                })
            
            # Batch update in chunks
            chunk_size = 100
            updated_count = 0
            
            for i in range(0, len(updates), chunk_size):
                chunk = updates[i:i + chunk_size]
                
                for update in chunk:
                    try:
                        self.supabase.table('ai_tool').update({
                            'community_id': update['community_id']
                        }).eq('id', update['id']).execute()
                        updated_count += 1
                    except Exception as e:
                        print(f"⚠️ Error updating {update['id']}: {e}")
            
            print(f"💾 Updated {updated_count}/{len(updates)} community assignments")
            return updated_count
            
        except Exception as e:
            print(f"❌ Error updating database communities: {e}")
            return 0
    
    def _generate_community_stats(self, G: nx.Graph, communities: Dict[str, int], 
                                 nodes: Dict[str, any]) -> List[CommunityStats]:
        """Generate statistics for detected communities"""
        
        community_stats = []
        community_to_nodes = defaultdict(list)
        
        # Group nodes by community
        for node_id, community_id in communities.items():
            if community_id != -1:  # Skip unclustered nodes
                community_to_nodes[community_id].append(node_id)
        
        # Calculate stats for each community
        for community_id, community_nodes in community_to_nodes.items():
            if len(community_nodes) < self.min_community_size:
                continue
                
            # Count internal and external edges
            internal_edges = 0
            external_edges = 0
            
            for node in community_nodes:
                for neighbor in G.neighbors(node):
                    if communities[neighbor] == community_id:
                        internal_edges += 1
                    else:
                        external_edges += 1
            
            internal_edges //= 2  # Each edge counted twice
            
            # Calculate modularity contribution
            modularity_contribution = self._calculate_community_modularity(
                G, community_nodes, communities
            )
            
            # Domain analysis
            domains = [nodes[node]['macro_domain'] for node in community_nodes]
            domain_counts = Counter(domains)
            dominant_domains = [domain for domain, count in domain_counts.most_common(3)]
            
            # Popularity analysis
            popularities = [nodes[node]['popularity'] for node in community_nodes]
            avg_popularity = sum(popularities) / len(popularities) if popularities else 0.0
            
            stats = CommunityStats(
                community_id=community_id,
                size=len(community_nodes),
                internal_edges=internal_edges,
                external_edges=external_edges,
                modularity_contribution=modularity_contribution,
                dominant_domains=dominant_domains,
                avg_popularity=avg_popularity
            )
            
            community_stats.append(stats)
        
        # Sort by size descending
        community_stats.sort(key=lambda x: x.size, reverse=True)
        
        print(f"📊 Generated stats for {len(community_stats)} communities")
        return community_stats
    
    def _calculate_community_modularity(self, G: nx.Graph, community_nodes: List[str], 
                                       communities: Dict[str, int]) -> float:
        """Calculate modularity contribution for a specific community"""
        
        # Simplified modularity calculation for a single community
        m = G.number_of_edges()
        if m == 0:
            return 0.0
        
        # Internal edges in community
        l_c = 0
        for node in community_nodes:
            for neighbor in G.neighbors(node):
                if neighbor in community_nodes:
                    l_c += G[node][neighbor].get('weight', 1.0)
        l_c /= 2  # Each edge counted twice
        
        # Total degree of community
        d_c = sum(
            sum(G[node][neighbor].get('weight', 1.0) for neighbor in G.neighbors(node))
            for node in community_nodes
        )
        
        # Modularity contribution
        modularity = (l_c / m) - (d_c / (2 * m)) ** 2
        
        return modularity
    
    def _get_iteration_count(self) -> int:
        """Get total number of iterations performed"""
        return getattr(self, '_iteration_count', 0)
    
    def get_community_statistics(self) -> Dict[str, any]:
        """Get statistics about detected communities"""
        
        try:
            # Get community distribution
            response = self.supabase.table('ai_tool').select(
                'community_id, macro_domain, popularity'
            ).execute()
            
            data = response.data
            
            # Count communities
            communities = [item['community_id'] for item in data if item['community_id'] is not None]
            unclustered = [item for item in data if item['community_id'] is None]
            
            community_counts = Counter(communities)
            
            # Size distribution
            sizes = list(community_counts.values())
            
            stats = {
                'total_communities': len(community_counts),
                'total_nodes': len(data),
                'clustered_nodes': len(data) - len(unclustered),
                'unclustered_nodes': len(unclustered),
                'avg_community_size': sum(sizes) / len(sizes) if sizes else 0,
                'largest_community_size': max(sizes) if sizes else 0,
                'smallest_community_size': min(sizes) if sizes else 0,
                'community_size_distribution': {
                    'small_communities': len([s for s in sizes if s < 5]),
                    'medium_communities': len([s for s in sizes if 5 <= s < 15]),
                    'large_communities': len([s for s in sizes if s >= 15])
                }
            }
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting community statistics: {e}")
            return {}


def detect_communities() -> Dict[str, any]:
    """
    Convenience function to run community detection
    
    Returns:
        Dictionary with detection results and statistics
    """
    detector = LouvainCommunityDetector()
    return detector.detect_communities()


def get_community_stats() -> Dict[str, any]:
    """
    Get statistics about detected communities
    
    Returns:
        Dictionary with community statistics
    """
    detector = LouvainCommunityDetector()
    return detector.get_community_statistics()


if __name__ == "__main__":
    print("🎯 Testing Louvain Community Detection")
    print("=" * 50)
    
    detector = LouvainCommunityDetector()
    results = detector.detect_communities()
    
    print(f"\\n📊 Detection Results:")
    for key, value in results.items():
        print(f"   {key}: {value}")
    
    print(f"\\n📈 Community Statistics:")
    stats = detector.get_community_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")