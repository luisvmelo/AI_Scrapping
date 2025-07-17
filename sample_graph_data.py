#!/usr/bin/env python3
"""
Sample graph data generator for 3D visualization preview
Shows exactly what data structure your frontend will receive
"""

import json
from datetime import datetime
from database.universal_merger import UniversalMerger


def generate_sample_graph_data():
    """Generate sample graph data that mimics Supabase output"""
    
    # Sample nodes (AI tools)
    nodes = [
        {
            'id': 'node_1',
            'name': 'OpenAI ChatGPT',
            'popularity': 98.0,
            'macro_domain': 'NLP',
            'categories': ['chatbot', 'writing', 'productivity'],
            'url': 'https://chat.openai.com',
            'logo_url': 'https://openai.com/favicon.ico',
            'node_color': '#3B82F6',  # Blue for NLP
            'node_size': 2.95,  # Large node for high popularity
            'graph_position': {'x': 0, 'y': 0, 'z': 0},
            'monthly_users': 200000000,
            'editor_score': 9.8
        },
        {
            'id': 'node_2', 
            'name': 'Anthropic Claude',
            'popularity': 92.0,
            'macro_domain': 'NLP',
            'categories': ['chatbot', 'analysis', 'writing'],
            'url': 'https://claude.ai',
            'logo_url': 'https://anthropic.com/favicon.ico',
            'node_color': '#3B82F6',  # Blue for NLP
            'node_size': 2.8,
            'graph_position': {'x': 5, 'y': 2, 'z': 1},
            'monthly_users': 50000000,
            'editor_score': 9.5
        },
        {
            'id': 'node_3',
            'name': 'Midjourney',
            'popularity': 90.0,
            'macro_domain': 'COMPUTER_VISION',
            'categories': ['image', 'art', 'design'],
            'url': 'https://midjourney.com',
            'logo_url': 'https://midjourney.com/logo.png',
            'node_color': '#10B981',  # Green for Computer Vision
            'node_size': 2.75,
            'graph_position': {'x': -3, 'y': 4, 'z': -2},
            'monthly_users': 15000000,
            'editor_score': 9.2
        },
        {
            'id': 'node_4',
            'name': 'GitHub Copilot',
            'popularity': 88.0,
            'macro_domain': 'CODING',
            'categories': ['coding', 'development', 'productivity'],
            'url': 'https://github.com/features/copilot',
            'logo_url': 'https://github.com/favicon.ico',
            'node_color': '#6366F1',  # Indigo for Coding
            'node_size': 2.7,
            'graph_position': {'x': 2, 'y': -3, 'z': 4},
            'monthly_users': 5000000,
            'editor_score': 9.0
        },
        {
            'id': 'node_5',
            'name': 'Stable Diffusion',
            'popularity': 85.0,
            'macro_domain': 'COMPUTER_VISION',
            'categories': ['image', 'ai', 'open-source'],
            'url': 'https://stability.ai/stablediffusion',
            'logo_url': 'https://stability.ai/favicon.ico',
            'node_color': '#10B981',  # Green for Computer Vision
            'node_size': 2.625,
            'graph_position': {'x': -5, 'y': 3, 'z': -1},
            'monthly_users': 8000000,
            'editor_score': 8.8
        }
    ]
    
    # Sample edges (relationships between tools)
    edges = [
        {
            'source_tool_id': 'node_1',
            'target_tool_id': 'node_2',
            'relationship_type': 'similar_functionality',
            'strength': 0.85,
            'edge_color': '#3B82F6',
            'edge_width': 2.5,
            'description': 'Both are conversational AI assistants'
        },
        {
            'source_tool_id': 'node_3',
            'target_tool_id': 'node_5',
            'relationship_type': 'similar_functionality',
            'strength': 0.90,
            'edge_color': '#10B981',
            'edge_width': 3.0,
            'description': 'Both generate images from text prompts'
        },
        {
            'source_tool_id': 'node_1',
            'target_tool_id': 'node_4',
            'relationship_type': 'integrates_with',
            'strength': 0.70,
            'edge_color': '#8B5CF6',
            'edge_width': 2.0,
            'description': 'ChatGPT can help with coding tasks'
        },
        {
            'source_tool_id': 'node_2',
            'target_tool_id': 'node_4',
            'relationship_type': 'integrates_with',
            'strength': 0.65,
            'edge_color': '#8B5CF6',
            'edge_width': 1.8,
            'description': 'Claude can assist with software development'
        }
    ]
    
    # Sample categories for clustering
    categories = [
        {
            'id': 'cat_1',
            'name': 'Conversational AI',
            'cluster_color': '#3B82F6',
            'cluster_position': {'x': 2.5, 'y': 1, 'z': 0.5},
            'tool_count': 2
        },
        {
            'id': 'cat_2',
            'name': 'Image Generation',
            'cluster_color': '#10B981',
            'cluster_position': {'x': -4, 'y': 3.5, 'z': -1.5},
            'tool_count': 2
        },
        {
            'id': 'cat_3',
            'name': 'Development Tools',
            'cluster_color': '#6366F1',
            'cluster_position': {'x': 2, 'y': -3, 'z': 4},
            'tool_count': 1
        }
    ]
    
    # Complete graph data structure
    graph_data = {
        'nodes': nodes,
        'edges': edges,
        'categories': categories,
        'metadata': {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'generated_at': datetime.now().isoformat(),
            'domains': ['NLP', 'COMPUTER_VISION', 'CODING'],
            'avg_popularity': sum(node['popularity'] for node in nodes) / len(nodes),
            'network_density': len(edges) / (len(nodes) * (len(nodes) - 1) / 2)
        }
    }
    
    return graph_data


