#!/usr/bin/env python3
"""
Teste dos scrapers sem conectar ao Supabase
"""

from scrapers.futurepedia import scrape_futurepedia
from scrapers.phygital_library import scrape_phygital_library
from scrapers.theresanaiforthat import scrape_theresanaiforthat
from scrapers.aitools_directory import scrape_aitools_directory

def test_scraper(scraper_name, scraper_func):
    """Testa um scraper específico"""
    print(f"\n{'='*50}")
    print(f"🧪 TESTANDO SCRAPER: {scraper_name.upper()}")
    print(f"{'='*50}")
    
    try:
        tools = scraper_func()
        
        print(f"✅ Scraper {scraper_name} funcionou!")
        print(f"📊 Coletou {len(tools)} ferramentas")
        
        # Mostra primeiras 3 ferramentas como exemplo
        for i, tool in enumerate(tools[:3]):
            print(f"\n🔧 Ferramenta {i+1}:")
            print(f"   Nome: {tool.name}")
            print(f"   Descrição: {tool.description[:100]}{'...' if len(tool.description) > 100 else ''}")
            print(f"   Preço: {tool.price}")
            print(f"   Popularidade: {tool.popularity}")
            print(f"   Categorias: {', '.join(tool.categories[:3])}")
            print(f"   Domínio: {tool.macro_domain}")
        
        if len(tools) > 3:
            print(f"\n   ... e mais {len(tools) - 3} ferramentas")
            
        return True, len(tools)
        
    except Exception as e:
        print(f"❌ Scraper {scraper_name} falhou: {e}")
        return False, 0

def main():
    """Testa todos os scrapers"""
    print("🚀 TESTE DE FUNCIONALIDADE DOS SCRAPERS")
    print("(Apenas scraping, sem conectar ao Supabase)")
    
    scrapers = [
        ("futurepedia", scrape_futurepedia),
        ("phygital_library", scrape_phygital_library),
        ("theresanaiforthat", scrape_theresanaiforthat),
        ("aitools_directory", scrape_aitools_directory)
    ]
    
    results = {}
    total_tools = 0
    
    for name, func in scrapers:
        success, count = test_scraper(name, func)
        results[name] = {
            'success': success,
            'count': count
        }
        total_tools += count
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📋 RESUMO DOS TESTES")
    print(f"{'='*60}")
    
    working_scrapers = 0
    for name, result in results.items():
        status = "✅ FUNCIONANDO" if result['success'] else "❌ FALHA"
        print(f"{name:20} {status:15} {result['count']:3} ferramentas")
        if result['success']:
            working_scrapers += 1
    
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"   Scrapers funcionando: {working_scrapers}/4 ({(working_scrapers/4)*100:.0f}%)")
    print(f"   Total de ferramentas: {total_tools}")
    print(f"   Média por scraper: {total_tools/4:.1f}")
    
    if working_scrapers > 0:
        print(f"\n✅ Sistema {(working_scrapers/4)*100:.0f}% funcional")
    else:
        print(f"\n❌ Sistema não funcional")

if __name__ == "__main__":
    main()