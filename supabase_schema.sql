-- Complete Idempotent SQL Migration for AI Tools Schema
-- Execute this directly in the Supabase SQL Editor

-- Step 1: Create ENUM type if it doesn't exist
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

-- Step 2: Create ai_tool table if it doesn't exist
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

-- Step 3: Create ai_synergy table if it doesn't exist
CREATE TABLE IF NOT EXISTS ai_synergy (
  tool_id_1 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  tool_id_2 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  strength  NUMERIC NOT NULL CHECK (strength >= 0 AND strength <= 1),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (tool_id_1, tool_id_2),
  CHECK (tool_id_1 < tool_id_2)
);

-- Step 4: Add new columns to ai_tool table
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

-- Step 5: Drop and recreate materialized view
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

-- Step 6: Create indexes if they don't exist
CREATE INDEX IF NOT EXISTS idx_ai_tool_degree ON ai_tool_degree(degree DESC);
CREATE INDEX IF NOT EXISTS idx_ai_tool_rank ON ai_tool(rank);
CREATE INDEX IF NOT EXISTS idx_ai_tool_monthly_users ON ai_tool(monthly_users DESC);
CREATE INDEX IF NOT EXISTS idx_ai_tool_upvotes ON ai_tool(upvotes DESC);

-- Step 7: Initial refresh of materialized view
REFRESH MATERIALIZED VIEW ai_tool_degree;

-- Verification queries (optional - run to verify schema)
-- SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name IN ('ai_tool', 'ai_synergy') ORDER BY table_name, ordinal_position;
-- SELECT COUNT(*) as total_tools FROM ai_tool;
-- SELECT COUNT(*) as degree_records FROM ai_tool_degree;