def save_sample_data():
    """Save sample data to files for frontend development"""
    
    graph_data = generate_sample_graph_data()
    
    # Save complete graph data
    with open('sample_graph_data.json', 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    # Save nodes only (for testing)
    with open('sample_nodes.json', 'w') as f:
        json.dump(graph_data['nodes'], f, indent=2)
    
    # Save edges only (for testing)
    with open('sample_edges.json', 'w') as f:
        json.dump(graph_data['edges'], f, indent=2)
    
    print("📄 Sample data files created:")
    print("   ✅ sample_graph_data.json - Complete graph data")
    print("   ✅ sample_nodes.json - Nodes only")
    print("   ✅ sample_edges.json - Edges only")
    
    return graph_data


def preview_graph_structure():
    """Preview what the graph structure looks like"""
    
    graph_data = generate_sample_graph_data()
    
    print("🎯 3D GRAPH VISUALIZATION - DATA STRUCTURE PREVIEW")
    print("=" * 60)
    
    print(f"\n📊 NODES ({len(graph_data['nodes'])} AI tools)")
    print("-" * 30)
    for node in graph_data['nodes']:
        print(f"🔹 {node['name']}")
        print(f"   Domain: {node['macro_domain']} | Popularity: {node['popularity']}")
        print(f"   Color: {node['node_color']} | Size: {node['node_size']}")
        print(f"   Position: ({node['graph_position']['x']}, {node['graph_position']['y']}, {node['graph_position']['z']})")
        print(f"   Users: {node['monthly_users']:,} | Score: {node['editor_score']}")
        print()
    
    print(f"🔗 EDGES ({len(graph_data['edges'])} relationships)")
    print("-" * 30)
    for edge in graph_data['edges']:
        source_name = next(n['name'] for n in graph_data['nodes'] if n['id'] == edge['source_tool_id'])
        target_name = next(n['name'] for n in graph_data['nodes'] if n['id'] == edge['target_tool_id'])
        print(f"🔸 {source_name} ↔ {target_name}")
        print(f"   Type: {edge['relationship_type']} | Strength: {edge['strength']}")
        print(f"   Color: {edge['edge_color']} | Width: {edge['edge_width']}")
        print(f"   Reason: {edge['description']}")
        print()
    
    print(f"🎨 CATEGORIES ({len(graph_data['categories'])} clusters)")
    print("-" * 30)
    for category in graph_data['categories']:
        print(f"🔸 {category['name']}")
        print(f"   Color: {category['cluster_color']} | Tools: {category['tool_count']}")
        print(f"   Center: ({category['cluster_position']['x']}, {category['cluster_position']['y']}, {category['cluster_position']['z']})")
        print()
    
    print("📈 METADATA")
    print("-" * 30)
    metadata = graph_data['metadata']
    print(f"🔸 Total nodes: {metadata['total_nodes']}")
    print(f"🔸 Total edges: {metadata['total_edges']}")
    print(f"🔸 Average popularity: {metadata['avg_popularity']:.1f}")
    print(f"🔸 Network density: {metadata['network_density']:.3f}")
    print(f"🔸 Domains: {', '.join(metadata['domains'])}")
    
    print("\n💡 FRONTEND INTEGRATION TIPS:")
    print("=" * 60)
    print("1. Use Three.js or D3.js for 3D visualization")
    print("2. Position nodes using graph_position coordinates")
    print("3. Color nodes by macro_domain using node_color")
    print("4. Size nodes by popularity using node_size")
    print("5. Draw edges between source_tool_id and target_tool_id")
    print("6. Use edge_color and edge_width for edge styling")
    print("7. Group nodes by categories for clustering")
    print("8. Implement hover tooltips with full tool data")
    print("9. Add click interactions to explore tool details")
    print("10. Use metadata for dashboard statistics")


def test_with_real_data():
    """Test with actual database data"""
    print("\n🧪 Testing with Real Local Database Data")
    print("-" * 50)
    
    try:
        merger = UniversalMerger(use_sqlite=True)
        stats = merger.get_statistics()
        
        print(f"📊 Real database stats:")
        print(f"   Tools: {stats.get('total_tools', 0)}")
        print(f"   Sources: {list(stats.get('by_source', {}).keys())}")
        print(f"   Domains: {list(stats.get('by_domain', {}).keys())}")
        
        if stats.get('total_tools', 0) > 0:
            print("✅ Real data available for graph visualization")
            print("💡 Your production graph will have much more data!")
        else:
            print("⚠️ No real data yet - run scrapers to populate")
        
    except Exception as e:
        print(f"❌ Error testing real data: {e}")


def main():
    """Main function to demonstrate graph data structure"""
    
    # Preview the structure
    preview_graph_structure()
    
    # Save sample files
    print("\n📁 SAVING SAMPLE FILES")
    print("=" * 60)
    graph_data = save_sample_data()
    
    # Test with real data
    test_with_real_data()
    
    print("\n🎉 GRAPH DATA PREVIEW COMPLETE!")
    print("\n🚀 Next steps:")
    print("   1. Use sample_graph_data.json to build your 3D frontend")
    print("   2. Run full scrapers to get 5,000+ real tools")
    print("   3. Deploy to Supabase for production graph database")
    print("   4. Build interactive 3D visualization website")


if __name__ == "__main__":
    main()