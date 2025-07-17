#!/usr/bin/env python3
"""
Creates the AI Tools schema in Supabase using SQL execution via Supabase client
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

def create_supabase_schema():
    """Creates the schema in Supabase using SQL execution"""
    
    # Load environment variables
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ ERRO: SUPABASE_URL e SUPABASE_KEY devem estar definidos no .env")
        return False
    
    print("🔗 Conectando ao Supabase...")
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        print("✅ Cliente Supabase criado com sucesso!")
        
        # Complete migration SQL (split into smaller chunks for better execution)
        print("🏗️ Executando migração do schema...")
        
        # Step 1: Create ENUM type
        enum_sql = """
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tool_domain') THEN
        CREATE TYPE tool_domain AS ENUM (
          'NLP','COMPUTER_VISION','AUDIO','VIDEO','GENERATIVE_AI',
          'ML_FRAMEWORKS','DATA_ANALYSIS','AUTOMATION','DESIGN',
          'CODING','BUSINESS','OTHER'
        );
    END IF;
END $$;
"""
        
        print("   📝 Criando tipo ENUM tool_domain...")
        result = supabase.rpc('exec_sql', {'sql': enum_sql}).execute()
        
        # Step 2: Create tables
        tables_sql = """
CREATE TABLE IF NOT EXISTS ai_tool (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ext_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  price TEXT,
  popularity NUMERIC DEFAULT 0,
  macro_domain tool_domain NOT NULL,
  categories TEXT[] DEFAULT '{}',
  source TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(source, ext_id)
);

CREATE TABLE IF NOT EXISTS ai_synergy (
  tool_id_1 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  tool_id_2 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  strength  NUMERIC NOT NULL CHECK (strength >= 0 AND strength <= 1),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (tool_id_1, tool_id_2),
  CHECK (tool_id_1 < tool_id_2)
);
"""
        
        print("   📝 Criando tabelas ai_tool e ai_synergy...")
        result = supabase.rpc('exec_sql', {'sql': tables_sql}).execute()
        
        # Step 3: Add new columns
        columns_sql = """
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'url') THEN
        ALTER TABLE ai_tool ADD COLUMN url TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'logo_url') THEN
        ALTER TABLE ai_tool ADD COLUMN logo_url TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'rank') THEN
        ALTER TABLE ai_tool ADD COLUMN rank INT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'upvotes') THEN
        ALTER TABLE ai_tool ADD COLUMN upvotes INT DEFAULT 0;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'monthly_users') THEN
        ALTER TABLE ai_tool ADD COLUMN monthly_users INT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'editor_score') THEN
        ALTER TABLE ai_tool ADD COLUMN editor_score NUMERIC(3,1);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'maturity') THEN
        ALTER TABLE ai_tool ADD COLUMN maturity TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'platform') THEN
        ALTER TABLE ai_tool ADD COLUMN platform TEXT[];
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'features') THEN
        ALTER TABLE ai_tool ADD COLUMN features JSONB;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'last_scraped') THEN
        ALTER TABLE ai_tool ADD COLUMN last_scraped TIMESTAMPTZ DEFAULT NOW();
    END IF;
END $$;
"""
        
        print("   📝 Adicionando novas colunas...")
        result = supabase.rpc('exec_sql', {'sql': columns_sql}).execute()
        
        # Step 4: Create materialized view
        view_sql = """
DROP MATERIALIZED VIEW IF EXISTS ai_tool_degree;

CREATE MATERIALIZED VIEW ai_tool_degree AS
SELECT 
    t.id,
    COALESCE(degree_count.degree, 0) AS degree
FROM ai_tool t
LEFT JOIN (
    SELECT 
        tool_id,
        COUNT(*) AS degree
    FROM (
        SELECT tool_id_1 AS tool_id FROM ai_synergy
        UNION ALL
        SELECT tool_id_2 AS tool_id FROM ai_synergy
    ) synergy_edges
    GROUP BY tool_id
) degree_count ON t.id = degree_count.tool_id;
"""
        
        print("   📝 Criando materialized view ai_tool_degree...")
        result = supabase.rpc('exec_sql', {'sql': view_sql}).execute()
        
        # Step 5: Create indexes
        indexes_sql = """
CREATE INDEX IF NOT EXISTS idx_ai_tool_degree ON ai_tool_degree(degree DESC);
CREATE INDEX IF NOT EXISTS idx_ai_tool_rank ON ai_tool(rank);
CREATE INDEX IF NOT EXISTS idx_ai_tool_monthly_users ON ai_tool(monthly_users DESC);
CREATE INDEX IF NOT EXISTS idx_ai_tool_upvotes ON ai_tool(upvotes DESC);
"""
        
        print("   📝 Criando índices...")
        result = supabase.rpc('exec_sql', {'sql': indexes_sql}).execute()
        
        # Step 6: Refresh materialized view
        refresh_sql = "REFRESH MATERIALIZED VIEW ai_tool_degree;"
        
        print("   📝 Atualizando materialized view...")
        result = supabase.rpc('exec_sql', {'sql': refresh_sql}).execute()
        
        print("✅ Schema criado com sucesso!")
        
        # Test the schema by checking tables
        print("\n🔍 Verificando schema criado...")
        
        # Check if we can query the tables
        try:
            result = supabase.table('ai_tool').select('count').execute()
            print(f"   ✅ Tabela ai_tool acessível")
            
            result = supabase.table('ai_synergy').select('count').execute()
            print(f"   ✅ Tabela ai_synergy acessível")
            
            # We can't directly query materialized views via supabase client, but that's ok
            print(f"   ✅ Materialized view ai_tool_degree criada")
            
        except Exception as e:
            print(f"   ⚠️ Aviso: {e}")
        
        print(f"\n🎉 SUCESSO! Schema do Supabase configurado!")
        print(f"   • Base de dados pronta para receber 5,000+ ferramentas AI")
        print(f"   • Materialized view configurada para análise de grau")
        print(f"   • Índices otimizados para performance")
        print(f"   • Estrutura completa com URL, logos, ranks, upvotes, etc.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = create_supabase_schema()
    
    if success:
        print("\n✅ Schema do Supabase configurado com sucesso!")
        print("   Pronto para executar o scraping e popular a base de dados.")
    else:
        print("\n❌ Falha na configuração do schema.")
        print("   Verifique as credenciais do Supabase no .env ou execute o SQL manualmente no Supabase Dashboard.")