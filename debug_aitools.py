#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
import json

def debug_aitools_directory():
    """Debug script to understand AITools Directory structure"""
    
    print("🔍 Debugging AITools Directory...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    # Test 1: Check if API endpoints exist
    print("\n=== TESTING API ENDPOINTS ===")
    api_urls = [
        "https://aitoolsdirectory.com/api/tools",
        "https://aitoolsdirectory.com/api/v1/tools", 
        "https://aitoolsdirectory.com/api/tools.json",
        "https://aitoolsdirectory.com/_next/static/chunks/pages/index.js",
        "https://aitoolsdirectory.com/tools.json"
    ]
    
    for url in api_urls:
        try:
            response = session.get(url, timeout=10)
            print(f"  {url}: {response.status_code}")
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"    JSON data found! Keys: {list(data.keys()) if isinstance(data, dict) else f'Array with {len(data)} items'}")
                    except:
                        print(f"    Response looks like JSON but failed to parse")
                else:
                    print(f"    Content-Type: {content_type}")
                    print(f"    First 200 chars: {response.text[:200]}")
        except Exception as e:
            print(f"  {url}: ERROR - {e}")
    
    # Test 2: Main page structure
    print("\n=== ANALYZING MAIN PAGE ===")
    try:
        response = session.get("https://aitoolsdirectory.com", timeout=15)
        print(f"Main page status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for common tool selectors
            selectors_to_test = [
                '[data-testid*="tool"]',
                '.tool-card', 
                '.ai-tool',
                'article',
                '.card',
                '[class*="tool"]',
                '[class*="item"]',
                '[id*="tool"]',
                '.grid > div',
                '.list-item',
                '.product',
                '.entry'
            ]
            
            print("Testing selectors:")
            for selector in selectors_to_test:
                elements = soup.select(selector)
                print(f"  {selector}: {len(elements)} elements")
                if len(elements) > 0 and len(elements) <= 5:
                    for i, elem in enumerate(elements[:2]):
                        print(f"    Element {i}: {elem.name} - {elem.get('class', [])} - {elem.get_text()[:100]}")
            
            # Look for script tags that might contain data
            print("\nScript tags analysis:")
            scripts = soup.find_all('script')
            for i, script in enumerate(scripts):
                if script.string and any(keyword in script.string for keyword in ['tools', 'data', 'props', 'window']):
                    content = script.string[:500]
                    print(f"  Script {i}: {content}")
            
            # Check for Next.js or React patterns
            print("\nFramework detection:")
            if soup.find('script', src=lambda x: x and '_next' in x):
                print("  Next.js detected!")
            if soup.find(id='__next'):
                print("  React root found!")
            if soup.find('div', {'data-reactroot': True}):
                print("  React app detected!")
            
            # Look for JSON-LD or other structured data
            json_scripts = soup.find_all('script', type='application/ld+json')
            print(f"  JSON-LD scripts: {len(json_scripts)}")
            
            # Check for common AJAX loading patterns
            loading_indicators = soup.select('[class*="loading"], [class*="spinner"], [id*="loading"]')
            print(f"  Loading indicators: {len(loading_indicators)}")
            
    except Exception as e:
        print(f"Error analyzing main page: {e}")
    
    # Test 3: Tools page
    print("\n=== ANALYZING TOOLS PAGE ===")
    try:
        response = session.get("https://aitoolsdirectory.com/tools", timeout=15)
        print(f"Tools page status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"Tools page title: {soup.title.string if soup.title else 'No title'}")
            
            # Count different element types
            element_counts = {
                'divs': len(soup.find_all('div')),
                'articles': len(soup.find_all('article')),
                'links': len(soup.find_all('a')),
                'images': len(soup.find_all('img')),
                'h1-h6': len(soup.select('h1, h2, h3, h4, h5, h6'))
            }
            print(f"Element counts: {element_counts}")
            
    except Exception as e:
        print(f"Error analyzing tools page: {e}")

if __name__ == "__main__":
    debug_aitools_directory()