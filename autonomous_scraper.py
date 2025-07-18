#!/usr/bin/env python3
"""
Autonomous AI Tools Scraper
Runs all scrapers automatically to build up to 1000+ AI tools database.
NO CREDIT CONSUMPTION - Runs independently on your machine.
"""

import time
import logging
import random
from datetime import datetime
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all available scrapers
from scrapers.futurepedia import FuturepediaScraper
from scrapers.theresanaiforthat import TheresAnAIForThatScraperAdvanced
from scrapers.aitools_directory import AIToolsDirectoryScraperJS
from scrapers.toolify import ToolifyScraper
# from scrapers.topai_tools import TopAIToolsScraper  # Removed due to blocking/errors
from scrapers.phygital_library import PhygitalLibraryScraper
from database.adapters import SQLiteAdapter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutonomousScraper:
    def __init__(self, target_count=1000):
        self.target_count = target_count
        self.db = SQLiteAdapter('database/ai_tools.db')
        
        # Initialize all scrapers (theresanaiforthat last - requires Selenium)
        # topai_tools removed due to blocking/errors
        self.scrapers = {
            'futurepedia': FuturepediaScraper(),
            'aitools_directory': AIToolsDirectoryScraperJS(),
            'toolify': ToolifyScraper(),
            'phygital_library': PhygitalLibraryScraper(),
            'theresanaiforthat': TheresAnAIForThatScraperAdvanced()
        }
        
        # Respectful delays between requests (seconds)
        self.delays = {
            'between_tools': (2, 5),    # Between individual tools
            'between_pages': (5, 10),   # Between pages on same site
            'between_sites': (30, 60),  # Between different sites
            'on_error': (60, 120)       # After encountering errors
        }
        
        self.stats = {
            'start_time': datetime.now(),
            'tools_before': 0,
            'tools_added': 0,
            'errors': 0,
            'sites_completed': 0
        }

    def get_current_count(self):
        """Get current number of tools in database"""
        try:
            stats = self.db.get_statistics()
            return stats.get('total_tools', 0)
        except Exception as e:
            logger.error(f"Error getting count: {e}")
            return 0

    def random_delay(self, delay_type):
        """Add random delay to be respectful to servers"""
        min_delay, max_delay = self.delays[delay_type]
        delay = random.uniform(min_delay, max_delay)
        logger.info(f"Waiting {delay:.1f}s ({delay_type})...")
        time.sleep(delay)

    def run_scraper(self, name, scraper, max_tools_per_site=200):
        """Run a single scraper with error handling"""
        logger.info(f"🚀 Starting scraper: {name}")
        tools_added = 0
        
        try:
            # Check if scraper has a batch method
            if hasattr(scraper, 'scrape_batch'):
                logger.info(f"Running batch scrape for {name}")
                tools = scraper.scrape_batch(limit=max_tools_per_site)
            elif hasattr(scraper, 'scrape_all'):
                logger.info(f"Running full scrape for {name}")
                tools = scraper.scrape_all()[:max_tools_per_site]
            else:
                logger.warning(f"Scraper {name} doesn't have batch method, trying manual pagination")
                tools = []
                page = 1
                while len(tools) < max_tools_per_site:
                    try:
                        if hasattr(scraper, 'scrape_page'):
                            page_tools = scraper.scrape_page(page)
                        else:
                            # Try to scrape first few tools
                            try:
                                # Try with max_tools parameter first
                                page_tools = scraper.scrape(max_tools=50)
                            except TypeError:
                                # Fallback to old method without parameter
                                page_tools = scraper.scrape()[:50]
                            break
                        
                        if not page_tools:
                            break
                            
                        tools.extend(page_tools)
                        page += 1
                        
                        self.random_delay('between_pages')
                        
                    except Exception as e:
                        logger.error(f"Error on page {page} of {name}: {e}")
                        break

            logger.info(f"Found {len(tools)} tools from {name}")
            
            # Add tools to database
            for i, tool in enumerate(tools):
                try:
                    # Add source info
                    tool.source = f"{name}_autonomous"
                    tool.last_scraped = datetime.now()
                    
                    # Insert into database
                    self.db.upsert_ai_tool(tool)
                    tools_added += 1
                    
                    if i % 10 == 0:  # Log progress every 10 tools
                        logger.info(f"Added {i+1}/{len(tools)} tools from {name}")
                    
                    # Small delay between tools
                    if i < len(tools) - 1:
                        time.sleep(random.uniform(0.5, 1.5))
                        
                except Exception as e:
                    logger.error(f"Error adding tool {tool.name}: {e}")
                    self.stats['errors'] += 1

        except Exception as e:
            logger.error(f"Error running scraper {name}: {e}")
            self.stats['errors'] += 1
            self.random_delay('on_error')
            
        self.stats['tools_added'] += tools_added
        self.stats['sites_completed'] += 1
        logger.info(f"✅ Completed {name}: {tools_added} tools added")
        
        return tools_added

    def run_full_autonomous_scraping(self):
        """Run all scrapers autonomously until target is reached"""
        logger.info("🤖 STARTING AUTONOMOUS AI TOOLS SCRAPING")
        logger.info(f"Target: {self.target_count} tools")
        
        self.stats['tools_before'] = self.get_current_count()
        logger.info(f"Current database: {self.stats['tools_before']} tools")
        
        if self.stats['tools_before'] >= self.target_count:
            logger.info("✅ Target already reached!")
            return
        
        remaining = self.target_count - self.stats['tools_before']
        tools_per_site = max(50, remaining // len(self.scrapers))
        
        logger.info(f"Need {remaining} more tools")
        logger.info(f"Will try to get ~{tools_per_site} tools per site")
        
        # Run each scraper
        for name, scraper in self.scrapers.items():
            current_count = self.get_current_count()
            
            if current_count >= self.target_count:
                logger.info(f"🎯 Target of {self.target_count} tools reached!")
                break
                
            logger.info(f"Current total: {current_count} tools")
            logger.info(f"Need {self.target_count - current_count} more")
            
            try:
                added = self.run_scraper(name, scraper, tools_per_site)
                logger.info(f"Site {name}: +{added} tools")
                
                # Delay between sites to be respectful
                if name != list(self.scrapers.keys())[-1]:  # Don't delay after last site
                    self.random_delay('between_sites')
                    
            except Exception as e:
                logger.error(f"Failed to run scraper {name}: {e}")
                self.random_delay('on_error')
        
        self.print_final_stats()

    def print_final_stats(self):
        """Print final scraping statistics"""
        end_time = datetime.now()
        duration = end_time - self.stats['start_time']
        final_count = self.get_current_count()
        
        logger.info("\n" + "="*60)
        logger.info("🏁 AUTONOMOUS SCRAPING COMPLETED")
        logger.info("="*60)
        logger.info(f"Duration: {duration}")
        logger.info(f"Tools before: {self.stats['tools_before']}")
        logger.info(f"Tools after: {final_count}")
        logger.info(f"New tools added: {final_count - self.stats['tools_before']}")
        logger.info(f"Sites completed: {self.stats['sites_completed']}/{len(self.scrapers)}")
        logger.info(f"Errors encountered: {self.stats['errors']}")
        logger.info(f"Target reached: {'✅ YES' if final_count >= self.target_count else '❌ NO'}")
        
        if final_count >= self.target_count:
            logger.info("🎉 SUCCESS! Ready to integrate with frontend!")
        else:
            remaining = self.target_count - final_count
            logger.info(f"📊 Progress: {final_count}/{self.target_count} ({(final_count/self.target_count)*100:.1f}%)")
            logger.info(f"💡 Suggestion: Run again later to get remaining {remaining} tools")

def main():
    """Main execution function"""
    print("🤖 AI Universe Autonomous Scraper")
    print("This will run independently without consuming AI credits!")
    print("-" * 50)
    
    # Check if user wants to customize target
    target = 1000
    if len(sys.argv) > 1:
        try:
            target = int(sys.argv[1])
        except ValueError:
            print("Invalid target number, using default 1000")
    
    print(f"Target: {target} AI tools")
    print("Press Ctrl+C to stop at any time")
    print("Logs will be saved to: autonomous_scraping.log")
    print("-" * 50)
    
    try:
        scraper = AutonomousScraper(target_count=target)
        scraper.run_full_autonomous_scraping()
        
    except KeyboardInterrupt:
        print("\n⏹️  Scraping stopped by user")
        print("Progress has been saved to database")
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Check autonomous_scraping.log for details")

if __name__ == "__main__":
    main()