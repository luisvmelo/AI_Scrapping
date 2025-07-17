#!/usr/bin/env python3
"""
Test script for AI Tools Graph API endpoints
"""

import requests
import json
import time
import sys

API_BASE = "http://localhost:5000/api"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing AI Tools Graph API")
    print("=" * 50)
    
    # Test health endpoint
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            health_data = response.json()
            print(f"   Status: {health_data['status']}")
            print(f"   Available endpoints: {len(health_data['endpoints'])}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("💡 Make sure to start the API server with: python api_server.py")
        return False
    
    # Test graph statistics
    print("\\n📊 Testing graph statistics...")
    try:
        response = requests.get(f"{API_BASE}/graph/statistics", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Graph statistics retrieved")
            print(f"   Total nodes: {stats['graph_overview']['total_nodes']}")
            print(f"   Total edges: {stats['graph_overview']['total_edges']}")
            print(f"   Graph density: {stats['graph_overview']['graph_density']:.4f}")
        else:
            print(f"⚠️ Graph statistics error: {response.status_code}")
    except Exception as e:
        print(f"❌ Graph statistics error: {e}")
    
    # Test communities endpoint
    print("\\n🏘️ Testing communities endpoint...")
    try:
        response = requests.get(f"{API_BASE}/communities", timeout=10)
        if response.status_code == 200:
            communities = response.json()
            print("✅ Communities data retrieved")
            print(f"   Total communities: {communities['total_communities']}")
            print(f"   Clustered nodes: {communities['total_clustered_nodes']}")
            
            if communities['communities']:
                largest = communities['communities'][0]
                print(f"   Largest community: {largest['size']} nodes")
        else:
            print(f"⚠️ Communities error: {response.status_code}")
    except Exception as e:
        print(f"❌ Communities error: {e}")
    
    # Test nodes endpoint (with limit)
    print("\\n📍 Testing nodes endpoint...")
    try:
        response = requests.get(f"{API_BASE}/graph/nodes?limit=10", timeout=10)
        if response.status_code == 200:
            nodes = response.json()
            print("✅ Nodes data retrieved")
            print(f"   Returned nodes: {nodes['total']}")
            
            if nodes['nodes']:
                sample_node = nodes['nodes'][0]
                print(f"   Sample node: {sample_node['name']} (domain: {sample_node['macro_domain']})")
        else:
            print(f"⚠️ Nodes error: {response.status_code}")
    except Exception as e:
        print(f"❌ Nodes error: {e}")
    
    # Test edges endpoint (with limit)
    print("\\n🔗 Testing edges endpoint...")
    try:
        response = requests.get(f"{API_BASE}/graph/edges?limit=10", timeout=10)
        if response.status_code == 200:
            edges = response.json()
            print("✅ Edges data retrieved")
            print(f"   Returned edges: {edges['total']}")
            print(f"   Edge types: {list(edges['statistics']['edge_type_distribution'].keys())}")
        else:
            print(f"⚠️ Edges error: {response.status_code}")
    except Exception as e:
        print(f"❌ Edges error: {e}")
    
    # Test specific node endpoint (if we have nodes)
    print("\\n🎯 Testing specific node endpoint...")
    try:
        # First get a node ID
        nodes_response = requests.get(f"{API_BASE}/graph/nodes?limit=1", timeout=10)
        if nodes_response.status_code == 200:
            nodes_data = nodes_response.json()
            if nodes_data['nodes']:
                test_node_id = nodes_data['nodes'][0]['id']
                
                # Test the specific node endpoint
                node_response = requests.get(f"{API_BASE}/node/{test_node_id}", timeout=10)
                if node_response.status_code == 200:
                    node_detail = node_response.json()
                    print("✅ Node detail retrieved")
                    print(f"   Node: {node_detail['name']}")
                    print(f"   Degree: {node_detail['degree']}")
                    print(f"   Edge types: {list(node_detail['edge_type_counts'].keys())}")
                    print(f"   Community ID: {node_detail['community_id']}")
                    print(f"   Node sizes: degree={node_detail['sizes']['degree_size']}, pop={node_detail['sizes']['popularity_size']}")
                else:
                    print(f"⚠️ Node detail error: {node_response.status_code}")
            else:
                print("⚠️ No nodes available to test")
        else:
            print("⚠️ Cannot get node for testing")
    except Exception as e:
        print(f"❌ Node detail error: {e}")
    
    print("\\n" + "=" * 50)
    print("🎉 API testing complete!")
    print("\\n💡 API is ready for frontend integration")
    print("📖 Use these endpoints in your 3D graph visualization")
    
    return True

def print_api_documentation():
    """Print API documentation"""
    print("\\n📚 API ENDPOINT DOCUMENTATION")
    print("=" * 50)
    
    endpoints = [
        {
            'endpoint': 'GET /api/health',
            'description': 'Health check and available endpoints',
            'example': f'{API_BASE}/health'
        },
        {
            'endpoint': 'GET /api/node/<id>',
            'description': 'Detailed node info with degree, edge types, community',
            'example': f'{API_BASE}/node/12345'
        },
        {
            'endpoint': 'GET /api/graph/nodes',
            'description': 'All nodes with filters (limit, community_id, domain)',
            'example': f'{API_BASE}/graph/nodes?limit=100&domain=AI'
        },
        {
            'endpoint': 'GET /api/graph/edges',
            'description': 'Graph edges with filters (limit, min_strength, edge_type)',
            'example': f'{API_BASE}/graph/edges?min_strength=0.5&edge_type=semantic_similarity'
        },
        {
            'endpoint': 'GET /api/communities',
            'description': 'Community detection results and statistics',
            'example': f'{API_BASE}/communities'
        },
        {
            'endpoint': 'GET /api/graph/statistics',
            'description': 'Overall graph metrics and analysis',
            'example': f'{API_BASE}/graph/statistics'
        }
    ]
    
    for endpoint in endpoints:
        print(f"\\n🔗 {endpoint['endpoint']}")
        print(f"   {endpoint['description']}")
        print(f"   Example: {endpoint['example']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--docs":
        print_api_documentation()
    else:
        success = test_api_endpoints()
        if success:
            print_api_documentation()
        sys.exit(0 if success else 1)