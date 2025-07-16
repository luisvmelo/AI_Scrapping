#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

def analyze_sitemap():
    """Analyze the sitemap to find all tool URLs"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })
    
    print("🗺️ Analyzing sitemap for tool URLs...")
    
    try:
        # Get sitemap
        response = session.get("https://aitoolsdirectory.com/sitemap.xml", timeout=15)
        if response.status_code == 200:
            print(f"Sitemap retrieved successfully ({len(response.text)} chars)")
            
            # Parse XML
            root = ET.fromstring(response.text)
            
            # Extract all URLs
            urls = []
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None:
                    urls.append(loc.text)
            
            print(f"Found {len(urls)} URLs in sitemap")
            
            # Categorize URLs
            tool_urls = []
            other_urls = []
            
            for url in urls:
                if '/tool/' in url or '/tools/' in url:
                    tool_urls.append(url)
                else:
                    other_urls.append(url)
            
            print(f"Tool URLs: {len(tool_urls)}")
            print(f"Other URLs: {len(other_urls)}")
            
            # Show some examples
            print("\n=== SAMPLE TOOL URLS ===")
            for url in tool_urls[:10]:
                print(f"  {url}")
            
            print("\n=== SAMPLE OTHER URLS ===")
            for url in other_urls[:10]:
                print(f"  {url}")
            
            # Test a few tool pages
            if tool_urls:
                print(f"\n=== TESTING INDIVIDUAL TOOL PAGES ===")
                for i, url in enumerate(tool_urls[:3]):
                    try:
                        print(f"\nTesting: {url}")
                        resp = session.get(url, timeout=10)
                        print(f"  Status: {resp.status_code}")
                        
                        if resp.status_code == 200:
                            soup = BeautifulSoup(resp.text, 'html.parser')
                            print(f"  Elements: {len(soup.find_all())}")
                            
                            # Look for any actual content
                            title = soup.find('title')
                            if title and title.string:
                                print(f"  Title: {title.string}")
                            
                            # Check for meta description
                            meta_desc = soup.find('meta', attrs={'name': 'description'})
                            if meta_desc:
                                print(f"  Description: {meta_desc.get('content', '')[:100]}")
                        
                        time.sleep(1)  # Be respectful
                        
                    except Exception as e:
                        print(f"  Error testing {url}: {e}")
            
            return tool_urls
            
    except Exception as e:
        print(f"Error analyzing sitemap: {e}")
        return []

def investigate_spreadsimple():
    """Investigate SpreadSimple platform"""
    print("\n🔍 Investigating SpreadSimple platform...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://aitoolsdirectory.com'
    })
    
    # Try to understand how SpreadSimple works
    try:
        # Check the main JS file that was referenced
        js_url = "https://spread.name/js/index.js?_hash=6bdbfc10"
        response = session.get(js_url, timeout=10)
        if response.status_code == 200:
            js_content = response.text
            print(f"Main JS file size: {len(js_content)} chars")
            
            # Look for API endpoints in the JS
            import re
            api_patterns = [
                r'["\']https?://[^"\']+api[^"\']*["\']',
                r'["\']https?://api\.[^"\']+["\']',
                r'/api/[^"\'\\s]+',
                r'spreadsheet[^"\']*',
                r'google.*sheets',
                r'api\.spreadsimple\.com[^"\']*'
            ]
            
            for pattern in api_patterns:
                matches = re.findall(pattern, js_content, re.IGNORECASE)
                if matches:
                    print(f"Found API pattern '{pattern}': {matches[:5]}")  # Show first 5
    
    except Exception as e:
        print(f"Error investigating SpreadSimple: {e}")

def main():
    tool_urls = analyze_sitemap()
    investigate_spreadsimple()
    
    print(f"\n=== SUMMARY ===")
    print(f"Total tool URLs found: {len(tool_urls)}")
    print("This appears to be a SpreadSimple-powered site (Google Sheets as backend)")
    print("Data is likely loaded via JavaScript from a Google Sheets API")

if __name__ == "__main__":
    main()