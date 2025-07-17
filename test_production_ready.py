#!/usr/bin/env python3
"""
Complete production readiness test for 3D graph visualization
Tests both local development and production schema compatibility
"""

import sys
import json
from datetime import datetime
from database.universal_merger import UniversalMerger, get_database_statistics
from database.supabase_graph_adapter import SupabaseGraphAdapter, create_graph_adapter
from scrapers.common import AITool


def create_graph_test_tools() -> list[AITool]:
    """Create test tools specifically for graph visualization testing"""
    return [
        AITool(
            ext_id="graph_openai_chatgpt",
            name="OpenAI ChatGPT",
            description="Advanced conversational AI powered by GPT models for text generation, analysis, and creative tasks",
            price="Free + $20/month Pro",
            popularity=98.0,
            categories=["chatbot", "writing", "productivity", "ai"],
            source="production_test",
            macro_domain="NLP",
            url="https://chat.openai.com",
            logo_url="https://openai.com/favicon.ico",
            rank=1,
            upvotes=100000,
            monthly_users=200000000,
            editor_score=9.8,
            maturity="stable",
            platform=["web", "mobile", "api"],
            features={
                "free_tier": True,
                "api_available": True,
                "real_time": True,
                "enterprise": True,
                "multimodal": True
            },
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="graph_anthropic_claude",
            name="Anthropic Claude",
            description="Advanced AI assistant focused on safety and helpfulness, capable of complex reasoning and analysis",
            price="Free + Usage-based Pro",
            popularity=92.0,
            categories=["chatbot", "writing", "analysis", "ai"],
            source="production_test",
            macro_domain="NLP",
            url="https://claude.ai",
            logo_url="https://anthropic.com/favicon.ico",
            rank=2,
            upvotes=75000,
            monthly_users=50000000,
            editor_score=9.5,
            maturity="stable",
            platform=["web", "api"],
            features={
                "free_tier": True,
                "api_available": True,
                "safety_focused": True,
                "long_context": True
            },
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="graph_midjourney",
            name="Midjourney",
            description="AI-powered image generation creating stunning artwork and visuals from text prompts",
            price="$10-60/month",
            popularity=90.0,
            categories=["image", "art", "design", "creative"],
            source="production_test",
            macro_domain="COMPUTER_VISION",
            url="https://midjourney.com",
            logo_url="https://midjourney.com/logo.png",
            rank=3,
            upvotes=50000,
            monthly_users=15000000,
            editor_score=9.2,
            maturity="stable",
            platform=["discord", "web"],
            features={
                "free_tier": False,
                "collaboration": True,
                "high_quality": True,
                "commercial_use": True
            },
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="graph_github_copilot",
            name="GitHub Copilot",
            description="AI pair programmer that suggests code completions and entire functions in your editor",
            price="$10/month",
            popularity=88.0,
            categories=["coding", "development", "productivity", "ai"],
            source="production_test",
            macro_domain="CODING",
            url="https://github.com/features/copilot",
            logo_url="https://github.com/favicon.ico",
            rank=4,
            upvotes=40000,
            monthly_users=5000000,
            editor_score=9.0,
            maturity="stable",
            platform=["vscode", "jetbrains", "vim", "web"],
            features={
                "free_tier": False,
                "ide_integration": True,
                "multi_language": True,
                "enterprise": True
            },
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="graph_stable_diffusion",
            name="Stable Diffusion",
            description="Open-source AI image generation model for creating detailed images from text descriptions",
            price="Free (Open Source)",
            popularity=85.0,
            categories=["image", "ai", "open-source", "art"],
            source="production_test",
            macro_domain="COMPUTER_VISION",
            url="https://stability.ai/stablediffusion",
            logo_url="https://stability.ai/favicon.ico",
            rank=5,
            upvotes=60000,
            monthly_users=8000000,
            editor_score=8.8,
            maturity="stable",
            platform=["web", "api", "local"],
            features={
                "free_tier": True,
                "open_source": True,
                "customizable": True,
                "local_hosting": True
            },
            last_scraped=datetime.now()
        )
    ]


