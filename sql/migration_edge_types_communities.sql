-- =====================================================
-- SQL MIGRATION: Edge Types & Community Detection
-- Adds edge classification and community clustering
-- =====================================================

-- Add edge_type column to ai_synergy table
ALTER TABLE ai_synergy ADD COLUMN IF NOT EXISTS edge_type TEXT DEFAULT 'unspecified';

-- Add community_id column to ai_tool table  
ALTER TABLE ai_tool ADD COLUMN IF NOT EXISTS community_id INT;

-- Create index for community queries
CREATE INDEX IF NOT EXISTS idx_ai_tool_community ON ai_tool(community_id);

-- Create index for edge_type queries
CREATE INDEX IF NOT EXISTS idx_ai_synergy_edge_type ON ai_synergy(edge_type);

-- Add comment documentation
COMMENT ON COLUMN ai_synergy.edge_type IS 'Classification of edge: same_domain, video_audio, semantic_similarity, weak';
COMMENT ON COLUMN ai_tool.community_id IS 'Community cluster ID from Louvain algorithm, NULL if not clustered';

-- Create edge type enum for validation (optional)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'edge_type_enum') THEN
        CREATE TYPE edge_type_enum AS ENUM (
            'same_domain',
            'video_audio', 
            'semantic_similarity',
            'weak',
            'unspecified'
        );
    END IF;
END
$$;

-- Optionally alter column to use enum (can be applied later)
-- ALTER TABLE ai_synergy ALTER COLUMN edge_type TYPE edge_type_enum USING edge_type::edge_type_enum;

-- Create view for edge type statistics
CREATE OR REPLACE VIEW edge_type_stats AS
SELECT 
    edge_type,
    COUNT(*) as edge_count,
    AVG(strength) as avg_strength,
    MIN(strength) as min_strength,
    MAX(strength) as max_strength
FROM ai_synergy 
GROUP BY edge_type
ORDER BY edge_count DESC;

-- Create view for community statistics
CREATE OR REPLACE VIEW community_stats AS
SELECT 
    community_id,
    COUNT(*) as tool_count,
    AVG(popularity) as avg_popularity,
    STRING_AGG(DISTINCT macro_domain, ', ') as domains,
    COUNT(DISTINCT macro_domain) as domain_diversity
FROM ai_tool 
WHERE community_id IS NOT NULL
GROUP BY community_id
ORDER BY tool_count DESC;

-- Function to get edge type distribution for a tool
CREATE OR REPLACE FUNCTION get_tool_edge_types(tool_uuid UUID)
RETURNS TABLE(edge_type TEXT, count BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.edge_type,
        COUNT(*)::BIGINT as count
    FROM ai_synergy s
    WHERE s.tool_id_1 = tool_uuid OR s.tool_id_2 = tool_uuid
    GROUP BY s.edge_type
    ORDER BY count DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to get community members
CREATE OR REPLACE FUNCTION get_community_members(comm_id INT)
RETURNS TABLE(id UUID, name TEXT, macro_domain TEXT, popularity REAL) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.name,
        t.macro_domain,
        t.popularity
    FROM ai_tool t
    WHERE t.community_id = comm_id
    ORDER BY t.popularity DESC NULLS LAST;
END;
$$ LANGUAGE plpgsql;

-- Migration completion log
INSERT INTO migration_log (migration_name, applied_at) 
VALUES ('edge_types_communities', NOW())
ON CONFLICT (migration_name) DO UPDATE SET applied_at = NOW();

-- Create migration_log table if it doesn't exist
CREATE TABLE IF NOT EXISTS migration_log (
    migration_name TEXT PRIMARY KEY,
    applied_at TIMESTAMPTZ DEFAULT NOW()
);

RAISE NOTICE 'Migration completed: Edge types and community detection schema ready';
RAISE NOTICE 'Next steps: 1) Run updated build_synergy.py 2) Run cluster_detect.py';