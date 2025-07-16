#!/usr/bin/env python3
"""
Teste do Futurepedia escalado para coletar 5,000+ tools
"""

from scrapers.futurepedia import scrape_futurepedia

def main():
    print("🚀 TESTE DO FUTUREPEDIA ESCALADO")
    print("Coletando todas as ferramentas sem limites...")
    print("Esperando 2,000+ ferramentas das 10 categorias")
    print()
    
    try:
        tools = scrape_futurepedia()
        
        print(f"\n🎯 RESULTADO FINAL:")
        print(f"Total de ferramentas coletadas: {len(tools)}")
        
        # Mostra estatísticas por categoria
        categories = {}
        for tool in tools:
            for cat in tool.categories:
                categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n📊 DISTRIBUIÇÃO POR CATEGORIA:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} ferramentas")
        
        # Mostra primeiras 5 ferramentas como exemplo
        print(f"\n🔧 PRIMEIRAS 5 FERRAMENTAS:")
        for i, tool in enumerate(tools[:5]):
            print(f"  {i+1}. {tool.name}")
            print(f"     Descrição: {tool.description[:80]}{'...' if len(tool.description) > 80 else ''}")
            print(f"     Categorias: {', '.join(tool.categories[:3])}")
            print(f"     Preço: {tool.price}")
            print()
        
        if len(tools) >= 2000:
            print("✅ META ATINGIDA: Mais de 2,000 ferramentas coletadas!")
        elif len(tools) >= 1000:
            print("🎯 BOA PERFORMANCE: Mais de 1,000 ferramentas coletadas!")
        elif len(tools) >= 500:
            print("⚠️ PERFORMANCE OK: Mais de 500 ferramentas coletadas")
        else:
            print("❌ PERFORMANCE BAIXA: Menos de 500 ferramentas")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    main()