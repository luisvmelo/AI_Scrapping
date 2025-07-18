#!/usr/bin/env python3
"""
Working Complete Futurepedia Scraper - ALL Tools by Popularity
Uses the proven category-based approach that actually works
"""

import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
from typing import List, Optional
from database.adapters import SQLiteAdapter
from scrapers.common import AITool, BaseScraper

class WorkingCompleteFuturepediaScraper(BaseScraper):
    """Complete Futurepedia scraper using proven category-based approach"""
    
    def __init__(self):
        super().__init__("futurepedia_complete", "https://www.futurepedia.io")
        self.db = SQLiteAdapter('database/ai_tools.db')
        
    def scrape_all_by_popularity(self) -> List[AITool]:
        """Scrape ALL tools from Futurepedia using category-based approach"""
        all_tools = []
        
        print("🚀 WORKING COMPLETE FUTUREPEDIA SCRAPER - ALL TOOLS")
        print("=" * 60)
        
        # Categories with comprehensive coverage (most popular first)
        categories = [
            ("business", "Business Tools"),
            ("productivity", "Productivity Tools"),
            ("image", "Image Tools"),
            ("code", "Code Tools"),
            ("video", "Video Tools"),
            ("art", "Art Tools"),
            ("marketing", "Marketing Tools"),
            ("design", "Design Tools"),
            ("writing", "Writing Tools"),
            ("audio", "Audio Tools"),
            ("data", "Data Tools"),
            ("finance", "Finance Tools"),
            ("education", "Education Tools"),
            ("health", "Health Tools"),
            ("research", "Research Tools"),
            ("automation", "Automation Tools"),
            ("analytics", "Analytics Tools"),
            ("social", "Social Tools"),
            ("sales", "Sales Tools"),
            ("hr", "HR Tools"),
            ("customer-service", "Customer Service Tools"),
            ("legal", "Legal Tools"),
            ("real-estate", "Real Estate Tools"),
            ("travel", "Travel Tools"),
            ("fitness", "Fitness Tools"),
            ("gaming", "Gaming Tools"),
            ("news", "News Tools"),
            ("shopping", "Shopping Tools"),
            ("sports", "Sports Tools"),
            ("weather", "Weather Tools"),
            ("lifestyle", "Lifestyle Tools"),
            ("food", "Food Tools"),
            ("entertainment", "Entertainment Tools"),
            ("pets", "Pet Tools"),
            ("parenting", "Parenting Tools"),
            ("dating", "Dating Tools"),
            ("fashion", "Fashion Tools"),
            ("beauty", "Beauty Tools"),
            ("home", "Home Tools"),
            ("garden", "Garden Tools"),
            ("automotive", "Automotive Tools"),
            ("construction", "Construction Tools"),
            ("agriculture", "Agriculture Tools"),
            ("manufacturing", "Manufacturing Tools"),
            ("logistics", "Logistics Tools"),
            ("energy", "Energy Tools"),
            ("environment", "Environment Tools"),
            ("science", "Science Tools"),
            ("medicine", "Medicine Tools"),
            ("psychology", "Psychology Tools"),
            ("sociology", "Sociology Tools"),
            ("philosophy", "Philosophy Tools"),
            ("religion", "Religion Tools"),
            ("history", "History Tools"),
            ("geography", "Geography Tools"),
            ("language", "Language Tools"),
            ("translation", "Translation Tools"),
            ("communication", "Communication Tools"),
            ("networking", "Networking Tools"),
            ("security", "Security Tools"),
            ("privacy", "Privacy Tools"),
            ("blockchain", "Blockchain Tools"),
            ("cryptocurrency", "Cryptocurrency Tools"),
            ("ai", "AI Tools"),
            ("machine-learning", "Machine Learning Tools"),
            ("deep-learning", "Deep Learning Tools"),
            ("nlp", "NLP Tools"),
            ("computer-vision", "Computer Vision Tools"),
            ("robotics", "Robotics Tools"),
            ("iot", "IoT Tools"),
            ("cloud", "Cloud Tools"),
            ("devops", "DevOps Tools"),
            ("database", "Database Tools"),
            ("testing", "Testing Tools"),
            ("monitoring", "Monitoring Tools"),
            ("deployment", "Deployment Tools"),
            ("version-control", "Version Control Tools"),
            ("collaboration", "Collaboration Tools"),
            ("project-management", "Project Management Tools"),
            ("time-tracking", "Time Tracking Tools"),
            ("invoicing", "Invoicing Tools"),
            ("accounting", "Accounting Tools"),
            ("crm", "CRM Tools"),
            ("erp", "ERP Tools"),
            ("hr-management", "HR Management Tools"),
            ("recruitment", "Recruitment Tools"),
            ("training", "Training Tools"),
            ("e-learning", "E-Learning Tools"),
            ("lms", "LMS Tools"),
            ("survey", "Survey Tools"),
            ("form", "Form Tools"),
            ("email", "Email Tools"),
            ("sms", "SMS Tools"),
            ("chat", "Chat Tools"),
            ("video-conferencing", "Video Conferencing Tools"),
            ("webinar", "Webinar Tools"),
            ("podcast", "Podcast Tools"),
            ("streaming", "Streaming Tools"),
            ("social-media", "Social Media Tools"),
            ("content-creation", "Content Creation Tools"),
            ("seo", "SEO Tools"),
            ("sem", "SEM Tools"),
            ("ppc", "PPC Tools"),
            ("affiliate", "Affiliate Tools"),
            ("influencer", "Influencer Tools"),
            ("pr", "PR Tools"),
            ("brand", "Brand Tools"),
            ("logo", "Logo Tools"),
            ("presentation", "Presentation Tools"),
            ("infographic", "Infographic Tools"),
            ("diagram", "Diagram Tools"),
            ("chart", "Chart Tools"),
            ("spreadsheet", "Spreadsheet Tools"),
            ("document", "Document Tools"),
            ("pdf", "PDF Tools"),
            ("note-taking", "Note Taking Tools"),
            ("mind-mapping", "Mind Mapping Tools"),
            ("calendar", "Calendar Tools"),
            ("scheduling", "Scheduling Tools"),
            ("reminder", "Reminder Tools"),
            ("habit", "Habit Tools"),
            ("goal", "Goal Tools"),
            ("budget", "Budget Tools"),
            ("expense", "Expense Tools"),
            ("investment", "Investment Tools"),
            ("trading", "Trading Tools"),
            ("insurance", "Insurance Tools"),
            ("loan", "Loan Tools"),
            ("mortgage", "Mortgage Tools"),
            ("tax", "Tax Tools"),
            ("payroll", "Payroll Tools")
        ]
        
        global_seen_tools = set()
        
        for category, category_name in categories:
            print(f"\n🔍 Scraping category: {category_name}")
            
            try:
                # Scrape ALL pages from this category
                page = 1
                category_tools = []
                
                while True:
                    if page == 1:
                        category_url = f"{self.base_url}/ai-tools/{category}"
                    else:
                        category_url = f"{self.base_url}/ai-tools/{category}?page={page}"
                    
                    response = self.get_page(category_url)
                    if not response:
                        break
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_tools = self._extract_tools_from_page(soup, f"{category}_p{page}")
                    
                    if not page_tools:
                        print(f"   ⚠️ No tools found on page {page} - End of category")
                        break
                    
                    # Filter out already seen tools
                    new_tools = []
                    for tool in page_tools:
                        if tool.ext_id not in global_seen_tools:
                            global_seen_tools.add(tool.ext_id)
                            new_tools.append(tool)
                    
                    category_tools.extend(new_tools)
                    print(f"   📄 Page {page}: {len(new_tools)} new tools")
                    
                    page += 1
                    if page > 100:  # Safety limit per category
                        break
                    
                    time.sleep(2)
                
                all_tools.extend(category_tools)
                print(f"✅ Category {category}: {len(category_tools)} total tools")
                
            except Exception as e:
                print(f"❌ Error in category {category}: {e}")
                continue
        
        print(f"\n🎯 TOTAL COLLECTED: {len(all_tools)} tools")
        return all_tools
    
    def _extract_tools_from_page(self, soup: BeautifulSoup, page_id: str) -> List[AITool]:
        """Extract all tools from a page using proven selector"""
        tools = []
        
        # Use the proven selector that works
        tool_links = soup.select('a[href*="/tool/"]')
        
        print(f"   📊 Found {len(tool_links)} tool links")
        
        # Extract data from each tool
        for i, link in enumerate(tool_links):
            try:
                tool = self._extract_tool_data(link, i, page_id)
                if tool:
                    tools.append(tool)
            except Exception as e:
                print(f"   ❌ Error extracting tool {i}: {e}")
                continue
        
        return tools
    
    def _extract_tool_data(self, link_element, index: int, page_id: str) -> Optional[AITool]:
        """Extract tool data using proven methods from working scraper"""
        
        # URL
        href = link_element.get('href', '')
        if not href or '/tool/' not in href:
            return None
        
        tool_url = href if href.startswith('http') else self.base_url + href
        
        # Get parent container
        parent = link_element.parent
        
        # Extract NAME
        name = ""
        
        # Try parent headings first
        if parent:
            name_elem = (
                parent.select_one('h1, h2, h3, h4, h5, h6') or
                parent.select_one('[class*="title"]') or
                parent.select_one('[class*="name"]')
            )
            if name_elem:
                name = name_elem.get_text().strip()
        
        # Try image alt text
        if not name:
            img_elem = link_element.select_one('img')
            if img_elem and img_elem.get('alt'):
                name = img_elem.get('alt').replace(' logo', '').strip()
        
        # Clean name
        if name:
            name = re.sub(r'\\s+', ' ', name.strip())[:100]
        
        if not name or len(name) < 2:
            name = f"Futurepedia Tool {index}"
        
        # Extract DESCRIPTION
        description = ""
        if parent:
            desc_elem = (
                parent.select_one('p') or
                parent.select_one('[class*="desc"]') or
                parent.select_one('[class*="summary"]')
            )
            if desc_elem:
                description = desc_elem.get_text().strip()
        
        # Clean description
        if description:
            description = re.sub(r'\\s+', ' ', description.strip())[:500]
        
        # Extract PRICE
        price_text = (parent.get_text() if parent else link_element.get_text()).lower()
        price = self._extract_price(price_text)
        
        # Calculate POPULARITY (based on position and page)
        popularity = self._calculate_popularity(index, page_id)
        
        # Extract CATEGORIES
        categories = self._extract_categories(parent or link_element, name, description)
        
        # Generate EXT_ID
        tool_slug = href.split('/tool/')[-1].split('?')[0]
        ext_id = f"fp_{tool_slug}"
        
        # Extract additional fields
        logo_url = self._extract_logo_url(parent or link_element)
        rank = index + 1
        
        return AITool(
            ext_id=ext_id,
            name=name,
            description=description,
            price=price,
            popularity=float(popularity),
            categories=categories,
            source=self.source_name,
            macro_domain=self.classify_domain(categories, description),
            url=tool_url,
            logo_url=logo_url,
            rank=rank,
            last_scraped=datetime.now()
        )
    
    def _extract_price(self, price_text: str) -> str:
        """Extract price from text"""
        # Price patterns
        price_patterns = [
            r'\\$(\\d+(?:,\\d+)?(?:\\.\\d{2})?)\\s*(?:/|\\s+per\\s+)?(?:month|mo|monthly)',
            r'\\$(\\d+(?:,\\d+)?(?:\\.\\d{2})?)\\s*(?:/|\\s+per\\s+)?(?:year|yr|yearly)',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, price_text)
            if match:
                amount = match.group(1).replace(',', '')
                if 'month' in pattern:
                    return f"${amount}/month"
                elif 'year' in pattern:
                    return f"${amount}/year"
        
        # Category-based pricing
        if 'free trial' in price_text:
            return "Free Trial"
        elif 'freemium' in price_text:
            return "Freemium"
        elif 'free' in price_text:
            return "Free"
        elif 'paid' in price_text or 'premium' in price_text:
            return "Paid"
        
        return "Unknown"
    
    def _calculate_popularity(self, index: int, page_id: str) -> float:
        """Calculate popularity based on position"""
        popularity = 50.0  # Base score
        
        # Position-based (earlier = more popular)
        position_bonus = max(0, 50 - index)
        popularity += position_bonus
        
        # Page-based
        page_match = re.search(r'_p(\\d+)', page_id)
        if page_match:
            page_num = int(page_match.group(1))
            page_penalty = min(30, page_num - 1)  # Later pages are less popular
            popularity -= page_penalty
        
        return max(1.0, min(100.0, popularity))
    
    def _extract_categories(self, container, name: str, description: str) -> List[str]:
        """Extract categories from container and text"""
        categories = []
        
        # Look for category tags
        for elem in container.select('[class*="category"], [class*="tag"], .badge'):
            cat_text = elem.get_text().strip()
            if cat_text and len(cat_text) < 30:
                categories.append(cat_text)
        
        # Infer from text if no categories found
        if not categories:
            text = f"{name} {description}".lower()
            if any(word in text for word in ['business', 'enterprise', 'company']):
                categories.append('business')
            elif any(word in text for word in ['productivity', 'task', 'organize']):
                categories.append('productivity')
            elif any(word in text for word in ['image', 'photo', 'picture']):
                categories.append('image')
            elif any(word in text for word in ['code', 'programming', 'developer']):
                categories.append('code')
            elif any(word in text for word in ['video', 'film', 'movie']):
                categories.append('video')
            elif any(word in text for word in ['design', 'ui', 'ux']):
                categories.append('design')
            elif any(word in text for word in ['writing', 'text', 'content']):
                categories.append('writing')
            elif any(word in text for word in ['marketing', 'seo', 'campaign']):
                categories.append('marketing')
            else:
                categories.append('general')
        
        return categories
    
    def _extract_logo_url(self, container) -> Optional[str]:
        """Extract logo URL from container"""
        img = container.find('img')
        if img and img.get('src'):
            src = img.get('src')
            return src if src.startswith('http') else self.base_url + src
        return None

