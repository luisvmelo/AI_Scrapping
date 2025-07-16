#!/usr/bin/env python3
"""
Teste rápido dos scrapers
"""

import sys
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    def handler(signum, frame):
        raise TimeoutError(f"Timeout after {seconds} seconds")
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def test_futurepedia():
    print("🧪 Testando Futurepedia...")
    try:
        with timeout(30):  # 30 seconds max
            from scrapers.futurepedia import scrape_futurepedia
            tools = scrape_futurepedia()
            print(f"✅ Futurepedia: {len(tools)} ferramentas")
            return len(tools)
    except TimeoutError:
        print("⏰ Futurepedia: Timeout (30s)")
        return -1
    except Exception as e:
        print(f"❌ Futurepedia: {e}")
        return 0

def test_phygital():
    print("🧪 Testando Phygital Library...")
    try:
        with timeout(20):  # 20 seconds max
            from scrapers.phygital_library import scrape_phygital_library
            tools = scrape_phygital_library()
            print(f"✅ Phygital Library: {len(tools)} ferramentas")
            return len(tools)
    except TimeoutError:
        print("⏰ Phygital Library: Timeout (20s)")
        return -1
    except Exception as e:
        print(f"❌ Phygital Library: {e}")
        return 0

def main():
    print("🚀 TESTE RÁPIDO DOS SCRAPERS")
    
    # Teste apenas os dois principais
    futurepedia_count = test_futurepedia()
    phygital_count = test_phygital()
    
    print(f"\n📊 RESULTADO:")
    print(f"Futurepedia: {futurepedia_count if futurepedia_count >= 0 else 'TIMEOUT'}")
    print(f"Phygital: {phygital_count if phygital_count >= 0 else 'TIMEOUT'}")
    
    working = sum(1 for count in [futurepedia_count, phygital_count] if count > 0)
    print(f"Scrapers funcionando: {working}/2")

if __name__ == "__main__":
    main()