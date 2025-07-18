#!/usr/bin/env python3
"""
Add the most famous and important AI tools that are missing
"""

import sqlite3
import json
from datetime import datetime

# Missing famous AI tools that should be in any comprehensive database
FAMOUS_MISSING_TOOLS = [
    {
        "name": "Bolt.new", 
        "description": "AI-powered full-stack web development platform", 
        "domain": "CODING", 
        "price": "Free/Premium", 
        "url": "https://bolt.new", 
        "categories": ["coding", "web-development", "ai", "full-stack"],
        "popularity": 95.0,
        "monthly_users": 2000000,
        "rank": 1
    },
    {
        "name": "Lovable", 
        "description": "AI website builder that generates full applications", 
        "domain": "CODING", 
        "price": "Premium", 
        "url": "https://lovable.dev", 
        "categories": ["coding", "web-development", "ai", "no-code"],
        "popularity": 92.0,
        "monthly_users": 1500000,
        "rank": 2
    },
    {
        "name": "V0 by Vercel", 
        "description": "AI UI generator for React components", 
        "domain": "CODING", 
        "price": "Free/Premium", 
        "url": "https://v0.dev", 
        "categories": ["coding", "react", "ui", "ai"],
        "popularity": 90.0,
        "monthly_users": 1800000,
        "rank": 3
    },
    {
        "name": "NotebookLM", 
        "description": "Google's AI research assistant for documents", 
        "domain": "NLP", 
        "price": "Free", 
        "url": "https://notebooklm.google.com", 
        "categories": ["research", "documents", "ai", "google"],
        "popularity": 88.0,
        "monthly_users": 3000000,
        "rank": 4
    },
    {
        "name": "Poe", 
        "description": "AI chatbot platform by Quora with multiple models", 
        "domain": "NLP", 
        "price": "Free/Premium", 
        "url": "https://poe.com", 
        "categories": ["chatbot", "ai", "multiple-models", "quora"],
        "popularity": 85.0,
        "monthly_users": 5000000,
        "rank": 5
    },
    {
        "name": "Character.AI", 
        "description": "AI chatbots with distinct personalities", 
        "domain": "NLP", 
        "price": "Free/Premium", 
        "url": "https://character.ai", 
        "categories": ["chatbot", "roleplay", "ai", "entertainment"],
        "popularity": 87.0,
        "monthly_users": 8000000,
        "rank": 6
    },
    {
        "name": "Suno AI", 
        "description": "AI music generation from text prompts", 
        "domain": "OTHER", 
        "price": "Free/Premium", 
        "url": "https://suno.ai", 
        "categories": ["music", "generation", "ai", "audio"],
        "popularity": 84.0,
        "monthly_users": 2500000,
        "rank": 7
    },
    {
        "name": "Udio", 
        "description": "AI music creation platform", 
        "domain": "OTHER", 
        "price": "Free/Premium", 
        "url": "https://udio.com", 
        "categories": ["music", "generation", "ai", "creation"],
        "popularity": 82.0,
        "monthly_users": 1200000,
        "rank": 8
    },
    {
        "name": "Luma AI", 
        "description": "AI 3D scene generation and video creation", 
        "domain": "COMPUTER_VISION", 
        "price": "Free/Premium", 
        "url": "https://lumalabs.ai", 
        "categories": ["3d", "video", "ai", "generation"],
        "popularity": 83.0,
        "monthly_users": 1000000,
        "rank": 9
    },
    {
        "name": "DeepMind Gemini", 
        "description": "Google DeepMind's advanced AI model", 
        "domain": "NLP", 
        "price": "Free/Premium", 
        "url": "https://deepmind.google/technologies/gemini", 
        "categories": ["ai", "language-model", "google", "research"],
        "popularity": 91.0,
        "monthly_users": 4000000,
        "rank": 10
    },
    {
        "name": "Replicate", 
        "description": "Run AI models in the cloud", 
        "domain": "OTHER", 
        "price": "Pay-per-use", 
        "url": "https://replicate.com", 
        "categories": ["ai", "cloud", "models", "api"],
        "popularity": 79.0,
        "monthly_users": 800000,
        "rank": 11
    },
    {
        "name": "Hugging Face", 
        "description": "Open source AI model hub and platform", 
        "domain": "OTHER", 
        "price": "Free/Premium", 
        "url": "https://huggingface.co", 
        "categories": ["ai", "open-source", "models", "hub"],
        "popularity": 86.0,
        "monthly_users": 6000000,
        "rank": 12
    },
    {
        "name": "Anthropic Console", 
        "description": "Claude API and development platform", 
        "domain": "NLP", 
        "price": "Pay-per-use", 
        "url": "https://console.anthropic.com", 
        "categories": ["ai", "api", "development", "claude"],
        "popularity": 81.0,
        "monthly_users": 1500000,
        "rank": 13
    },
    {
        "name": "OpenAI API", 
        "description": "OpenAI's API platform for developers", 
        "domain": "NLP", 
        "price": "Pay-per-use", 
        "url": "https://platform.openai.com", 
        "categories": ["ai", "api", "development", "openai"],
        "popularity": 89.0,
        "monthly_users": 7000000,
        "rank": 14
    },
    {
        "name": "Replit Agent", 
        "description": "AI coding assistant in Replit", 
        "domain": "CODING", 
        "price": "Premium", 
        "url": "https://replit.com/ai", 
        "categories": ["coding", "ai", "assistant", "cloud"],
        "popularity": 78.0,
        "monthly_users": 2000000,
        "rank": 15
    }
]

