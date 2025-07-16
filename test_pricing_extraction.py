#!/usr/bin/env python3
"""
Teste específico para verificar a extração de preços dos scrapers
Testa apenas 1-2 ferramentas de cada scraper para verificar se o pricing funciona
"""

def test_pricing_extraction():
    """Testa a extração de preços de forma rápida"""
    print("🔍 TESTE DE EXTRAÇÃO DE PREÇOS")
    print("="*50)
    
    try:
        # Testa apenas o Futurepedia (mais rápido e confiável)
        print("\n📊 Testando Futurepedia (amostra pequena)...")
        from scrapers.futurepedia import FuturepediaScraper
        
        scraper = FuturepediaScraper()
        
        # Testa apenas uma página pequena
        response = scraper.get_page("https://www.futurepedia.io/ai-tools/business")
        if response:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pega apenas os primeiros 3 links para teste rápido
            tool_links = soup.select('a[href*="/tool/"]')[:3]
            
            pricing_examples = []
            for i, link in enumerate(tool_links):
                try:
                    tool = scraper._parse_tool_card(link, i, "business")
                    if tool:
                        pricing_examples.append({
                            'name': tool.name,
                            'price': tool.price,
                            'description': tool.description[:60] + "..."
                        })
                except:
                    continue
            
            print(f"✅ Futurepedia: {len(pricing_examples)} ferramentas testadas")
            for example in pricing_examples:
                print(f"   • {example['name']} - Preço: {example['price']}")
                print(f"     {example['description']}")
            
            # Verifica se conseguiu extrair preços específicos
            specific_prices = [ex for ex in pricing_examples if ex['price'] not in ['Unknown', 'Paid', 'Free']]
            print(f"\n💰 Preços específicos extraídos: {len(specific_prices)}/{len(pricing_examples)}")
            
            if specific_prices:
                print("✅ Extração de preços funcionando!")
                for sp in specific_prices:
                    print(f"   🎯 {sp['name']}: {sp['price']}")
            else:
                print("⚠️ Apenas preços genéricos extraídos")
        
        else:
            print("❌ Não foi possível acessar o Futurepedia")
    
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    test_pricing_extraction()