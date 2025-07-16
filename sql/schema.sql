-- Enum para macro-domínios
CREATE TYPE tool_domain AS ENUM (
  'NLP',
  'COMPUTER_VISION', 
  'AUDIO',
  'VIDEO',
  'GENERATIVE_AI',
  'ML_FRAMEWORKS',
  'DATA_ANALYSIS',
  'AUTOMATION',
  'DESIGN',
  'CODING',
  'BUSINESS',
  'OTHER'
);

-- Tabela principal de ferramentas de IA
CREATE TABLE ai_tool (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ext_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  price TEXT,
  popularity DECIMAL DEFAULT 0,
  macro_domain tool_domain NOT NULL,
  categories TEXT[] DEFAULT '{}',
  source TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(source, ext_id)
);

-- Tabela de sinergias entre ferramentas  
CREATE TABLE ai_synergy (
  tool_id_1 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  tool_id_2 UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
  strength DECIMAL NOT NULL CHECK (strength >= 0 AND strength <= 1),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (tool_id_1, tool_id_2),
  CHECK (tool_id_1 < tool_id_2)
);

-- Índices para performance
CREATE INDEX idx_ai_tool_popularity ON ai_tool(popularity DESC);
CREATE INDEX idx_ai_tool_domain ON ai_tool(macro_domain);
CREATE INDEX idx_ai_synergy_strength ON ai_synergy(strength DESC);