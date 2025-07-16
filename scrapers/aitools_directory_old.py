"""
Scraper para AI Tools Directory
Endpoint: https://aitoolsdirectory.com/api/tools (ou página HTML se API não estiver disponível)
"""

import json
from bs4 import BeautifulSoup
from typing import List
from .common import BaseScraper, AITool

class AIToolsDirectoryScraper(BaseScraper):
    """Scraper para aitoolsdirectory.com"""
    
    def __init__(self):
        super().__init__("aitoolsdir", "https://aitoolsdirectory.com")
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas via API ou HTML"""
        tools = []
        
        # Tenta primeiro a API
        api_tools = self._try_api_scraping()
        if api_tools:
            return api_tools
        
        # Se API falhar, usa HTML scraping
        return self._try_html_scraping()
    
    def _try_api_scraping(self) -> List[AITool]:
        """Tenta fazer scraping via API JSON"""
        tools = []
        
        try:
            print(f"🔍 Tentando API do AI Tools Directory...")
            
            response = self.get_page(f"{self.base_url}/api/tools")
            if not response:
                print("❌ API não acessível, tentando HTML...")
                return []
            
            data = response.json()
            tools_data = data if isinstance(data, list) else data.get('tools', [])
            
            print(f"📊 API: Encontradas {len(tools_data)} ferramentas")
            
            for tool_data in tools_data:
                try:
                    tool = self._parse_api_tool(tool_data)
                    if tool:
                        tools.append(tool)
                except Exception as e:
                    print(f"❌ Erro ao processar ferramenta da API: {e}")
                    continue
            
            print(f"✅ API: Scraped {len(tools)} ferramentas")
            
        except Exception as e:
            print(f"❌ Erro na API, tentando HTML: {e}")
            return []
        
        return tools
    
    def _try_html_scraping(self) -> List[AITool]:
        """Faz scraping via HTML"""
        tools = []
        
        try:
            print(f"🔍 Fazendo HTML scraping do AI Tools Directory...")
            
            response = self.get_page(self.base_url)
            if not response:
                print(f"❌ Erro ao acessar {self.base_url}")
                return tools
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca por diferentes padrões de cards de ferramentas
            tool_elements = (
                soup.select('[data-testid*="tool"]') or
                soup.select('.tool-card') or 
                soup.select('.ai-tool') or
                soup.select('article') or
                soup.select('.card')
            )
            
            print(f"📊 HTML: Encontrados {len(tool_elements)} elementos")
            
            for i, element in enumerate(tool_elements[:50]):  # Limita a 50
                try:
                    tool = self._parse_html_tool(element, i)
                    if tool:
                        tools.append(tool)
                except Exception as e:
                    print(f"❌ Erro ao processar elemento {i}: {e}")
                    continue
            
            print(f"✅ HTML: Scraped {len(tools)} ferramentas")
            
        except Exception as e:
            print(f"❌ Erro geral no HTML scraping: {e}")
        
        return tools
    
    def _parse_api_tool(self, data: dict) -> AITool:
        """Extrai dados de uma ferramenta da API JSON"""
        
        ext_id = str(data.get('id', '')) or data.get('slug', '')
        name = data.get('name', 'Unknown Tool').strip()
        description = data.get('description', '').strip()
        
        # Preço
        price_info = data.get('price') or data.get('pricing', {})
        if isinstance(price_info, dict):
            price = price_info.get('type', 'Unknown')
        else:
            price = str(price_info) if price_info else 'Unknown'
        
        # Categorias
        categories = []
        for field in ['tags', 'features', 'categories']:
            if field in data and data[field]:
                categories.extend(data[field])
        
        # Popularidade
        popularity = float(data.get('upvotes', 0) or data.get('rating', 0) or 0)
        
        # Classificação de domínio
        macro_domain = self.classify_domain(categories, description)
        
        return AITool(
            ext_id=ext_id,
            name=name,
            description=description,
            price=price,
            popularity=popularity,
            categories=categories,
            source=self.source_name,
            macro_domain=macro_domain
        )
    
    def _parse_html_tool(self, element, index: int) -> AITool:
        """Extrai dados de uma ferramenta do HTML"""
        
        # Nome
        name_elem = (
            element.select_one('h1, h2, h3, h4') or
            element.select_one('[class*="title"]') or
            element.select_one('[class*="name"]')
        )
        name = name_elem.get_text().strip() if name_elem else f"AI Tool {index}"
        
        # Descrição
        desc_elem = (
            element.select_one('p') or
            element.select_one('[class*="desc"]') or
            element.select_one('[class*="summary"]')
        )
        description = desc_elem.get_text().strip() if desc_elem else ""
        
        # Categorias/tags
        tag_elements = element.select('[class*="tag"], [class*="category"], .badge')
        categories = [tag.get_text().strip() for tag in tag_elements if tag.get_text().strip()]
        
        # Se não tem categorias, infere do texto
        if not categories and description:
            text_lower = description.lower()
            if any(word in text_lower for word in ['chat', 'conversation', 'text']):
                categories = ['chatbot', 'nlp']
            elif any(word in text_lower for word in ['image', 'photo', 'visual']):
                categories = ['image', 'computer vision']
            else:
                categories = ['ai', 'general']
        
        # Preço
        price_elem = element.select_one('[class*="price"], [class*="free"], [class*="paid"]')
        price_text = price_elem.get_text().strip() if price_elem else ""
        if "free" in price_text.lower():
            price = "Free"
        elif "$" in price_text or "paid" in price_text.lower():
            price = "Paid"
        else:
            price = "Unknown"
        
        # Popularidade baseada na posição
        popularity = max(0, 100 - index)
        
        # ID único
        ext_id = name.lower().replace(' ', '_').replace('-', '_')[:50]
        if not ext_id:
            ext_id = f"tool_{index}"
        
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

def scrape_aitools_directory() -> List[AITool]:
    """Função de conveniência"""
    scraper = AIToolsDirectoryScraper()
    return scraper.scrape()