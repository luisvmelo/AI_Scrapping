#!/usr/bin/env python3

import requests
import json
import re

def find_spreadsimple_api():
    """Find the SpreadSimple API endpoint for AITools Directory"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://aitoolsdirectory.com',
        'Origin': 'https://aitoolsdirectory.com'
    })
    
    print("🔍 Looking for SpreadSimple API endpoint...")
    
    # First, let's try to get the site's configuration
    try:
        # Try common SpreadSimple API patterns
        # The JS showed api.spreadsimple.com endpoints
        
        # Method 1: Try to find the spreadsheet ID from the main page
        response = session.get("https://aitoolsdirectory.com", timeout=15)
        if response.status_code == 200:
            # Look for any IDs or config in the HTML
            content = response.text
            
            # Common patterns for SpreadSimple sites
            patterns = [
                r'spreadsheet[_-]?id["\']?\s*[=:]\s*["\']([^"\']+)["\']',
                r'spread[_-]?view[_-]?id["\']?\s*[=:]\s*["\']([^"\']+)["\']',
                r'data[_-]?id["\']?\s*[=:]\s*["\']([^"\']+)["\']',
                r'id["\']?\s*[=:]\s*["\']([a-zA-Z0-9_-]{10,})["\']',
                r'/api/([a-zA-Z0-9_-]+)',
                r'spreadsheet/([a-zA-Z0-9_-]+)'
            ]
            
            found_ids = []
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_ids.extend(matches)
            
            print(f"Potential IDs found: {list(set(found_ids))}")
            
            # Extract domain to see if we can find the sheet ID
            domain_match = re.search(r'aitoolsdirectory\.com', content)
            if domain_match:
                print("Domain confirmed in content")
    
    except Exception as e:
        print(f"Error getting main page: {e}")
    
    # Method 2: Try direct SpreadSimple API patterns
    print("\n=== TESTING SPREADSIMPLE API PATTERNS ===")
    
    # Common SpreadSimple endpoints
    api_patterns = [
        "https://api.spreadsimple.com/getspreadsheetdata/aitoolsdirectory",
        "https://api.spreadsimple.com/spreadsheet/aitoolsdirectory", 
        "https://api.spreadsimple.com/getdata/aitoolsdirectory",
        "https://api.spreadsimple.com/api/v1/aitoolsdirectory",
        "https://api.spreadsimple.com/api/aitoolsdirectory",
        "https://api.spreadsimple.com/data/aitoolsdirectory"
    ]
    
    # Also try with the domain
    site_id = "aitoolsdirectory.com"
    api_patterns.extend([
        f"https://api.spreadsimple.com/getspreadsheetdata/{site_id}",
        f"https://api.spreadsimple.com/spreadsheet/{site_id}",
        f"https://api.spreadsimple.com/getdata/{site_id}",
        f"https://api.spreadsimple.com/api/v1/{site_id}",
        f"https://api.spreadsimple.com/api/{site_id}",
        f"https://api.spreadsimple.com/data/{site_id}"
    ])
    
    for api_url in api_patterns:
        try:
            response = session.get(api_url, timeout=10)
            print(f"{api_url}: {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"  🎉 SUCCESS! JSON data found")
                        print(f"  Content-Type: {content_type}")
                        
                        if isinstance(data, dict):
                            print(f"  Keys: {list(data.keys())}")
                            if 'data' in data:
                                print(f"  Data length: {len(data['data']) if isinstance(data['data'], list) else 'Not a list'}")
                        elif isinstance(data, list):
                            print(f"  Array length: {len(data)}")
                            if len(data) > 0:
                                print(f"  First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
                        
                        # Save a sample for analysis
                        with open('sample_api_response.json', 'w') as f:
                            json.dump(data, f, indent=2)
                        print(f"  Sample saved to sample_api_response.json")
                        
                        return api_url, data
                        
                    except json.JSONDecodeError:
                        print(f"  Response is not valid JSON")
                        print(f"  First 200 chars: {response.text[:200]}")
                else:
                    print(f"  Content-Type: {content_type}")
                    if response.text:
                        print(f"  First 200 chars: {response.text[:200]}")
                        
        except Exception as e:
            print(f"{api_url}: ERROR - {e}")
    
    # Method 3: Try to reverse engineer from the main JS file
    print("\n=== ANALYZING MAIN JS FOR API CALLS ===")
    try:
        js_response = session.get("https://spread.name/js/index.js?_hash=6bdbfc10", timeout=15)
        if js_response.status_code == 200:
            js_content = js_response.text
            
            # Look for API endpoint patterns in the JS
            api_patterns_in_js = [
                r'https://api\.spreadsimple\.com/[^"\'\\s]+',
                r'/api/[^"\'\\s]+',
                r'getspreadsheetdata[^"\'\\s]*',
                r'spreadsheet/[^"\'\\s]+',
                r'data/[^"\'\\s]+'
            ]
            
            for pattern in api_patterns_in_js:
                matches = re.findall(pattern, js_content, re.IGNORECASE)
                if matches:
                    print(f"JS Pattern '{pattern}': {list(set(matches))[:10]}")  # First 10 unique
                    
                    # Try to construct full URLs from relative paths
                    for match in set(matches):
                        if match.startswith('/'):
                            full_url = f"https://api.spreadsimple.com{match}"
                            print(f"  Trying constructed URL: {full_url}")
                            try:
                                test_response = session.get(full_url, timeout=5)
                                print(f"    Status: {test_response.status_code}")
                            except:
                                pass
    
    except Exception as e:
        print(f"Error analyzing JS: {e}")
    
    return None, None

if __name__ == "__main__":
    api_url, data = find_spreadsimple_api()
    
    if api_url:
        print(f"\n🎉 FOUND WORKING API: {api_url}")
        print(f"Data structure discovered and saved to sample_api_response.json")
    else:
        print("\n❌ No working API endpoint found")
        print("The site likely uses dynamic loading with authentication or different patterns")