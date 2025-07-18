#!/usr/bin/env python3
"""
Fast AI Tools Scraper - Maximum Efficiency
"""

import time
from datetime import datetime
from scrapers.futurepedia import FuturepediaScraper
from database.adapters import SQLiteAdapter

def main():
    print("⚡ FAST AI TOOLS SCRAPER")
    print("=" * 40)
    
    scraper = FuturepediaScraper()
    db = SQLiteAdapter('database/ai_tools.db')
    
    # Get current count
    stats = db.get_statistics()
    current_count = stats.get('total_tools', 0)
    print(f"Current: {current_count} tools")
    
    # Run continuously
    batch_number = 1
    
    while current_count < 1000:
        print(f"\n🚀 Batch {batch_number} - Target: 100 tools")
        start_time = time.time()
        
        try:
            # Scrape 100 tools
            tools = scraper.scrape(max_tools=100)
            print(f"Scraped: {len(tools)} tools")
            
            # Add to database
            added = 0
            for tool in tools:
                tool.source = f'futurepedia_fast_batch_{batch_number}'
                tool.last_scraped = datetime.now()
                
                if db.upsert_ai_tool(tool):
                    added += 1
            
            end_time = time.time()
            
            # Update count
            stats = db.get_statistics()
            current_count = stats.get('total_tools', 0)
            
            print(f"✅ Added: {added} tools in {end_time - start_time:.1f}s")
            print(f"📊 Total: {current_count} tools ({(current_count/1000)*100:.1f}%)")
            
            batch_number += 1
            
            # Quick pause
            if current_count < 1000:
                print("⏳ 5s pause...")
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(10)
    
    print(f"\n🎉 COMPLETED! {current_count} tools in database")

if __name__ == "__main__":
    main()