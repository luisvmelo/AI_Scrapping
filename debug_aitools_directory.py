#!/usr/bin/env python3
"""
Debug AITools Directory para entender a estrutura do site
"""

import requests
from bs4 import BeautifulSoup

def debug_aitools_directory():
    """Debug da estrutura do AITools Directory"""
    print("🔍 DEBUG: AITools Directory Structure")
    print("="*50)
    
    try:
        # Testa acesso direto ao site
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get("https://aitoolsdirectory.com", headers=headers, timeout=15)
        print(f"Status: {response.status_code}")
        print(f"HTML Length: {len(response.text)} characters")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica se é uma SPA ou tem conteúdo estático
            print(f"\n📄 Título da página: {soup.title.get_text() if soup.title else 'N/A'}")
            
            # Busca por diferentes padrões de elementos
            patterns_to_check = [
                ('Links com "tool"', 'a[href*="tool"]'),
                ('Links com "ai"', 'a[href*="ai"]'),
                ('Divs com "tool"', 'div[class*="tool"]'),
                ('Divs com "card"', 'div[class*="card"]'),
                ('Articles', 'article'),
                ('Scripts', 'script'),
                ('Divs com id', 'div[id]'),
                ('Divs com data-*', 'div[data-*]')
            ]
            
            for name, selector in patterns_to_check:
                elements = soup.select(selector)
                print(f"   {name}: {len(elements)} encontrados")
                
                if elements and len(elements) > 0:
                    # Mostra exemplo
                    first_elem = elements[0]
                    if name.startswith('Links'):
                        print(f"     Exemplo: href='{first_elem.get('href', 'N/A')}' text='{first_elem.get_text()[:30]}...'")
                    elif name == 'Scripts':
                        src = first_elem.get('src', '')
                        print(f"     Exemplo: src='{src}' {'(inline)' if not src else ''}")
                    else:
                        class_name = first_elem.get('class', [])
                        print(f"     Exemplo: class='{class_name}' text='{first_elem.get_text()[:30]}...'")
            
            # Verifica se tem indicações de SPA
            scripts = soup.select('script')
            spa_indicators = ['react', 'vue', 'angular', 'spa', 'app.js', 'bundle']
            
            spa_found = False
            for script in scripts:
                script_text = script.get_text().lower()
                script_src = script.get('src', '').lower()
                
                for indicator in spa_indicators:
                    if indicator in script_text or indicator in script_src:
                        print(f"   🔍 SPA indicador encontrado: {indicator} em script")
                        spa_found = True
                        break
            
            if spa_found:
                print("   ⚠️ Site parece ser uma SPA - JavaScript necessário")
            else:
                print("   ✅ Site parece ter conteúdo estático")
            
            # Verifica HTML bruto por padrões
            html_lower = response.text.lower()
            if 'loading' in html_lower and 'spinner' in html_lower:
                print("   ⚠️ Indicadores de carregamento dinâmico encontrados")
        
        else:
            print(f"❌ Erro de acesso: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Erro no debug: {e}")

if __name__ == "__main__":
    debug_aitools_directory()