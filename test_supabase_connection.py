#!/usr/bin/env python3
"""
Test script to verify Supabase connection and schema synchronization
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test basic Supabase connection"""
    try:
        print("🔍 Testing Supabase connection...")
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            print("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env file")
            return False
        
        print(f"📡 Connecting to: {url}")
        supabase: Client = create_client(url, key)
        
        # Test simple query
        response = supabase.table('ai_tool').select('id').limit(1).execute()
        print(f"✅ Connection successful! Table exists with {len(response.data)} sample records")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_schema_structure():
    """Test if all expected columns exist in ai_tool table"""
    try:
        print("\n🔍 Testing schema structure...")
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        
        # Try to select all columns that should exist
        expected_columns = [
            'id', 'ext_id', 'name', 'description', 'price', 'popularity', 
            'categories', 'source', 'macro_domain', 'content_hash',
            'created_at', 'updated_at',
            # Enhanced fields
            'url', 'logo_url', 'rank', 'upvotes', 'monthly_users', 
            'editor_score', 'maturity', 'platform', 'features', 'last_scraped'
        ]
        
        # Test selecting all columns
        columns_str = ', '.join(expected_columns)
        response = supabase.table('ai_tool').select(columns_str).limit(1).execute()
        
        if response.data:
            print("✅ All expected columns exist in the schema!")
            sample_record = response.data[0]
            print(f"📊 Sample record keys: {list(sample_record.keys())}")
            return True
        else:
            print("⚠️ Table exists but no data found")
            return True
            
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        
        # Try to identify which columns are missing
        print("\n🔍 Checking individual columns...")
        basic_columns = ['id', 'name', 'description', 'source']
        
        try:
            response = supabase.table('ai_tool').select(', '.join(basic_columns)).limit(1).execute()
            print(f"✅ Basic columns exist: {basic_columns}")
        except Exception as e2:
            print(f"❌ Even basic columns failed: {e2}")
        
        # Test enhanced columns individually
        enhanced_columns = ['url', 'logo_url', 'rank', 'upvotes', 'monthly_users', 
                          'editor_score', 'maturity', 'platform', 'features', 'last_scraped']
        
        for col in enhanced_columns:
            try:
                response = supabase.table('ai_tool').select(f'id, {col}').limit(1).execute()
                print(f"✅ Column '{col}' exists")
            except Exception as e3:
                print(f"❌ Column '{col}' missing: {e3}")
        
        return False

def test_insert_sample_tool():
    """Test inserting a sample tool with all enhanced fields"""
    try:
        print("\n🔍 Testing sample tool insertion...")
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        
        # Create sample tool data
        sample_tool = {
            'ext_id': 'test_tool_123',
            'name': 'Test AI Tool',
            'description': 'This is a test tool for schema validation',
            'price': 'Free',
            'popularity': 85.5,
            'categories': ['test', 'ai'],
            'source': 'test_source',
            'macro_domain': 'OTHER',
            'content_hash': 'test_hash_123',
            # Enhanced fields
            'url': 'https://example.com/test-tool',
            'logo_url': 'https://example.com/logo.png',
            'rank': 1,
            'upvotes': 100,
            'monthly_users': 5000,
            'editor_score': 8.5,
            'maturity': 'stable',
            'platform': ['web', 'mobile'],
            'features': {'free_tier': True, 'api_available': True},
            'last_scraped': datetime.now().isoformat()
        }
        
        # Insert sample tool
        response = supabase.table('ai_tool').insert(sample_tool).execute()
        
        if response.data:
            inserted_id = response.data[0]['id']
            print(f"✅ Sample tool inserted successfully with ID: {inserted_id}")
            
            # Clean up - delete the test record
            delete_response = supabase.table('ai_tool').delete().eq('id', inserted_id).execute()
            print("🧹 Test record cleaned up")
            
            return True
        else:
            print("❌ Insert failed - no data returned")
            return False
            
    except Exception as e:
        print(f"❌ Insert test failed: {e}")
        return False

def test_merge_functionality():
    """Test the enhanced merge functionality"""
    try:
        print("\n🔍 Testing merge functionality...")
        
        # Import our enhanced merger
        from merge.merge_and_upsert import SupabaseMerger
        from scrapers.common import AITool
        
        merger = SupabaseMerger()
        
        # Create test tools
        test_tools = [
            AITool(
                ext_id='test_merge_1',
                name='Test Merge Tool',
                description='Test tool for merge functionality',
                price='Free',
                popularity=70,
                categories=['test'],
                source='test_source',
                url='https://example.com/merge-test',
                upvotes=50,
                monthly_users=1000,
                last_scraped=datetime.now()
            )
        ]
        
        # Test the merge
        stats = merger.merge_and_upsert_tools(test_tools)
        print(f"✅ Merge test completed: {stats}")
        
        # Clean up
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        supabase = create_client(url, key)
        
        # Delete test record
        supabase.table('ai_tool').delete().eq('ext_id', 'test_merge_1').execute()
        print("🧹 Test merge record cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Merge test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Supabase synchronization tests...\n")
    
    tests = [
        ("Connection Test", test_supabase_connection),
        ("Schema Structure Test", test_schema_structure),
        ("Sample Insert Test", test_insert_sample_tool),
        ("Merge Functionality Test", test_merge_functionality)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print('='*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Supabase is properly synchronized with the code.")
    else:
        print(f"\n⚠️ {len(tests) - passed} tests failed. Database schema may need updates.")
        print("\nTo fix schema issues, you may need to run the SQL migration:")
        print("1. Open Supabase dashboard")
        print("2. Go to SQL Editor")
        print("3. Run the schema from sql/schema.sql")

if __name__ == "__main__":
    main()