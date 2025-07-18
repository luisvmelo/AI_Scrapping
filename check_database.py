#!/usr/bin/env python3
"""
Database inspector for AI Tools SQLite database
"""

import sqlite3
import json
from datetime import datetime

def check_database():
    """Check the SQLite database contents"""
    
    conn = sqlite3.connect('database/ai_tools.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cur = conn.cursor()
    
    print("🗄️  AI TOOLS DATABASE INSPECTOR")
    print("=" * 60)
    
    # Database file info
    print(f"📁 Database file: database/ai_tools.db")
    print(f"🕐 Current time: {datetime.now()}")
    print()
    
    # Tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    print(f"📊 Tables: {tables}")
    print()
    
    # Total count
    cur.execute("SELECT COUNT(*) FROM ai_tool")
    total_count = cur.fetchone()[0]
    print(f"🔢 Total AI Tools: {total_count}")
    print()
    
    # Domain distribution
    print("🌍 DOMAIN DISTRIBUTION")
    print("-" * 30)
    cur.execute("SELECT macro_domain, COUNT(*) as count FROM ai_tool GROUP BY macro_domain ORDER BY count DESC")
    for row in cur.fetchall():
        print(f"  {row['macro_domain']}: {row['count']} tools")
    print()
    
    # Source distribution
    print("📡 SOURCE DISTRIBUTION")
    print("-" * 30)
    cur.execute("SELECT source, COUNT(*) as count FROM ai_tool GROUP BY source ORDER BY count DESC")
    for row in cur.fetchall():
        print(f"  {row['source']}: {row['count']} tools")
    print()
    
    # Recent additions
    print("🆕 RECENT ADDITIONS")
    print("-" * 30)
    cur.execute("SELECT name, macro_domain, source, created_at FROM ai_tool ORDER BY created_at DESC LIMIT 5")
    for row in cur.fetchall():
        print(f"  {row['name'][:30]:<30} | {row['macro_domain']:<15} | {row['source']}")
    print()
    
    # Sample detailed record
    print("🔍 SAMPLE DETAILED RECORD")
    print("-" * 30)
    cur.execute("SELECT * FROM ai_tool LIMIT 1")
    sample = cur.fetchone()
    if sample:
        print(f"ID: {sample['id']}")
        print(f"Name: {sample['name']}")
        print(f"Description: {sample['description']}")
        print(f"Domain: {sample['macro_domain']}")
        print(f"Source: {sample['source']}")
        print(f"Price: {sample['price']}")
        print(f"Popularity: {sample['popularity']}")
        print(f"URL: {sample['url']}")
        
        # Parse JSON fields
        if sample['categories']:
            try:
                categories = json.loads(sample['categories'])
                print(f"Categories: {categories}")
            except:
                print(f"Categories (raw): {sample['categories']}")
        
        if sample['features']:
            try:
                features = json.loads(sample['features'])
                print(f"Features: {features}")
            except:
                print(f"Features (raw): {sample['features']}")
    
    conn.close()
    print("\n✅ Database inspection complete!")

if __name__ == "__main__":
    check_database()