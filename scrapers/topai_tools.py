"""
Scraper para TopAI.tools
URL: https://topai.tools
"""

import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from .common import BaseScraper, AITool

class TopAIToolsScraper(BaseScraper):
    """Scraper para topai.tools com anti-detecção"""
    
    def __init__(self):
        super().__init__("topai_tools", "https://topai.tools")
        
        # Headers mais sofisticados para evitar bloqueio
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        })
        
        # Configurações adicionais
        self.session.timeout = 15
        
    def get_page(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """Requisição com headers anti-detecção avançados"""
        for attempt in range(max_retries):
            try:
                # Pausa aleatória mais longa para evitar detecção
                time.sleep(random.uniform(3, 8))
                
                # Varia alguns headers para parecer mais humano
                varied_headers = self.session.headers.copy()
                varied_headers.update({
                    'User-Agent': random.choice([
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ])
                })
                
                response = self.session.get(url, headers=varied_headers, timeout=15)
                
                # Verifica se foi bloqueado
                if response.status_code == 403:
                    print(f"🚫 Bloqueado (403) na tentativa {attempt + 1} para {url}")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(10, 20))  # Pausa maior em caso de bloqueio
                        continue
                    else:
                        return None
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                print(f"Erro na tentativa {attempt + 1} para {url}: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(random.uniform(5, 10))
        return None
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas de AI"""
        tools = []
        
        print("🔍 Iniciando scraping do TopAI.tools...")
        
        # Estratégia 1: Tenta página principal primeiro
        main_tools = self._scrape_main_page()
        if main_tools:
            tools.extend(main_tools)
        
        # Estratégia 2: Tenta página de browse  
        browse_tools = self._scrape_browse_page()
        tools.extend(browse_tools)
        
        # Estratégia 3: Tenta categorias específicas
        if len(tools) < 50:  # Se não conseguiu muitas ferramentas, tenta categorias
            category_tools = self._scrape_categories()
            tools.extend(category_tools)
        
        print(f"✅ TopAI.tools: Total de {len(tools)} ferramentas coletadas")
        return tools
    
    def _scrape_main_page(self) -> List[AITool]:
        """Scrape da página principal"""
        tools = []
        
        try:
            print(f"🔍 Fazendo scraping da página principal: {self.base_url}")
            
            response = self.get_page(self.base_url)
            if not response:
                print(f"❌ Erro ao acessar página principal")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca por diferentes padrões de links de ferramentas
            tool_links = self._find_tool_links(soup)
            
            if tool_links:
                print(f"📊 Encontrados {len(tool_links)} links na página principal")
                tools = self._process_tool_links(tool_links, "main")
            else:
                print("⚠️ Nenhum link de ferramenta encontrado na página principal")
            
        except Exception as e:
            print(f"❌ Erro no scraping da página principal: {e}")
        
        return tools
    
    def _scrape_browse_page(self) -> List[AITool]:
        """Scrape da página de browse"""
        tools = []
        
        try:
            browse_url = f"{self.base_url}/browse"
            print(f"🔍 Fazendo scraping da página browse: {browse_url}")
            
            response = self.get_page(browse_url)
            if not response:
                print(f"❌ Erro ao acessar página browse")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca por links de ferramentas
            tool_links = self._find_tool_links(soup)
            
            if tool_links:
                print(f"📊 Encontrados {len(tool_links)} links na página browse")
                tools = self._process_tool_links(tool_links, "browse")
            else:
                print("⚠️ Nenhum link de ferramenta encontrado na página browse")
            
        except Exception as e:
            print(f"❌ Erro no scraping da página browse: {e}")
        
        return tools
    
    def _scrape_categories(self) -> List[AITool]:
        """Scrape de categorias específicas"""
        tools = []
        
        # Categorias comuns que podem estar disponíveis
        categories = [
            "ai-writing", "chatbots", "image-generation", "video", "productivity", 
            "marketing", "design", "code", "business", "audio", "education", "research"
        ]
        
        for category in categories:
            try:
                category_url = f"{self.base_url}/category/{category}"
                print(f"🔍 Tentando categoria: {category}")
                
                response = self.get_page(category_url)
                if not response:
                    # Tenta formato alternativo
                    category_url = f"{self.base_url}/browse?category={category}"
                    response = self.get_page(category_url)
                
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tool_links = self._find_tool_links(soup)
                    
                    if tool_links:
                        category_tools = self._process_tool_links(tool_links[:20], category)  # Limita a 20 por categoria
                        tools.extend(category_tools)
                        print(f"✅ Categoria {category}: {len(category_tools)} ferramentas")
                    
                # Pausa entre categorias
                time.sleep(random.uniform(5, 10))
                
            except Exception as e:
                print(f"❌ Erro na categoria {category}: {e}")
                continue
        
        return tools
    
    def _find_tool_links(self, soup: BeautifulSoup) -> List:
        """Encontra links de ferramentas na página"""
        tool_links = []
        
        # Padrões possíveis para links de ferramentas
        patterns = [
            'a[href*="/tool/"]',
            'a[href*="/ai-tool/"]', 
            'a[href*="/tools/"]',
            'a[class*="tool"]',
            'a[class*="card"]',
            'a[data-*="tool"]',
            'a[href*="/t/"]',  # Formato curto comum
            '.tool-card a',
            '.ai-tool a',
            'article a'
        ]
        
        for pattern in patterns:
            links = soup.select(pattern)
            if links:
                tool_links.extend(links)
                print(f"   📍 Padrão '{pattern}': {len(links)} links")
        
        # Remove duplicatas
        seen_hrefs = set()
        unique_links = []
        for link in tool_links:
            href = link.get('href', '')
            if href and href not in seen_hrefs and not any(skip in href.lower() for skip in ['login', 'register', 'about', 'contact', 'privacy', 'terms', 'blog']):
                seen_hrefs.add(href)
                unique_links.append(link)
        
        return unique_links
    
    def _process_tool_links(self, links: List, section: str = "") -> List[AITool]:
        """Processa links de ferramentas"""
        tools = []
        
        for i, link in enumerate(links):
            try:
                tool = self._parse_tool_from_link(link, i, section)
                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                    tools.append(tool)
            except Exception as e:
                continue
        
        return tools
    
    def _parse_tool_from_link(self, link_element, index: int, section: str = "") -> Optional[AITool]:
        """Extrai dados de uma ferramenta a partir de um link"""
        
        # URL da ferramenta
        href = link_element.get('href', '')
        if not href:
            return None
        
        # Torna URL absoluta se necessário
        tool_url = href
        if href.startswith('/'):
            tool_url = self.base_url + href
        elif not href.startswith('http'):
            tool_url = f"{self.base_url}/{href}"
        
        # Nome da ferramenta
        name = ""
        
        # Estratégias para extrair nome
        strategies = [
            lambda: link_element.get_text().strip(),
            lambda: link_element.get('title', ''),
            lambda: link_element.get('aria-label', ''),
            lambda: link_element.select_one('img').get('alt', '') if link_element.select_one('img') else '',
            lambda: link_element.parent.select_one('h1, h2, h3, h4, h5, h6').get_text().strip() if link_element.parent and link_element.parent.select_one('h1, h2, h3, h4, h5, h6') else ''
        ]
        
        for strategy in strategies:
            try:
                name = strategy()
                if name and len(name.strip()) > 2:
                    name = name.strip()
                    break
            except:
                continue
        
        if not name or len(name) < 2:
            name = f"TopAI Tool {index}"
        
        # Limpa o nome
        name = re.sub(r'\s+', ' ', name.strip())[:100]
        
        # Descrição - busca no elemento pai
        description = ""
        parent = link_element.parent
        if parent:
            desc_elem = (
                parent.select_one('p') or
                parent.select_one('[class*="desc"]') or
                parent.select_one('[class*="summary"]') or
                parent.select_one('.description')
            )
            if desc_elem:
                description = desc_elem.get_text().strip()
                description = re.sub(r'\s+', ' ', description)[:500]
        
        # Categorias - infere da seção e do texto
        categories = []
        if section:
            categories.append(section)
        
        # Adiciona categorias inferidas
        inferred_categories = self._infer_categories_from_text(name + " " + description)
        categories.extend(inferred_categories)
        
        # Remove duplicatas
        categories = list(dict.fromkeys(categories))
        
        # Preço - extrai de badges, texto do elemento ou URLs
        price = "Unknown"
        
        # Estratégias para extrair preço
        # 1. Busca por badges/tags de preço
        price_elements = parent.select('.price, .pricing, .badge, [class*="price"], [class*="free"]') if parent else []
        for price_elem in price_elements:
            price_text = price_elem.get_text().strip().lower()
            if price_text and len(price_text) < 50:  # Evita textos muito longos
                if 'free' in price_text:
                    price = "Free"
                elif 'trial' in price_text:
                    price = "Free Trial"
                elif 'freemium' in price_text:
                    price = "Freemium"
                elif '$' in price_text:
                    price = price_text.replace('$', '$')  # Normaliza
                break
        
        # 2. Se não encontrou badge, busca no texto geral do elemento
        if price == "Unknown" and parent:
            element_text = parent.get_text().lower()
            
            # Busca por padrões de preço específicos
            price_patterns = [
                r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:month|mo)',
                r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:year|yr)',
                r'(\d+)\s*(?:usd|dollars?)\s*(?:/|\s+per\s+)?(?:month|mo)',
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, element_text, re.IGNORECASE)
                if match:
                    amount = match.group(1).replace(',', '')
                    if 'month' in pattern or '/mo' in pattern:
                        price = f"${amount}/month"
                    elif 'year' in pattern or '/yr' in pattern:
                        price = f"${amount}/year"
                    else:
                        price = f"${amount}"
                    break
            
            # Se não encontrou padrão específico, busca por categorias
            if price == "Unknown":
                if 'free trial' in element_text:
                    price = "Free Trial"
                elif 'freemium' in element_text:
                    price = "Freemium"
                elif 'free' in element_text and 'trial' not in element_text:
                    price = "Free"
                elif any(word in element_text for word in ['paid', 'premium', 'subscription']):
                    price = "Paid"
        
        # 3. Estratégia adicional: verifica se está na seção de ferramentas gratuitas
        if price == "Unknown" and href and 'pricing=free' in href:
            price = "Free"
        
        # Popularidade baseada na posição na página
        popularity = max(10, 100 - (index * 2))
        
        # ID único
        ext_id = self._generate_ext_id(href, name, index)
        
        # Extrai informações adicionais
        # Logo URL
        logo_url = self.extract_logo_url(parent, tool_url)
        
        # Platform info
        platform = self.extract_platform_info(parent or link_element, description)
        
        # Features
        features = self.extract_features(parent or link_element, description)
        
        # Rank baseado na posição
        rank = index + 1
        
        # Upvotes/likes - busca por padrões específicos do TopAI
        upvotes = None
        if parent:
            element_text = parent.get_text()
            upvotes_patterns = [
                r'(\d+)\s*(?:votes?|upvotes?|likes?)', 
                r'(\d+)\s*👍', 
                r'(\d+)\s*⭐'
            ]
            upvotes = self.extract_numeric_value(element_text, upvotes_patterns)
        
        # Monthly users
        monthly_users = None
        if parent:
            users_patterns = [
                r'(\d+(?:,\d+)*)\s*(?:monthly\s+)?users?',
                r'(\d+(?:,\d+)*)\s*visitors?',
                r'(\d+(?:k|K|m|M))\s*users?'
            ]
            monthly_users = self.extract_numeric_value(element_text, users_patterns)
            
            # Converte K/M notation
            if monthly_users:
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
        if parent:
            maturity_text = parent.get_text().lower()
            if 'beta' in maturity_text:
                maturity = 'beta'
            elif 'new' in maturity_text or 'recently' in maturity_text:
                maturity = 'beta'
            elif any(term in maturity_text for term in ['established', 'stable', 'proven']):
                maturity = 'stable'
        
        # Classificação de domínio
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
            # Enhanced fields
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
    
    def _infer_categories_from_text(self, text: str) -> List[str]:
        """Infere categorias baseado no texto"""
        text_lower = text.lower()
        categories = []
        
        keyword_map = {
            "writing": ["write", "writing", "text", "content", "copywriting", "blog", "article"],
            "chatbot": ["chat", "conversation", "bot", "assistant", "talk", "dialogue"],
            "image": ["image", "photo", "picture", "visual", "graphic", "art", "generate"],
            "video": ["video", "film", "movie", "clip", "animation", "editing"],
            "audio": ["audio", "music", "sound", "voice", "podcast", "speech"],
            "code": ["code", "programming", "developer", "api", "coding", "development"],
            "design": ["design", "ui", "ux", "creative", "prototype", "mockup"],
            "productivity": ["productivity", "organize", "task", "management", "workflow"],
            "marketing": ["marketing", "seo", "social", "campaign", "advertising", "promotion"],
            "business": ["business", "startup", "entrepreneur", "finance", "sales"],
            "education": ["education", "learning", "teach", "course", "training"],
            "research": ["research", "analysis", "data", "insight", "study"]
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
                if part and len(part) > 2 and part not in ['tool', 'ai-tool', 'tools']:
                    clean_part = re.sub(r'[^\w\-]', '', part)[:20]
                    if clean_part:
                        return f"topai_{clean_part}"
        
        # Usa o nome da ferramenta
        if name:
            clean_name = re.sub(r'[^\w\s]', '', name.lower())
            clean_name = re.sub(r'\s+', '_', clean_name)[:30]
            if clean_name:
                return f"topai_{clean_name}"
        
        # Fallback para índice
        return f"topai_tool_{index}"


def scrape_topai_tools() -> List[AITool]:
    """Função de conveniência para fazer scraping do TopAI.tools"""
    scraper = TopAIToolsScraper()
    return scraper.scrape()