def add_famous_ai_tools():
    """Add the most famous AI tools to the database"""
    
    conn = sqlite3.connect('database/ai_tools.db')
    
    print("🌟 ADDING FAMOUS AI TOOLS")
    print("=" * 60)
    
    # Get current count
    current_count = conn.execute("SELECT COUNT(*) FROM ai_tool").fetchone()[0]
    print(f"Current tools in database: {current_count}")
    
    added_count = 0
    
    for i, tool_data in enumerate(FAMOUS_MISSING_TOOLS, 1):
        try:
            # Check if tool already exists (by name or URL)
            existing = conn.execute(
                "SELECT id FROM ai_tool WHERE name = ? OR url = ?", 
                (tool_data["name"], tool_data["url"])
            ).fetchone()
            
            if existing:
                print(f"  ⚠️  [{i:2d}] {tool_data['name']} - Already exists")
                continue
            
            # Insert into database
            conn.execute("""
                INSERT INTO ai_tool (
                    ext_id, name, description, price, popularity, categories, source, 
                    macro_domain, url, monthly_users, rank, upvotes, 
                    created_at, updated_at, last_scraped
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"famous_{i}",
                tool_data["name"],
                tool_data["description"],
                tool_data["price"],
                tool_data["popularity"],
                json.dumps(tool_data["categories"]),
                "famous_ai_curated",
                tool_data["domain"],
                tool_data["url"],
                tool_data.get("monthly_users", 1000000),
                tool_data.get("rank", i),
                tool_data.get("monthly_users", 1000000) // 1000,  # Convert to upvotes estimate
                datetime.now(),
                datetime.now(),
                datetime.now()
            ))
            
            added_count += 1
            print(f"  ✅ [{i:2d}] {tool_data['name']} - Added ({tool_data['domain']}) - Pop: {tool_data['popularity']}")
            
        except Exception as e:
            print(f"  ❌ [{i:2d}] {tool_data['name']} - Error: {e}")
    
    conn.commit()
    
    # Final count
    final_count = conn.execute("SELECT COUNT(*) FROM ai_tool").fetchone()[0]
    
    print("\n📊 Summary:")
    print(f"  Initial count: {current_count}")
    print(f"  Added: {added_count}")
    print(f"  Final count: {final_count}")
    
    # Show updated statistics
    print("\n🌍 Updated Domain Distribution:")
    domains = conn.execute("""
        SELECT macro_domain, COUNT(*) as count 
        FROM ai_tool 
        GROUP BY macro_domain 
        ORDER BY count DESC
    """).fetchall()
    
    for domain, count in domains:
        print(f"  {domain}: {count} tools")
    
    # Show most popular tools
    print("\n⭐ Top 10 Most Popular Tools:")
    top_tools = conn.execute("""
        SELECT name, popularity, macro_domain, source, monthly_users
        FROM ai_tool 
        ORDER BY popularity DESC 
        LIMIT 10
    """).fetchall()
    
    for i, (name, pop, domain, source, users) in enumerate(top_tools, 1):
        users_str = f"{users//1000000}M" if users and users > 1000000 else f"{users//1000}K" if users and users > 1000 else str(users or "N/A")
        print(f"  {i:2d}. {name:<25} | Pop: {pop:5.1f} | {domain:<15} | Users: {users_str}")
    
    conn.close()
    print("\n✅ Famous AI tools added successfully!")

if __name__ == "__main__":
    add_famous_ai_tools()