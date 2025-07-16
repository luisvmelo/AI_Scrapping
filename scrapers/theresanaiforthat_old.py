"""
Scraper para There's An AI For That
URL: https://theresanaiforthat.com
"""

import json
from bs4 import BeautifulSoup
from typing import List
from .common import BaseScraper, AITool

class TheresAnAIForThatScraper(BaseScraper):
    """Scraper para theresanaiforthat.com"""
    
    def __init__(self):
        super().__init__("theresanaiforthat", "https://theresanaiforthat.com")
    
    def scrape(self) -> List[AITool]:
        """Scrape das ferramentas de AI"""
        tools = []
        
        # Tenta primeiro buscar na página principal
        main_tools = self._scrape_main_page()
        if main_tools:
            tools.extend(main_tools)
        
        # Tenta buscar em categorias específicas
        category_tools = self._scrape_categories()
        tools.extend(category_tools)
        
        return tools
    
    def _scrape_main_page(self) -> List[AITool]:
        """Scrape da página principal"""
        tools = []
        
        try:
            print(f"🔍 Fazendo scraping da página principal: {self.base_url}")
            
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
                soup.select('.card') or
                soup.select('[class*="item"]') or
                soup.select('[id*="tool"]')
            )
            
            print(f"📊 Encontrados {len(tool_elements)} elementos na página principal")
            
            for i, element in enumerate(tool_elements[:30]):  # Limita a 30
                try:
                    tool = self._parse_tool_element(element, i)
                    if tool and tool.name != "Unknown Tool":
                        tools.append(tool)
                except Exception as e:
                    print(f"❌ Erro ao processar elemento {i}: {e}")
                    continue
            
            print(f"✅ Página principal: Scraped {len(tools)} ferramentas")
            
        except Exception as e:
            print(f"❌ Erro geral no scraping da página principal: {e}")
        
        return tools
    
    def _scrape_categories(self) -> List[AITool]:
        """Scrape de páginas de categorias específicas"""
        tools = []
        
        # Categorias populares do site
        categories = [
            "writing",
            "image-generation", 
            "chatbots",
            "code",
            "productivity",
            "video",
            "audio",
            "design"
        ]
        
        for category in categories:
            try:
                category_url = f"{self.base_url}/category/{category}"
                print(f"🔍 Scraping categoria: {category}")
                
                response = self.get_page(category_url)
                if not response:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Busca por elementos de ferramentas na categoria
                tool_elements = (
                    soup.select('[data-testid*="tool"]') or
                    soup.select('.tool-card') or 
                    soup.select('.ai-tool') or
                    soup.select('article') or
                    soup.select('.card') or
                    soup.select('[class*="item"]')
                )
                
                category_tools = []
                for i, element in enumerate(tool_elements[:20]):  # Limita a 20 por categoria
                    try:
                        tool = self._parse_tool_element(element, i, category)
                        if tool and tool.name != "Unknown Tool":
                            category_tools.append(tool)
                    except Exception as e:
                        continue
                
                tools.extend(category_tools)
                print(f"✅ Categoria {category}: {len(category_tools)} ferramentas")
                
            except Exception as e:
                print(f"❌ Erro na categoria {category}: {e}")
                continue
        
        return tools
    
    def _parse_tool_element(self, element, index: int, category: str = "") -> AITool:
        """Extrai dados de uma ferramenta do HTML"""
        
        # Nome da ferramenta
        name_elem = (
            element.select_one('h1, h2, h3, h4, h5') or
            element.select_one('[class*="title"]') or
            element.select_one('[class*="name"]') or
            element.select_one('a') or
            element.select_one('strong')
        )
        
        if name_elem:
            name = name_elem.get_text().strip()
            # Remove caracteres especiais e limita tamanho
            name = name.replace('\n', ' ').replace('\t', ' ')
            name = ' '.join(name.split())[:100]
        else:
            name = f"AI Tool {index}"
        
        # Descrição
        desc_elem = (
            element.select_one('p') or
            element.select_one('[class*="desc"]') or
            element.select_one('[class*="summary"]') or
            element.select_one('[class*="text"]')
        )
        
        if desc_elem:
            description = desc_elem.get_text().strip()
            description = description.replace('\n', ' ').replace('\t', ' ')
            description = ' '.join(description.split())[:500]
        else:
            description = ""
        
        # Categorias/tags
        tag_elements = element.select(
            '[class*="tag"], [class*="category"], .badge, [class*="label"]'
        )
        categories = [tag.get_text().strip() for tag in tag_elements if tag.get_text().strip()]
        
        # Adiciona categoria da URL se disponível
        if category:
            categories.append(category)
        
        # Se não tem categorias, infere do texto
        if not categories:
            categories = self._infer_categories_from_text(name + " " + description)
        
        # Preço - busca por indicadores comuns
        price_elem = element.select_one(
            '[class*="price"], [class*="free"], [class*="paid"], [class*="cost"]'
        )
        
        price = "Unknown"
        if price_elem:
            price_text = price_elem.get_text().strip().lower()
            if "free" in price_text:
                price = "Free"
            elif any(word in price_text for word in ["$", "paid", "premium", "pro"]):
                price = "Paid"
            elif "freemium" in price_text:
                price = "Freemium"
        else:
            # Busca por texto de preço no conteúdo geral
            full_text = element.get_text().lower()
            if "free" in full_text and "trial" not in full_text:
                price = "Free"
            elif any(word in full_text for word in ["$", "paid", "premium"]):
                price = "Paid"
        
        # Popularidade baseada na posição (páginas principais têm prioridade)
        base_popularity = 100 - (index * 2)
        if category:  # Se veio de categoria específica, menor prioridade
            base_popularity = max(10, base_popularity - 20)
        
        popularity = max(0, base_popularity)
        
        # ID único baseado no nome
        ext_id = self._generate_ext_id(name, index)
        
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
            "writing": ["write", "writing", "text", "content", "blog", "article"],
            "chatbot": ["chat", "conversation", "bot", "assistant", "talk"],
            "image": ["image", "photo", "picture", "visual", "graphic"],
            "video": ["video", "film", "movie", "clip"],
            "audio": ["audio", "music", "sound", "voice", "podcast"],
            "code": ["code", "programming", "developer", "api"],
            "design": ["design", "ui", "ux", "creative"],
            "productivity": ["productivity", "organize", "task", "management"],
            "analytics": ["analytics", "data", "analysis", "insight"],
            "marketing": ["marketing", "seo", "social", "campaign"]
        }
        
        for category, keywords in keyword_map.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        # Se não encontrou nenhuma categoria, adiciona 'ai' como padrão
        if not categories:
            categories = ["ai", "general"]
        
        return categories
    
    def _generate_ext_id(self, name: str, index: int) -> str:
        """Gera um ID único para a ferramenta"""
        # Remove caracteres especiais e converte para snake_case
        clean_name = ''.join(c.lower() if c.isalnum() else '_' for c in name)
        clean_name = '_'.join(filter(None, clean_name.split('_')))
        
        # Limita o tamanho
        if len(clean_name) > 30:
            clean_name = clean_name[:30]
        
        # Se ficou vazio, usa um ID genérico
        if not clean_name:
            clean_name = f"tool_{index}"
        
        return f"taift_{clean_name}"


def scrape_theresanaiforthat() -> List[AITool]:
    """Função de conveniência para fazer scraping do There's An AI For That"""
    scraper = TheresAnAIForThatScraper()
    return scraper.scrape()