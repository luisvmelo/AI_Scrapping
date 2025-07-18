#!/usr/bin/env python3
"""
Autonomous Scraping Progress Monitor
Check scraping progress without consuming AI credits.
"""

import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
import json

class ProgressMonitor:
    def __init__(self, db_path='database/ai_tools.db'):
        self.db_path = db_path
    
    def get_stats(self):
        """Get current database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Total count
            cursor.execute("SELECT COUNT(*) as total FROM ai_tool")
            total = cursor.fetchone()['total']
            
            # Count by domain
            cursor.execute("""
                SELECT macro_domain, COUNT(*) as count 
                FROM ai_tool 
                GROUP BY macro_domain 
                ORDER BY count DESC
            """)
            domains = {row['macro_domain']: row['count'] for row in cursor.fetchall()}
            
            # Count by source
            cursor.execute("""
                SELECT source, COUNT(*) as count 
                FROM ai_tool 
                GROUP BY source 
                ORDER BY count DESC
            """)
            sources = {row['source']: row['count'] for row in cursor.fetchall()}
            
            # Recent additions (last 24 hours)
            cursor.execute("""
                SELECT name, macro_domain, source 
                FROM ai_tool 
                WHERE datetime(created_at) > datetime('now', '-1 day')
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            recent = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            return {
                'total': total,
                'domains': domains,
                'sources': sources,
                'recent': recent,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e), 'total': 0}
    
    def print_progress(self, target=1000):
        """Print current progress to console"""
        stats = self.get_stats()
        
        if 'error' in stats:
            print(f"❌ Error: {stats['error']}")
            return
        
        total = stats['total']
        progress_pct = (total / target) * 100
        
        print("\n" + "="*50)
        print("🤖 AI UNIVERSE SCRAPING PROGRESS")
        print("="*50)
        print(f"📊 Total AI Tools: {total:,}")
        print(f"🎯 Target: {target:,}")
        print(f"📈 Progress: {progress_pct:.1f}%")
        print(f"⏰ Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Progress bar
        bar_length = 30
        filled = int(bar_length * progress_pct / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"📊 [{bar}] {progress_pct:.1f}%")
        
        print(f"\n🏷️  BY CATEGORY:")
        for domain, count in stats['domains'].items():
            print(f"   {domain}: {count:,} tools")
        
        print(f"\n🔗 BY SOURCE:")
        for source, count in list(stats['sources'].items())[:5]:
            print(f"   {source}: {count:,} tools")
        
        if stats['recent']:
            print(f"\n🆕 RECENT ADDITIONS:")
            for tool in stats['recent'][:5]:
                print(f"   • {tool['name']} ({tool['macro_domain']})")
        
        if total >= target:
            print("\n🎉 TARGET REACHED! Ready for frontend integration!")
        else:
            remaining = target - total
            print(f"\n📝 Still need: {remaining:,} more tools")
        
        print("="*50)
    
    def export_for_frontend(self, output_file='frontend_data.json'):
        """Export data in format ready for frontend"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all tools with required fields
            cursor.execute("""
                SELECT 
                    id,
                    name,
                    description,
                    macro_domain as category,
                    popularity,
                    price,
                    url,
                    rank,
                    monthly_users,
                    source
                FROM ai_tool
                ORDER BY popularity DESC, id
            """)
            
            tools = []
            for i, row in enumerate(cursor.fetchall()):
                tool = dict(row)
                # Add calculated fields
                tool['connections'] = min(50, max(5, int(tool['popularity'] / 2)))
                tool['val'] = max(1, (tool['popularity'] / 100) * 3 + 
                                    (tool['connections'] / 50) * 2)
                tool['rank'] = i + 1
                tools.append(tool)
            
            conn.close()
            
            # Export to JSON
            with open(output_file, 'w') as f:
                json.dump({
                    'tools': tools,
                    'count': len(tools),
                    'exported_at': datetime.now().isoformat()
                }, f, indent=2)
            
            print(f"✅ Exported {len(tools)} tools to {output_file}")
            return len(tools)
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return 0

def monitor_continuous(interval_minutes=5, target=1000):
    """Monitor progress continuously"""
    monitor = ProgressMonitor()
    
    print(f"🔄 Monitoring every {interval_minutes} minutes...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            monitor.print_progress(target)
            
            # Check if target reached
            stats = monitor.get_stats()
            if stats.get('total', 0) >= target:
                print("🎯 Target reached! Monitoring complete.")
                break
            
            time.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped")

def main():
    """Main function"""
    import sys
    
    monitor = ProgressMonitor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'monitor':
            target = 1000
            if len(sys.argv) > 2:
                target = int(sys.argv[2])
            monitor_continuous(target=target)
        elif sys.argv[1] == 'export':
            monitor.export_for_frontend()
        else:
            print("Usage: python monitor_progress.py [monitor|export] [target]")
    else:
        # Single progress check
        monitor.print_progress()

if __name__ == "__main__":
    main()