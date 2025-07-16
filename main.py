#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Scraping de Ferramentas de IA
Pipeline completo: Scraping -> Merge -> Synergy
"""

import sys
import argparse
from typing import List

from scrapers.aitools_directory import scrape_aitools_directory
from scrapers.theresanaiforthat import scrape_theresanaiforthat
from scrapers.futurepedia import scrape_futurepedia
from scrapers.phygital_library import scrape_phygital_library
from scrapers.topai_tools import scrape_topai_tools
from scrapers.toolify import scrape_toolify
from merge.merge_and_upsert import merge_tools_to_supabase, get_supabase_statistics, cleanup_supabase_duplicates
from synergy.build_synergy import build_synergies, get_synergy_stats


def run_scraper(scraper_name: str) -> int:
    """Executa um scraper específico"""
    print(f"\n🤖 Executando scraper: {scraper_name}")
    
    scrapers = {
        'aitools_directory': scrape_aitools_directory,
        'theresanaiforthat': scrape_theresanaiforthat,
        'futurepedia': scrape_futurepedia,
        'phygital_library': scrape_phygital_library,
        'topai_tools': scrape_topai_tools,
        'toolify': scrape_toolify
    }
    
    if scraper_name not in scrapers:
        print(f"❌ Scraper '{scraper_name}' não encontrado")
        return 0
    
    try:
        tools = scrapers[scraper_name]()
        print(f"📊 Scraped {len(tools)} ferramentas")
        
        if tools:
            stats = merge_tools_to_supabase(tools)
            print(f"💾 Merge stats: {stats}")
            return len(tools)
        else:
            print("⚠️ Nenhuma ferramenta encontrada")
            return 0
            
    except Exception as e:
        print(f"❌ Erro no scraper {scraper_name}: {e}")
        return 0


def run_all_scrapers() -> int:
    """Executa todos os scrapers"""
    print("\n🚀 Executando todos os scrapers...")
    
    scrapers = ['aitools_directory', 'theresanaiforthat', 'futurepedia', 'phygital_library']
    total_tools = 0
    
    for scraper in scrapers:
        count = run_scraper(scraper)
        total_tools += count
    
    return total_tools


def run_synergy_calculation():
    """Executa cálculo de sinergias"""
    print("\n🔗 Calculando sinergias...")
    try:
        stats = build_synergies()
        print(f"📊 Synergy stats: {stats}")
    except Exception as e:
        print(f"❌ Erro no cálculo de sinergias: {e}")


def show_statistics():
    """Mostra estatísticas do banco"""
    print("\n📊 === ESTATÍSTICAS DO BANCO ===")
    
    try:
        db_stats = get_supabase_statistics()
        print(f"Total de ferramentas: {db_stats.get('total_tools', 0)}")
        
        print("\nPor fonte:")
        for source, count in db_stats.get('by_source', {}).items():
            print(f"  {source}: {count}")
        
        print("\nPor domínio:")
        for domain, count in db_stats.get('by_domain', {}).items():
            print(f"  {domain}: {count}")
        
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
    
    print("\n🔗 === ESTATÍSTICAS DE SINERGIAS ===")
    
    try:
        synergy_stats = get_synergy_stats()
        print(f"Total de sinergias: {synergy_stats.get('total_synergies', 0)}")
        print(f"Score médio: {synergy_stats.get('avg_score', 0)}")
        print(f"Score máximo: {synergy_stats.get('max_score', 0)}")
        
        distribution = synergy_stats.get('distribution', {})
        print(f"\nDistribuição:")
        print(f"  Alta sinergia (≥0.7): {distribution.get('high_synergy', 0)}")
        print(f"  Média sinergia (0.4-0.7): {distribution.get('medium_synergy', 0)}")
        print(f"  Baixa sinergia (<0.4): {distribution.get('low_synergy', 0)}")
        
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas de sinergias: {e}")


def cleanup_database():
    """Limpa duplicatas do banco"""
    print("\n🧹 Limpando duplicatas...")
    try:
        removed = cleanup_supabase_duplicates()
        print(f"✅ Removidas {removed} duplicatas")
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Sistema de Scraping de Ferramentas de IA')
    parser.add_argument(
        'action', 
        choices=['scrape', 'synergy', 'stats', 'cleanup', 'full'],
        help='Ação a executar'
    )
    parser.add_argument(
        '--scraper',
        choices=['aitools_directory', 'theresanaiforthat', 'futurepedia', 'phygital_library'],
        help='Scraper específico para executar (apenas com action=scrape)'
    )
    
    args = parser.parse_args()
    
    print("🚀 === SISTEMA AI_SCRAPPING ===")
    
    if args.action == 'scrape':
        if args.scraper:
            run_scraper(args.scraper)
        else:
            run_all_scrapers()
            
    elif args.action == 'synergy':
        run_synergy_calculation()
        
    elif args.action == 'stats':
        show_statistics()
        
    elif args.action == 'cleanup':
        cleanup_database()
        
    elif args.action == 'full':
        print("🔄 Executando pipeline completo...")
        
        # 1. Scraping
        total_tools = run_all_scrapers()
        
        # 2. Limpeza
        cleanup_database()
        
        # 3. Sinergias (apenas se tiver ferramentas)
        if total_tools > 0:
            run_synergy_calculation()
        
        # 4. Estatísticas
        show_statistics()
        
        print("\n✅ Pipeline completo executado!")
    
    print("\n🏁 Concluído!")


if __name__ == "__main__":
    main()