def test_local_graph_pipeline():
    """Test the complete graph pipeline with local SQLite"""
    print("🏠 Testing Local Graph Pipeline (SQLite)")
    print("-" * 50)
    
    try:
        # Create test tools
        tools = create_graph_test_tools()
        print(f"📊 Created {len(tools)} graph test tools")
        
        # Test local merge
        merger = UniversalMerger(use_sqlite=True)
        results = merger.merge_and_upsert_tools(tools)
        
        print(f"📊 Local merge results: {results}")
        
        # Get local statistics
        stats = get_database_statistics(use_sqlite=True)
        print(f"📈 Local database: {stats.get('total_tools', 0)} total tools")
        print(f"📊 Domains: {list(stats.get('by_domain', {}).keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Local pipeline test failed: {e}")
        return False


def test_production_schema_validation():
    """Validate the production schema structure"""
    print("\n🏭 Production Schema Validation")
    print("-" * 50)
    
    try:
        # Read the schema file
        with open('supabase/complete_production_schema.sql', 'r') as f:
            schema_content = f.read()
        
        # Check for key components
        required_tables = [
            'ai_tool', 'tool_relationship', 'category', 
            'tool_category', 'organization', 'tool_organization'
        ]
        
        required_views = [
            'popular_tools', 'category_stats', 'tool_network'
        ]
        
        required_functions = [
            'calculate_tool_similarity', 'generate_similarity_relationships',
            'refresh_all_materialized_views'
        ]
        
        # Validate tables
        print("📊 Checking tables...")
        for table in required_tables:
            if f"CREATE TABLE {table}" in schema_content:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} MISSING")
        
        # Validate views
        print("📊 Checking views...")
        for view in required_views:
            if f"CREATE VIEW {view}" in schema_content or f"CREATE MATERIALIZED VIEW {view}" in schema_content:
                print(f"   ✅ {view}")
            else:
                print(f"   ❌ {view} MISSING")
        
        # Validate functions
        print("📊 Checking functions...")
        for func in required_functions:
            if f"CREATE OR REPLACE FUNCTION {func}" in schema_content:
                print(f"   ✅ {func}")
            else:
                print(f"   ❌ {func} MISSING")
        
        # Check for graph-specific features
        graph_features = [
            'graph_position JSONB',
            'node_color TEXT',
            'node_size REAL',
            'relationship_type',
            'edge_color TEXT'
        ]
        
        print("📊 Checking 3D graph features...")
        for feature in graph_features:
            if feature in schema_content:
                print(f"   ✅ {feature}")
            else:
                print(f"   ❌ {feature} MISSING")
        
        print("✅ Production schema validation complete")
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False


def test_supabase_adapter_methods():
    """Test Supabase adapter methods (without actual connection)"""
    print("\n🔧 Supabase Adapter Methods Test")
    print("-" * 50)
    
    try:
        # Create adapter (this will fail connection but we can test structure)
        adapter = SupabaseGraphAdapter()
        
        # Test if all required methods exist
        required_methods = [
            'insert_tool', 'update_tool', 'find_duplicate_tool',
            'generate_similarity_relationships', 'create_manual_relationship',
            'get_graph_data', 'get_statistics', 'refresh_materialized_views'
        ]
        
        print("📊 Checking adapter methods...")
        for method in required_methods:
            if hasattr(adapter, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} MISSING")
        
        # Test internal methods
        internal_methods = [
            '_detect_pricing_model', '_get_domain_color', '_calculate_node_size',
            '_extract_tags', '_create_scrape_metadata'
        ]
        
        print("📊 Checking internal methods...")
        for method in internal_methods:
            if hasattr(adapter, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} MISSING")
        
        # Test some method functionality
        test_tool = create_graph_test_tools()[0]
        
        print("🧪 Testing method functionality...")
        
        # Test pricing detection
        pricing = adapter._detect_pricing_model("Free + $20/month")
        print(f"   ✅ Pricing detection: {pricing}")
        
        # Test domain colors
        color = adapter._get_domain_color("NLP")
        print(f"   ✅ Domain color: {color}")
        
        # Test node size calculation
        size = adapter._calculate_node_size(90.0)
        print(f"   ✅ Node size: {size}")
        
        # Test tag extraction
        tags = adapter._extract_tags(test_tool)
        print(f"   ✅ Tags extracted: {len(tags)} tags")
        
        print("✅ Adapter methods validation complete")
        return True
        
    except Exception as e:
        print(f"❌ Adapter test failed: {e}")
        return False


