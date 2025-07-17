-- =====================================================
-- COMPLETE SUPABASE SCHEMA FOR 3D GRAPH VISUALIZATION
-- AI Tools Network Database - Production Ready
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- ENUMS FOR STANDARDIZED VALUES
-- =====================================================

-- Tool domains for classification
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

-- Tool maturity levels
CREATE TYPE tool_maturity AS ENUM (
    'alpha',
    'beta', 
    'stable',
    'deprecated'
);

-- Pricing models
CREATE TYPE pricing_model AS ENUM (
    'free',
    'freemium',
    'free_trial',
    'subscription',
    'one_time',
    'enterprise',
    'unknown'
);

-- Graph relationship types
CREATE TYPE relationship_type AS ENUM (
    'similar_functionality',
    'same_category',
    'alternative_to',
    'integrates_with',
    'builds_on',
    'competes_with',
    'same_company',
    'api_connection'
);

-- =====================================================
-- CORE TOOLS TABLE
-- =====================================================

CREATE TABLE ai_tool (
    -- Primary identifiers
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ext_id TEXT NOT NULL,
    source TEXT NOT NULL,
    
    -- Basic tool information
    name TEXT NOT NULL,
    description TEXT,
    url TEXT,
    logo_url TEXT,
    
    -- Pricing and business model
    price TEXT,
    pricing_model pricing_model DEFAULT 'unknown',
    
    -- Metrics and scores
    popularity REAL DEFAULT 0 CHECK (popularity >= 0 AND popularity <= 100),
    rank INTEGER,
    upvotes INTEGER DEFAULT 0,
    monthly_users BIGINT,
    editor_score REAL CHECK (editor_score >= 0 AND editor_score <= 10),
    
    -- Classification
    categories TEXT[] DEFAULT '{}',
    macro_domain tool_domain DEFAULT 'OTHER',
    maturity tool_maturity DEFAULT 'beta',
    platform TEXT[] DEFAULT '{}',
    
    -- Rich metadata for graph visualization
    features JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    
    -- Graph positioning (for 3D visualization)
    graph_position JSONB, -- {x: float, y: float, z: float}
    node_size REAL DEFAULT 1.0,
    node_color TEXT DEFAULT '#3B82F6',
    
    -- Scraping metadata
    content_hash TEXT,
    last_scraped TIMESTAMPTZ,
    scrape_source_data JSONB, -- Raw scraping data for debugging
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(ext_id, source)
);

-- =====================================================
-- TOOL RELATIONSHIPS (FOR GRAPH CONNECTIONS)
-- =====================================================

CREATE TABLE tool_relationship (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relationship definition
    source_tool_id UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
    target_tool_id UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
    relationship_type relationship_type NOT NULL,
    
    -- Relationship strength (for visual weight)
    strength REAL DEFAULT 1.0 CHECK (strength >= 0 AND strength <= 1),
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    
    -- Visual properties for edges
    edge_color TEXT DEFAULT '#6B7280',
    edge_width REAL DEFAULT 1.0,
    
    -- Metadata
    description TEXT,
    auto_detected BOOLEAN DEFAULT TRUE,
    verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Prevent self-relationships and duplicates
    CHECK (source_tool_id != target_tool_id),
    UNIQUE(source_tool_id, target_tool_id, relationship_type)
);

-- =====================================================
-- CATEGORY HIERARCHY (FOR GRAPH CLUSTERING)
-- =====================================================

CREATE TABLE category (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    
    -- Hierarchy
    parent_id UUID REFERENCES category(id) ON DELETE SET NULL,
    level INTEGER DEFAULT 0,
    
    -- Visual properties for graph clusters
    cluster_color TEXT DEFAULT '#EF4444',
    cluster_position JSONB, -- {x: float, y: float, z: float}
    
    -- Metadata
    tool_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- TOOL-CATEGORY MAPPINGS
-- =====================================================

CREATE TABLE tool_category (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES category(id) ON DELETE CASCADE,
    
    -- Confidence in categorization
    confidence REAL DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1),
    auto_assigned BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(tool_id, category_id)
);

