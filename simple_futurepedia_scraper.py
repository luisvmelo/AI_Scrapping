#!/usr/bin/env python3
"""
Simple Futurepedia Scraper - Direct and Efficient
Focuses only on the working Futurepedia scraper
"""

import time
from datetime import datetime
from scrapers.futurepedia import FuturepediaScraper
from database.adapters import SQLiteAdapter

def main():
    print("🚀 Simple Futurepedia Scraper")
    print("=" * 50)
    
    # Initialize
    scraper = FuturepediaScraper()
    db = SQLiteAdapter('database/ai_tools.db')
    
    # Get current count
    stats = db.get_statistics()
    current_count = stats.get('total_tools', 0)
    print(f"Current database: {current_count} tools")
    
    # Target
    target = 1000
    remaining = target - current_count
    print(f"Target: {target} tools")
    print(f"Need: {remaining} more tools")
    print("=" * 50)
    
    # Scrape in batches
    batch_size = 50
    total_added = 0
    
    while current_count < target:
        remaining = target - current_count
        batch_target = min(batch_size, remaining)
        
        print(f"\n🔍 Scraping batch of {batch_target} tools...")
        start_time = time.time()
        
        try:
            # Scrape tools
            tools = scraper.scrape(max_tools=batch_target)
            print(f"Found {len(tools)} tools")
            
            # Add to database
            added_this_batch = 0
            for tool in tools:
                tool.source = 'futurepedia_direct'
                tool.last_scraped = datetime.now()
                
                result = db.upsert_ai_tool(tool)
                if result:
                    added_this_batch += 1
                    if added_this_batch % 10 == 0:
                        print(f"  Added {added_this_batch}/{len(tools)} tools...")
            
            total_added += added_this_batch
            end_time = time.time()
            
            print(f"✅ Batch complete: {added_this_batch} tools added in {end_time - start_time:.1f}s")
            
            # Update current count
            stats = db.get_statistics()
            current_count = stats.get('total_tools', 0)
            print(f"📊 Database now has {current_count} tools")
            
            # Progress
            progress = (current_count / target) * 100
            print(f"🎯 Progress: {progress:.1f}% ({current_count}/{target})")
            
            # Break if no tools were added
            if added_this_batch == 0:
                print("⚠️ No tools added this batch, stopping...")
                break
            
            # Brief pause between batches
            if current_count < target:
                print("⏳ Pausing 10 seconds between batches...")
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Error in batch: {e}")
            time.sleep(30)  # Wait longer on error
    
    print("\n" + "=" * 50)
    print("🏁 SCRAPING COMPLETED")
    print("=" * 50)
    print(f"Total tools added: {total_added}")
    print(f"Final database count: {current_count}")
    
    if current_count >= target:
        print("🎉 TARGET REACHED!")
    else:
        print(f"📊 Progress: {current_count}/{target} ({(current_count/target)*100:.1f}%)")

if __name__ == "__main__":
    main()