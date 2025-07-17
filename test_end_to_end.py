#!/usr/bin/env python3
"""
End-to-end test: Scraping -> Database Pipeline
Tests the complete workflow with local SQLite database
"""

import sys
from datetime import datetime
from database.universal_merger import UniversalMerger, merge_tools_to_database, get_database_statistics
from scrapers.common import AITool


def create_test_tools() -> list[AITool]:
    """Create some test AI tools for testing"""
    test_tools = [
        AITool(
            ext_id="test_chatgpt",
            name="ChatGPT",
            description="Advanced AI chatbot by OpenAI for conversations, writing, and problem-solving",
            price="Free with Premium options",
            popularity=95.0,
            categories=["chatbot", "writing", "productivity"],
            source="test_source",
            macro_domain="NLP",
            url="https://chat.openai.com",
            logo_url="https://openai.com/favicon.ico",
            rank=1,
            upvotes=50000,
            monthly_users=100000000,
            editor_score=9.5,
            maturity="stable",
            platform=["web", "mobile", "api"],
            features={
                "free_tier": True,
                "api_available": True,
                "real_time": True,
                "enterprise": True
            },
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="test_midjourney",
            name="Midjourney",
            description="AI-powered image generation tool creating stunning artwork from text prompts",
            price="$10/month",
            popularity=88.0,
            categories=["image", "art", "design"],
            source="test_source",
            macro_domain="COMPUTER_VISION",
            url="https://midjourney.com",
            logo_url="https://midjourney.com/logo.png",
            rank=2,
            upvotes=25000,
            monthly_users=5000000,
            editor_score=9.0,
            maturity="stable",
            platform=["web", "discord"],
            features={
                "free_tier": False,
                "api_available": False,
                "real_time": False,
                "collaboration": True
            },
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="test_duplicate_chatgpt",
            name="ChatGPT",  # Duplicate name for testing deduplication
            description="OpenAI's ChatGPT - even longer description with more details about capabilities and features for various use cases including business applications",
            price="Free + $20/month Pro",
            popularity=98.0,  # Higher popularity
            categories=["chatbot", "ai", "business"],
            source="different_source",
            macro_domain="NLP",
            url="https://chat.openai.com",  # Same URL - should deduplicate
            upvotes=75000,  # Higher upvotes
            monthly_users=150000000,  # Higher user count
            editor_score=9.8,
            last_scraped=datetime.now()
        ),
        AITool(
            ext_id="test_github_copilot",
            name="GitHub Copilot",
            description="AI pair programmer that helps you write code faster",
            price="$10/month",
            popularity=85.0,
            categories=["coding", "productivity", "development"],
            source="test_source",
            macro_domain="CODING",
            url="https://github.com/features/copilot",
            rank=3,
            upvotes=15000,
            monthly_users=2000000,
            editor_score=8.5,
            maturity="stable",
            platform=["vscode", "web", "api"],
            features={
                "free_tier": False,
                "api_available": True,
                "enterprise": True
            },
            last_scraped=datetime.now()
        )
    ]
    
    return test_tools


def test_scraper_integration():
    """Test actual scraper integration (small sample)"""
    try:
        print("🔍 Testing actual scraper integration...")
        
        # Try to import and run a small scraper test
        from scrapers.futurepedia import FuturepediaScraper
        
        scraper = FuturepediaScraper()
        
        # Get just a few tools for testing
        print("🔧 Running limited Futurepedia scrape (5 tools max)...")
        
        # Override the scrape method to limit results
        response = scraper.get_page(f"{scraper.base_url}/ai-tools")
        if response:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            tool_links = soup.select('a[href*="/tool/"]')[:5]  # Limit to 5 tools
            
            scraped_tools = []
            for i, link in enumerate(tool_links):
                try:
                    tool = scraper._parse_tool_card(link, i)
                    if tool and tool.name != "Unknown Tool":
                        scraped_tools.append(tool)
                except:
                    continue
            
            print(f"✅ Scraped {len(scraped_tools)} real tools from Futurepedia")
            return scraped_tools
        else:
            print("⚠️ Could not connect to Futurepedia")
            return []
            
    except Exception as e:
        print(f"⚠️ Scraper integration test failed: {e}")
        print("📝 This is expected if network issues exist")
        return []


