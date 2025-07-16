#!/usr/bin/env python3

import requests
import json
from urllib.parse import urljoin

def check_with_proper_headers():
    """Try with headers that mimic a real browser visiting the site"""
    
    session = requests.Session()
    
    # Set comprehensive browser headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    })
    
    print("🌐 Trying with comprehensive browser headers...")
    
    # First, visit main page to establish session
    print("\n=== ESTABLISHING SESSION ===")
    try:
        main_response = session.get("https://aitoolsdirectory.com", timeout=15)
        print(f"Main page: {main_response.status_code}")
        
        # Check for any cookies or session data
        if main_response.cookies:
            print(f"Cookies received: {dict(main_response.cookies)}")
        
        # Update headers for subsequent requests
        session.headers.update({
            'Referer': 'https://aitoolsdirectory.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        })
        
    except Exception as e:
        print(f"Error establishing session: {e}")
        return
    
    # Now try API endpoints with proper session
    print("\n=== TESTING API WITH SESSION ===")
    
    # Try different possible API endpoints
    api_endpoints = [
        "https://api.spreadsimple.com/web/public",
        "https://api.spreadsimple.com/web/data", 
        "https://api.spreadsimple.com/public/data",
        "https://api.spreadsimple.com/v1/data",
        "https://api.spreadsimple.com/v1/public",
        # Try with domain as parameter
        "https://api.spreadsimple.com/web/public?domain=aitoolsdirectory.com",
        "https://api.spreadsimple.com/web/data?domain=aitoolsdirectory.com",
        "https://api.spreadsimple.com/web/public?site=aitoolsdirectory.com",
        "https://api.spreadsimple.com/web/data?site=aitoolsdirectory.com",
        # Try with different domain formats
        "https://api.spreadsimple.com/web/public?host=aitoolsdirectory.com",
        "https://api.spreadsimple.com/web/data?host=aitoolsdirectory.com",
    ]
    
    for endpoint in api_endpoints:
        try:
            response = session.get(endpoint, timeout=10)
            print(f"{endpoint}")
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"  Content-Type: {content_type}")
                
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"  🎉 JSON Response received!")
                        
                        if isinstance(data, dict):
                            print(f"  Dict keys: {list(data.keys())}")
                            # Look for common data keys
                            for key in ['data', 'items', 'tools', 'results', 'records']:
                                if key in data:
                                    value = data[key]
                                    if isinstance(value, list):
                                        print(f"  {key}: List with {len(value)} items")
                                        if len(value) > 0:
                                            print(f"    First item: {list(value[0].keys()) if isinstance(value[0], dict) else value[0]}")
                        elif isinstance(data, list):
                            print(f"  List with {len(data)} items")
                            if len(data) > 0:
                                print(f"  First item: {list(data[0].keys()) if isinstance(data[0], dict) else data[0]}")
                        
                        # Save the response
                        with open(f'api_response_{endpoint.split("/")[-1].replace("?", "_").replace("=", "_")}.json', 'w') as f:
                            json.dump(data, f, indent=2)
                        
                        return endpoint, data
                        
                    except json.JSONDecodeError as e:
                        print(f"  JSON decode error: {e}")
                        print(f"  Raw response: {response.text[:200]}")
                else:
                    print(f"  Non-JSON response: {response.text[:100]}")
                    
            elif response.status_code == 404:
                print(f"  Not found")
            elif response.status_code == 403:
                print(f"  Forbidden - might need authentication")
            elif response.status_code == 401:
                print(f"  Unauthorized - needs authentication")
            else:
                print(f"  Unexpected status")
                if response.text:
                    print(f"  Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ERROR: {e}")
    
    # Try to find any references to the actual spreadsheet
    print("\n=== SEARCHING FOR GOOGLE SHEETS REFERENCES ===")
    try:
        main_response = session.get("https://aitoolsdirectory.com", timeout=15)
        content = main_response.text.lower()
        
        # Look for Google Sheets patterns
        patterns = [
            'docs.google.com/spreadsheets',
            'sheets.googleapis.com',
            'spreadsheet',
            'sheet_id',
            'gid='
        ]
        
        for pattern in patterns:
            if pattern in content:
                print(f"Found pattern: {pattern}")
                # Try to extract the context
                import re
                context_pattern = rf'.{{0,50}}{pattern}.{{0,50}}'
                matches = re.findall(context_pattern, content)
                for match in matches[:3]:  # Show first 3 matches
                    print(f"  Context: ...{match}...")

    except Exception as e:
        print(f"Error searching for sheets: {e}")

if __name__ == "__main__":
    result = check_with_proper_headers()
    if result:
        endpoint, data = result
        print(f"\n🎉 SUCCESS! Working endpoint: {endpoint}")
    else:
        print("\n❌ No working endpoint found with session headers")