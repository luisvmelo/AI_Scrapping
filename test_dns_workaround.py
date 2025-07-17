#!/usr/bin/env python3
"""
Test DNS workaround for WSL2
"""

import os
import socket
import subprocess
from dotenv import load_dotenv

load_dotenv()

def test_with_dns_workaround():
    """Test with DNS workaround"""
    try:
        # Try manually setting DNS
        hostname = "figybjxmgmyzmmlphatm.supabase.co"
        
        print(f"🔍 Testing DNS workaround for: {hostname}")
        
        # Method 1: Try to get IP from system DNS
        try:
            result = subprocess.run(['getent', 'hosts', hostname], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                ip = result.stdout.split()[0]
                print(f"✅ System DNS resolution: {hostname} -> {ip}")
                
                # Now test connection with this IP
                return test_connection_with_ip(ip, hostname)
            else:
                print(f"❌ System DNS failed: {result.stderr}")
        except Exception as e:
            print(f"❌ System DNS command failed: {e}")
        
        # Method 2: Use known Cloudflare IPs for supabase.co
        print("\n🔍 Trying with known DNS...")
        try:
            # Supabase uses Cloudflare, try some common IPs
            cloudflare_ips = ["104.18.38.10", "104.18.39.10"]
            
            for ip in cloudflare_ips:
                print(f"🔍 Trying IP: {ip}")
                if test_connection_with_ip(ip, hostname):
                    return True
                    
        except Exception as e:
            print(f"❌ Cloudflare IP test failed: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ DNS workaround failed: {e}")
        return False

def test_connection_with_ip(ip, hostname):
    """Test connection using specific IP"""
    try:
        import requests
        import urllib3
        
        # Disable SSL warnings for this test
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        url = f"https://{ip}/rest/v1/ai_tool?select=id&limit=1"
        key = os.getenv("SUPABASE_KEY")
        
        headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Host': hostname  # This is crucial for virtual hosting
        }
        
        print(f"🔗 Testing: {url}")
        print(f"🏠 Host header: {hostname}")
        
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        
        print(f"📡 Status: {response.status_code}")
        print(f"📄 Response length: {len(response.text)}")
        
        if response.status_code == 200:
            print(f"✅ Connection successful with IP {ip}!")
            
            # Test if we have data
            try:
                data = response.json()
                print(f"📊 Data received: {len(data) if isinstance(data, list) else 'Object'} records")
                return True
            except:
                print("⚠️ Response not JSON, but connection successful")
                return True
                
        elif response.status_code == 401:
            print("🔐 Authentication issue (but connection works!)")
            return True  # Connection works, just auth issue
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_supabase_with_workaround():
    """Test Supabase client with IP workaround"""
    try:
        print("\n🔍 Testing Supabase client with IP workaround...")
        
        # Monkey patch socket.getaddrinfo to return our IP
        original_getaddrinfo = socket.getaddrinfo
        
        def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            if 'figybjxmgmyzmmlphatm.supabase.co' in host:
                # Return our known IP
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('104.18.38.10', port))]
            return original_getaddrinfo(host, port, family, type, proto, flags)
        
        socket.getaddrinfo = custom_getaddrinfo
        
        try:
            from supabase import create_client
            
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            print(f"🔌 Creating Supabase client...")
            supabase = create_client(url, key)
            
            print(f"🔍 Testing query...")
            response = supabase.table('ai_tool').select('id').limit(1).execute()
            
            print(f"✅ Supabase client works! Got {len(response.data)} records")
            return True
            
        finally:
            # Restore original function
            socket.getaddrinfo = original_getaddrinfo
            
    except Exception as e:
        print(f"❌ Supabase client test failed: {e}")
        return False

if __name__ == "__main__":
    print("🩺 DNS Workaround Test\n")
    
    # Test 1: Direct connection with IP
    success1 = test_with_dns_workaround()
    
    # Test 2: Supabase client with monkey patch
    success2 = test_supabase_with_workaround()
    
    print(f"\n📊 Results:")
    print(f"Direct IP connection: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Supabase client: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 or success2:
        print("\n💡 Solution found! The issue is DNS resolution in WSL2.")
        print("Recommended fixes:")
        print("1. Use the monkey-patch approach in your code")
        print("2. Configure WSL2 DNS properly")
        print("3. Use a different network setup")
    else:
        print("\n❌ No workaround succeeded. May need different approach.")