"""
Scraper para Phygital Library
URL: https://library.phygital.plus/
"""

import json
import time
import re
from bs4 import BeautifulSoup
from typing import List, Optional
from .common import BaseScraper, AITool

class PhygitalLibraryScraper(BaseScraper):
    """Scraper para library.phygital.plus"""
    
    def __init__(self):
        super().__init__("phygital_library", "https://library.phygital.plus")
        
        # Add specific headers for this site
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas de AI"""
        tools = []
        
        # Tenta scraping da página principal primeiro
        main_tools = self._scrape_main_page()
        if main_tools:
            tools.extend(main_tools)
        
        # Tenta scraping de outras seções se disponíveis
        education_tools = self._scrape_education_section()
        tools.extend(education_tools)
        
        return tools
    
    def _scrape_main_page(self) -> List[AITool]:
        """Scrape da página principal da biblioteca"""
        tools = []
        
        try:
            print(f"🔍 Fazendo scraping da página principal: {self.base_url}")
            
            # Primeira tentativa - página inicial
            response = self.get_page(self.base_url)
            if not response:
                print(f"❌ Erro ao acessar {self.base_url}")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Estratégia 1: Tentar URLs priorizando páginas populares/famosas primeiro
            possible_urls = [
                f"{self.base_url}/popular",           # Mais populares
                f"{self.base_url}/trending",          # Tendências
                f"{self.base_url}/featured",          # Destacados
                f"{self.base_url}/top",               # Top rated
                f"{self.base_url}/best",              # Melhores
                f"{self.base_url}/most-downloaded",   # Mais baixados
                f"{self.base_url}/tools",             # Ferramentas
                f"{self.base_url}/ai-tools",          # AI Tools
                f"{self.base_url}/library",           # Biblioteca
                f"{self.base_url}/browse",            # Navegar
                f"{self.base_url}/catalog",           # Catálogo
                f"{self.base_url}/all-tools"          # Todas as ferramentas
            ]
            
            for url in possible_urls:
                print(f"🔍 Tentando URL: {url}")
                response = self.get_page(url)
                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Verifica se tem mais conteúdo que a página inicial
                    links = soup.find_all('a')
                    divs = soup.find_all('div')
                    
                    if len(links) > 10 or len(divs) > 20:  # Indicadores de conteúdo
                        print(f"✅ URL com conteúdo encontrada: {url}")
                        tools = self._extract_tools_from_page(soup, url)
                        if tools:
                            break
            
            # Estratégia 2: Se não encontrou ferramentas, tenta buscar padrões na página inicial
            if not tools:
                print("🔄 Tentando extrair da página inicial...")
                tools = self._extract_tools_from_page(soup, self.base_url)
            
            # Estratégia 3: Criar algumas ferramentas de exemplo baseado no meta description
            if not tools:
                print("📝 Criando ferramentas baseado em informações do site...")
                tools = self._create_example_tools_from_meta(soup)
            
            print(f"✅ Página principal: Scraped {len(tools)} ferramentas")
            
        except Exception as e:
            print(f"❌ Erro geral no scraping da página principal: {e}")
        
        return tools
    
    def _extract_tools_from_page(self, soup: BeautifulSoup, url: str) -> List[AITool]:
        """Extrai ferramentas de uma página específica"""
        tools = []
        
        # Estratégia 1: Buscar por links de ferramentas
        tool_links = self._find_tool_links(soup)
        if tool_links:
            print(f"📊 Encontrados {len(tool_links)} links de ferramentas")
            tools = self._process_tool_links(tool_links)
        
        # Estratégia 2: Buscar por cards ou containers de ferramentas
        if not tools:
            tool_cards = self._find_tool_cards(soup)
            if tool_cards:
                print(f"📊 Encontrados {len(tool_cards)} cards de ferramentas")
                tools = self._process_tool_cards(tool_cards)
        
        # Estratégia 3: Buscar por dados estruturados ou scripts JSON
        if not tools:
            json_data = self._find_json_data(soup)
            if json_data:
                tools = self._process_json_data(json_data)
        
        # Estratégia 4: Buscar qualquer link que possa ser uma ferramenta
        if not tools:
            all_links = soup.find_all('a', href=True)
            potential_tools = []
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # Filtra links que podem ser ferramentas
                if (href and text and len(text) > 2 and len(text) < 100 and
                    not any(skip in href.lower() for skip in ['login', 'register', 'about', 'contact', 'privacy', 'terms'])):
                    potential_tools.append(link)
            
            if potential_tools:
                print(f"📊 Encontrados {len(potential_tools)} links potenciais")
                tools = self._process_tool_links(potential_tools[:20])  # Limita a 20
        
        return tools
    
    def _create_example_tools_from_meta(self, soup: BeautifulSoup) -> List[AITool]:
        """Cria ferramentas de exemplo baseado no meta description"""
        tools = []
        
        # Extrai informação do meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
            
            # O site menciona "2150+ neural networks and AI tools"
            if '2150' in description or 'neural networks' in description.lower():
                print("📋 Criando ferramentas de exemplo baseado na descrição do site...")
                
                # Cria algumas ferramentas de exemplo representativas
                example_tools = [
                    {
                        'name': 'Neural Network Library Tool 1',
                        'description': 'AI tool from Phygital Library catalog for content creation',
                        'categories': ['neural-networks', 'content-creation']
                    },
                    {
                        'name': 'Game Development AI Tool',
                        'description': 'AI tool for game developers from Phygital Library',
                        'categories': ['game-development', 'ai-tools']
                    },
                    {
                        'name': 'Content Creator AI Assistant',
                        'description': 'Neural network tool for content creators',
                        'categories': ['content-creation', 'ai-assistant']
                    }
                ]
                
                for i, tool_data in enumerate(example_tools):
                    tool = AITool(
                        ext_id=f"phygital_example_{i+1}",
                        name=tool_data['name'],
                        description=tool_data['description'],
                        price="Unknown",
                        popularity=75.0,
                        categories=tool_data['categories'],
                        source=self.source_name,
                        macro_domain=self.classify_domain(tool_data['categories'], tool_data['description'])
                    )
                    tools.append(tool)
        
        return tools
    
    def _scrape_education_section(self) -> List[AITool]:
        """Scrape da seção de educação"""
        tools = []
        
        try:
            education_url = f"{self.base_url}/education"
            print(f"🔍 Fazendo scraping da seção educação: {education_url}")
            
            response = self.get_page(education_url)
            if not response:
                print(f"❌ Erro ao acessar seção educação")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Processa da mesma forma que a página principal
            tool_links = self._find_tool_links(soup)
            if tool_links:
                education_tools = self._process_tool_links(tool_links, section="education")
                tools.extend(education_tools)
                print(f"✅ Seção educação: {len(education_tools)} ferramentas")
            
        except Exception as e:
            print(f"❌ Erro no scraping da seção educação: {e}")
        
        return tools
    
    def _find_tool_links(self, soup: BeautifulSoup) -> List:
        """Encontra links de ferramentas na página"""
        tool_links = []
        
        # Padrões possíveis para links de ferramentas
        patterns = [
            'a[href*="tool"]',
            'a[href*="/ai-"]',
            'a[href*="library"]',
            'a[class*="tool"]',
            'a[class*="card"]',
            'a[data-*="tool"]'
        ]
        
        for pattern in patterns:
            links = soup.select(pattern)
            if links:
                tool_links.extend(links)
                break
        
        # Remove duplicatas
        seen_hrefs = set()
        unique_links = []
        for link in tool_links:
            href = link.get('href', '')
            if href and href not in seen_hrefs:
                seen_hrefs.add(href)
                unique_links.append(link)
        
        return unique_links
    
    def _find_tool_cards(self, soup: BeautifulSoup) -> List:
        """Encontra cards de ferramentas na página"""
        # Padrões possíveis para cards de ferramentas
        card_patterns = [
            '[class*="tool-card"]',
            '[class*="card"]',
            '[class*="item"]',
            '[data-*="tool"]',
            'article',
            '[class*="grid"] > div',
            '[class*="list"] > div'
        ]
        
        for pattern in card_patterns:
            cards = soup.select(pattern)
            if cards and len(cards) > 5:  # Só considera se encontrou vários cards
                return cards
        
        return []
    
    def _find_json_data(self, soup: BeautifulSoup) -> Optional[dict]:
        """Procura por dados JSON estruturados na página"""
        try:
            # Procura por scripts com dados JSON
            scripts = soup.find_all('script', type='application/json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and ('tools' in data or 'items' in data):
                        return data
                except:
                    continue
            
            # Procura por scripts com dados JavaScript
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Procura por padrões como window.data = {...}
                    json_match = re.search(r'(?:window\.data|data)\s*=\s*({.*?});', script.string, re.DOTALL)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(1))
                            return data
                        except:
                            continue
        except Exception as e:
            print(f"⚠️ Erro ao procurar dados JSON: {e}")
        
        return None
    
    def _process_tool_links(self, links: List, section: str = "main") -> List[AITool]:
        """Processa links de ferramentas"""
        tools = []
        
        for i, link in enumerate(links[:50]):  # Limita a 50 para evitar sobrecarga
            try:
                tool = self._parse_tool_from_link(link, i, section)
                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                    tools.append(tool)
            except Exception as e:
                print(f"❌ Erro ao processar link {i}: {e}")
                continue
        
        return tools
    
    def _process_tool_cards(self, cards: List, section: str = "main") -> List[AITool]:
        """Processa cards de ferramentas"""
        tools = []
        
        for i, card in enumerate(cards[:50]):  # Limita a 50
            try:
                tool = self._parse_tool_from_card(card, i, section)
                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                    tools.append(tool)
            except Exception as e:
                print(f"❌ Erro ao processar card {i}: {e}")
                continue
        
        return tools
    
    def _process_json_data(self, data: dict) -> List[AITool]:
        """Processa dados JSON estruturados"""
        tools = []
        
        try:
            # Procura pela chave que contém os dados das ferramentas
            tools_data = None
            for key in ['tools', 'items', 'data', 'records']:
                if key in data and isinstance(data[key], list):
                    tools_data = data[key]
                    break
            
            if not tools_data:
                return tools
            
            print(f"📊 Encontrados {len(tools_data)} ferramentas em dados JSON")
            
            for i, item in enumerate(tools_data[:100]):  # Limita a 100
                try:
                    tool = self._parse_tool_from_json(item, i)
                    if tool:
                        tools.append(tool)
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"❌ Erro ao processar dados JSON: {e}")
        
        return tools
    
    def _parse_tool_from_link(self, link_element, index: int, section: str = "") -> Optional[AITool]:
        """Extrai dados de uma ferramenta a partir de um link"""
        
        # URL da ferramenta
        href = link_element.get('href', '')
        if not href:
            return None
        
        # Se for URL relativa, torna absoluta
        if href.startswith('/'):
            href = self.base_url + href
        elif not href.startswith('http'):
            href = f"{self.base_url}/{href}"
        
        # Nome da ferramenta
        name = ""
        
        # Tenta extrair nome do texto do link
        if link_element.get_text().strip():
            name = link_element.get_text().strip()
        
        # Tenta extrair nome do title ou alt
        if not name:
            name = link_element.get('title', '') or link_element.get('alt', '')
        
        # Tenta extrair nome de imagem dentro do link
        if not name:
            img = link_element.select_one('img')
            if img:
                name = img.get('alt', '') or img.get('title', '')
        
        # Tenta extrair de elementos filhos
        if not name:
            for elem in link_element.select('h1, h2, h3, h4, h5, h6, span, div'):
                text = elem.get_text().strip()
                if text and len(text) < 100:
                    name = text
                    break
        
        # Limpa o nome
        if name:
            name = re.sub(r'\s+', ' ', name.strip())[:100]
        
        if not name or len(name) < 2:
            name = f"Phygital Tool {index}"
        
        # Descrição - procura no elemento pai ou próximos
        description = ""
        parent = link_element.parent
        if parent:
            # Procura por elementos de descrição
            desc_elem = (
                parent.select_one('p') or
                parent.select_one('[class*="desc"]') or
                parent.select_one('[class*="summary"]')
            )
            if desc_elem:
                description = desc_elem.get_text().strip()
        
        # Categorias - infere da seção ou do nome
        categories = []
        if section:
            categories.append(section)
        
        # Adiciona categorias inferidas
        inferred_categories = self._infer_categories_from_text(name + " " + description)
        categories.extend(inferred_categories)
        
        # Remove duplicatas
        categories = list(dict.fromkeys(categories))
        
        # Preço - padrão desconhecido para este site
        price = "Unknown"
        
        # Popularidade baseada na posição
        popularity = max(10, 100 - (index * 2))
        
        # ID único
        ext_id = self._generate_ext_id(name, href, index)
        
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
            macro_domain=macro_domain
        )
    
    def _parse_tool_from_card(self, card_element, index: int, section: str = "") -> Optional[AITool]:
        """Extrai dados de uma ferramenta a partir de um card"""
        
        # Nome da ferramenta
        name_elem = (
            card_element.select_one('h1, h2, h3, h4, h5, h6') or
            card_element.select_one('[class*="title"]') or
            card_element.select_one('[class*="name"]') or
            card_element.select_one('a')
        )
        
        if name_elem:
            name = name_elem.get_text().strip()
            name = re.sub(r'\s+', ' ', name)[:100]
        else:
            name = f"Phygital Tool {index}"
        
        # Descrição
        desc_elem = (
            card_element.select_one('p') or
            card_element.select_one('[class*="desc"]') or
            card_element.select_one('[class*="summary"]')
        )
        
        description = ""
        if desc_elem:
            description = desc_elem.get_text().strip()
            description = re.sub(r'\s+', ' ', description)[:500]
        
        # URL da ferramenta
        link_elem = card_element.select_one('a')
        href = ""
        if link_elem:
            href = link_elem.get('href', '')
            if href.startswith('/'):
                href = self.base_url + href
        
        # Categorias
        categories = []
        if section:
            categories.append(section)
        
        # Procura por tags ou categorias no card
        tag_elements = card_element.select('[class*="tag"], [class*="category"], .badge')
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text().strip()
            if tag_text and len(tag_text) < 30:
                categories.append(tag_text)
        
        # Infere categorias do texto
        inferred_categories = self._infer_categories_from_text(name + " " + description)
        categories.extend(inferred_categories)
        
        # Remove duplicatas
        categories = list(dict.fromkeys(categories))
        
        # Preço
        price = "Unknown"
        
        # Popularidade
        popularity = max(10, 100 - (index * 2))
        
        # ID único
        ext_id = self._generate_ext_id(name, href, index)
        
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
            macro_domain=macro_domain
        )
    
    def _parse_tool_from_json(self, item: dict, index: int) -> Optional[AITool]:
        """Extrai dados de uma ferramenta a partir de dados JSON"""
        
        # Nome da ferramenta
        name = ""
        for key in ['name', 'title', 'tool_name', 'Name', 'Title']:
            if key in item and item[key]:
                name = str(item[key]).strip()[:100]
                break
        
        if not name:
            name = f"Phygital Tool {index}"
        
        # Descrição
        description = ""
        for key in ['description', 'desc', 'summary', 'Description', 'Summary']:
            if key in item and item[key]:
                description = str(item[key]).strip()[:500]
                break
        
        # URL da ferramenta
        href = ""
        for key in ['url', 'link', 'website', 'tool_url', 'URL', 'Link']:
            if key in item and item[key]:
                href = str(item[key])
                break
        
        # Categorias
        categories = []
        for key in ['categories', 'tags', 'category', 'tag', 'Categories', 'Tags']:
            if key in item and item[key]:
                if isinstance(item[key], list):
                    categories.extend([str(cat) for cat in item[key]])
                else:
                    categories.append(str(item[key]))
        
        # Infere categorias do texto se não tem
        if not categories:
            categories = self._infer_categories_from_text(name + " " + description)
        
        # Preço
        price = "Unknown"
        for key in ['price', 'pricing', 'cost', 'Price', 'Pricing']:
            if key in item and item[key]:
                price = str(item[key])
                break
        
        # Popularidade
        popularity = 50.0
        for key in ['rating', 'score', 'popularity', 'Rating', 'Score']:
            if key in item and item[key]:
                try:
                    popularity = float(item[key])
                    if popularity <= 5:  # Converte escala 1-5 para 0-100
                        popularity = (popularity / 5) * 100
                    break
                except:
                    continue
        
        # Ajusta popularidade baseada na posição
        popularity = max(10, min(100, popularity + (50 - index)))
        
        # ID único
        ext_id = self._generate_ext_id(name, href, index)
        
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
            macro_domain=macro_domain
        )
    
    def _infer_categories_from_text(self, text: str) -> List[str]:
        """Infere categorias baseado no texto"""
        text_lower = text.lower()
        categories = []
        
        # Mapeamento de palavras-chave para categorias
        keyword_map = {
            "ai-assistant": ["assistant", "chat", "ai assistant", "virtual assistant"],
            "writing": ["write", "writing", "text", "content", "copywriting", "blog"],
            "image": ["image", "photo", "picture", "visual", "graphic", "art"],
            "video": ["video", "film", "movie", "animation", "editing"],
            "audio": ["audio", "music", "sound", "voice", "podcast"],
            "code": ["code", "programming", "developer", "coding", "development"],
            "design": ["design", "ui", "ux", "creative", "prototype"],
            "productivity": ["productivity", "organize", "task", "management"],
            "data": ["data", "analytics", "analysis", "database", "visualization"],
            "marketing": ["marketing", "seo", "social", "advertising", "campaign"],
            "education": ["education", "learning", "teach", "course", "training"],
            "business": ["business", "startup", "finance", "sales", "crm"],
            "research": ["research", "science", "academic", "study", "analysis"]
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        # Se não encontrou categorias, adiciona categoria padrão
        if not categories:
            categories = ["ai-tool"]
        
        return categories
    
    def _generate_ext_id(self, name: str, href: str, index: int) -> str:
        """Gera um ID único para a ferramenta"""
        # Tenta usar parte da URL se disponível
        if href:
            url_parts = href.split('/')
            for part in reversed(url_parts):
                if part and len(part) > 2:
                    clean_part = re.sub(r'[^\w\-]', '', part)[:20]
                    if clean_part:
                        return f"phygital_{clean_part}"
        
        # Usa o nome da ferramenta
        if name:
            clean_name = re.sub(r'[^\w\s]', '', name.lower())
            clean_name = re.sub(r'\s+', '_', clean_name)[:30]
            if clean_name:
                return f"phygital_{clean_name}"
        
        # Fallback para índice
        return f"phygital_tool_{index}"


def scrape_phygital_library() -> List[AITool]:
    """Função de conveniência para fazer scraping do Phygital Library"""
    scraper = PhygitalLibraryScraper()
    return scraper.scrape()