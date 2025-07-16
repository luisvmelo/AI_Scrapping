#!/usr/bin/env python3
"""
Debug pricing extraction para entender a estrutura HTML
"""

def debug_futurepedia_pricing():
    """Debug da estrutura de preços do Futurepedia"""
    print("🔍 DEBUG: Estrutura de preços do Futurepedia")
    print("="*50)
    
    try:
        from scrapers.futurepedia import FuturepediaScraper
        from bs4 import BeautifulSoup
        
        scraper = FuturepediaScraper()
        response = scraper.get_page("https://www.futurepedia.io/ai-tools/business")
        
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pega o primeiro link de ferramenta
            tool_links = soup.select('a[href*="/tool/"]')[:2]
            
            for i, link in enumerate(tool_links):
                print(f"\n🛠️ FERRAMENTA {i+1}:")
                print(f"Link href: {link.get('href', 'N/A')}")
                
                # Mostra o elemento pai
                parent = link.parent
                if parent:
                    print(f"\nTexto completo do elemento pai:")
                    parent_text = parent.get_text()
                    print(f"'{parent_text[:200]}...'")
                    
                    # Busca por elementos com classes relacionadas a preço
                    price_related = parent.select('[class*="price"], [class*="cost"], [class*="plan"], .badge, .tag')
                    if price_related:
                        print(f"\nElementos relacionados a preço encontrados:")
                        for elem in price_related:
                            print(f"  - Classe: {elem.get('class')}")
                            print(f"    Texto: '{elem.get_text().strip()}'")
                    
                    # Busca por texto que contenha símbolos de moeda
                    import re
                    dollar_matches = re.findall(r'\$[\d,.]+ ?/?[a-zA-Z]*', parent_text)
                    if dollar_matches:
                        print(f"\nPadrões de $ encontrados: {dollar_matches}")
                    
                    free_matches = re.findall(r'\b(free|paid|premium|trial|freemium)\b', parent_text.lower())
                    if free_matches:
                        print(f"Palavras de preço encontradas: {free_matches}")
                
                print("-" * 40)
        
        else:
            print("❌ Não foi possível acessar o Futurepedia")
    
    except Exception as e:
        print(f"❌ Erro no debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_futurepedia_pricing()