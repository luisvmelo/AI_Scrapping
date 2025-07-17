#!/usr/bin/env python3
"""
Creates the AI Tools schema in Supabase database
Executes the complete idempotent migration for ai_tool table enhancements
"""

import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse

def create_supabase_schema():
    """Creates the schema in Supabase using the migration SQL"""
    
    # Load environment variables
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ ERRO: SUPABASE_URL e SUPABASE_KEY devem estar definidos no .env")
        return False
    
    # Parse Supabase URL to get database connection info
    parsed_url = urlparse(supabase_url)
    
    # Supabase PostgreSQL connection string format
    # Replace https://xxx.supabase.co with postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
    project_ref = parsed_url.hostname.split('.')[0]  # figybjxmgmyzmmlphatm
    
    # The service_role key is used as password for direct DB connections
    # Try multiple connection formats
    connection_strings = [
        f"postgresql://postgres:{supabase_key}@db.{project_ref}.supabase.co:5432/postgres",
        f"postgresql://postgres.{project_ref}:{supabase_key}@aws-0-us-west-1.pooler.supabase.com:6543/postgres",
        f"postgresql://postgres:{supabase_key}@{project_ref}.pooler.supabase.com:6543/postgres"
    ]
    
    print("🔗 Conectando ao Supabase PostgreSQL...")
    print(f"   Project: {project_ref}")
    
    try:
        # Connect to Supabase PostgreSQL
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexão estabelecida com sucesso!")
        
        # Complete migration SQL
        migration_sql = """
-- Idempotent SQL migration for AI tool enrichment and degree materialized view

-- First, create the ENUM type if it doesn't exist
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

-- Create ai_tool table if it doesn't exist
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

-- Create ai_synergy table if it doesn't exist
CREATE TABLE IF NOT EXISTS ai_synergy (
  tool_id_1 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  tool_id_2 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  strength  NUMERIC NOT NULL CHECK (strength >= 0 AND strength <= 1),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (tool_id_1, tool_id_2),
  CHECK (tool_id_1 < tool_id_2)
);

-- Add new columns to ai_tool table
DO $$ 
BEGIN
    -- Add url column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'url') THEN
        ALTER TABLE ai_tool ADD COLUMN url TEXT;
    END IF;
    
    -- Add logo_url column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'logo_url') THEN
        ALTER TABLE ai_tool ADD COLUMN logo_url TEXT;
    END IF;
    
    -- Add rank column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'rank') THEN
        ALTER TABLE ai_tool ADD COLUMN rank INT;
    END IF;
    
    -- Add upvotes column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'upvotes') THEN
        ALTER TABLE ai_tool ADD COLUMN upvotes INT DEFAULT 0;
    END IF;
    
    -- Add monthly_users column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'monthly_users') THEN
        ALTER TABLE ai_tool ADD COLUMN monthly_users INT;
    END IF;
    
    -- Add editor_score column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'editor_score') THEN
        ALTER TABLE ai_tool ADD COLUMN editor_score NUMERIC(3,1);
    END IF;
    
    -- Add maturity column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'maturity') THEN
        ALTER TABLE ai_tool ADD COLUMN maturity TEXT;
    END IF;
    
    -- Add platform column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'platform') THEN
        ALTER TABLE ai_tool ADD COLUMN platform TEXT[];
    END IF;
    
    -- Add features column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'features') THEN
        ALTER TABLE ai_tool ADD COLUMN features JSONB;
    END IF;
    
    -- Add last_scraped column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ai_tool' AND column_name = 'last_scraped') THEN
        ALTER TABLE ai_tool ADD COLUMN last_scraped TIMESTAMPTZ DEFAULT NOW();
    END IF;
END $$;

-- Drop materialized view if exists to recreate it
DROP MATERIALIZED VIEW IF EXISTS ai_tool_degree;

-- Create materialized view for tool degrees
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

-- Create indexes if they don't exist
CREATE INDEX IF NOT EXISTS idx_ai_tool_degree ON ai_tool_degree(degree DESC);
CREATE INDEX IF NOT EXISTS idx_ai_tool_rank ON ai_tool(rank);
CREATE INDEX IF NOT EXISTS idx_ai_tool_monthly_users ON ai_tool(monthly_users DESC);
CREATE INDEX IF NOT EXISTS idx_ai_tool_upvotes ON ai_tool(upvotes DESC);

-- Initial refresh of materialized view
REFRESH MATERIALIZED VIEW ai_tool_degree;
"""
        
        print("🏗️ Executando migração do schema...")
        
        # Execute the migration
        cursor.execute(migration_sql)
        
        print("✅ Schema criado com sucesso!")
        
        # Verify the schema creation
        cursor.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name IN ('ai_tool', 'ai_synergy') 
            ORDER BY table_name, ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        print(f"\n📋 Schema verificado - {len(columns)} colunas criadas:")
        current_table = None
        for table, column, data_type in columns:
            if table != current_table:
                print(f"\n   📝 Tabela: {table}")
                current_table = table
            print(f"      • {column} ({data_type})")
        
        # Check materialized view
        cursor.execute("""
            SELECT COUNT(*) FROM ai_tool_degree
        """)
        
        degree_count = cursor.fetchone()[0]
        print(f"\n   📊 Materialized view ai_tool_degree: {degree_count} registros")
        
        # Check indexes
        cursor.execute("""
            SELECT indexname FROM pg_indexes 
            WHERE tablename IN ('ai_tool', 'ai_tool_degree') 
            AND indexname LIKE 'idx_%'
        """)
        
        indexes = cursor.fetchall()
        print(f"\n   🔍 Índices criados: {len(indexes)}")
        for idx in indexes:
            print(f"      • {idx[0]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n🎉 SUCESSO! Schema do Supabase criado e verificado!")
        print(f"   • Base de dados pronta para receber 5,000+ ferramentas AI")
        print(f"   • Materialized view configurada para análise de grau")
        print(f"   • Índices otimizados para performance")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    success = create_supabase_schema()
    
    if success:
        print("\n✅ Schema do Supabase configurado com sucesso!")
        print("   Pronto para executar o scraping e popular a base de dados.")
    else:
        print("\n❌ Falha na configuração do schema.")
        print("   Verifique as credenciais do Supabase no .env")