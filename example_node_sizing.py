#!/usr/bin/env python3
"""
Example usage of node size computation functions for 3D graph visualization

This demonstrates how to use the backend helper functions to compute node sizes
for AI tools based on graph connectivity and popularity metrics.
"""

import sys
sys.path.append('.')

import pandas as pd
from utils.node_size import size_by_degree, size_by_popularity, compute_stats


def demonstrate_degree_sizing():
    """Demonstrate degree-based node sizing"""
    print("🔗 DEGREE-BASED NODE SIZING")
    print("=" * 40)
    
    print("Formula: size = 4 + log1p(degree) * 1.01")
    print("Range: [4, 20] (clipped)")
    print()
    
    # Example degrees and their sizes
    example_degrees = [0, 1, 5, 10, 25, 50, 100, 500, 1000]
    
    print("Degree → Size Examples:")
    for degree in example_degrees:
        size = size_by_degree(degree)
        description = get_degree_description(degree)
        print(f"   {degree:4d} → {size:5.2f}  ({description})")
    
    print("\n💡 Usage in export script:")
    print("```python")
    print("from utils.node_size import size_by_degree")
    print()
    print("# Query from ai_tool_degree materialized view")
    print("query = 'SELECT id, degree FROM ai_tool_degree'")
    print("for row in cursor.execute(query):")
    print("    tool_id, degree = row")
    print("    node_size = size_by_degree(degree)")
    print("    # Use node_size in 3D visualization")
    print("```")


def demonstrate_popularity_sizing():
    """Demonstrate popularity-based node sizing"""
    print("\n\n📊 POPULARITY-BASED NODE SIZING")
    print("=" * 40)
    
    print("Formula: z-score blend of monthly_users, upvotes, rank")
    print("Weights: 50% users, 30% upvotes, 20% rank")
    print("Range: [4, 12] approximately")
    print()
    
    # Create sample AI tools data
    sample_data = pd.DataFrame({
        'name': [
            'ChatGPT', 'Midjourney', 'GitHub Copilot', 
            'Niche Tool A', 'Startup Tool B', 'Unknown Tool C'
        ],
        'monthly_users': [200000000, 15000000, 5000000, 100000, 10000, None],
        'upvotes': [100000, 50000, 25000, 1000, 500, 10],
        'rank': [1, 3, 5, 50, 200, 999]
    })
    
    print("Sample AI Tools Dataset:")
    print(sample_data.to_string(index=False))
    
    # Compute statistics
    stats = compute_stats(sample_data)
    print(f"\nComputed Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value:.2f}")
    
    # Calculate sizes for each tool
    print(f"\nPopularity-Based Sizes:")
    for _, row in sample_data.iterrows():
        size = size_by_popularity(
            row['monthly_users'], 
            row['upvotes'], 
            row['rank'], 
            stats
        )
        print(f"   {row['name']:15s} → {size:5.2f}")
    
    print("\n💡 Usage in export script:")
    print("```python")
    print("from utils.node_size import size_by_popularity, compute_stats")
    print("import pandas as pd")
    print()
    print("# Load data from PostgreSQL")
    print("df = pd.read_sql('''")
    print("    SELECT id, monthly_users, upvotes, rank")
    print("    FROM ai_tool")
    print("''', connection)")
    print()
    print("# Compute statistics once")
    print("stats = compute_stats(df)")
    print()
    print("# Calculate sizes for all tools")
    print("for _, row in df.iterrows():")
    print("    size = size_by_popularity(")
    print("        row['monthly_users'], row['upvotes'], row['rank'], stats")
    print("    )")
    print("    # Use size in 3D visualization")
    print("```")


def demonstrate_batch_processing():
    """Demonstrate batch processing for large datasets"""
    print("\n\n⚡ BATCH PROCESSING FOR LARGE DATASETS")
    print("=" * 50)
    
    # Simulate large dataset
    large_dataset = pd.DataFrame({
        'id': range(1000),
        'monthly_users': [1000 * (i + 1) for i in range(1000)],
        'upvotes': [10 * (i + 1) for i in range(1000)],
        'rank': [(i % 100) + 1 for i in range(1000)],
        'degree': [(i % 50) for i in range(1000)]
    })
    
    print(f"Dataset size: {len(large_dataset):,} tools")
    
    # Batch process degree sizes
    from utils.node_size import compute_all_degree_sizes, compute_all_popularity_sizes
    
    degree_sizes = compute_all_degree_sizes(large_dataset['degree'])
    
    stats = compute_stats(large_dataset)
    popularity_sizes = compute_all_popularity_sizes(large_dataset, stats)
    
    print(f"\nDegree Sizes Statistics:")
    print(f"   Min: {degree_sizes.min():.2f}")
    print(f"   Max: {degree_sizes.max():.2f}")
    print(f"   Mean: {degree_sizes.mean():.2f}")
    
    print(f"\nPopularity Sizes Statistics:")
    print(f"   Min: {popularity_sizes.min():.2f}")
    print(f"   Max: {popularity_sizes.max():.2f}")
    print(f"   Mean: {popularity_sizes.mean():.2f}")
    
    print("\n💡 Efficient batch processing:")
    print("```python")
    print("# Process all tools at once")
    print("degree_sizes = compute_all_degree_sizes(df['degree'])")
    print("popularity_sizes = compute_all_popularity_sizes(df)")
    print()
    print("# Add to DataFrame")
    print("df['degree_size'] = degree_sizes")
    print("df['popularity_size'] = popularity_sizes")
    print("```")


