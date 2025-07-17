#!/usr/bin/env python3
"""
Test DNS resolution in Python
"""

import socket
import os
from dotenv import load_dotenv

load_dotenv()

def test_dns_resolution():
    """Test DNS resolution"""
    try:
        url = os.getenv("SUPABASE_URL")
        hostname = url.replace("https://", "").replace("http://", "")
        
        print(f"🔍 Testing DNS resolution for: {hostname}")
        
        # Test socket resolution
        try:
            ip = socket.gethostbyname(hostname)
            print(f"✅ Socket resolution successful: {hostname} -> {ip}")
        except Exception as e:
            print(f"❌ Socket resolution failed: {e}")
        
        # Test getaddrinfo
        try:
            result = socket.getaddrinfo(hostname, 443)
            print(f"✅ getaddrinfo successful: {len(result)} addresses found")
            for r in result[:3]:  # Show first 3
                print(f"   {r[4][0]}")
        except Exception as e:
            print(f"❌ getaddrinfo failed: {e}")
        
        # Test with different DNS servers
        print("\n🔍 Testing alternative approach...")
        try:
            import requests
            # Try to connect directly with IP from ping
            ip_url = "https://104.18.38.10/rest/v1/ai_tool?select=id&limit=1"
            key = os.getenv("SUPABASE_KEY")
            
            headers = {
                'apikey': key,
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json',
                'Host': hostname  # Important: specify the correct host header
            }
            
            response = requests.get(ip_url, headers=headers, timeout=10, verify=False)
            print(f"📡 Direct IP connection: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Direct IP connection failed: {e}")
        
    except Exception as e:
        print(f"❌ DNS test failed: {e}")

if __name__ == "__main__":
    test_dns_resolution()