"""
Scraper para AI Tools Directory com suporte a JavaScript
URL: https://aitoolsdirectory.com
Usa Selenium para carregar conteúdo dinâmico JavaScript
"""

import json
import time
import re
from bs4 import BeautifulSoup
from typing import List, Optional
from .common import BaseScraper, AITool

class AIToolsDirectoryScraperJS(BaseScraper):
    """Scraper para aitoolsdirectory.com com execução JavaScript"""
    
    def __init__(self):
        super().__init__("aitoolsdir", "https://aitoolsdirectory.com")
        self.driver = None
    
    def _setup_selenium(self):
        """Configura Selenium WebDriver com webdriver-manager"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            print("🔧 Configurando Selenium WebDriver...")
            
            options = Options()
            options.add_argument('--headless')  # Executa sem interface gráfica
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Usa webdriver-manager para baixar e gerenciar o ChromeDriver automaticamente
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Remove propriedades que identificam como bot
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 15)
            print("✅ Selenium configurado com sucesso!")
            return True
            
        except ImportError as e:
            print(f"❌ Selenium ou webdriver-manager não instalado: {e}")
            return False
        except Exception as e:
            print(f"❌ Erro ao configurar Selenium: {e}")
            return False
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas com execução JavaScript"""
        tools = []
        
        print("🔍 Iniciando scraping do AI Tools Directory (392 ferramentas esperadas)...")
        
        # Tenta com Selenium primeiro
        if self._setup_selenium():
            try:
                tools = self._scrape_with_javascript()
            finally:
                if self.driver:
                    self.driver.quit()
        
        # Fallback: scraping sem JavaScript
        if not tools:
            print("🔄 Tentando scraping sem JavaScript como fallback...")
            tools = self._scrape_without_javascript()
        
        print(f"✅ AI Tools Directory: {len(tools)} ferramentas coletadas")
        return tools
    
    def _scrape_with_javascript(self) -> List[AITool]:
        """Scrape com execução JavaScript usando Selenium"""
        tools = []
        
        try:
            print(f"🌐 Carregando página com JavaScript: {self.base_url}")
            self.driver.get(self.base_url)
            
            # Aguarda carregamento inicial
            time.sleep(5)
            
            # Aguarda elementos serem carregados
            print("⏳ Aguardando carregamento do conteúdo JavaScript...")
            
            # Tenta aguardar diferentes tipos de elementos
            selectors_to_wait = [
                "div[class*='tool']",
                "div[class*='card']", 
                "div[class*='item']",
                "article",
                ".tool-item",
                ".ai-tool",
                "[data-tool]"
            ]
            
            content_loaded = False
            for selector in selectors_to_wait:
                try:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support import expected_conditions as EC
                    
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f"✅ Conteúdo carregado! Encontrado: {selector}")
                    content_loaded = True
                    break
                except:
                    continue
            
            # Se não conseguiu aguardar, continua mesmo assim
            if not content_loaded:
                print("⚠️ Timeout aguardando conteúdo específico, continuando...")
                time.sleep(10)  # Aguarda mais tempo
            
            # Rola a página para baixo para carregar mais conteúdo
            print("📜 Rolando página para carregar todo o conteúdo...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Executa scroll gradual para carregar conteúdo dinâmico
            for i in range(3):
                self.driver.execute_script(f"window.scrollTo(0, {(i+1) * 1000});")
                time.sleep(2)
            
            # Obtém HTML após execução JavaScript
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            print(f"📄 HTML carregado: {len(page_source)} caracteres")
            
            # Procura por ferramentas usando múltiplos seletores
            tools = self._extract_tools_from_soup(soup)
            
            print(f"🔧 Extraídas {len(tools)} ferramentas com JavaScript")
            
        except Exception as e:
            print(f"❌ Erro no scraping com JavaScript: {e}")
        
        return tools
    
    def _scrape_without_javascript(self) -> List[AITool]:
        """Scrape sem JavaScript como fallback, priorizando páginas populares"""
        tools = []
        
        # URLs priorizando páginas populares/famosas primeiro
        priority_urls = [
            f"{self.base_url}/popular",           # Mais populares
            f"{self.base_url}/trending",          # Tendências  
            f"{self.base_url}/featured",          # Destacados
            f"{self.base_url}/top",               # Top rated
            f"{self.base_url}/best",              # Melhores
            f"{self.base_url}/most-used",         # Mais usados
            f"{self.base_url}/directory",         # Diretório
            f"{self.base_url}",                   # Página principal
            f"{self.base_url}/tools",             # Ferramentas
            f"{self.base_url}/ai-tools"           # AI Tools
        ]
        
        for url in priority_urls:
            try:
                print(f"🔍 Tentando URL prioritária: {url}")
                response = self.get_page(url)
                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    url_tools = self._extract_tools_from_soup(soup)
                    if url_tools:
                        tools.extend(url_tools)
                        print(f"✅ {url}: {len(url_tools)} ferramentas encontradas")
                        break  # Para no primeiro que encontrar ferramentas
                else:
                    print(f"❌ {url}: Não acessível")
            except Exception as e:
                print(f"❌ Erro em {url}: {e}")
                continue
        
        # Se ainda não conseguiu, tenta URLs individuais do sitemap
        if not tools:
            print("🗺️ Tentando sitemap como último recurso...")
            tools = self._scrape_individual_tools()
        
        return tools
    
    def _extract_tools_from_soup(self, soup: BeautifulSoup) -> List[AITool]:
        """Extrai ferramentas do BeautifulSoup"""
        tools = []
        
        # Múltiplos seletores para diferentes estruturas
        selectors = [
            # Seletores específicos
            '.tool-card',
            '.ai-tool',
            '.tool-item',
            '.directory-item',
            
            # Seletores genéricos
            'div[class*="tool"]',
            'div[class*="card"]',
            'div[class*="item"]',
            'article',
            
            # Seletores por atributos
            '[data-tool]',
            '[data-id]',
            
            # Links que podem ser ferramentas
            'a[href*="/tool/"]',
            'a[href*="/ai/"]'
        ]
        
        found_elements = []
        for selector in selectors:
            elements = soup.select(selector)
            if elements and len(elements) > 5:  # Só considera se encontrou vários elementos
                print(f"   📍 Seletor '{selector}': {len(elements)} elementos")
                found_elements = elements
                break
        
        # Se não encontrou elementos estruturados, busca por qualquer link
        if not found_elements:
            print("   🔍 Buscando por links potenciais...")
            all_links = soup.select('a[href]')
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                # Filtra links que podem ser ferramentas
                if (href and text and len(text) > 2 and len(text) < 100 and
                    not any(skip in href.lower() for skip in ['login', 'register', 'about', 'contact', 'privacy', 'terms', 'blog'])):
                    found_elements.append(link)
            
            found_elements = found_elements[:100]  # Limita
            print(f"   📍 Links potenciais: {len(found_elements)}")
        
        # Processa elementos encontrados
        for i, element in enumerate(found_elements):
            try:
                tool = self._parse_tool_element(element, i)
                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                    tools.append(tool)
            except Exception as e:
                continue
        
        return tools
    
    def _parse_tool_element(self, element, index: int) -> Optional[AITool]:
        """Extrai dados de uma ferramenta do elemento HTML"""
        
        # Nome da ferramenta
        name = ""
        
        # Estratégias para extrair nome
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
        
        # Se é um link, pode ser que o nome esteja no texto
        if not name and element.name == 'a':
            name = element.get_text().strip()
        
        # Limpa o nome
        if name:
            name = re.sub(r'\s+', ' ', name.strip())[:100]
        
        if not name or len(name) < 2:
            name = f"AITools Tool {index}"
        
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
        
        # Limpa a descrição
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
        
        # Torna URL absoluta
        if href and href.startswith('/'):
            href = self.base_url + href
        
        # Categorias - busca por tags
        categories = []
        tag_selectors = ['.tag', '.category', '[class*="tag"]', '[class*="category"]']
        
        for selector in tag_selectors:
            tags = element.select(selector)
            for tag in tags:
                tag_text = tag.get_text().strip()
                if tag_text and len(tag_text) < 30:
                    categories.append(tag_text)
        
        # Infere categorias do texto se não tem
        if not categories:
            categories = self._infer_categories_from_text(name + " " + description)
        
        # Remove duplicatas
        categories = list(dict.fromkeys(categories))
        
        # Preço
        price = "Unknown"
        price_text = element.get_text().lower()
        
        if 'free' in price_text:
            price = "Free"
        elif 'paid' in price_text or '$' in price_text:
            price = "Paid"
        
        # Popularidade baseada na posição
        popularity = max(10, 100 - (index * 2))
        
        # ID único
        ext_id = self._generate_ext_id(href, name, index)
        
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
    
    def _scrape_individual_tools(self) -> List[AITool]:
        """Scrape ferramentas individuais do sitemap"""
        tools = []
        
        print("🗺️ Tentando scraping individual via sitemap...")
        
        # URLs conhecidas de ferramentas individuais baseadas na investigação
        individual_urls = [
            "/tool/akool-ai",
            "/tool/pippit-ai", 
            "/tool/chatgpt",
            "/tool/midjourney",
            "/tool/stable-diffusion"
        ]
        
        for url_path in individual_urls[:10]:  # Limita a 10 para teste
            try:
                full_url = self.base_url + url_path
                response = self.get_page(full_url)
                
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extrai dados da página individual
                    name = self._extract_title(soup)
                    description = self._extract_description(soup)
                    
                    if name and len(name) > 2:
                        tool = AITool(
                            ext_id=f"aitoolsdir_{url_path.split('/')[-1]}",
                            name=name,
                            description=description,
                            price="Unknown",
                            popularity=70.0,
                            categories=["ai-tool"],
                            source=self.source_name,
                            macro_domain="OTHER"
                        )
                        tools.append(tool)
                        print(f"   ✅ {name}")
                
                time.sleep(2)  # Pausa entre requisições
                
            except Exception as e:
                continue
        
        return tools
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extrai título da página"""
        title_elem = (
            soup.select_one('h1') or
            soup.select_one('title') or
            soup.select_one('[class*="title"]')
        )
        
        if title_elem:
            return title_elem.get_text().strip()
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extrai descrição da página"""
        desc_elem = (
            soup.select_one('meta[name="description"]') or
            soup.select_one('p') or
            soup.select_one('[class*="desc"]')
        )
        
        if desc_elem:
            if desc_elem.name == 'meta':
                return desc_elem.get('content', '')
            else:
                return desc_elem.get_text().strip()
        
        return ""
    
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
                        return f"aitoolsdir_{clean_part}"
        
        if name:
            clean_name = re.sub(r'[^\w\s]', '', name.lower())
            clean_name = re.sub(r'\s+', '_', clean_name)[:30]
            if clean_name:
                return f"aitoolsdir_{clean_name}"
        
        return f"aitoolsdir_tool_{index}"


def scrape_aitools_directory() -> List[AITool]:
    """Função de conveniência para fazer scraping do AI Tools Directory"""
    scraper = AIToolsDirectoryScraperJS()
    return scraper.scrape()