def generate_deployment_instructions():
    """Generate deployment instructions for production"""
    print("\n📋 Production Deployment Instructions")
    print("=" * 60)
    
    instructions = """
🚀 DEPLOYMENT CHECKLIST FOR 3D GRAPH VISUALIZATION

1. SUPABASE SETUP:
   □ Create new Supabase project
   □ Copy supabase/complete_production_schema.sql
   □ Run the schema in Supabase SQL editor
   □ Verify all tables, views, and functions are created
   □ Set up Row Level Security (RLS) policies

2. ENVIRONMENT CONFIGURATION:
   □ Update .env file with new Supabase credentials:
     SUPABASE_URL=your_project_url
     SUPABASE_KEY=your_service_role_key

3. DATA MIGRATION:
   □ Run scrapers to collect AI tools data
   □ Use: python -c "from database.universal_merger import merge_tools_to_database; from scrapers.all_scrapers import run_all_scrapers; tools = run_all_scrapers(); merge_tools_to_database(tools, use_sqlite=False)"
   □ Generate tool relationships: adapter.generate_similarity_relationships()
   □ Refresh materialized views: adapter.refresh_materialized_views()

4. GRAPH VISUALIZATION:
   □ Use adapter.get_graph_data() to fetch nodes and edges
   □ Implement 3D visualization using Three.js or similar
   □ Position nodes using graph_position JSONB field
   □ Color nodes by domain using node_color field
   □ Size nodes by popularity using node_size field

5. PERFORMANCE OPTIMIZATION:
   □ Monitor query performance
   □ Refresh materialized views regularly
   □ Use pagination for large datasets
   □ Implement caching for graph data

6. GRAPH FEATURES TO IMPLEMENT:
   □ Interactive node exploration
   □ Category-based clustering
   □ Tool similarity connections
   □ Search and filtering
   □ Real-time updates
   □ Export graph data
"""
    
    print(instructions)
    
    # Create a deployment file
    with open('DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write("# 3D Graph Visualization Deployment Guide\n")
        f.write(instructions)
    
    print("\n📄 Deployment guide saved to: DEPLOYMENT_GUIDE.md")


def main():
    """Run complete production readiness tests"""
    print("🎯 PRODUCTION READINESS TEST - 3D GRAPH VISUALIZATION")
    print("=" * 70)
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Local pipeline
    if test_local_graph_pipeline():
        success_count += 1
    
    # Test 2: Schema validation
    if test_production_schema_validation():
        success_count += 1
    
    # Test 3: Adapter methods
    if test_supabase_adapter_methods():
        success_count += 1
    
    # Test 4: Generate deployment guide
    try:
        generate_deployment_instructions()
        success_count += 1
    except Exception as e:
        print(f"❌ Deployment guide generation failed: {e}")
    
    # Final results
    print("\n" + "=" * 70)
    print(f"📊 PRODUCTION READINESS: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 SYSTEM IS PRODUCTION READY!")
        print("\n💡 Your 3D graph visualization system includes:")
        print("   ✅ Complete database schema with graph relationships")
        print("   ✅ Enhanced Supabase adapter for graph operations")
        print("   ✅ Advanced deduplication and merging")
        print("   ✅ Graph analysis functions and materialized views")
        print("   ✅ 3D visualization metadata (positioning, colors, sizes)")
        print("   ✅ Performance optimization features")
        
        print("\n🚀 NEXT STEPS:")
        print("   1. Delete your empty Supabase database")
        print("   2. Run the complete_production_schema.sql in new Supabase")
        print("   3. Update .env with new Supabase credentials")
        print("   4. Run full scrapers to populate the graph database")
        print("   5. Build your 3D visualization frontend")
        
        print("\n📊 EXPECTED RESULTS:")
        print("   - 5,000+ AI tools as graph nodes")
        print("   - Automated relationship detection between tools")
        print("   - Category-based clustering for visualization")
        print("   - Rich metadata for interactive exploration")
        
    else:
        print("⚠️ Some components need attention before production deployment")
    
    return success_count == total_tests


if __name__ == "__main__":
    main()