def demonstrate_api_integration():
    """Demonstrate API integration patterns"""
    print("\n\n🌐 API INTEGRATION PATTERNS")
    print("=" * 35)
    
    print("Example API endpoint for 3D graph data:")
    print("```python")
    print("from flask import Flask, jsonify")
    print("from utils.node_size import size_by_degree, size_by_popularity, compute_stats")
    print("import pandas as pd")
    print()
    print("app = Flask(__name__)")
    print()
    print("@app.route('/api/graph/nodes')")
    print("def get_graph_nodes():")
    print("    # Query database")
    print("    df = pd.read_sql('''")
    print("        SELECT t.id, t.name, t.monthly_users, t.upvotes, t.rank,")
    print("               d.degree")
    print("        FROM ai_tool t")
    print("        JOIN ai_tool_degree d ON t.id = d.id")
    print("    ''', connection)")
    print("    ")
    print("    # Compute statistics")
    print("    stats = compute_stats(df)")
    print("    ")
    print("    # Generate node data")
    print("    nodes = []")
    print("    for _, row in df.iterrows():")
    print("        degree_size = size_by_degree(row['degree'])")
    print("        pop_size = size_by_popularity(")
    print("            row['monthly_users'], row['upvotes'], row['rank'], stats")
    print("        )")
    print("        ")
    print("        nodes.append({")
    print("            'id': row['id'],")
    print("            'name': row['name'],")
    print("            'degree_size': degree_size,")
    print("            'popularity_size': pop_size,")
    print("            'combined_size': (degree_size + pop_size) / 2")
    print("        })")
    print("    ")
    print("    return jsonify({'nodes': nodes})")
    print("```")


def get_degree_description(degree):
    """Get human-readable description for degree value"""
    if degree == 0:
        return "isolated tool"
    elif degree == 1:
        return "single connection"
    elif degree <= 5:
        return "lightly connected"
    elif degree <= 15:
        return "well connected"
    elif degree <= 50:
        return "highly connected"
    else:
        return "hub tool"


def demonstrate_size_comparison():
    """Demonstrate comparison between sizing methods"""
    print("\n\n🔄 SIZING METHOD COMPARISON")
    print("=" * 35)
    
    # Create tools with different characteristics
    tools = pd.DataFrame({
        'name': ['Hub Tool', 'Popular Tool', 'New Tool', 'Niche Tool'],
        'degree': [100, 5, 1, 25],
        'monthly_users': [100000, 10000000, 1000, 50000],
        'upvotes': [1000, 50000, 10, 2000],
        'rank': [50, 1, 999, 100]
    })
    
    stats = compute_stats(tools)
    
    print("Tool Comparison:")
    print(f"{'Tool':12s} {'Degree':>6s} {'Deg Size':>8s} {'Pop Size':>8s} {'Combined':>8s}")
    print("-" * 50)
    
    for _, row in tools.iterrows():
        deg_size = size_by_degree(row['degree'])
        pop_size = size_by_popularity(
            row['monthly_users'], row['upvotes'], row['rank'], stats
        )
        combined = (deg_size + pop_size) / 2
        
        print(f"{row['name']:12s} {row['degree']:6d} "
              f"{deg_size:8.2f} {pop_size:8.2f} {combined:8.2f}")
    
    print("\n💡 Insights:")
    print("   • Hub Tool: High degree → large degree-based size")
    print("   • Popular Tool: High users/votes, low rank → large popularity size")
    print("   • New Tool: Low metrics → small sizes")
    print("   • Niche Tool: Medium degree, moderate popularity")


def main():
    """Run all demonstrations"""
    print("🎯 NODE SIZE COMPUTATION - USAGE EXAMPLES")
    print("=" * 60)
    
    demonstrate_degree_sizing()
    demonstrate_popularity_sizing()
    demonstrate_batch_processing()
    demonstrate_api_integration()
    demonstrate_size_comparison()
    
    print("\n" + "=" * 60)
    print("🎉 NODE SIZE FUNCTIONS READY FOR BACKEND INTEGRATION!")
    
    print("\n📋 SUMMARY:")
    print("   ✅ size_by_degree(degree) → [4, 20] range")
    print("   ✅ size_by_popularity(users, votes, rank, stats) → [4, 12] range")
    print("   ✅ compute_stats(df) → statistics dictionary")
    print("   ✅ Batch processing functions available")
    print("   ✅ None value handling")
    print("   ✅ Production-ready for PostgreSQL integration")
    
    print("\n🚀 NEXT STEPS:")
    print("   1. Import from utils.node_size in export scripts")
    print("   2. Query ai_tool and ai_tool_degree tables")
    print("   3. Compute node sizes for 3D visualization")
    print("   4. Use in API endpoints for frontend")
    print("   5. Consider combining degree + popularity sizes")


if __name__ == "__main__":
    main()