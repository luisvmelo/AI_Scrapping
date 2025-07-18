#!/usr/bin/env python3
"""
REST API Server for AI Tools Graph Visualization - SQLite Version

Provides endpoints for 3D graph visualization using local SQLite database
"""

import os
import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import Dict, List, Any, Optional
import pandas as pd
from utils.node_size import size_by_degree, size_by_popularity, compute_stats
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'ai_tools.db')

def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

@app.route('/api/node/<node_id>')
def get_node(node_id: str):
    """
    Get detailed node information including degree, edge types, and community
    """
    try:
        conn = get_db_connection()
        
        # Get base node data
        node_query = """
        SELECT id, name, description, macro_domain, categories, 
               monthly_users, upvotes, rank, popularity, 
               url, logo_url, price, source, features, platform
        FROM ai_tool 
        WHERE id = ?
        """
        
        node = conn.execute(node_query, (node_id,)).fetchone()
        
        if not node:
            return jsonify({'error': 'Node not found'}), 404
        
        # Convert to dict
        node_dict = dict(node)
        
        # Parse JSON fields
        if node_dict['categories']:
            try:
                node_dict['categories'] = json.loads(node_dict['categories'])
            except:
                node_dict['categories'] = []
        else:
            node_dict['categories'] = []
            
        if node_dict['features']:
            try:
                node_dict['features'] = json.loads(node_dict['features'])
            except:
                node_dict['features'] = {}
        else:
            node_dict['features'] = {}
            
        if node_dict['platform']:
            try:
                node_dict['platform'] = json.loads(node_dict['platform'])
            except:
                node_dict['platform'] = []
        else:
            node_dict['platform'] = []
        
        # For now, we'll use mock synergy data since we don't have ai_synergy table yet
        # In a real implementation, you'd query the ai_synergy table
        degree = 5  # Mock degree
        edge_type_counts = {'functional': 3, 'domain': 2}  # Mock edge types
        community_id = 1  # Mock community
        
        # Calculate node sizes
        degree_size = size_by_degree(degree)
        
        # Calculate popularity size
        popularity_size = 4.0  # Default
        if node_dict['monthly_users'] or node_dict['upvotes'] or node_dict['rank']:
            users = node_dict['monthly_users'] or 1
            votes = node_dict['upvotes'] or 1
            rank = node_dict['rank'] or 999
            
            # Basic popularity score
            pop_score = (users / 1000000) + (votes / 10000) + (1000 - rank) / 1000
            popularity_size = min(12.0, max(4.0, 4.0 + pop_score * 4))
        
        # Build response
        response_data = {
            'id': node_dict['id'],
            'name': node_dict['name'],
            'description': node_dict['description'],
            'macro_domain': node_dict['macro_domain'],
            'categories': node_dict['categories'],
            'degree': degree,
            'edge_type_counts': edge_type_counts,
            'community_id': community_id,
            'sizes': {
                'degree_size': round(degree_size, 2),
                'popularity_size': round(popularity_size, 2),
                'combined_size': round((degree_size + popularity_size) / 2, 2)
            },
            'popularity': {
                'monthly_users': node_dict['monthly_users'],
                'upvotes': node_dict['upvotes'],
                'rank': node_dict['rank'],
                'popularity_score': node_dict['popularity']
            },
            'details': {
                'url': node_dict['url'],
                'logo_url': node_dict['logo_url'],
                'price': node_dict['price'],
                'source': node_dict['source'],
                'features': node_dict['features'],
                'platform': node_dict['platform']
            },
            'connections': {
                'total': degree,
                'top_connections': []  # Mock for now
            }
        }
        
        conn.close()
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/graph/nodes')
def get_all_nodes():
    """
    Get all nodes with basic information for graph visualization
    """
    try:
        limit = min(int(request.args.get('limit', 1000)), 5000)
        domain = request.args.get('domain')
        source = request.args.get('source')
        
        conn = get_db_connection()
        
        # Build query
        query = """
        SELECT id, name, macro_domain, popularity, 
               monthly_users, url, logo_url, price, source, categories
        FROM ai_tool
        """
        
        params = []
        conditions = []
        
        if domain:
            conditions.append("macro_domain = ?")
            params.append(domain)
        if source:
            conditions.append("source = ?")
            params.append(source)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " LIMIT ?"
        params.append(limit)
        
        nodes = conn.execute(query, params).fetchall()
        
        # Convert to list of dicts and process
        nodes_list = []
        for node in nodes:
            node_dict = dict(node)
            
            # Parse categories JSON
            if node_dict['categories']:
                try:
                    node_dict['categories'] = json.loads(node_dict['categories'])
                except:
                    node_dict['categories'] = []
            else:
                node_dict['categories'] = []
            
            # Calculate node sizes
            node_dict['degree'] = 5  # Mock degree
            node_dict['degree_size'] = size_by_degree(node_dict['degree'])
            
            # Calculate popularity size
            popularity_size = 4.0 + (node_dict.get('popularity', 0) * 4)
            node_dict['popularity_size'] = min(12.0, max(4.0, popularity_size))
            
            nodes_list.append(node_dict)
        
        conn.close()
        
        return jsonify({
            'nodes': nodes_list,
            'total': len(nodes_list),
            'filters_applied': {
                'domain': domain,
                'source': source,
                'limit': limit
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/graph/edges')
def get_edges():
    """
    Get edge data for graph visualization
    Mock implementation for now since we don't have ai_synergy table
    """
    try:
        limit = min(int(request.args.get('limit', 2000)), 10000)
        min_strength = float(request.args.get('min_strength', 0.3))
        
        # Mock edges data
        edges = [
            {'tool_id_1': 1, 'tool_id_2': 2, 'strength': 0.8, 'edge_type': 'functional'},
            {'tool_id_1': 1, 'tool_id_2': 3, 'strength': 0.6, 'edge_type': 'domain'},
            {'tool_id_1': 2, 'tool_id_2': 4, 'strength': 0.7, 'edge_type': 'functional'},
        ]
        
        # Filter by strength
        filtered_edges = [e for e in edges if e['strength'] >= min_strength]
        
        edge_type_stats = Counter(edge['edge_type'] for edge in filtered_edges)
        
        return jsonify({
            'edges': filtered_edges[:limit],
            'total': len(filtered_edges),
            'statistics': {
                'edge_type_distribution': dict(edge_type_stats),
                'avg_strength': sum(e['strength'] for e in filtered_edges) / len(filtered_edges) if filtered_edges else 0,
                'min_strength_filter': min_strength
            },
            'filters_applied': {
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
    Mock implementation for now
    """
    try:
        conn = get_db_connection()
        
        # Get domain statistics as a proxy for communities
        query = """
        SELECT macro_domain, COUNT(*) as size, AVG(popularity) as avg_popularity
        FROM ai_tool 
        GROUP BY macro_domain
        ORDER BY size DESC
        """
        
        communities_data = conn.execute(query).fetchall()
        
        communities = []
        for i, row in enumerate(communities_data):
            communities.append({
                'community_id': i + 1,
                'size': row['size'],
                'dominant_domains': [row['macro_domain']],
                'avg_popularity': row['avg_popularity'],
                'domain_diversity': 1
            })
        
        conn.close()
        
        return jsonify({
            'communities': communities,
            'total_communities': len(communities),
            'total_clustered_nodes': sum(c['size'] for c in communities),
            'statistics': {
                'largest_community_size': max(c['size'] for c in communities) if communities else 0,
                'avg_community_size': sum(c['size'] for c in communities) / len(communities) if communities else 0
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
        conn = get_db_connection()
        
        # Get node count
        node_count = conn.execute("SELECT COUNT(*) FROM ai_tool").fetchone()[0]
        
        # Get domain distribution
        domain_stats = conn.execute("""
        SELECT macro_domain, COUNT(*) as count 
        FROM ai_tool 
        GROUP BY macro_domain
        """).fetchall()
        
        # Get source distribution
        source_stats = conn.execute("""
        SELECT source, COUNT(*) as count 
        FROM ai_tool 
        GROUP BY source
        """).fetchall()
        
        # Mock edge statistics (would be real with ai_synergy table)
        edge_count = 50  # Mock
        avg_strength = 0.65  # Mock
        
        conn.close()
        
        return jsonify({
            'graph_overview': {
                'total_nodes': node_count,
                'total_edges': edge_count,
                'graph_density': (2 * edge_count) / (node_count * (node_count - 1)) if node_count > 1 else 0,
                'avg_edge_strength': avg_strength
            },
            'node_statistics': {
                'domain_distribution': {row['macro_domain']: row['count'] for row in domain_stats},
                'source_distribution': {row['source']: row['count'] for row in source_stats}
            },
            'edge_statistics': {
                'edge_type_distribution': {'functional': 30, 'domain': 20},  # Mock
                'strength_distribution': {
                    'strong_edges': 15,
                    'medium_edges': 25,
                    'weak_edges': 10
                }
            },
            'community_statistics': {
                'total_communities': len(domain_stats),
                'clustered_nodes': node_count,
                'unclustered_nodes': 0,
                'clustering_ratio': 1.0
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        count = conn.execute("SELECT COUNT(*) FROM ai_tool").fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'message': 'AI Tools Graph API is running (SQLite)',
            'database': {
                'type': 'SQLite',
                'path': DB_PATH,
                'total_tools': count
            },
            'endpoints': [
                '/api/node/<id>',
                '/api/graph/nodes',
                '/api/graph/edges', 
                '/api/communities',
                '/api/graph/statistics'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting AI Tools Graph API Server (SQLite)")
    print("=" * 50)
    print("📊 Available endpoints:")
    print("   GET /api/node/<id>        - Get node details")
    print("   GET /api/graph/nodes      - Get all nodes")
    print("   GET /api/graph/edges      - Get edges")
    print("   GET /api/communities      - Get communities")
    print("   GET /api/graph/statistics - Get graph stats")
    print("   GET /api/health           - Health check")
    print()
    print("💾 Database: SQLite")
    print(f"📁 Database path: {DB_PATH}")
    print()
    print("🔗 Example URLs:")
    print("   http://localhost:5000/api/health")
    print("   http://localhost:5000/api/graph/statistics")
    print("   http://localhost:5000/api/communities")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)