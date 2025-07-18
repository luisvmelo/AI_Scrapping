"""
Scraper para There's An AI For That com anti-detecção avançada
URL: https://theresanaiforthat.com
Implementa múltiplas estratégias para contornar bloqueios 403
"""

import json
import time
import random
import re
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from .common import BaseScraper, AITool

class TheresAnAIForThatScraperAdvanced(BaseScraper):
    """Scraper para theresanaiforthat.com com anti-detecção avançada"""
    
    def __init__(self):
        super().__init__("theresanaiforthat", "https://theresanaiforthat.com")
        
        # Headers mais sofisticados com rotação
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0'
        ]
        
        self._setup_advanced_session()
    
    def _setup_advanced_session(self):
        """Configura sessão com headers anti-detecção avançados"""
        
        # Headers base comuns
        base_headers = {
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
        }
        
        self.session.headers.update(base_headers)
        
        # Configurações adicionais da sessão
        self.session.timeout = 20
        
        # Adiciona cookies comuns
        self.session.cookies.update({
            'session_id': f'sess_{random.randint(100000, 999999)}',
            'user_pref': 'en',
            'timezone': 'UTC'
        })
    
    def get_page(self, url: str, max_retries: int = 5) -> Optional:
        """Requisição com anti-detecção avançada"""
        
        for attempt in range(max_retries):
            try:
                # Pausa aleatória longa
                time.sleep(random.uniform(5, 12))
                
                # Rotaciona User-Agent
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                
                # Adiciona headers variáveis
                variable_headers = {
                    'X-Requested-With': random.choice(['XMLHttpRequest', '']),
                    'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    'Referer': random.choice([
                        'https://www.google.com/',
                        'https://www.bing.com/',
                        'https://duckduckgo.com/',
                        ''
                    ])
                }
                
                # Remove headers vazios
                variable_headers = {k: v for k, v in variable_headers.items() if v}
                
                response = self.session.get(url, headers=variable_headers, timeout=20)
                
                # Verifica diferentes tipos de bloqueio
                if response.status_code == 403:
                    print(f"🚫 Bloqueado (403) na tentativa {attempt + 1} para {url}")
                    if attempt < max_retries - 1:
                        # Pausa mais longa em caso de bloqueio
                        wait_time = random.uniform(20, 40) * (attempt + 1)
                        print(f"   ⏳ Aguardando {wait_time:.1f}s antes de tentar novamente...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"   ❌ Todas as tentativas falharam para {url}")
                        return None
                
                elif response.status_code == 429:  # Rate limited
                    print(f"🕐 Rate limited (429) na tentativa {attempt + 1}")
                    if attempt < max_retries - 1:
                        wait_time = random.uniform(60, 120)  # Aguarda 1-2 minutos
                        print(f"   ⏳ Aguardando {wait_time:.1f}s devido ao rate limit...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return None
                
                elif response.status_code == 503:  # Service unavailable
                    print(f"🚧 Serviço indisponível (503) na tentativa {attempt + 1}")
                    if attempt < max_retries - 1:
                        wait_time = random.uniform(30, 60)
                        time.sleep(wait_time)
                        continue
                    else:
                        return None
                
                response.raise_for_status()
                
                # Verifica se a resposta contém conteúdo válido
                if len(response.text) < 1000:
                    print(f"⚠️ Resposta muito pequena ({len(response.text)} chars), possível bloqueio")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(10, 20))
                        continue
                
                print(f"✅ Sucesso na tentativa {attempt + 1} para {url}")
                return response
                
            except Exception as e:
                print(f"❌ Erro na tentativa {attempt + 1} para {url}: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(random.uniform(8, 15))
        
        return None
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas de AI com estratégias múltiplas"""
        tools = []
        
        print("🔍 Iniciando scraping do There's An AI For That com anti-detecção...")
        
        # Estratégia 1: Página principal
        main_tools = self._scrape_main_page()
        if main_tools:
            tools.extend(main_tools)
            print(f"✅ Página principal: {len(main_tools)} ferramentas")
        
        # Estratégia 2: Páginas de categorias
        if len(tools) < 50:  # Se não conseguiu muitas ferramentas
            category_tools = self._scrape_categories()
            tools.extend(category_tools)
            print(f"✅ Categorias: {len(category_tools)} ferramentas")
        
        # Estratégia 3: API endpoints (se existirem)
        if len(tools) < 20:
            api_tools = self._try_api_endpoints()
            tools.extend(api_tools)
            print(f"✅ API: {len(api_tools)} ferramentas")
        
        # Estratégia 4: URLs alternativas
        if len(tools) < 10:
            alt_tools = self._try_alternative_urls()
            tools.extend(alt_tools)
            print(f"✅ URLs alternativas: {len(alt_tools)} ferramentas")
        
        # Remove duplicatas
        tools = self._remove_duplicates(tools)
        
        print(f"🎯 There's An AI For That: {len(tools)} ferramentas únicas coletadas")
        return tools
    
    def _scrape_main_page(self) -> List[AITool]:
        """Scrape da página principal com múltiplas tentativas"""
        tools = []
        
        try:
            print(f"🔍 Fazendo scraping da página principal: {self.base_url}")
            
            response = self.get_page(self.base_url)
            if not response:
                print(f"❌ Erro ao acessar página principal")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"📄 HTML carregado: {len(response.text)} caracteres")
            
            # Procura por ferramentas usando múltiplos seletores
            tools = self._extract_tools_from_soup(soup, "main")
            
        except Exception as e:
            print(f"❌ Erro no scraping da página principal: {e}")
        
        return tools
    
    def _scrape_categories(self) -> List[AITool]:
        """Scrape de categorias específicas"""
        tools = []
        
        # Categorias conhecidas do site
        categories = [
            "writing", "productivity", "marketing", "design", "video", 
            "image", "chatbots", "business", "education", "research",
            "audio", "code", "sales", "customer-service", "social-media"
        ]
        
        for category in categories:
            try:
                # Diferentes formatos de URL de categoria
                category_urls = [
                    f"{self.base_url}/c/{category}",
                    f"{self.base_url}/category/{category}",
                    f"{self.base_url}/tools/{category}",
                    f"{self.base_url}/{category}"
                ]
                
                category_tools = []
                for category_url in category_urls:
                    print(f"🔍 Tentando categoria {category}: {category_url}")
                    
                    response = self.get_page(category_url)
                    if response and response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        category_tools = self._extract_tools_from_soup(soup, category)
                        
                        if category_tools:
                            print(f"✅ Categoria {category}: {len(category_tools)} ferramentas")
                            break
                
                tools.extend(category_tools)
                
                # Pausa entre categorias
                if category_tools:
                    time.sleep(random.uniform(8, 15))
                
            except Exception as e:
                print(f"❌ Erro na categoria {category}: {e}")
                continue
        
        return tools
    
    def _try_api_endpoints(self) -> List[AITool]:
        """Tenta acessar possíveis endpoints de API"""
        tools = []
        
        # Possíveis endpoints de API
        api_endpoints = [
            f"{self.base_url}/api/tools",
            f"{self.base_url}/api/v1/tools", 
            f"{self.base_url}/api/ai-tools",
            f"{self.base_url}/wp-json/wp/v2/tools",  # Se for WordPress
            f"{self.base_url}/tools.json"
        ]
        
        for endpoint in api_endpoints:
            try:
                print(f"🔌 Tentando API: {endpoint}")
                
                # Adiciona headers específicos para API
                api_headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                }
                
                response = self.session.get(endpoint, headers=api_headers, timeout=15)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            tools_data = data
                        elif isinstance(data, dict):
                            tools_data = data.get('tools', data.get('data', data.get('results', [])))
                        else:
                            continue
                        
                        if tools_data:
                            print(f"✅ API {endpoint}: {len(tools_data)} ferramentas encontradas")
                            
                            for i, tool_data in enumerate(tools_data[:50]):  # Limita a 50
                                try:
                                    tool = self._parse_api_tool(tool_data, i)
                                    if tool:
                                        tools.append(tool)
                                except:
                                    continue
                            
                            break  # Para na primeira API que funcionar
                    
                    except json.JSONDecodeError:
                        continue
                
            except Exception as e:
                continue
        
        return tools
    
    def _try_alternative_urls(self) -> List[AITool]:
        """Tenta URLs alternativas do site"""
        tools = []
        
        # URLs alternativas priorizando páginas populares/famosas primeiro
        alt_urls = [
            f"{self.base_url}/popular",           # PRIMEIRO: Mais populares
            f"{self.base_url}/featured",          # SEGUNDO: Destacados
            f"{self.base_url}/trending",          # TERCEIRO: Tendências
            f"{self.base_url}/top",               # QUARTO: Top rated
            f"{self.base_url}/best",              # QUINTO: Melhores
            f"{self.base_url}/directory",         # Diretório geral
            f"{self.base_url}/browse",            # Navegação
            f"{self.base_url}/all-tools",         # Todas as ferramentas
            f"{self.base_url}/new"                # ÚLTIMO: Mais recentes
        ]
        
        for url in alt_urls:
            try:
                print(f"🔗 Tentando URL alternativa: {url}")
                
                response = self.get_page(url)
                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    alt_tools = self._extract_tools_from_soup(soup, "alternative")
                    
                    if alt_tools:
                        tools.extend(alt_tools)
                        print(f"✅ {url}: {len(alt_tools)} ferramentas")
                        break  # Para na primeira URL que funcionar
                
            except Exception as e:
                continue
        
        return tools
    
    def _extract_tools_from_soup(self, soup: BeautifulSoup, section: str = "") -> List[AITool]:
        """Extrai ferramentas do BeautifulSoup"""
        tools = []
        
        # Múltiplos seletores para diferentes estruturas
        selectors = [
            # Seletores específicos do There's An AI For That
            '[data-testid*="tool"]',
            '.tool-card',
            '.ai-tool',
            '.directory-item',
            
            # Seletores genéricos
            'div[class*="tool"]',
            'div[class*="card"]',
            'div[class*="item"]',
            'article',
            
            # Links de ferramentas
            'a[href*="/tool/"]',
            'a[href*="/ai/"]'
        ]
        
        found_elements = []
        for selector in selectors:
            elements = soup.select(selector)
            if elements and len(elements) > 3:
                print(f"   📍 Seletor '{selector}': {len(elements)} elementos")
                found_elements = elements
                break
        
        # Se não encontrou, busca por qualquer link potencial
        if not found_elements:
            print("   🔍 Buscando por links potenciais...")
            all_links = soup.select('a[href]')
            
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if (href and text and len(text) > 2 and len(text) < 100 and
                    not any(skip in href.lower() for skip in ['login', 'register', 'about', 'contact', 'privacy', 'terms', 'blog'])):
                    found_elements.append(link)
            
            found_elements = found_elements[:50]  # Limita
            print(f"   📍 Links potenciais: {len(found_elements)}")
        
        # Processa elementos encontrados
        for i, element in enumerate(found_elements):
            try:
                tool = self._parse_tool_element(element, i, section)
                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                    tools.append(tool)
            except Exception as e:
                continue
        
        return tools
    
    def _parse_tool_element(self, element, index: int, section: str = "") -> Optional[AITool]:
        """Extrai dados de uma ferramenta do elemento HTML"""
        
        # Nome da ferramenta
        name = ""
        
        name_selectors = [
            'h1, h2, h3, h4, h5, h6',
            '[class*="title"]', 
            '[class*="name"]',
            'a'
        ]
        
        for selector in name_selectors:
            name_elem = element.select_one(selector)
            if name_elem:
                name = name_elem.get_text().strip()
                if name and len(name) > 2:
                    break
        
        if not name and element.name == 'a':
            name = element.get_text().strip()
        
        if name:
            name = re.sub(r'\s+', ' ', name.strip())[:100]
        
        if not name or len(name) < 2:
            name = f"TheresAnAI Tool {index}"
        
        # Descrição
        description = ""
        desc_selectors = [
            'p',
            '[class*="desc"]',
            '[class*="summary"]',
            '.content'
        ]
        
        for selector in desc_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                description = desc_elem.get_text().strip()
                if description and len(description) > 10:
                    break
        
        if description:
            description = re.sub(r'\s+', ' ', description.strip())[:500]
        
        # URL da ferramenta
        href = ""
        if element.name == 'a':
            href = element.get('href', '')
        else:
            link_elem = element.select_one('a')
            if link_elem:
                href = link_elem.get('href', '')
        
        tool_url = href
        if href and href.startswith('/'):
            tool_url = self.base_url + href
        
        # Categorias
        categories = []
        if section:
            categories.append(section)
        
        # Busca por tags
        tag_selectors = ['.tag', '.category', '[class*="tag"]']
        for selector in tag_selectors:
            tags = element.select(selector)
            for tag in tags:
                tag_text = tag.get_text().strip()
                if tag_text and len(tag_text) < 30:
                    categories.append(tag_text)
        
        # Infere categorias do texto
        if len(categories) <= 1:
            inferred = self._infer_categories_from_text(name + " " + description)
            categories.extend(inferred)
        
        categories = list(dict.fromkeys(categories))
        
        # Preço - extração melhorada com padrões específicos
        price = "Unknown"
        price_text = element.get_text().lower()
        
        # Busca por badges/elementos específicos de preço primeiro
        price_elements = element.select('.price, .pricing, .badge, [class*="price"], [class*="free"], [class*="paid"]')
        for price_elem in price_elements:
            elem_text = price_elem.get_text().strip().lower()
            if elem_text and len(elem_text) < 50:  # Evita textos muito longos
                if 'free' in elem_text:
                    price = "Free"
                elif 'trial' in elem_text:
                    price = "Free Trial"
                elif 'freemium' in elem_text:
                    price = "Freemium"
                elif '$' in elem_text:
                    price = elem_text.replace('$', '$')  # Normaliza
                break
        
        # Se não encontrou badge específico, busca por padrões de preço no texto geral
        if price == "Unknown":
            # Busca por preços específicos primeiro ($X/month, $X/year)
            price_patterns = [
                r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:month|mo|monthly)',
                r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:year|yr|yearly|annually)',
                r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+per\s+)?(?:week|weekly)',
                r'\$(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:/|\s+one.?time|once)',
                r'(\d+(?:,\d+)?(?:\.\d{2})?)\s*(?:usd|dollars?)\s*(?:/|\s+per\s+)?(?:month|mo)',
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, price_text, re.IGNORECASE)
                if match:
                    amount = match.group(1).replace(',', '')
                    if 'month' in pattern or '/mo' in pattern:
                        price = f"${amount}/month"
                    elif 'year' in pattern or '/yr' in pattern:
                        price = f"${amount}/year"
                    elif 'week' in pattern:
                        price = f"${amount}/week"
                    elif 'one.?time' in pattern or 'once' in pattern:
                        price = f"${amount} one-time"
                    else:
                        price = f"${amount}/month"  # Default to monthly
                    break
            
            # Se não encontrou preço específico, busca por categorias
            if price == "Unknown":
                if 'free trial' in price_text:
                    price = "Free Trial"
                elif 'freemium' in price_text:
                    price = "Freemium"
                elif 'free' in price_text and 'trial' not in price_text:
                    price = "Free"
                elif any(word in price_text for word in ['paid', 'premium', 'subscription', 'plans']):
                    price = "Paid"
                elif '$' in price_text:
                    # Busca qualquer valor em dólar
                    dollar_match = re.search(r'\$(\d+(?:,\d+)?(?:\.\d{2})?)', price_text)
                    if dollar_match:
                        amount = dollar_match.group(1)
                        price = f"${amount}"
        
        # Popularidade
        popularity = max(10, 100 - (index * 2))
        
        # ID único
        ext_id = self._generate_ext_id(href, name, index)
        
        # Extrai informações adicionais
        # Logo URL
        logo_url = self.extract_logo_url(element, tool_url)
        
        # Platform info
        platform = self.extract_platform_info(element, description)
        
        # Features
        features = self.extract_features(element, description)
        
        # Rank baseado na posição
        rank = index + 1
        
        # Upvotes - TheresAnAI pode ter sistemas de voting
        upvotes = None
        element_text = element.get_text()
        upvotes_patterns = [
            r'(\d+)\s*(?:votes?|upvotes?|likes?)', 
            r'(\d+)\s*👍', 
            r'(\d+)\s*hearts?'
        ]
        upvotes = self.extract_numeric_value(element_text, upvotes_patterns)
        
        # Monthly users
        monthly_users = None
        users_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:monthly\s+)?users?',
            r'(\d+(?:,\d+)*)\s*people\s+use',
            r'used\s+by\s+(\d+(?:,\d+)*)',
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
    
    def _parse_api_tool(self, data: dict, index: int) -> Optional[AITool]:
        """Extrai dados de uma ferramenta de resposta API"""
        
        # Nome
        name = ""
        for key in ['name', 'title', 'tool_name']:
            if key in data and data[key]:
                name = str(data[key]).strip()[:100]
                break
        
        if not name:
            name = f"TheresAnAI API Tool {index}"
        
        # Descrição
        description = ""
        for key in ['description', 'desc', 'summary']:
            if key in data and data[key]:
                description = str(data[key]).strip()[:500]
                break
        
        # URL
        href = ""
        for key in ['url', 'link', 'website']:
            if key in data and data[key]:
                href = str(data[key])
                break
        
        # Categorias
        categories = []
        for key in ['categories', 'tags', 'category']:
            if key in data and data[key]:
                if isinstance(data[key], list):
                    categories.extend([str(cat) for cat in data[key]])
                else:
                    categories.append(str(data[key]))
        
        if not categories:
            categories = self._infer_categories_from_text(name + " " + description)
        
        # Preço
        price = "Unknown"
        for key in ['price', 'pricing']:
            if key in data and data[key]:
                price = str(data[key])
                break
        
        # Popularidade
        popularity = 50.0
        for key in ['rating', 'score', 'popularity']:
            if key in data and data[key]:
                try:
                    popularity = float(data[key])
                    if popularity <= 5:
                        popularity = (popularity / 5) * 100
                    break
                except:
                    continue
        
        # ID único
        ext_id = self._generate_ext_id(href, name, index)
        
        # Enhanced fields for API tools
        # URL
        tool_url = href
        
        # Logo URL - não disponível via API geralmente
        logo_url = None
        
        # Platform info - pode estar nos dados
        platform = data.get('platforms', ['web'])
        if isinstance(platform, str):
            platform = [platform]
        
        # Features - pode estar nos dados como tags/categories
        features = {}
        if 'tags' in data:
            features['tags'] = data['tags']
        if 'features' in data:
            features.update(data['features'])
        
        # Rank baseado no índice
        rank = index + 1
        
        # Upvotes/rating - pode estar nos dados
        upvotes = data.get('upvotes') or data.get('likes') or data.get('votes')
        
        # Monthly users - pode estar nos dados  
        monthly_users = data.get('monthly_users') or data.get('users') or data.get('usage')
        
        # Editor score - pode estar nos dados como rating
        editor_score = data.get('editor_score') or data.get('rating')
        if editor_score and isinstance(editor_score, (int, float)):
            # Normaliza para escala 0-10
            if editor_score > 10:
                editor_score = editor_score / 10
            editor_score = round(float(editor_score), 1)
        
        # Maturity - pode estar nos dados
        maturity = data.get('maturity') or data.get('status')
        
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
            features=features if features else None,
            last_scraped=datetime.now()
        )
    
    def _infer_categories_from_text(self, text: str) -> List[str]:
        """Infere categorias baseado no texto"""
        text_lower = text.lower()
        categories = []
        
        keyword_map = {
            "writing": ["write", "writing", "text", "content", "copywriting"],
            "chatbot": ["chat", "conversation", "bot", "assistant"],
            "image": ["image", "photo", "picture", "visual", "art"],
            "video": ["video", "film", "movie", "animation"],
            "audio": ["audio", "music", "sound", "voice"],
            "code": ["code", "programming", "developer", "api"],
            "productivity": ["productivity", "organize", "task", "management"],
            "marketing": ["marketing", "seo", "social", "campaign"],
            "business": ["business", "startup", "finance", "sales"]
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        if not categories:
            categories = ["ai-tool"]
        
        return categories
    
    def _generate_ext_id(self, href: str, name: str, index: int) -> str:
        """Gera um ID único para a ferramenta"""
        if href:
            url_parts = href.split('/')
            for part in reversed(url_parts):
                if part and len(part) > 2:
                    clean_part = re.sub(r'[^\w\-]', '', part)[:20]
                    if clean_part:
                        return f"theresanai_{clean_part}"
        
        if name:
            clean_name = re.sub(r'[^\w\s]', '', name.lower())
            clean_name = re.sub(r'\s+', '_', clean_name)[:30]
            if clean_name:
                return f"theresanai_{clean_name}"
        
        return f"theresanai_tool_{index}"
    
    def _remove_duplicates(self, tools: List[AITool]) -> List[AITool]:
        """Remove ferramentas duplicadas"""
        seen_names = set()
        unique_tools = []
        
        for tool in tools:
            name_key = tool.name.lower().strip()
            if name_key not in seen_names:
                seen_names.add(name_key)
                unique_tools.append(tool)
        
        removed_count = len(tools) - len(unique_tools)
        if removed_count > 0:
            print(f"🧹 Removidas {removed_count} duplicatas do TheresAnAI")
        
        return unique_tools


def scrape_theresanaiforthat() -> List[AITool]:
    """Função de conveniência para fazer scraping do There's An AI For That"""
    scraper = TheresAnAIForThatScraperAdvanced()
    return scraper.scrape()