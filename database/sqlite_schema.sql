-- SQLite schema matching Supabase ai_tool table
-- Local development database

CREATE TABLE IF NOT EXISTS ai_tool (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ext_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price TEXT,
    popularity REAL DEFAULT 0,
    categories TEXT, -- JSON array as string in SQLite
    source TEXT NOT NULL,
    macro_domain TEXT DEFAULT 'OTHER',
    content_hash TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Enhanced fields
    url TEXT,
    logo_url TEXT,
    rank INTEGER,
    upvotes INTEGER,
    monthly_users INTEGER,
    editor_score REAL,
    maturity TEXT,
    platform TEXT, -- JSON array as string in SQLite
    features TEXT, -- JSON object as string in SQLite
    last_scraped DATETIME
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_ai_tool_ext_id_source ON ai_tool(ext_id, source);
CREATE INDEX IF NOT EXISTS idx_ai_tool_url ON ai_tool(url);
CREATE INDEX IF NOT EXISTS idx_ai_tool_name ON ai_tool(name);
CREATE INDEX IF NOT EXISTS idx_ai_tool_source ON ai_tool(source);
CREATE INDEX IF NOT EXISTS idx_ai_tool_macro_domain ON ai_tool(macro_domain);
CREATE INDEX IF NOT EXISTS idx_ai_tool_popularity ON ai_tool(popularity);
CREATE INDEX IF NOT EXISTS idx_ai_tool_last_scraped ON ai_tool(last_scraped);

-- Trigger to update updated_at on changes
CREATE TRIGGER IF NOT EXISTS update_ai_tool_updated_at 
    AFTER UPDATE ON ai_tool
BEGIN
    UPDATE ai_tool SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- View for tool statistics (similar to Supabase materialized view)
CREATE VIEW IF NOT EXISTS ai_tool_stats AS
SELECT 
    source,
    macro_domain,
    COUNT(*) as tool_count,
    AVG(popularity) as avg_popularity,
    MAX(last_scraped) as last_update
FROM ai_tool 
GROUP BY source, macro_domain;

-- Insert some sample data for testing
INSERT OR IGNORE INTO ai_tool (
    ext_id, name, description, price, popularity, categories, source, macro_domain,
    url, logo_url, rank, upvotes, monthly_users, editor_score, maturity, platform, features
) VALUES 
(
    'sample_tool_1', 
    'Sample AI Tool', 
    'This is a sample tool for testing the database schema',
    'Free',
    85.5,
    '["ai", "productivity"]',
    'test_source',
    'NLP',
    'https://example.com/sample-tool',
    'https://example.com/logo.png',
    1,
    150,
    5000,
    8.5,
    'stable',
    '["web", "mobile"]',
    '{"free_tier": true, "api_available": true, "real_time": false}'
);