-- =====================================================
-- COMPANIES/ORGANIZATIONS
-- =====================================================

CREATE TABLE organization (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    website TEXT,
    logo_url TEXT,
    description TEXT,
    
    -- Business info
    founded_year INTEGER,
    headquarters TEXT,
    company_size TEXT, -- 'startup', 'small', 'medium', 'large', 'enterprise'
    
    -- Graph visualization
    node_color TEXT DEFAULT '#10B981',
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- TOOL-ORGANIZATION RELATIONSHIPS
-- =====================================================

CREATE TABLE tool_organization (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id UUID NOT NULL REFERENCES ai_tool(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    
    -- Relationship type
    relationship TEXT DEFAULT 'developer', -- 'developer', 'owner', 'sponsor', 'partner'
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(tool_id, organization_id, relationship)
);

-- =====================================================
-- GRAPH VIEWS AND ANALYTICS
-- =====================================================

-- Popular tools view
CREATE VIEW popular_tools AS
SELECT 
    t.*,
    o.name as organization_name,
    ARRAY_AGG(DISTINCT c.name) as category_names,
    COUNT(DISTINCT tr1.target_tool_id) as outgoing_connections,
    COUNT(DISTINCT tr2.source_tool_id) as incoming_connections
FROM ai_tool t
LEFT JOIN tool_organization to_rel ON t.id = to_rel.tool_id
LEFT JOIN organization o ON to_rel.organization_id = o.id
LEFT JOIN tool_category tc ON t.id = tc.tool_id
LEFT JOIN category c ON tc.category_id = c.id
LEFT JOIN tool_relationship tr1 ON t.id = tr1.source_tool_id
LEFT JOIN tool_relationship tr2 ON t.id = tr2.target_tool_id
GROUP BY t.id, o.name
ORDER BY t.popularity DESC;

-- Category statistics view
CREATE VIEW category_stats AS
SELECT 
    c.*,
    COUNT(DISTINCT tc.tool_id) as actual_tool_count,
    AVG(t.popularity) as avg_popularity,
    MAX(t.popularity) as max_popularity,
    COUNT(DISTINCT tr.source_tool_id) as total_connections
FROM category c
LEFT JOIN tool_category tc ON c.id = tc.category_id
LEFT JOIN ai_tool t ON tc.tool_id = t.id
LEFT JOIN tool_relationship tr ON t.id = tr.source_tool_id
GROUP BY c.id
ORDER BY actual_tool_count DESC;

-- Network analysis view (for graph algorithms)
CREATE VIEW tool_network AS
SELECT 
    t.id,
    t.name,
    t.popularity,
    t.categories,
    t.macro_domain,
    t.graph_position,
    t.node_color,
    t.node_size,
    ARRAY_AGG(DISTINCT tr.target_tool_id) FILTER (WHERE tr.target_tool_id IS NOT NULL) as connected_tools,
    COUNT(DISTINCT tr.target_tool_id) as connection_count
FROM ai_tool t
LEFT JOIN tool_relationship tr ON t.id = tr.source_tool_id
GROUP BY t.id
ORDER BY connection_count DESC;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Primary lookup indexes
CREATE INDEX idx_ai_tool_ext_id_source ON ai_tool(ext_id, source);
CREATE INDEX idx_ai_tool_url ON ai_tool(url);
CREATE INDEX idx_ai_tool_name_lower ON ai_tool(LOWER(name));
CREATE INDEX idx_ai_tool_popularity ON ai_tool(popularity DESC);
CREATE INDEX idx_ai_tool_domain ON ai_tool(macro_domain);
CREATE INDEX idx_ai_tool_last_scraped ON ai_tool(last_scraped DESC);

-- Graph relationship indexes
CREATE INDEX idx_tool_relationship_source ON tool_relationship(source_tool_id);
CREATE INDEX idx_tool_relationship_target ON tool_relationship(target_tool_id);
CREATE INDEX idx_tool_relationship_type ON tool_relationship(relationship_type);
CREATE INDEX idx_tool_relationship_strength ON tool_relationship(strength DESC);

-- Category indexes
CREATE INDEX idx_category_parent ON category(parent_id);
CREATE INDEX idx_category_slug ON category(slug);
CREATE INDEX idx_tool_category_tool ON tool_category(tool_id);
CREATE INDEX idx_tool_category_category ON tool_category(category_id);

-- JSONB indexes for features and positioning
CREATE INDEX idx_ai_tool_features_gin ON ai_tool USING gin (features);
CREATE INDEX idx_ai_tool_graph_position_gin ON ai_tool USING gin (graph_position);

-- Full-text search indexes
CREATE INDEX idx_ai_tool_search ON ai_tool USING gin (
    to_tsvector('english', 
        COALESCE(name, '') || ' ' || 
        COALESCE(description, '') || ' ' || 
        array_to_string(COALESCE(categories, '{}'), ' ')
    )
);

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update triggers
CREATE TRIGGER update_ai_tool_updated_at 
    BEFORE UPDATE ON ai_tool 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tool_relationship_updated_at 
    BEFORE UPDATE ON tool_relationship 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_category_updated_at 
    BEFORE UPDATE ON category 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_organization_updated_at 
    BEFORE UPDATE ON organization 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Auto-update category tool counts
CREATE OR REPLACE FUNCTION update_category_tool_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE category 
        SET tool_count = tool_count + 1 
        WHERE id = NEW.category_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE category 
        SET tool_count = tool_count - 1 
        WHERE id = OLD.category_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_category_tool_count
    AFTER INSERT OR DELETE ON tool_category
    FOR EACH ROW EXECUTE FUNCTION update_category_tool_count();

-- =====================================================
-- FUNCTIONS FOR GRAPH ANALYSIS
-- =====================================================

-- Calculate tool similarity score
CREATE OR REPLACE FUNCTION calculate_tool_similarity(tool_id_1 UUID, tool_id_2 UUID)
RETURNS REAL AS $$
DECLARE
    similarity_score REAL := 0;
    t1 ai_tool%ROWTYPE;
    t2 ai_tool%ROWTYPE;
    shared_categories INTEGER;
    shared_platforms INTEGER;
BEGIN
    SELECT * INTO t1 FROM ai_tool WHERE id = tool_id_1;
    SELECT * INTO t2 FROM ai_tool WHERE id = tool_id_2;
    
    IF NOT FOUND THEN
        RETURN 0;
    END IF;
    
    -- Category similarity (40% weight)
    SELECT COUNT(*) INTO shared_categories
    FROM unnest(t1.categories) AS cat1
    INNER JOIN unnest(t2.categories) AS cat2 ON cat1 = cat2;
    
    similarity_score := similarity_score + (shared_categories::REAL / GREATEST(array_length(t1.categories, 1), array_length(t2.categories, 1), 1)) * 0.4;
    
    -- Domain similarity (30% weight)
    IF t1.macro_domain = t2.macro_domain THEN
        similarity_score := similarity_score + 0.3;
    END IF;
    
    -- Platform similarity (20% weight)
    SELECT COUNT(*) INTO shared_platforms
    FROM unnest(t1.platform) AS plat1
    INNER JOIN unnest(t2.platform) AS plat2 ON plat1 = plat2;
    
    similarity_score := similarity_score + (shared_platforms::REAL / GREATEST(array_length(t1.platform, 1), array_length(t2.platform, 1), 1)) * 0.2;
    
    -- Popularity similarity (10% weight)
    similarity_score := similarity_score + (1 - ABS(t1.popularity - t2.popularity) / 100.0) * 0.1;
    
    RETURN LEAST(similarity_score, 1.0);
END;
$$ LANGUAGE plpgsql;

-- Auto-generate relationships based on similarity
CREATE OR REPLACE FUNCTION generate_similarity_relationships(similarity_threshold REAL DEFAULT 0.7)
RETURNS INTEGER AS $$
DECLARE
    tool_pair RECORD;
    similarity REAL;
    relationships_created INTEGER := 0;
BEGIN
    FOR tool_pair IN 
        SELECT t1.id as id1, t2.id as id2
        FROM ai_tool t1
        CROSS JOIN ai_tool t2
        WHERE t1.id < t2.id  -- Avoid duplicates and self-joins
        AND NOT EXISTS (
            SELECT 1 FROM tool_relationship tr 
            WHERE (tr.source_tool_id = t1.id AND tr.target_tool_id = t2.id)
               OR (tr.source_tool_id = t2.id AND tr.target_tool_id = t1.id)
        )
    LOOP
        similarity := calculate_tool_similarity(tool_pair.id1, tool_pair.id2);
        
        IF similarity >= similarity_threshold THEN
            INSERT INTO tool_relationship (
                source_tool_id, 
                target_tool_id, 
                relationship_type, 
                strength, 
                confidence,
                description
            ) VALUES (
                tool_pair.id1,
                tool_pair.id2,
                'similar_functionality',
                similarity,
                similarity,
                'Auto-generated based on similarity analysis'
            );
            
            relationships_created := relationships_created + 1;
        END IF;
    END LOOP;
    
    RETURN relationships_created;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- MATERIALIZED VIEWS FOR PERFORMANCE
-- =====================================================

-- Graph layout cache (for 3D positioning)
CREATE MATERIALIZED VIEW tool_graph_layout AS
SELECT 
    t.id,
    t.name,
    t.popularity,
    t.macro_domain,
    t.graph_position,
    t.node_color,
    t.node_size,
    COUNT(DISTINCT tr1.target_tool_id) as outgoing_edges,
    COUNT(DISTINCT tr2.source_tool_id) as incoming_edges,
    AVG(tr1.strength) as avg_outgoing_strength,
    AVG(tr2.strength) as avg_incoming_strength
FROM ai_tool t
LEFT JOIN tool_relationship tr1 ON t.id = tr1.source_tool_id
LEFT JOIN tool_relationship tr2 ON t.id = tr2.target_tool_id
GROUP BY t.id, t.name, t.popularity, t.macro_domain, t.graph_position, t.node_color, t.node_size;

-- Create unique index for faster refresh
CREATE UNIQUE INDEX idx_tool_graph_layout_id ON tool_graph_layout(id);

-- =====================================================
-- ROW LEVEL SECURITY (RLS) SETUP
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE ai_tool ENABLE ROW LEVEL SECURITY;
ALTER TABLE tool_relationship ENABLE ROW LEVEL SECURITY;
ALTER TABLE category ENABLE ROW LEVEL SECURITY;
ALTER TABLE tool_category ENABLE ROW LEVEL SECURITY;
ALTER TABLE organization ENABLE ROW LEVEL SECURITY;
ALTER TABLE tool_organization ENABLE ROW LEVEL SECURITY;

-- Basic read policy for public access (for your website)
CREATE POLICY "Public read access" ON ai_tool FOR SELECT USING (true);
CREATE POLICY "Public read access" ON tool_relationship FOR SELECT USING (true);
CREATE POLICY "Public read access" ON category FOR SELECT USING (true);
CREATE POLICY "Public read access" ON tool_category FOR SELECT USING (true);
CREATE POLICY "Public read access" ON organization FOR SELECT USING (true);
CREATE POLICY "Public read access" ON tool_organization FOR SELECT USING (true);

-- Write policies (restrict to authenticated service role)
CREATE POLICY "Service role write access" ON ai_tool FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role write access" ON tool_relationship FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role write access" ON category FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role write access" ON tool_category FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role write access" ON organization FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role write access" ON tool_organization FOR ALL USING (auth.role() = 'service_role');

-- =====================================================
-- SAMPLE DATA FOR DEVELOPMENT
-- =====================================================

-- Insert sample categories
INSERT INTO category (name, slug, description, cluster_color) VALUES
('Artificial Intelligence', 'ai', 'General AI and machine learning tools', '#3B82F6'),
('Natural Language Processing', 'nlp', 'Text processing and language understanding', '#10B981'),
('Computer Vision', 'computer-vision', 'Image and video analysis tools', '#F59E0B'),
('Audio Processing', 'audio', 'Speech, music, and sound processing', '#EF4444'),
('Productivity', 'productivity', 'Tools for enhancing productivity', '#8B5CF6'),
('Development', 'development', 'Programming and development tools', '#06B6D4');

-- Insert sample organizations
INSERT INTO organization (name, website, description, company_size) VALUES
('OpenAI', 'https://openai.com', 'AI research and deployment company', 'large'),
('Anthropic', 'https://anthropic.com', 'AI safety research company', 'medium'),
('Google', 'https://google.com', 'Technology multinational corporation', 'enterprise'),
('Microsoft', 'https://microsoft.com', 'Technology corporation', 'enterprise');

-- =====================================================
-- MAINTENANCE FUNCTIONS
-- =====================================================

-- Refresh all materialized views
CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY tool_graph_layout;
    -- Add more materialized views here as needed
END;
$$ LANGUAGE plpgsql;

-- Cleanup old scraping data
CREATE OR REPLACE FUNCTION cleanup_old_scrape_data(days_old INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    UPDATE ai_tool 
    SET scrape_source_data = NULL
    WHERE last_scraped < NOW() - INTERVAL '1 day' * days_old
    AND scrape_source_data IS NOT NULL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- ANALYTICS QUERIES (EXAMPLES FOR YOUR FRONTEND)
-- =====================================================

/*
-- Popular tools by domain
SELECT macro_domain, name, popularity, monthly_users 
FROM ai_tool 
WHERE macro_domain != 'OTHER'
ORDER BY macro_domain, popularity DESC;

-- Most connected tools (graph hubs)
SELECT t.name, t.popularity, 
       COUNT(DISTINCT tr1.target_tool_id) as outgoing,
       COUNT(DISTINCT tr2.source_tool_id) as incoming,
       COUNT(DISTINCT tr1.target_tool_id) + COUNT(DISTINCT tr2.source_tool_id) as total_connections
FROM ai_tool t
LEFT JOIN tool_relationship tr1 ON t.id = tr1.source_tool_id
LEFT JOIN tool_relationship tr2 ON t.id = tr2.target_tool_id
GROUP BY t.id, t.name, t.popularity
ORDER BY total_connections DESC
LIMIT 20;

-- Category network strength
SELECT c.name, 
       COUNT(DISTINCT tc.tool_id) as tool_count,
       AVG(t.popularity) as avg_popularity,
       COUNT(DISTINCT tr.id) as total_relationships
FROM category c
JOIN tool_category tc ON c.id = tc.category_id
JOIN ai_tool t ON tc.tool_id = t.id
LEFT JOIN tool_relationship tr ON t.id IN (tr.source_tool_id, tr.target_tool_id)
GROUP BY c.id, c.name
ORDER BY total_relationships DESC;
*/

-- =====================================================
-- SCHEMA CREATION COMPLETE
-- =====================================================

-- Log schema creation
DO $$
BEGIN
    RAISE NOTICE 'AI Tools 3D Graph Database Schema Created Successfully!';
    RAISE NOTICE 'Tables: ai_tool, tool_relationship, category, tool_category, organization, tool_organization';
    RAISE NOTICE 'Views: popular_tools, category_stats, tool_network';
    RAISE NOTICE 'Materialized Views: tool_graph_layout';
    RAISE NOTICE 'Functions: calculate_tool_similarity, generate_similarity_relationships, refresh_all_materialized_views';
    RAISE NOTICE 'Ready for 3D graph visualization!';
END
$$;