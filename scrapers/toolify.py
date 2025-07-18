"""
Scraper para Toolify
URL: https://www.toolify.ai
"""

import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Dict
from datetime import datetime
from .common import BaseScraper, AITool

class ToolifyScraper(BaseScraper):
    """Scraper para toolify.ai - 26,374+ AI tools"""
    
    def __init__(self):
        super().__init__("toolify", "https://www.toolify.ai")
        
        # Headers otimizados para Toolify
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas de AI do Toolify"""
        tools = []
        
        print("🔍 Iniciando scraping do Toolify.ai (26,374+ ferramentas)...")
        
        # Estratégia 1: Página principal
        main_tools = self._scrape_main_page()
        if main_tools:
            tools.extend(main_tools)
            print(f"✅ Página principal: {len(main_tools)} ferramentas")
        
        # Estratégia 2: Ferramentas novas
        new_tools = self._scrape_new_tools()
        tools.extend(new_tools)
        print(f"✅ Ferramentas novas: {len(new_tools)} ferramentas")
        
        # Estratégia 3: Categorias principais
        category_tools = self._scrape_main_categories()
        tools.extend(category_tools)
        print(f"✅ Categorias principais: {len(category_tools)} ferramentas")
        
        # Estratégia 4: GPTs (se tempo permitir)
        if len(tools) < 200:  # Se não conseguiu muitas ferramentas
            gpt_tools = self._scrape_gpts()
            tools.extend(gpt_tools)
            print(f"✅ GPTs: {len(gpt_tools)} ferramentas")
        
        # Remove duplicatas
        tools = self._remove_duplicates(tools)
        
        print(f"🎯 Toolify.ai: Total de {len(tools)} ferramentas únicas coletadas")
        return tools
    
    def _scrape_main_page(self) -> List[AITool]:
        """Scrape da página principal priorizando populares"""
        tools = []
        
        # URLs priorizando páginas populares/famosas primeiro
        priority_urls = [
            f"{self.base_url}/popular",           # Mais populares
            f"{self.base_url}/trending",          # Tendências
            f"{self.base_url}/featured",          # Destacados
            f"{self.base_url}/top-rated",         # Mais bem avaliados
            f"{self.base_url}/best",              # Melhores
            f"{self.base_url}/most-used",         # Mais usados
            f"{self.base_url}",                   # Página principal
            f"{self.base_url}/tools",             # Ferramentas
            f"{self.base_url}/ai-tools"           # AI Tools
        ]
        
        for url in priority_urls:
            try:
                print(f"🔍 Fazendo scraping de: {url}")
                
                response = self.get_page(url)
                if not response or response.status_code != 200:
                    print(f"❌ Erro ao acessar {url}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Procura por cards de ferramentas
                tool_cards = self._find_tool_cards(soup)
                
                if tool_cards:
                    print(f"📊 Encontrados {len(tool_cards)} cards na página principal")
                    tools = self._process_tool_cards(tool_cards, "homepage")
                    break  # Exit loop on success
                
            except Exception as e:
                print(f"❌ Erro no scraping da página principal: {e}")
        
        return tools
    
    def _scrape_new_tools(self) -> List[AITool]:
        """Scrape da página de ferramentas novas"""
        tools = []
        
        try:
            new_url = f"{self.base_url}/new"
            print(f"🔍 Fazendo scraping de ferramentas novas: {new_url}")
            
            response = self.get_page(new_url)
            if not response:
                print(f"❌ Erro ao acessar página de ferramentas novas")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procura por cards de ferramentas
            tool_cards = self._find_tool_cards(soup)
            
            if tool_cards:
                print(f"📊 Encontrados {len(tool_cards)} cards em ferramentas novas")
                tools = self._process_tool_cards(tool_cards, "new")
            
        except Exception as e:
            print(f"❌ Erro no scraping de ferramentas novas: {e}")
        
        return tools
    
    def _scrape_main_categories(self) -> List[AITool]:
        """Scrape das principais categorias"""
        tools = []
        
        # Principais categorias para focar (baseado na investigação)
        categories = [
            ("writing", "Writing & Editing"),
            ("image", "Image Generation"),
            ("music", "Music & Audio"), 
            ("voice", "Voice Generation"),
            ("social", "Social Media"),
            ("coding", "Coding & Development"),
            ("video", "Video & Animation"),
            ("business", "Business Management"),
            ("marketing", "Marketing & Advertising"),
            ("health", "Health & Wellness"),
            ("education", "Education & Translation"),
            ("research", "Research & Data Analysis")
        ]
        
        for category_slug, category_name in categories:
            try:
                # Tenta diferentes formatos de URL de categoria
                urls_to_try = [
                    f"{self.base_url}/category/{category_slug}",
                    f"{self.base_url}/categories/{category_slug}",
                    f"{self.base_url}/c/{category_slug}"
                ]
                
                category_tools = []
                for category_url in urls_to_try:
                    print(f"🔍 Tentando categoria {category_name}: {category_url}")
                    
                    response = self.get_page(category_url)
                    if response and response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        tool_cards = self._find_tool_cards(soup)
                        
                        if tool_cards:
                            category_tools = self._process_tool_cards(tool_cards[:30], category_slug)  # Limita a 30 por categoria
                            print(f"✅ Categoria {category_name}: {len(category_tools)} ferramentas")
                            break
                
                tools.extend(category_tools)
                
                # Pausa entre categorias
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"❌ Erro na categoria {category_name}: {e}")
                continue
        
        return tools
    
    def _scrape_gpts(self) -> List[AITool]:
        """Scrape da seção de GPTs (limitado por ter 223,275+)"""
        tools = []
        
        try:
            gpts_url = f"{self.base_url}/gpts"
            print(f"🔍 Fazendo scraping de GPTs (amostra): {gpts_url}")
            
            response = self.get_page(gpts_url)
            if not response:
                print(f"❌ Erro ao acessar página de GPTs")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procura por cards de GPTs
            tool_cards = self._find_tool_cards(soup)
            
            if tool_cards:
                # Limita a 50 GPTs para não sobrecarregar
                sample_cards = tool_cards[:50]
                print(f"📊 Processando amostra de {len(sample_cards)} GPTs de {len(tool_cards)} encontrados")
                tools = self._process_tool_cards(sample_cards, "gpts")
            
        except Exception as e:
            print(f"❌ Erro no scraping de GPTs: {e}")
        
        return tools
    
    def _find_tool_cards(self, soup: BeautifulSoup) -> List:
        """Encontra cards de ferramentas na página"""
        tool_cards = []
        
        # Padrões possíveis para cards do Toolify
        patterns = [
            # Cards específicos
            '.tool-card',
            '.ai-tool-card', 
            '.product-card',
            '.item-card',
            
            # Containers comuns
            '[class*="tool"]',
            '[class*="product"]',
            '[class*="item"]',
            '[class*="card"]',
            
            # Elementos estruturais
            'article',
            '.list-item',
            '.grid-item',
            
            # Links de ferramentas
            'a[href*="/tool/"]',
            'a[href*="/ai/"]',
            'a[href*="/product/"]'
        ]
        
        for pattern in patterns:
            cards = soup.select(pattern)
            if cards and len(cards) > 3:  # Só considera se encontrou vários cards
                print(f"   📍 Padrão '{pattern}': {len(cards)} elementos")
                tool_cards.extend(cards)
                break  # Usa o primeiro padrão que funcionar bem
        
        # Se não encontrou cards, busca por qualquer link que pode ser ferramenta
        if not tool_cards:
            links = soup.select('a[href]')
            potential_tools = []
            for link in links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # Filtra links que podem ser ferramentas
                if (href and text and len(text) > 2 and len(text) < 100 and
                    not any(skip in href.lower() for skip in ['login', 'register', 'about', 'contact', 'privacy', 'terms', 'blog', 'help'])):
                    potential_tools.append(link)
            
            tool_cards = potential_tools[:100]  # Limita a 100
            print(f"   📍 Links potenciais: {len(tool_cards)} encontrados")
        
        return tool_cards
    
    def _process_tool_cards(self, cards: List, section: str = "") -> List[AITool]:
        """Processa cards de ferramentas"""
        tools = []
        
        for i, card in enumerate(cards):
            try:
                tool = self._parse_tool_card(card, i, section)
                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                    tools.append(tool)
            except Exception as e:
                continue
        
        return tools
    
    def _parse_tool_card(self, card_element, index: int, section: str = "") -> Optional[AITool]:
        """Extrai dados de uma ferramenta a partir de um card"""
        
        # Nome da ferramenta
        name = ""
        
        # Estratégias para extrair nome
        name_selectors = [
            'h1, h2, h3, h4, h5, h6',
            '[class*="title"]',
            '[class*="name"]',
            '[class*="tool-name"]',
            '.product-name',
            'a'
        ]
        
        for selector in name_selectors:
            name_elem = card_element.select_one(selector)
            if name_elem:
                name = name_elem.get_text().strip()
                if name and len(name) > 2:
                    break
        
        # Se é um link, pode ser que o nome esteja no texto do link
        if not name and card_element.name == 'a':
            name = card_element.get_text().strip()
        
        # Limpa o nome
        if name:
            name = re.sub(r'\s+', ' ', name.strip())[:100]
        
        if not name or len(name) < 2:
            name = f"Toolify Tool {index}"
        
        # Descrição
        description = ""
        desc_selectors = [
            'p',
            '[class*="desc"]',
            '[class*="summary"]', 
            '[class*="description"]',
            '.excerpt',
            '.content'
        ]
        
        for selector in desc_selectors:
            desc_elem = card_element.select_one(selector)
            if desc_elem:
                description = desc_elem.get_text().strip()
                if description and len(description) > 10:
                    break
        
        # Limpa a descrição
        if description:
            description = re.sub(r'\s+', ' ', description.strip())[:500]
        
        # URL da ferramenta
        href = ""
        if card_element.name == 'a':
            href = card_element.get('href', '')
        else:
            link_elem = card_element.select_one('a')
            if link_elem:
                href = link_elem.get('href', '')
        
        # Torna URL absoluta se necessário
        if href and href.startswith('/'):
            href = self.base_url + href
        
        # Categorias
        categories = []
        if section:
            categories.append(section)
        
        # Busca por tags de categoria
        tag_selectors = [
            '.tag',
            '.category',
            '.label',
            '[class*="tag"]',
            '[class*="category"]'
        ]
        
        for selector in tag_selectors:
            tags = card_element.select(selector)
            for tag in tags:
                tag_text = tag.get_text().strip()
                if tag_text and len(tag_text) < 30:
                    categories.append(tag_text)
        
        # Infere categorias do texto se não tem
        if len(categories) <= 1:
            inferred = self._infer_categories_from_text(name + " " + description)
            categories.extend(inferred)
        
        # Remove duplicatas
        categories = list(dict.fromkeys(categories))
        
        # Preço - busca por indicadores de preço
        price = "Unknown"
        price_text = card_element.get_text().lower()
        
        if 'free' in price_text and 'trial' not in price_text:
            price = "Free"
        elif 'freemium' in price_text:
            price = "Freemium"
        elif 'trial' in price_text or 'demo' in price_text:
            price = "Free Trial"
        elif '$' in price_text or 'paid' in price_text or 'premium' in price_text:
            price = "Paid"
        
        # Popularidade - tenta extrair de métricas se disponível
        popularity = 50  # valor padrão
        
        # Busca por números que podem ser visitas/saves
        numbers = re.findall(r'(\d+(?:,\d+)*)', card_element.get_text())
        if numbers:
            try:
                # Pega o maior número encontrado como métrica de popularidade
                largest_num = max([int(num.replace(',', '')) for num in numbers])
                if largest_num > 1000:
                    # Converte para escala 0-100
                    popularity = min(100, (largest_num / 1000) + 50)
            except:
                pass
        
        # Ajusta baseado na posição
        position_bonus = max(0, 20 - index)
        popularity = min(100, popularity + position_bonus)
        
        # ID único
        ext_id = self._generate_ext_id(href, name, index)
        
        # Classificação de domínio
        macro_domain = self.classify_domain(categories, description)
        
        # Extrai informações adicionais
        # Logo URL
        logo_url = self.extract_logo_url(card_element, href)
        
        # Platform info
        platform = self.extract_platform_info(card_element, description)
        
        # Features
        features = self.extract_features(card_element, description)
        
        # Rank baseado na posição na página
        rank = index + 1
        
        # Upvotes - busca por padrões de votação
        upvotes = None
        element_text = card_element.get_text()
        upvotes_patterns = [
            r'(\d+)\s*(?:votes?|upvotes?|likes?)', 
            r'(\d+)\s*👍', 
            r'(\d+)\s*⭐'
        ]
        upvotes = self.extract_numeric_value(element_text, upvotes_patterns)
        
        # Monthly users
        monthly_users = None
        users_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:monthly\s+)?users?',
            r'(\d+(?:,\d+)*)\s*people\s+use',
            r'(\d+(?:k|K|m|M))\s*users?'
        ]
        monthly_users = self.extract_numeric_value(element_text, users_patterns)
        
        # Converte K/M notation
        if monthly_users and any(suffix in element_text.lower() for suffix in ['k', 'm']):
            if 'k' in element_text.lower():
                monthly_users *= 1000
            elif 'm' in element_text.lower():
                monthly_users *= 1000000
        
        # Editor score baseado na popularidade
        editor_score = None
        if popularity > 10:
            editor_score = min(10.0, round(popularity / 10, 1))
        
        # Maturity
        maturity = None
        maturity_text = element_text.lower()
        if 'beta' in maturity_text:
            maturity = 'beta'
        elif 'alpha' in maturity_text:
            maturity = 'alpha'
        elif 'new' in maturity_text:
            maturity = 'beta'
        elif any(term in maturity_text for term in ['established', 'stable', 'mature']):
            maturity = 'stable'
        
        return AITool(
            ext_id=ext_id,
            name=name,
            description=description,
            price=price,
            popularity=float(popularity),
            categories=categories,
            source=self.source_name,
            macro_domain=macro_domain,
            # Enhanced fields
            url=href,
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
    
    def _infer_categories_from_text(self, text: str) -> List[str]:
        """Infere categorias baseado no texto"""
        text_lower = text.lower()
        categories = []
        
        keyword_map = {
            "writing": ["write", "writing", "text", "content", "copywriting", "blog", "article", "essay"],
            "chatbot": ["chat", "conversation", "bot", "assistant", "talk", "dialogue", "gpt"],
            "image": ["image", "photo", "picture", "visual", "graphic", "art", "generate", "design"],
            "video": ["video", "film", "movie", "clip", "animation", "editing", "youtube"],
            "audio": ["audio", "music", "sound", "voice", "podcast", "speech", "tts"],
            "code": ["code", "programming", "developer", "api", "coding", "development", "github"],
            "design": ["design", "ui", "ux", "creative", "prototype", "mockup", "figma"],
            "productivity": ["productivity", "organize", "task", "management", "workflow", "efficiency"],
            "marketing": ["marketing", "seo", "social", "campaign", "advertising", "promotion"],
            "business": ["business", "startup", "entrepreneur", "finance", "sales", "crm"],
            "education": ["education", "learning", "teach", "course", "training", "tutorial"],
            "research": ["research", "analysis", "data", "insight", "study", "analytics"],
            "health": ["health", "medical", "wellness", "fitness", "therapy", "mental"],
            "translation": ["translation", "translate", "language", "multilingual", "localization"]
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        if not categories:
            categories = ["ai-tool"]
        
        return categories
    
    def _generate_ext_id(self, href: str, name: str, index: int) -> str:
        """Gera um ID único para a ferramenta"""
        # Tenta usar parte da URL
        if href:
            url_parts = href.split('/')
            for part in reversed(url_parts):
                if part and len(part) > 2 and part not in ['tool', 'ai', 'product', 'gpts']:
                    clean_part = re.sub(r'[^\w\-]', '', part)[:20]
                    if clean_part:
                        return f"toolify_{clean_part}"
        
        # Usa o nome da ferramenta
        if name:
            clean_name = re.sub(r'[^\w\s]', '', name.lower())
            clean_name = re.sub(r'\s+', '_', clean_name)[:30]
            if clean_name:
                return f"toolify_{clean_name}"
        
        # Fallback para índice
        return f"toolify_tool_{index}"
    
    def _remove_duplicates(self, tools: List[AITool]) -> List[AITool]:
        """Remove ferramentas duplicadas baseado no nome"""
        seen_names = set()
        unique_tools = []
        
        for tool in tools:
            name_key = tool.name.lower().strip()
            if name_key not in seen_names:
                seen_names.add(name_key)
                unique_tools.append(tool)
        
        removed_count = len(tools) - len(unique_tools)
        if removed_count > 0:
            print(f"🧹 Removidas {removed_count} duplicatas do Toolify")
        
        return unique_tools


def scrape_toolify() -> List[AITool]:
    """Função de conveniência para fazer scraping do Toolify"""
    scraper = ToolifyScraper()
    return scraper.scrape()