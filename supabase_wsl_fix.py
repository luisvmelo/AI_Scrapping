#!/usr/bin/env python3
"""
WSL2 DNS fix for Supabase connections
"""

import socket
import os
from contextlib import contextmanager

# Store the original getaddrinfo function
_original_getaddrinfo = socket.getaddrinfo

# Known working IP for the Supabase instance
SUPABASE_IP_MAP = {
    'figybjxmgmyzmmlphatm.supabase.co': '104.18.38.10'
}

def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """
    Patched getaddrinfo that resolves known Supabase hosts to their IPs
    """
    # Check if this is a known Supabase host
    for hostname, ip in SUPABASE_IP_MAP.items():
        if hostname in host:
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, port))]
    
    # For all other hosts, use original function
    return _original_getaddrinfo(host, port, family, type, proto, flags)

@contextmanager
def supabase_dns_fix():
    """
    Context manager that temporarily patches DNS resolution for Supabase
    """
    # Apply the patch
    socket.getaddrinfo = patched_getaddrinfo
    
    try:
        yield
    finally:
        # Restore original function
        socket.getaddrinfo = _original_getaddrinfo

def test_fixed_connection():
    """Test Supabase connection with DNS fix"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        print("🔧 Testing Supabase connection with DNS fix...")
        
        with supabase_dns_fix():
            from supabase import create_client
            
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            print(f"📡 Connecting to: {url}")
            supabase = create_client(url, key)
            
            print("🔍 Testing simple query...")
            response = supabase.table('ai_tool').select('id').limit(1).execute()
            
            print(f"✅ SUCCESS! Retrieved {len(response.data)} records")
            
            if response.data:
                print(f"📊 Sample record ID: {response.data[0].get('id')}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_schema_with_fix():
    """Test schema structure with DNS fix"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        print("\n🔧 Testing schema structure with DNS fix...")
        
        with supabase_dns_fix():
            from supabase import create_client
            
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            supabase = create_client(url, key)
            
            # Test enhanced columns
            enhanced_columns = [
                'id', 'name', 'url', 'logo_url', 'rank', 'upvotes', 
                'monthly_users', 'editor_score', 'maturity', 'platform', 
                'features', 'last_scraped'
            ]
            
            columns_str = ', '.join(enhanced_columns)
            response = supabase.table('ai_tool').select(columns_str).limit(1).execute()
            
            if response.data:
                sample = response.data[0]
                print(f"✅ Enhanced schema test successful!")
                print(f"📊 Available columns: {list(sample.keys())}")
                
                # Check which enhanced fields are None vs have data
                enhanced_fields = ['url', 'logo_url', 'rank', 'upvotes', 'monthly_users', 
                                 'editor_score', 'maturity', 'platform', 'features', 'last_scraped']
                
                populated_fields = [field for field in enhanced_fields if sample.get(field) is not None]
                empty_fields = [field for field in enhanced_fields if sample.get(field) is None]
                
                print(f"📈 Populated enhanced fields: {populated_fields}")
                print(f"📉 Empty enhanced fields: {empty_fields}")
                
                return True
            else:
                print("⚠️ No data in table to test schema")
                return True
                
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        
        # Try individual column tests
        try:
            with supabase_dns_fix():
                from supabase import create_client
                
                url = os.getenv("SUPABASE_URL")
                key = os.getenv("SUPABASE_KEY")
                supabase = create_client(url, key)
                
                print("\n🔍 Testing individual columns...")
                
                # Test basic columns first
                basic_response = supabase.table('ai_tool').select('id, name, description').limit(1).execute()
                print(f"✅ Basic columns work: {len(basic_response.data)} records")
                
                # Test enhanced columns one by one
                enhanced_fields = ['url', 'logo_url', 'rank', 'upvotes', 'monthly_users', 
                                 'editor_score', 'maturity', 'platform', 'features', 'last_scraped']
                
                working_fields = []
                broken_fields = []
                
                for field in enhanced_fields:
                    try:
                        test_response = supabase.table('ai_tool').select(f'id, {field}').limit(1).execute()
                        working_fields.append(field)
                        print(f"✅ {field}")
                    except Exception as field_error:
                        broken_fields.append(field)
                        print(f"❌ {field}: {field_error}")
                
                print(f"\n📊 Working enhanced fields: {working_fields}")
                print(f"💥 Broken enhanced fields: {broken_fields}")
                
                return len(broken_fields) == 0
                
        except Exception as e2:
            print(f"❌ Individual column test also failed: {e2}")
            return False

if __name__ == "__main__":
    print("🔧 Supabase WSL2 DNS Fix Test\n")
    
    # Test connection
    connection_works = test_fixed_connection()
    
    # Test schema
    schema_works = test_schema_with_fix()
    
    print(f"\n📊 Results:")
    print(f"Connection: {'✅ WORKING' if connection_works else '❌ BROKEN'}")
    print(f"Schema: {'✅ SYNCHRONIZED' if schema_works else '❌ NEEDS UPDATE'}")
    
    if connection_works and schema_works:
        print("\n🎉 SUCCESS! Supabase is working and synchronized!")
        print("\n💡 To use this fix in your code:")
        print("```python")
        print("from supabase_wsl_fix import supabase_dns_fix")
        print("")
        print("with supabase_dns_fix():")
        print("    # Your Supabase code here")
        print("    supabase = create_client(url, key)")
        print("    response = supabase.table('ai_tool').select('*').execute()")
        print("```")
    elif connection_works:
        print("\n⚠️ Connection works but schema needs updates!")
        print("Run the SQL migration in Supabase dashboard.")
    else:
        print("\n❌ Connection still not working. Check credentials and network.")