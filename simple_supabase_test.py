#!/usr/bin/env python3
"""
Simple test to diagnose Supabase connection issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_basic_connection():
    """Test basic connection with detailed error info"""
    try:
        print("🔍 Testing basic Supabase connection...")
        
        # Check environment variables
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        print(f"📡 URL: {url}")
        print(f"🔑 Key: {key[:50]}..." if key else "❌ No key found")
        
        if not url or not key:
            print("❌ Missing environment variables")
            return False
        
        # Test import
        print("📦 Importing supabase...")
        from supabase import create_client, Client
        print("✅ Import successful")
        
        # Test connection
        print("🔌 Creating client...")
        supabase: Client = create_client(url, key)
        print("✅ Client created")
        
        # Test simple query
        print("🔍 Testing simple query...")
        response = supabase.table('ai_tool').select('count').execute()
        print(f"✅ Query successful: {response}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print(f"❌ Error type: {type(e)}")
        return False

def test_requests_connection():
    """Test connection using requests library"""
    try:
        print("\n🔍 Testing with requests library...")
        
        import requests
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        
        # Test REST API directly
        rest_url = f"{url}/rest/v1/ai_tool?select=id&limit=1"
        response = requests.get(rest_url, headers=headers, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ REST API connection successful")
            return True
        else:
            print(f"❌ REST API failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Requests test failed: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        print("\n🔍 Checking dependencies...")
        
        dependencies = [
            'supabase',
            'requests',
            'dotenv'
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
                print(f"✅ {dep} - installed")
            except ImportError:
                print(f"❌ {dep} - missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependency check failed: {e}")
        return False

def main():
    """Run diagnostic tests"""
    print("🩺 Supabase Connection Diagnostic\n")
    
    tests = [
        ("Dependencies Check", check_dependencies),
        ("Basic Connection Test", test_basic_connection),
        ("Requests Connection Test", test_requests_connection)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Running: {test_name}")
        print('='*40)
        
        try:
            result = test_func()
            print(f"Result: {'✅ PASS' if result else '❌ FAIL'}")
        except Exception as e:
            print(f"❌ Test crashed: {e}")

if __name__ == "__main__":
    main()