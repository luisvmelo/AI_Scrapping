#!/usr/bin/env python3
"""
REST API Server for AI Tools Graph Visualization

Provides endpoints for 3D graph visualization including:
- Node data with degree, edge types, and community information
- Graph statistics and community analysis
- Edge data with classification and strength
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, List, Any, Optional
import pandas as pd
from utils.node_size import size_by_degree, size_by_popularity, compute_stats
from collections import Counter

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(supabase_url, supabase_key)


@app.route('/api/node/<node_id>')
def get_node(node_id: str):
    """
    Get detailed node information including degree, edge types, and community
    
    Returns:
        JSON object with node data:
        - id, name, description, macro_domain
        - degree: number of connections
        - edge_type_counts: breakdown by edge type
        - community_id: Louvain cluster assignment
        - node_size: computed size for visualization
        - popularity metrics
    """
    try:
        # Get base node data
        node_response = supabase.table('ai_tool').select(
            'id, name, description, macro_domain, categories, '
            'monthly_users, upvotes, rank, popularity, community_id'
        ).eq('id', node_id).execute()
        
        if not node_response.data:
            return jsonify({'error': 'Node not found'}), 404
        
        node = node_response.data[0]
        
        # Get edge data for this node
        edges_response = supabase.table('ai_synergy').select(
            'tool_id_1, tool_id_2, strength, edge_type'
        ).or_(f'tool_id_1.eq.{node_id},tool_id_2.eq.{node_id}').execute()
        
        edges = edges_response.data
        
        # Calculate degree
        degree = len(edges)
        
        # Calculate edge type counts
        edge_type_counts = Counter(edge['edge_type'] for edge in edges)
        
        # Get connected nodes for additional context
        connected_nodes = []
        for edge in edges:
            other_node_id = edge['tool_id_2'] if edge['tool_id_1'] == node_id else edge['tool_id_1']
            connected_nodes.append({
                'id': other_node_id,
                'strength': edge['strength'],
                'edge_type': edge['edge_type']
            })
        
        # Sort by strength descending
        connected_nodes.sort(key=lambda x: x['strength'], reverse=True)
        
        # Calculate node sizes
        degree_size = size_by_degree(degree)
        
        # For popularity size, we need stats (compute from a sample for now)
        popularity_size = 4.0  # Default
        if node['monthly_users'] or node['upvotes'] or node['rank']:
            # Simplified popularity calculation
            users = node['monthly_users'] or 1
            votes = node['upvotes'] or 1
            rank = node['rank'] or 999
            
            # Basic popularity score
            pop_score = (users / 1000000) + (votes / 10000) + (1000 - rank) / 1000
            popularity_size = min(12.0, max(4.0, 4.0 + pop_score * 4))
        
        # Build response
        response_data = {
            'id': node['id'],
            'name': node['name'],
            'description': node['description'],
            'macro_domain': node['macro_domain'],
            'categories': node['categories'] or [],
            'degree': degree,
            'edge_type_counts': dict(edge_type_counts),
            'community_id': node['community_id'],
            'sizes': {
                'degree_size': round(degree_size, 2),
                'popularity_size': round(popularity_size, 2),
                'combined_size': round((degree_size + popularity_size) / 2, 2)
            },
            'popularity': {
                'monthly_users': node['monthly_users'],
                'upvotes': node['upvotes'],
                'rank': node['rank'],
                'popularity_score': node['popularity']
            },
            'connections': {
                'total': len(connected_nodes),
                'top_connections': connected_nodes[:10]  # Top 10 strongest connections
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/graph/nodes')
def get_all_nodes():
    """
    Get all nodes with basic information for graph visualization
    
    Query parameters:
    - limit: Maximum number of nodes (default: 1000)
    - community_id: Filter by community ID
    - domain: Filter by macro_domain
    """
    try:
        limit = min(int(request.args.get('limit', 1000)), 5000)  # Max 5000 nodes
        community_id = request.args.get('community_id')
        domain = request.args.get('domain')
        
        # Build query
        query = supabase.table('ai_tool').select(
            'id, name, macro_domain, popularity, community_id, monthly_users'
        )
        
        if community_id:
            query = query.eq('community_id', community_id)
        if domain:
            query = query.eq('macro_domain', domain)
            
        response = query.limit(limit).execute()
        nodes = response.data
        
        # Calculate node sizes for all nodes
        df = pd.DataFrame(nodes)
        if not df.empty:
            # Compute degree sizes (would need to join with ai_synergy for accurate counts)
            for node in nodes:
                # Simplified degree calculation - in production, use materialized view
                node['degree'] = 5  # Placeholder
                node['degree_size'] = size_by_degree(node['degree'])
                
                # Simplified popularity size
                node['popularity_size'] = 4.0 + (node.get('popularity', 0) * 4)
                node['popularity_size'] = min(12.0, max(4.0, node['popularity_size']))
        
        return jsonify({
            'nodes': nodes,
            'total': len(nodes),
            'filters_applied': {
                'community_id': community_id,
                'domain': domain,
                'limit': limit
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/graph/edges')
def get_edges():
    """
    Get edge data for graph visualization
    
    Query parameters:
    - limit: Maximum number of edges (default: 2000)
    - min_strength: Minimum edge strength (default: 0.3)
    - edge_type: Filter by edge type
    """
    try:
        limit = min(int(request.args.get('limit', 2000)), 10000)
        min_strength = float(request.args.get('min_strength', 0.3))
        edge_type = request.args.get('edge_type')
        
        # Build query
        query = supabase.table('ai_synergy').select(
            'tool_id_1, tool_id_2, strength, edge_type'
        ).gte('strength', min_strength)
        
        if edge_type:
            query = query.eq('edge_type', edge_type)
            
        response = query.order('strength', desc=True).limit(limit).execute()
        edges = response.data
        
        # Group by edge type for statistics
        edge_type_stats = Counter(edge['edge_type'] for edge in edges)
        
        return jsonify({
            'edges': edges,
            'total': len(edges),
            'statistics': {
                'edge_type_distribution': dict(edge_type_stats),
                'avg_strength': sum(e['strength'] for e in edges) / len(edges) if edges else 0,
                'min_strength_filter': min_strength
            },
            'filters_applied': {
                'edge_type': edge_type,
                'min_strength': min_strength,
                'limit': limit
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/communities')
def get_communities():
    """
    Get community information and statistics
    """
    try:
        # Get community statistics
        response = supabase.table('ai_tool').select(
            'community_id, macro_domain, popularity, name'
        ).is_('community_id', 'not.null').execute()
        
        data = response.data
        
        # Group by community
        communities = {}
        for item in data:
            comm_id = item['community_id']
            if comm_id not in communities:
                communities[comm_id] = {
                    'community_id': comm_id,
                    'size': 0,
                    'domains': Counter(),
                    'avg_popularity': 0.0,
                    'total_popularity': 0.0,
                    'tools': []
                }
            
            communities[comm_id]['size'] += 1
            communities[comm_id]['domains'][item['macro_domain']] += 1
            communities[comm_id]['total_popularity'] += item.get('popularity', 0)
            communities[comm_id]['tools'].append({
                'id': item['id'] if 'id' in item else '',
                'name': item['name'],
                'domain': item['macro_domain']
            })
        
        # Calculate averages and format output
        community_list = []
        for comm_id, community in communities.items():
            community['avg_popularity'] = community['total_popularity'] / community['size']
            community['dominant_domains'] = [domain for domain, count in community['domains'].most_common(3)]
            community['domain_diversity'] = len(community['domains'])
            
            # Remove internal counters
            del community['domains']
            del community['total_popularity']
            
            community_list.append(community)
        
        # Sort by size descending
        community_list.sort(key=lambda x: x['size'], reverse=True)
        
        return jsonify({
            'communities': community_list,
            'total_communities': len(community_list),
            'total_clustered_nodes': sum(c['size'] for c in community_list),
            'statistics': {
                'largest_community_size': max(c['size'] for c in community_list) if community_list else 0,
                'avg_community_size': sum(c['size'] for c in community_list) / len(community_list) if community_list else 0,
                'size_distribution': {
                    'small_communities': len([c for c in community_list if c['size'] < 5]),
                    'medium_communities': len([c for c in community_list if 5 <= c['size'] < 15]),
                    'large_communities': len([c for c in community_list if c['size'] >= 15])
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/graph/statistics')
def get_graph_statistics():
    """
    Get overall graph statistics
    """
    try:
        # Get node count
        nodes_response = supabase.table('ai_tool').select('id', count='exact').execute()
        node_count = nodes_response.count
        
        # Get edge count and statistics
        edges_response = supabase.table('ai_synergy').select('strength, edge_type').execute()
        edges = edges_response.data
        
        edge_count = len(edges)
        edge_type_stats = Counter(edge['edge_type'] for edge in edges)
        
        strengths = [edge['strength'] for edge in edges]
        avg_strength = sum(strengths) / len(strengths) if strengths else 0
        
        # Get community statistics
        communities_response = supabase.table('ai_tool').select('community_id').is_('community_id', 'not.null').execute()
        clustered_nodes = len(communities_response.data)
        unique_communities = len(set(item['community_id'] for item in communities_response.data))
        
        return jsonify({
            'graph_overview': {
                'total_nodes': node_count,
                'total_edges': edge_count,
                'graph_density': (2 * edge_count) / (node_count * (node_count - 1)) if node_count > 1 else 0,
                'avg_edge_strength': round(avg_strength, 4)
            },
            'edge_statistics': {
                'edge_type_distribution': dict(edge_type_stats),
                'strength_distribution': {
                    'strong_edges': len([s for s in strengths if s >= 0.7]),
                    'medium_edges': len([s for s in strengths if 0.4 <= s < 0.7]),
                    'weak_edges': len([s for s in strengths if s < 0.4])
                }
            },
            'community_statistics': {
                'total_communities': unique_communities,
                'clustered_nodes': clustered_nodes,
                'unclustered_nodes': node_count - clustered_nodes,
                'clustering_ratio': clustered_nodes / node_count if node_count > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Tools Graph API is running',
        'endpoints': [
            '/api/node/<id>',
            '/api/graph/nodes',
            '/api/graph/edges', 
            '/api/communities',
            '/api/graph/statistics'
        ]
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting AI Tools Graph API Server")
    print("=" * 50)
    print("📊 Available endpoints:")
    print("   GET /api/node/<id>        - Get node details")
    print("   GET /api/graph/nodes      - Get all nodes")
    print("   GET /api/graph/edges      - Get edges")
    print("   GET /api/communities      - Get communities")
    print("   GET /api/graph/statistics - Get graph stats")
    print("   GET /api/health           - Health check")
    print()
    print("🔗 Example URLs:")
    print("   http://localhost:5000/api/health")
    print("   http://localhost:5000/api/graph/statistics")
    print("   http://localhost:5000/api/communities")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)