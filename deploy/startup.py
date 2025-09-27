#!/usr/bin/env python3
"""
Railway startup script - forces database setup before starting FastAPI.
"""

import os
import sys
import subprocess

def main():
    print("🚀 Jam Hot API - Railway Startup")
    print("=" * 50)
    
    # Step 1: Test database connection
    print("🔍 Step 1: Testing database connection...")
    try:
        result = subprocess.run([sys.executable, "test_db.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Database connection test passed!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Database connection test failed: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    
    # Step 2: Restore database from dump
    print("\n📊 Step 2: Restoring database from dump file...")
    try:
        result = subprocess.run([sys.executable, "restore_from_dump.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Database restored from dump!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Database restoration failed: {e}")
        print(f"Error output: {e.stderr}")
        print(f"Standard output: {e.stdout}")
        # Don't exit - continue with basic setup
        print("⚠️  Continuing with basic database setup...")
        
        # Fallback to basic schema
        try:
            result = subprocess.run([sys.executable, "restore_database_python.py"], 
                                  capture_output=True, text=True, check=True)
            print("✅ Basic database schema created as fallback!")
        except subprocess.CalledProcessError as fallback_error:
            print(f"❌ Fallback schema creation also failed: {fallback_error}")
            print("⚠️  Continuing with empty database...")
    
    # Step 3: Start FastAPI
    print("\n🌐 Step 3: Starting FastAPI server...")
    print("=" * 50)
    
    # Start uvicorn
    os.execvp("uvicorn", ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", os.getenv("PORT", "8080")])

if __name__ == "__main__":
    main()
