"""
Scraper para Futurepedia
URL: https://www.futurepedia.io
"""

import json
import re
import time
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from .common import BaseScraper, AITool

class FuturepediaScraper(BaseScraper):
    """Scraper para futurepedia.io"""
    
    def __init__(self):
        super().__init__("futurepedia", "https://www.futurepedia.io")
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas de AI"""
        tools = []
        
        # Tenta primeiro a página de ferramentas
        tools_page = self._scrape_tools_page()
        if tools_page:
            tools.extend(tools_page)
        
        # Tenta buscar em categorias específicas
        category_tools = self._scrape_categories()
        tools.extend(category_tools)
        
        return tools
    
    def _scrape_tools_page(self) -> List[AITool]:
        """Scrape da página principal de ferramentas"""
        tools = []
        
        try:
            tools_url = f"{self.base_url}/ai-tools"
            print(f"🔍 Fazendo scraping da página de ferramentas: {tools_url}")
            
            response = self.get_page(tools_url)
            if not response:
                print(f"❌ Erro ao acessar página de ferramentas")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca por links de ferramentas (padrão: /tool/{slug})
            tool_links = soup.select('a[href*="/tool/"]')
            
            print(f"📊 Encontrados {len(tool_links)} links de ferramentas na página principal")
            
            # Processa TODOS os links únicos para evitar duplicatas
            seen_tools = set()
            for i, link in enumerate(tool_links):  # SEM LIMITE - processa todos
                try:
                    href = link.get('href', '')
                    if href in seen_tools:
                        continue
                    seen_tools.add(href)
                    
                    tool = self._parse_tool_card(link, i)
                    if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                        tools.append(tool)
                except Exception as e:
                    print(f"❌ Erro ao processar link {i}: {e}")
                    continue
            
            print(f"✅ Página principal: Scraped {len(tools)} ferramentas")
            
        except Exception as e:
            print(f"❌ Erro geral no scraping da página principal: {e}")
        
        return tools
    
    def _scrape_categories(self) -> List[AITool]:
        """Scrape de páginas de categorias específicas com paginação"""
        tools = []
        
        # Todas as 10 categorias do Futurepedia - SCRAPE TODAS AS PÁGINAS (sem limites)
        categories = [
            ("business", 1517),      # AI Business Tools - ~30 páginas
            ("productivity", 605),   # AI Productivity Tools - ~12 páginas
            ("misc", 590),           # Misc AI Tools - ~12 páginas
            ("automation", 451),     # Automation Tools - ~9 páginas
            ("text", 302),           # AI Text Generators - ~6 páginas
            ("image", 298),          # AI Image Tools - ~6 páginas
            ("code", 187),           # AI Code Tools - ~4 páginas
            ("video", 169),          # AI Video Tools - ~3 páginas
            ("audio", 142),          # AI Audio Generators - ~3 páginas
            ("art", 117)             # AI Art Generators - ~2 páginas
        ]
        
        global_seen_tools = set()  # Evita duplicatas entre categorias
        
        for category, total_tools in categories:
            try:
                print(f"🔍 Scraping categoria: {category} ({total_tools} ferramentas, TODAS as páginas)")
                category_tools = []
                
                # Scrape TODAS as páginas da categoria (sem limite)
                page = 1
                while True:
                    try:
                        # URL com paginação
                        if page == 1:
                            category_url = f"{self.base_url}/ai-tools/{category}"
                        else:
                            category_url = f"{self.base_url}/ai-tools/{category}?page={page}"
                        
                        print(f"   📄 Página {page}: {category_url}")
                        
                        response = self.get_page(category_url)
                        if not response:
                            print(f"   ❌ Erro ao acessar página {page} da categoria {category}")
                            break
                        
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Busca por links de ferramentas (padrão: /tool/{slug})
                        tool_links = soup.select('a[href*="/tool/"]')
                        
                        if not tool_links:
                            print(f"   ⚠️ Nenhuma ferramenta encontrada na página {page} - FIM da categoria")
                            break
                        
                        print(f"   📊 Encontrados {len(tool_links)} links na página {page}")
                        
                        page_tools = []
                        for i, link in enumerate(tool_links):
                            try:
                                href = link.get('href', '')
                                if href in global_seen_tools:
                                    continue
                                global_seen_tools.add(href)
                                
                                tool = self._parse_tool_card(link, len(category_tools) + i, category)
                                if tool and tool.name != "Unknown Tool" and len(tool.name) > 2:
                                    page_tools.append(tool)
                            except Exception as e:
                                continue
                        
                        category_tools.extend(page_tools)
                        print(f"   ✅ Página {page}: {len(page_tools)} ferramentas extraídas")
                        
                        # Incrementa página e pausa entre páginas
                        page += 1
                        time.sleep(2)
                            
                    except Exception as e:
                        print(f"   ❌ Erro na página {page} da categoria {category}: {e}")
                        page += 1  # Incrementa mesmo em caso de erro
                        if page > 50:  # Limite de segurança para evitar loop infinito
                            print(f"   🛑 Limite de segurança atingido (50 páginas) para categoria {category}")
                            break
                        continue
                
                tools.extend(category_tools)
                print(f"✅ Categoria {category}: {len(category_tools)} ferramentas totais")
                
                # Pausa entre categorias
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ Erro na categoria {category}: {e}")
                continue
        
        return tools
    
    def _parse_tool_card(self, link_element, index: int, category: str = "") -> AITool:
        """Extrai dados de uma ferramenta do card link do Futurepedia"""
        
        # URL da ferramenta
        href = link_element.get('href', '')
        if not ('/tool/' in href):
            return None
        
        # Torna URL absoluta se necessário
        if href.startswith('/'):
            tool_url = self.base_url + href
        else:
            tool_url = href
        
        # Nome da ferramenta - busca no elemento pai e nos elementos próximos
        name = ""
        
        # Primeiro, tenta encontrar o nome no elemento pai
        parent_element = link_element.parent
        if parent_element:
            # Busca por headings no pai
            name_elem = (
                parent_element.select_one('h1, h2, h3, h4, h5, h6') or
                parent_element.select_one('[class*="title"]') or
                parent_element.select_one('[class*="name"]')
            )
            
            if name_elem:
                name = name_elem.get_text().strip()
            else:
                # Se não achou heading, extrai o nome do texto do pai
                parent_text = parent_element.get_text().strip()
                if parent_text:
                    # O nome geralmente é a primeira palavra/frase antes de "Rated"
                    lines = parent_text.split('Rated')[0].strip()
                    name = lines.split('\n')[0].strip()
        
        # Se ainda não encontrou, tenta o img alt text
        if not name:
            img_elem = link_element.select_one('img')
            if img_elem and img_elem.get('alt'):
                alt_text = img_elem.get('alt')
                # Remove " logo" do final se estiver presente
                name = alt_text.replace(' logo', '').strip()
        
        # Limpa e valida o nome
        if name:
            name = name.replace('\n', ' ').replace('\t', ' ')
            name = ' '.join(name.split())[:100]
        
        if not name or len(name) < 2:
            name = f"Futurepedia Tool {index}"
        
        # Descrição - busca no elemento pai e elementos próximos
        description = ""
        
        # Tenta encontrar descrição no elemento pai ou elementos irmãos
        if parent_element:
            desc_elem = (
                parent_element.select_one('p') or
                parent_element.select_one('[class*="desc"]') or
                parent_element.select_one('[class*="summary"]') or
                parent_element.select_one('div[class*="text"]')
            )
            
            if desc_elem:
                description = desc_elem.get_text().strip()
        
        # Se não encontrou, procura no próximo elemento irmão do pai
        if not description and parent_element and parent_element.next_sibling:
            sibling = parent_element.next_sibling
            if hasattr(sibling, 'select_one'):
                desc_elem = (
                    sibling.select_one('p') or
                    sibling.select_one('[class*="desc"]') or
                    sibling.select_one('[class*="summary"]')
                )
                if desc_elem:
                    description = desc_elem.get_text().strip()
        
        # Limpa a descrição
        if description:
            description = description.replace('\n', ' ').replace('\t', ' ')
            description = ' '.join(description.split())[:500]
        
        # Busca por rating (padrão: "Rated X.X out of 5")
        rating_text = ""
        if parent_element:
            rating_text = parent_element.get_text().lower()
        else:
            rating_text = link_element.get_text().lower()
            
        popularity = 50  # valor padrão
        
        if 'rated' in rating_text and 'out of 5' in rating_text:
            try:
                # Extrai o rating do texto
                rating_match = re.search(r'rated\s+(\d+\.?\d*)\s+out\s+of\s+5', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
                    popularity = (rating / 5) * 100  # Converte para escala 0-100
            except:
                pass
        
        # Busca por informações de preço MELHORADAS
        if parent_element:
            price_text = parent_element.get_text().lower()
        else:
            price_text = link_element.get_text().lower()
            
        price = "Unknown"
        
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
        
        # Busca por tags de categoria (podem estar em spans ou divs com # prefix)
        categories = []
        
        # Busca tags no elemento pai também
        search_elements = [link_element]
        if parent_element:
            search_elements.append(parent_element)
        
        for search_elem in search_elements:
            tag_elements = search_elem.select('span, div')
            for tag_elem in tag_elements:
                tag_text = tag_elem.get_text().strip()
                if tag_text.startswith('#'):
                    # Remove o # e adiciona à lista
                    clean_tag = tag_text[1:].strip()
                    if clean_tag and clean_tag not in categories:
                        categories.append(clean_tag)
        
        # Adiciona categoria da URL se disponível
        if category:
            categories.append(category)
        
        # Se não tem categorias, infere do texto
        if not categories:
            categories = self._infer_categories_from_text(name + " " + description)
        
        # Ajusta popularidade baseada na posição
        position_bonus = max(0, 20 - index)
        popularity = min(100, popularity + position_bonus)
        
        # ID único baseado na URL da ferramenta
        tool_slug = href.split('/tool/')[-1]  # Funciona para URLs completas e relativas
        ext_id = f"fp_{tool_slug}"
        
        # Extrai informações adicionais
        # Logo URL
        logo_url = self.extract_logo_url(parent_element or link_element, tool_url)
        
        # Platform info
        platform = self.extract_platform_info(parent_element or link_element, description)
        
        # Features
        features = self.extract_features(parent_element or link_element, description)
        
        # Rank baseado na posição na página (ferramentas no topo são mais relevantes)
        rank = index + 1
        
        # Upvotes - tenta extrair de elementos de rating/votes
        upvotes = None
        upvotes_patterns = [r'(\d+)\s*(?:votes?|upvotes?)', r'(\d+)\s*👍', r'(\d+)\s*likes?']
        element_text = (parent_element.get_text() if parent_element else link_element.get_text())
        upvotes = self.extract_numeric_value(element_text, upvotes_patterns)
        
        # Monthly users - busca por padrões de usuários
        monthly_users = None
        users_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:monthly\s+)?users?',
            r'(\d+(?:,\d+)*)\s*people\s+use',
            r'(\d+(?:,\d+)*)\s*active\s+users?'
        ]
        monthly_users = self.extract_numeric_value(element_text, users_patterns)
        
        # Editor score baseado no rating do Futurepedia
        editor_score = None
        if popularity and popularity > 0:
            # Converte popularidade (0-100) para score (0-10)
            editor_score = round(popularity / 10, 1)
        
        # Maturity - infere do texto
        maturity = None
        maturity_text = element_text.lower()
        if 'beta' in maturity_text:
            maturity = 'beta'
        elif 'alpha' in maturity_text:
            maturity = 'alpha'
        elif any(term in maturity_text for term in ['stable', 'production', 'ga', 'v1', 'version 1']):
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
        
        # Mapeamento de palavras-chave para categorias específicas do Futurepedia
        keyword_map = {
            "writing": ["write", "writing", "text", "content", "copywriting", "blog", "article", "essay"],
            "chatbot": ["chat", "conversation", "bot", "assistant", "talk", "dialogue"],
            "image": ["image", "photo", "picture", "visual", "graphic", "art", "generate"],
            "video": ["video", "film", "movie", "clip", "animation"],
            "audio": ["audio", "music", "sound", "voice", "podcast", "speech"],
            "code": ["code", "programming", "developer", "api", "coding", "development"],
            "design": ["design", "ui", "ux", "creative", "prototype"],
            "productivity": ["productivity", "organize", "task", "management", "workflow"],
            "research": ["research", "analysis", "data", "insight", "study"],
            "marketing": ["marketing", "seo", "social", "campaign", "advertising"],
            "education": ["education", "learning", "teach", "course", "training"],
            "business": ["business", "startup", "entrepreneur", "finance", "sales"]
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        # Se não encontrou nenhuma categoria, adiciona categorias padrão
        if not categories:
            categories = ["ai-tool", "general"]
        
        return categories


def scrape_futurepedia() -> List[AITool]:
    """Função de conveniência para fazer scraping do Futurepedia"""
    scraper = FuturepediaScraper()
    return scraper.scrape()