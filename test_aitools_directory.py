#!/usr/bin/env python3
"""
Teste específico do AITools Directory scraper
"""

def test_aitools_directory():
    """Testa o scraper do AITools Directory"""
    print("🔍 TESTE: AITools Directory Scraper")
    print("="*50)
    
    try:
        from scrapers.aitools_directory import scrape_aitools_directory
        
        print("🚀 Iniciando teste do AITools Directory...")
        tools = scrape_aitools_directory()
        
        if tools and len(tools) > 0:
            print(f"✅ SUCESSO! Coletadas {len(tools)} ferramentas")
            
            # Mostra algumas ferramentas como exemplo
            print(f"\n📋 EXEMPLOS DE FERRAMENTAS:")
            for i, tool in enumerate(tools[:3]):
                print(f"   {i+1}. {tool.name}")
                print(f"      Descrição: {tool.description[:60]}{'...' if len(tool.description) > 60 else ''}")
                print(f"      Categorias: {', '.join(tool.categories[:2])}")
                print(f"      Fonte: {tool.source}")
                print()
            
            return True
        else:
            print("❌ FALHA: Nenhuma ferramenta coletada")
            return False
            
    except ImportError as e:
        print(f"❌ ERRO DE IMPORT: {e}")
        print("   Possível problema: Selenium não instalado ou chromedriver não encontrado")
        return False
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_aitools_directory()
    
    if success:
        print("🎉 AITools Directory scraper está funcionando!")
    else:
        print("⚠️ AITools Directory scraper precisa de ajustes")