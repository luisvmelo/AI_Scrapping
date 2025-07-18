#!/usr/bin/env python3
"""
Complete Futurepedia Scraper - All Tools by Popularity
Scrapes ALL ~2400 AI tools from Futurepedia ordered by popularity
Maximizes data extraction for all database columns
"""

import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import hashlib
from typing import List, Optional
from database.adapters import SQLiteAdapter
from scrapers.common import AITool, BaseScraper

class CompleteFuturepediaScraper(BaseScraper):
    """Complete Futurepedia scraper targeting ALL tools by popularity"""
    
    def __init__(self):
        super().__init__("futurepedia_complete", "https://www.futurepedia.io")
        self.db = SQLiteAdapter('database/ai_tools.db')
        
    def scrape_all_by_popularity(self) -> List[AITool]:
        """Scrape ALL tools from Futurepedia ordered by popularity"""
        all_tools = []
        
        print("🚀 COMPLETE FUTUREPEDIA SCRAPER - ALL TOOLS BY POPULARITY")
        print("=" * 60)
        
        # Strategy: Focus on category pages (what actually works)
        priority_strategies = [
            self._scrape_all_categories_comprehensive,
            self._scrape_popular_pages,
            self._scrape_trending_pages,
            self._scrape_featured_pages
        ]
        
        seen_tools = set()
        
        for strategy_num, strategy in enumerate(priority_strategies, 1):
            print(f"\n📊 STRATEGY {strategy_num}: {strategy.__name__}")
            print("-" * 40)
            
            try:
                strategy_tools = strategy()
                
                # Deduplicate
                new_tools = []
                for tool in strategy_tools:
                    if tool.ext_id not in seen_tools:
                        seen_tools.add(tool.ext_id)
                        new_tools.append(tool)
                
                all_tools.extend(new_tools)
                print(f"✅ Strategy {strategy_num}: {len(new_tools)} new tools (total: {len(all_tools)})")
                
            except Exception as e:
                print(f"❌ Strategy {strategy_num} failed: {e}")
                continue
        
        print(f"\n🎯 TOTAL COLLECTED: {len(all_tools)} tools")
        return all_tools
    
    def _scrape_popular_pages(self) -> List[AITool]:
        """Scrape from popularity-sorted pages"""
        tools = []
        
        # Popular/trending URLs (most important first)
        popular_urls = [
            f"{self.base_url}/ai-tools?sort=popular",
            f"{self.base_url}/ai-tools?sort=trending", 
            f"{self.base_url}/ai-tools?sort=featured",
            f"{self.base_url}/ai-tools?sort=top",
            f"{self.base_url}/popular",
            f"{self.base_url}/trending"
        ]
        
        for url in popular_urls:
            print(f"🔍 Scraping popularity page: {url}")
            
            try:
                # Scrape ALL pages from this URL
                page = 1
                while True:
                    page_url = f"{url}&page={page}" if '?' in url else f"{url}?page={page}"
                    
                    response = self.get_page(page_url)
                    if not response:
                        break
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_tools = self._extract_tools_from_page(soup, f"popular_p{page}")
                    
                    if not page_tools:
                        break
                    
                    tools.extend(page_tools)
                    print(f"   📄 Page {page}: {len(page_tools)} tools")
                    
                    page += 1
                    if page > 50:  # Safety limit
                        break
                    
                    time.sleep(2)  # Respectful delay
                    
            except Exception as e:
                print(f"❌ Error on {url}: {e}")
                continue
        
        return tools
    
    def _scrape_trending_pages(self) -> List[AITool]:
        """Scrape trending/new tools"""
        tools = []
        
        trending_urls = [
            f"{self.base_url}/ai-tools?sort=newest",
            f"{self.base_url}/ai-tools?sort=recent",
            f"{self.base_url}/new"
        ]
        
        for url in trending_urls:
            print(f"🔍 Scraping trending page: {url}")
            
            try:
                page = 1
                while page <= 20:  # Limit trending to 20 pages
                    page_url = f"{url}&page={page}" if '?' in url else f"{url}?page={page}"
                    
                    response = self.get_page(page_url)
                    if not response:
                        break
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_tools = self._extract_tools_from_page(soup, f"trending_p{page}")
                    
                    if not page_tools:
                        break
                    
                    tools.extend(page_tools)
                    print(f"   📄 Page {page}: {len(page_tools)} tools")
                    
                    page += 1
                    time.sleep(2)
                    
            except Exception as e:
                print(f"❌ Error on {url}: {e}")
                continue
        
        return tools
    
    def _scrape_featured_pages(self) -> List[AITool]:
        """Scrape featured/editor's choice tools"""
        tools = []
        
        featured_urls = [
            f"{self.base_url}/ai-tools?sort=featured",
            f"{self.base_url}/featured",
            f"{self.base_url}/ai-tools?sort=editor"
        ]
        
        for url in featured_urls:
            print(f"🔍 Scraping featured page: {url}")
            
            try:
                page = 1
                while page <= 10:  # Featured typically has fewer pages
                    page_url = f"{url}&page={page}" if '?' in url else f"{url}?page={page}"
                    
                    response = self.get_page(page_url)
                    if not response:
                        break
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_tools = self._extract_tools_from_page(soup, f"featured_p{page}")
                    
                    if not page_tools:
                        break
                    
                    tools.extend(page_tools)
                    print(f"   📄 Page {page}: {len(page_tools)} tools")
                    
                    page += 1
                    time.sleep(2)
                    
            except Exception as e:
                print(f"❌ Error on {url}: {e}")
                continue
        
        return tools
    
    def _scrape_all_categories_comprehensive(self) -> List[AITool]:
        """Comprehensive scraping of all categories"""
        tools = []
        
        # All categories with comprehensive coverage
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
            ("hr", "HR Tools")
        ]
        
        for category, category_name in categories:
            print(f"🔍 Scraping category: {category_name}")
            
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
                        break
                    
                    category_tools.extend(page_tools)
                    print(f"   📄 Page {page}: {len(page_tools)} tools")
                    
                    page += 1
                    if page > 100:  # Safety limit per category
                        break
                    
                    time.sleep(2)
                
                tools.extend(category_tools)
                print(f"✅ Category {category}: {len(category_tools)} total tools")
                
            except Exception as e:
                print(f"❌ Error in category {category}: {e}")
                continue
        
        return tools
    
    def _extract_tools_from_page(self, soup: BeautifulSoup, page_id: str) -> List[AITool]:
        """Extract all tools from a page with maximum data"""
        tools = []
        
        # Multiple selectors for maximum coverage
        selectors = [
            'a[href*="/tool/"]',  # Primary: tool links
            '.tool-card a',       # Tool cards
            '.ai-tool a',         # AI tool elements
            '[data-testid*="tool"] a',  # Test ID based
            '.directory-item a',  # Directory items
        ]
        
        found_links = []
        for selector in selectors:
            links = soup.select(selector)
            found_links.extend(links)
        
        # Deduplicate links
        seen_hrefs = set()
        unique_links = []
        for link in found_links:
            href = link.get('href', '')
            if href and '/tool/' in href and href not in seen_hrefs:
                seen_hrefs.add(href)
                unique_links.append(link)
        
        print(f"   📊 Found {len(unique_links)} unique tool links")
        
        # Extract maximum data from each tool
        for i, link in enumerate(unique_links):
            try:
                tool = self._extract_comprehensive_tool_data(link, i, page_id)
                if tool:
                    tools.append(tool)
            except Exception as e:
                print(f"   ❌ Error extracting tool {i}: {e}")
                continue
        
        return tools
    
    def _extract_comprehensive_tool_data(self, link_element, index: int, page_id: str) -> Optional[AITool]:
        """Extract comprehensive data for a single tool"""
        
        # URL
        href = link_element.get('href', '')
        if not href or '/tool/' not in href:
            return None
        
        tool_url = href if href.startswith('http') else self.base_url + href
        
        # Get parent containers for more data
        parent = link_element.parent
        card_container = parent
        
        # Look for larger container
        current = parent
        for _ in range(3):  # Go up 3 levels max
            if current and current.parent:
                current = current.parent
                if len(current.get_text()) > len(card_container.get_text()):
                    card_container = current
        
        # Extract NAME with multiple strategies
        name = self._extract_name(link_element, card_container)
        
        # Extract DESCRIPTION comprehensively
        description = self._extract_description(link_element, card_container)
        
        # Extract PRICE with advanced patterns
        price = self._extract_price(card_container)
        
        # Extract POPULARITY with multiple signals
        popularity = self._calculate_popularity(card_container, index, page_id)
        
        # Extract CATEGORIES comprehensively
        categories = self._extract_categories(card_container, name, description)
        
        # Extract LOGO URL
        logo_url = self._extract_logo_url(card_container, tool_url)
        
        # Extract UPVOTES/RATING
        upvotes = self._extract_upvotes(card_container)
        
        # Extract MONTHLY USERS
        monthly_users = self._extract_monthly_users(card_container)
        
        # Extract EDITOR SCORE
        editor_score = self._extract_editor_score(card_container, popularity)
        
        # Extract MATURITY
        maturity = self._extract_maturity(card_container)
        
        # Extract PLATFORM
        platform = self._extract_platform(card_container, description)
        
        # Extract FEATURES
        features = self._extract_features(card_container, description)
        
        # Calculate RANK (position-based)
        rank = index + 1
        
        # Generate EXT_ID
        tool_slug = href.split('/tool/')[-1].split('?')[0]
        ext_id = f"fp_{tool_slug}"
        
        # Classify MACRO_DOMAIN
        macro_domain = self.classify_domain(categories, description)
        
        return AITool(
            ext_id=ext_id,
            name=name,
            description=description,
            price=price,
            popularity=float(popularity),
            categories=categories,
            source=self.source_name,
            macro_domain=macro_domain,
            url=tool_url,
            logo_url=logo_url,
            rank=rank,
            upvotes=upvotes,
            monthly_users=monthly_users,
            editor_score=editor_score,
            maturity=maturity,
            platform=platform,
            features=features,
            last_scraped=datetime.now()
        )
    
    def _extract_name(self, link_element, container) -> str:
        """Extract tool name with multiple strategies"""
        name = ""
        
        # Strategy 1: Link text
        if link_element.get_text().strip():
            name = link_element.get_text().strip()
        
        # Strategy 2: Image alt text
        if not name:
            img = link_element.find('img')
            if img and img.get('alt'):
                name = img.get('alt').replace(' logo', '').strip()
        
        # Strategy 3: Headings in container
        if not name:
            for heading in container.select('h1, h2, h3, h4, h5, h6'):
                if heading.get_text().strip():
                    name = heading.get_text().strip()
                    break
        
        # Strategy 4: Title attributes
        if not name:
            title = link_element.get('title') or container.get('title')
            if title:
                name = title.strip()
        
        # Clean name
        if name:
            name = re.sub(r'\s+', ' ', name.strip())[:100]
        
        return name or f"Futurepedia Tool"
    
    def _extract_description(self, link_element, container) -> str:
        """Extract comprehensive description"""
        description = ""
        
        # Strategy 1: Paragraphs in container
        for p in container.select('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:
                description = text
                break
        
        # Strategy 2: Div with description-like classes
        if not description:
            for div in container.select('[class*="desc"], [class*="summary"], [class*="content"]'):
                text = div.get_text().strip()
                if text and len(text) > 20:
                    description = text
                    break
        
        # Strategy 3: Any substantial text
        if not description:
            text = container.get_text().strip()
            sentences = text.split('.')
            for sentence in sentences:
                if len(sentence.strip()) > 30:
                    description = sentence.strip()
                    break
        
        # Clean description
        if description:
            description = re.sub(r'\s+', ' ', description.strip())[:500]
        
        return description
    
    def _extract_price(self, container) -> str:
        """Extract price with comprehensive patterns"""
        text = container.get_text().lower()
        
        # Price patterns (most specific first)
        price_patterns = [
            (r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:month|mo|monthly)', lambda m: f"${m.group(1)}/month"),
            (r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:year|yr|yearly|annually)', lambda m: f"${m.group(1)}/year"),
            (r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:week|weekly)', lambda m: f"${m.group(1)}/week"),
            (r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+one.?time|once)', lambda m: f"${m.group(1)} one-time"),
            (r'(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:usd|dollars?)\s*(?:/|\s+per\s+)?(?:month|mo)', lambda m: f"${m.group(1)}/month"),
        ]
        
        for pattern, formatter in price_patterns:
            match = re.search(pattern, text)
            if match:
                return formatter(match)
        
        # Category-based pricing
        if 'free trial' in text:
            return "Free Trial"
        elif 'freemium' in text:
            return "Freemium"
        elif 'free' in text and 'trial' not in text:
            return "Free"
        elif any(word in text for word in ['paid', 'premium', 'subscription', 'plans']):
            return "Paid"
        elif '$' in text:
            dollar_match = re.search(r'\$(\d+(?:,\d+)?(?:\.\d{2})?)', text)
            if dollar_match:
                return f"${dollar_match.group(1)}"
        
        return "Unknown"
    
    def _calculate_popularity(self, container, index: int, page_id: str) -> float:
        """Calculate popularity from multiple signals"""
        popularity = 50.0  # Base score
        
        # Position-based popularity (earlier = more popular)
        position_bonus = max(0, 50 - index)
        popularity += position_bonus
        
        # Page-based popularity
        if 'popular' in page_id:
            popularity += 30
        elif 'trending' in page_id:
            popularity += 20
        elif 'featured' in page_id:
            popularity += 25
        
        # Rating-based popularity
        text = container.get_text().lower()
        rating_match = re.search(r'rated?\s+(\d+(?:\.\d+)?)\s*(?:out\s*of\s*)?(?:5|10)', text)
        if rating_match:
            rating = float(rating_match.group(1))
            if rating <= 5:
                popularity += (rating / 5) * 30
            elif rating <= 10:
                popularity += (rating / 10) * 30
        
        return min(100.0, popularity)
    
    def _extract_categories(self, container, name: str, description: str) -> List[str]:
        """Extract categories from multiple sources"""
        categories = []
        
        # Strategy 1: Hash tags
        text = container.get_text()
        hashtags = re.findall(r'#(\w+)', text)
        categories.extend(hashtags)
        
        # Strategy 2: Category elements
        for elem in container.select('[class*="category"], [class*="tag"], .badge'):
            cat_text = elem.get_text().strip()
            if cat_text and len(cat_text) < 30:
                categories.append(cat_text)
        
        # Strategy 3: Infer from text
        full_text = f"{name} {description}".lower()
        category_keywords = {
            "business": ["business", "enterprise", "corporate", "company"],
            "productivity": ["productivity", "organize", "task", "workflow", "efficiency"],
            "image": ["image", "photo", "picture", "visual", "graphic", "art"],
            "video": ["video", "film", "movie", "animation", "clip"],
            "code": ["code", "programming", "developer", "api", "coding"],
            "writing": ["writing", "text", "content", "copywriting", "blog"],
            "marketing": ["marketing", "seo", "social", "campaign", "advertising"],
            "design": ["design", "ui", "ux", "creative", "prototype"],
            "audio": ["audio", "music", "sound", "voice", "podcast"],
            "data": ["data", "analytics", "analysis", "insight", "report"],
            "automation": ["automation", "automate", "workflow", "bot"],
            "research": ["research", "study", "analysis", "insight"]
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in full_text for keyword in keywords):
                categories.append(category)
        
        # Clean and deduplicate
        categories = list(set([cat.strip().lower() for cat in categories if cat.strip()]))
        
        return categories or ["general"]
    
    def _extract_logo_url(self, container, tool_url: str) -> Optional[str]:
        """Extract logo URL"""
        # Look for images
        for img in container.select('img'):
            src = img.get('src')
            if src and ('logo' in src.lower() or 'icon' in src.lower()):
                return src if src.startswith('http') else self.base_url + src
        
        # Any image as fallback
        img = container.find('img')
        if img and img.get('src'):
            src = img.get('src')
            return src if src.startswith('http') else self.base_url + src
        
        return None
    
    def _extract_upvotes(self, container) -> Optional[int]:
        """Extract upvotes/likes"""
        text = container.get_text()
        patterns = [
            r'(\d+)\s*(?:upvotes?|likes?|votes?|👍)',
            r'(\d+)\s*people\s+like',
            r'(\d+)\s*hearts?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_monthly_users(self, container) -> Optional[int]:
        """Extract monthly users"""
        text = container.get_text()
        patterns = [
            r'(\d+(?:,\d+)*)\s*(?:monthly\s+)?users?',
            r'(\d+(?:,\d+)*)\s*people\s+use',
            r'used\s+by\s+(\d+(?:,\d+)*)',
            r'(\d+)k\s*users?',
            r'(\d+)m\s*users?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '')
                if 'k' in pattern:
                    return int(value) * 1000
                elif 'm' in pattern:
                    return int(value) * 1000000
                else:
                    return int(value)
        
        return None
    
    def _extract_editor_score(self, container, popularity: float) -> Optional[float]:
        """Extract or calculate editor score"""
        text = container.get_text()
        
        # Look for explicit scores
        score_match = re.search(r'score:?\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if score_match:
            return float(score_match.group(1))
        
        # Convert from popularity
        if popularity > 0:
            return round(popularity / 10, 1)
        
        return None
    
    def _extract_maturity(self, container) -> Optional[str]:
        """Extract maturity/development stage"""
        text = container.get_text().lower()
        
        if 'beta' in text:
            return 'beta'
        elif 'alpha' in text:
            return 'alpha'
        elif any(term in text for term in ['stable', 'production', 'ga', 'v1.0', 'released']):
            return 'stable'
        elif 'new' in text or 'launch' in text:
            return 'beta'
        
        return None
    
    def _extract_platform(self, container, description: str) -> List[str]:
        """Extract supported platforms"""
        text = f"{container.get_text()} {description}".lower()
        platforms = []
        
        platform_keywords = {
            "web": ["web", "browser", "online", "webapp"],
            "mobile": ["mobile", "app", "ios", "android"],
            "desktop": ["desktop", "windows", "mac", "linux"],
            "api": ["api", "integration", "webhook"],
            "chrome": ["chrome", "extension", "plugin"],
            "slack": ["slack", "bot"],
            "discord": ["discord", "bot"]
        }
        
        for platform, keywords in platform_keywords.items():
            if any(keyword in text for keyword in keywords):
                platforms.append(platform)
        
        return platforms or ["web"]
    
    def _extract_features(self, container, description: str) -> dict:
        """Extract features and capabilities"""
        text = f"{container.get_text()} {description}".lower()
        features = {}
        
        # Feature detection
        if 'free' in text:
            features['free_tier'] = True
        if 'trial' in text:
            features['free_trial'] = True
        if 'api' in text:
            features['api_available'] = True
        if any(term in text for term in ['real-time', 'realtime', 'instant']):
            features['real_time'] = True
        if any(term in text for term in ['ai', 'machine learning', 'ml']):
            features['ai_powered'] = True
        if any(term in text for term in ['team', 'collaboration', 'share']):
            features['collaboration'] = True
        if any(term in text for term in ['cloud', 'saas']):
            features['cloud_based'] = True
        
        return features

def main():
    """Main execution function"""
    print("🚀 COMPLETE FUTUREPEDIA SCRAPER - ALL TOOLS")
    print("Starting comprehensive scraping of ALL Futurepedia tools...")
    print("=" * 60)
    
    scraper = CompleteFuturepediaScraper()
    
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
        print("🎉 COMPLETE FUTUREPEDIA SCRAPING FINISHED!")
        print("=" * 60)
        print(f"⏱️  Duration: {duration/60:.1f} minutes")
        print(f"📊 Tools found: {len(all_tools)}")
        print(f"💾 Tools added: {added_count}")
        print(f"📈 Database before: {start_count}")
        print(f"📈 Database after: {final_count}")
        print(f"📈 Growth: +{final_count - start_count} tools")
        print(f"🎯 Success rate: {(added_count/len(all_tools)*100):.1f}%")
        
        # Show categories
        print(f"\n📊 FINAL DATABASE STATS:")
        print(f"🏷️  Categories: {len(final_stats.get('by_domain', {}))}")
        print(f"🔗 Sources: {len(final_stats.get('by_source', {}))}")
        
    except Exception as e:
        print(f"💥 Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()