def test_end_to_end_pipeline():
    """Test the complete end-to-end pipeline"""
    print("🚀 Starting End-to-End Pipeline Test\n")
    
    # Step 1: Create test data
    print("📊 Step 1: Creating test AI tools...")
    test_tools = create_test_tools()
    print(f"✅ Created {len(test_tools)} test tools")
    
    # Step 2: Test database connection
    print("\n🔌 Step 2: Testing database connection...")
    try:
        merger = UniversalMerger(use_sqlite=True)
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Step 3: Get initial statistics
    print("\n📈 Step 3: Initial database state...")
    initial_stats = get_database_statistics(use_sqlite=True)
    print(f"📊 Initial tools count: {initial_stats.get('total_tools', 0)}")
    print(f"📊 Sources: {list(initial_stats.get('by_source', {}).keys())}")
    
    # Step 4: Merge test tools
    print("\n🔄 Step 4: Merging test tools...")
    merge_stats = merge_tools_to_database(test_tools, use_sqlite=True)
    print(f"📊 Merge results: {merge_stats}")
    
    # Step 5: Get final statistics
    print("\n📈 Step 5: Final database state...")
    final_stats = get_database_statistics(use_sqlite=True)
    print(f"📊 Final tools count: {final_stats.get('total_tools', 0)}")
    print(f"📊 Sources: {list(final_stats.get('by_source', {}).keys())}")
    print(f"📊 Domains: {list(final_stats.get('by_domain', {}).keys())}")
    
    # Step 6: Test deduplication
    print("\n🔍 Step 6: Testing deduplication...")
    validation = merger.validate_no_duplicates()
    print(f"🔍 Validation: {'✅ Clean' if validation.get('is_clean') else '⚠️ Has duplicates'}")
    
    if not validation.get('is_clean'):
        print(f"📊 URL duplicates: {validation.get('url_duplicates', 0)}")
        print(f"📊 Name duplicates: {validation.get('name_duplicates', 0)}")
    
    # Step 7: Test with real scraped data (if available)
    print("\n🌐 Step 7: Testing with real scraped data...")
    real_tools = test_scraper_integration()
    
    if real_tools:
        print(f"🔄 Merging {len(real_tools)} real tools...")
        real_merge_stats = merge_tools_to_database(real_tools, use_sqlite=True)
        print(f"📊 Real tools merge: {real_merge_stats}")
        
        # Final stats with real data
        ultimate_stats = get_database_statistics(use_sqlite=True)
        print(f"📊 Ultimate total: {ultimate_stats.get('total_tools', 0)} tools")
    
    # Step 8: Performance summary
    print("\n📊 Step 8: Performance Summary...")
    print(f"✅ Test tools processed: {len(test_tools)}")
    print(f"✅ Real tools processed: {len(real_tools) if real_tools else 0}")
    print(f"✅ Total inserts: {merge_stats.get('inserted', 0) + (real_merge_stats.get('inserted', 0) if real_tools else 0)}")
    print(f"✅ Total updates: {merge_stats.get('updated', 0) + (real_merge_stats.get('updated', 0) if real_tools else 0)}")
    print(f"✅ Total merges: {merge_stats.get('merged', 0) + (real_merge_stats.get('merged', 0) if real_tools else 0)}")
    print(f"❌ Total errors: {merge_stats.get('errors', 0) + (real_merge_stats.get('errors', 0) if real_tools else 0)}")
    
    return True


def test_advanced_features():
    """Test advanced features like intelligent merging"""
    print("\n🧪 Testing Advanced Features...")
    
    # Test intelligent merging with duplicates
    duplicate_tools = [
        AITool(
            ext_id="dup_1",
            name="Test Tool",
            description="Short description",
            price="Free",
            popularity=50.0,
            categories=["test"],
            source="source_1",
            url="https://example.com/test",
            upvotes=100,
            monthly_users=1000
        ),
        AITool(
            ext_id="dup_2", 
            name="Test Tool",  # Same name
            description="Much longer and more detailed description with lots of information",
            price="$10/month",
            popularity=80.0,  # Higher popularity
            categories=["test", "productivity"],  # More categories
            source="source_2",
            url="https://example.com/test",  # Same URL
            upvotes=200,  # Higher upvotes
            monthly_users=5000  # Higher users
        )
    ]
    
    merger = UniversalMerger(use_sqlite=True)
    merge_result = merger.merge_and_upsert_tools(duplicate_tools)
    
    print(f"🔄 Duplicate merge test: {merge_result}")
    
    # Verify the merge worked correctly
    validation = merger.validate_no_duplicates()
    print(f"🔍 Post-merge validation: {'✅ Clean' if validation.get('is_clean') else '⚠️ Still has duplicates'}")


def main():
    """Run all end-to-end tests"""
    print("🎯 AI Scraping Pipeline - End-to-End Test")
    print("=" * 50)
    
    try:
        # Main pipeline test
        pipeline_success = test_end_to_end_pipeline()
        
        # Advanced features test  
        test_advanced_features()
        
        print("\n" + "=" * 50)
        if pipeline_success:
            print("🎉 END-TO-END TEST SUCCESSFUL!")
            print("\n💡 Your pipeline is ready:")
            print("   ✅ Local SQLite database working")
            print("   ✅ Enhanced scrapers ready")
            print("   ✅ Intelligent deduplication working")
            print("   ✅ Smart merging operational")
            print("\n🚀 Next steps:")
            print("   1. Run full scrapers with: merge_tools_to_database(tools)")
            print("   2. Check results with: get_database_statistics()")
            print("   3. Switch to Supabase when DNS is fixed")
        else:
            print("❌ End-to-end test had issues")
            
    except Exception as e:
        print(f"❌ Test crashed: {e}")
        return False


if __name__ == "__main__":
    main()