#!/usr/bin/env python3
"""
Teste dos scrapers melhorados para verificar se estão coletando dados
"""

def test_scraper(scraper_name, scraper_func, expected_min=5):
    """Testa um scraper específico"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTANDO SCRAPER: {scraper_name.upper()}")
    print(f"{'='*60}")
    
    try:
        tools = scraper_func()
        
        success = len(tools) >= expected_min
        status = "✅ SUCESSO" if success else "⚠️ PARCIAL" if len(tools) > 0 else "❌ FALHA"
        
        print(f"{status} - {scraper_name}: {len(tools)} ferramentas coletadas")
        
        if len(tools) > 0:
            # Mostra primeira ferramenta como exemplo
            tool = tools[0]
            print(f"\n📋 EXEMPLO DE FERRAMENTA:")
            print(f"   Nome: {tool.name}")
            print(f"   Descrição: {tool.description[:80]}{'...' if len(tool.description) > 80 else ''}")
            print(f"   Categorias: {', '.join(tool.categories[:3])}")
            print(f"   Fonte: {tool.source}")
            print(f"   Domínio: {tool.macro_domain}")
        
        return success, len(tools)
        
    except Exception as e:
        print(f"❌ ERRO - {scraper_name}: {e}")
        return False, 0

def main():
    """Testa os scrapers melhorados"""
    print("🚀 TESTE DOS SCRAPERS MELHORADOS")
    print("Verificando se as correções funcionaram...")
    print()
    
    # Lista de scrapers para testar
    scrapers_to_test = [
        ("AITools Directory (c/ JavaScript)", "scrapers.aitools_directory", "scrape_aitools_directory", 10),
        ("There's An AI For That (c/ Anti-detecção)", "scrapers.theresanaiforthat", "scrape_theresanaiforthat", 5),
        ("TopAI.tools (Novo)", "scrapers.topai_tools", "scrape_topai_tools", 10),
        ("Toolify (Novo)", "scrapers.toolify", "scrape_toolify", 20)
    ]
    
    results = {}
    total_tools = 0
    working_scrapers = 0
    
    for name, module_name, func_name, expected in scrapers_to_test:
        try:
            # Importa o módulo dinamicamente
            module = __import__(module_name, fromlist=[func_name])
            scraper_func = getattr(module, func_name)
            
            success, count = test_scraper(name, scraper_func, expected)
            
            results[name] = {
                'success': success,
                'count': count,
                'expected': expected
            }
            
            total_tools += count
            if success:
                working_scrapers += 1
                
        except ImportError as e:
            print(f"❌ ERRO DE IMPORT - {name}: {e}")
            results[name] = {'success': False, 'count': 0, 'expected': expected}
        except Exception as e:
            print(f"❌ ERRO GERAL - {name}: {e}")
            results[name] = {'success': False, 'count': 0, 'expected': expected}
    
    # Resumo final
    print(f"\n{'='*80}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*80}")
    
    for name, result in results.items():
        status_icon = "✅" if result['success'] else "⚠️" if result['count'] > 0 else "❌"
        expected = result['expected']
        actual = result['count']
        
        print(f"{status_icon} {name:<50} {actual:>3}/{expected:<3} ferramentas")
    
    print(f"\n🎯 ESTATÍSTICAS FINAIS:")
    print(f"   Scrapers funcionando: {working_scrapers}/{len(scrapers_to_test)} ({(working_scrapers/len(scrapers_to_test))*100:.0f}%)")
    print(f"   Total de ferramentas: {total_tools}")
    print(f"   Média por scraper: {total_tools/len(scrapers_to_test):.1f}")
    
    if working_scrapers >= 3:
        print(f"\n🎉 EXCELENTE! {working_scrapers} scrapers funcionando - Sistema pronto para 5,000+ ferramentas!")
    elif working_scrapers >= 2:
        print(f"\n👍 BOM! {working_scrapers} scrapers funcionando - Sistema parcialmente funcional")
    elif working_scrapers >= 1:
        print(f"\n⚠️ PARCIAL: {working_scrapers} scraper funcionando - Alguns scrapers precisam de ajustes")
    else:
        print(f"\n❌ PROBLEMAS: Nenhum scraper funcionando - Verificar conexão e configurações")

if __name__ == "__main__":
    main()