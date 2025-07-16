# Teste simples para common.py
import os
import sys

# Adiciona o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🧪 Testando scrapers/common.py")
print(f"Diretório atual: {current_dir}")

try:
    from scrapers.common import AITool, BaseScraper
    print("✅ Import funcionou!")
    
    # Teste básico
    tool = AITool(
        ext_id="test_001",
        name="Test Tool",
        description="A test tool",
        price="Free",
        popularity=100,
        categories=["test"],
        source="test"
    )
    
    print(f"✅ AITool criado: {tool.name}")
    
    # Teste do scraper
    scraper = BaseScraper("test", "https://example.com")
    domain = scraper.classify_domain(["chatbot"], "AI tool")
    print(f"✅ Classificação funcionou: {domain}")
    
    print("🎉 Todos os testes passaram!")
    
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("Verificando estrutura de arquivos...")
    print("Arquivos na pasta:")
    for item in os.listdir("."):
        print(f"  - {item}")
        
except Exception as e:
    print(f"❌ Erro: {e}")