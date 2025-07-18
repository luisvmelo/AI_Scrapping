#!/usr/bin/env python3
"""
Easy Startup Script for AI Universe Scraping
Run this to start autonomous scraping with zero credit consumption!
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_banner():
    print("🤖" + "="*58 + "🤖")
    print("   AI UNIVERSE AUTONOMOUS SCRAPER - ZERO CREDIT MODE")
    print("🤖" + "="*58 + "🤖")
    print()
    print("This script will:")
    print("✅ Run scrapers autonomously on your machine")
    print("✅ Build database to 1000+ AI tools")
    print("✅ Consume ZERO AI credits")
    print("✅ Save all progress automatically")
    print("✅ Update frontend when ready")
    print()

def check_requirements():
    """Check if environment is ready"""
    print("🔍 Checking requirements...")
    
    # Check if we're in the right directory
    if not Path('autonomous_scraper.py').exists():
        print("❌ Please run this from the AI_Scrapping directory")
        return False
    
    # Check if database exists
    if not Path('database/ai_tools.db').exists():
        print("❌ Database not found. Please run setup first.")
        return False
    
    # Check if scrapers directory exists
    if not Path('scrapers').exists():
        print("❌ Scrapers directory not found")
        return False
    
    print("✅ Environment ready!")
    return True

def show_menu():
    """Show main menu"""
    print("\n🚀 AUTONOMOUS SCRAPING OPTIONS:")
    print("1. 📊 Check current progress")
    print("2. 🤖 Start autonomous scraping (1000 tools)")
    print("3. 🎯 Custom target scraping")
    print("4. 🔄 Monitor progress continuously")
    print("5. 📤 Export data for frontend")
    print("6. 🖥️  Start API server")
    print("7. 🌐 Test frontend")
    print("0. ❌ Exit")
    print()
    
    choice = input("Choose option (0-7): ").strip()
    return choice

def run_command(cmd, description):
    """Run a command with nice output"""
    print(f"\n🚀 {description}")
    print(f"Running: {cmd}")
    print("-" * 40)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n⏹️  Command stopped by user")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print_banner()
    
    if not check_requirements():
        print("💡 Please fix the issues above and try again")
        return
    
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("👋 Goodbye! Your progress is saved.")
            break
            
        elif choice == '1':
            print("\n📊 Checking current progress...")
            run_command("python monitor_progress.py", "Getting current database stats")
            
        elif choice == '2':
            print("\n🤖 Starting autonomous scraping to 1000 tools...")
            print("This will run independently without consuming AI credits!")
            print("Press Ctrl+C to stop at any time (progress will be saved)")
            input("\nPress Enter to start or Ctrl+C to cancel...")
            run_command("python autonomous_scraper.py 1000", "Running autonomous scraper")
            
        elif choice == '3':
            try:
                target = int(input("Enter target number of tools: "))
                if target < 1:
                    print("❌ Target must be positive")
                    continue
                print(f"\n🎯 Starting autonomous scraping to {target} tools...")
                input("\nPress Enter to start or Ctrl+C to cancel...")
                run_command(f"python autonomous_scraper.py {target}", f"Running autonomous scraper (target: {target})")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == '4':
            print("\n🔄 Starting continuous monitoring...")
            print("This will check progress every 5 minutes")
            print("Press Ctrl+C to stop monitoring")
            input("\nPress Enter to start or Ctrl+C to cancel...")
            run_command("python monitor_progress.py monitor", "Monitoring progress")
            
        elif choice == '5':
            print("\n📤 Exporting data for frontend...")
            run_command("python monitor_progress.py export", "Exporting frontend data")
            
        elif choice == '6':
            print("\n🖥️  Starting API server...")
            print("This will start the backend API for the frontend")
            print("Press Ctrl+C to stop the server")
            input("\nPress Enter to start or Ctrl+C to cancel...")
            run_command("python api_server_sqlite.py", "Starting API server")
            
        elif choice == '7':
            print("\n🌐 Testing frontend...")
            print("This will check if the frontend can connect to real data")
            
            # Check if API is running
            try:
                import requests
                response = requests.get('http://localhost:5000/api/graph/nodes?limit=1', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('nodes', []))
                    print(f"✅ API is running with {count} tools available")
                    print("🌐 Frontend will automatically use real data!")
                    print("🔗 Open: http://localhost:4173/")
                else:
                    print("❌ API is not responding correctly")
            except Exception as e:
                print("❌ API is not running. Please start it first (option 6)")
                
        else:
            print("❌ Invalid choice. Please enter 0-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()