def main():
    """Main execution function"""
    print("🚀 WORKING COMPLETE FUTUREPEDIA SCRAPER - ALL TOOLS")
    print("Starting comprehensive scraping of ALL Futurepedia tools...")
    print("=" * 60)
    
    scraper = WorkingCompleteFuturepediaScraper()
    
    # Get current database status
    stats = scraper.db.get_statistics()
    start_count = stats.get('total_tools', 0)
    print(f"📊 Starting database count: {start_count} tools")
    
    start_time = time.time()
    
    try:
        # Scrape all tools
        all_tools = scraper.scrape_all_by_popularity()
        
        print(f"\n💾 SAVING TO DATABASE...")
        print("=" * 40)
        
        # Save to database
        added_count = 0
        for i, tool in enumerate(all_tools):
            try:
                result = scraper.db.upsert_ai_tool(tool)
                if result:
                    added_count += 1
                    
                if (i + 1) % 100 == 0:
                    print(f"💾 Progress: {i + 1}/{len(all_tools)} tools processed...")
                    
            except Exception as e:
                print(f"❌ Error saving tool {tool.name}: {e}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Final stats
        final_stats = scraper.db.get_statistics()
        final_count = final_stats.get('total_tools', 0)
        
        print("\n" + "=" * 60)
        print("🎉 WORKING COMPLETE FUTUREPEDIA SCRAPING FINISHED!")
        print("=" * 60)
        print(f"⏱️  Duration: {duration/60:.1f} minutes")
        print(f"📊 Tools found: {len(all_tools)}")
        print(f"💾 Tools added: {added_count}")
        print(f"📈 Database before: {start_count}")
        print(f"📈 Database after: {final_count}")
        print(f"📈 Growth: +{final_count - start_count} tools")
        print(f"🎯 Success rate: {(added_count/len(all_tools)*100):.1f}%")
        
    except Exception as e:
        print(f"💥 Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()