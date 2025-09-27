#!/usr/bin/env python3
"""
Simple script to restore database from the dump file.
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def get_railway_connection():
    """Get Railway database connection."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    return psycopg2.connect(database_url)

def restore_from_dump():
    """Restore database from dump file."""
    print("🚀 Restoring Database from Dump File")
    print("=" * 40)
    
    # Check if dump file exists
    if not os.path.exists('db-dump.sql'):
        print("❌ db-dump.sql not found!")
        return False
    
    print(f"📁 Found dump file: {os.path.getsize('db-dump.sql')} bytes")
    
    try:
        # Connect to database first
        print("🔌 Connecting to database...")
        conn = get_railway_connection()
        cursor = conn.cursor()
        
        # Clear existing database
        print("🧹 Clearing existing database...")
        cursor.execute("DROP TABLE IF EXISTS recipe_fruits CASCADE")
        cursor.execute("DROP TABLE IF EXISTS recipes CASCADE")
        cursor.execute("DROP TABLE IF EXISTS profiles CASCADE")
        cursor.execute("DROP TABLE IF EXISTS fruits CASCADE")
        conn.commit()
        print("✅ Existing tables cleared")
        
        # Read the dump file
        print("📖 Reading dump file...")
        with open('db-dump.sql', 'r') as f:
            dump_content = f.read()
        
        # Execute the entire dump
        print("📊 Executing dump file...")
        cursor.execute(dump_content)
        conn.commit()
        
        # Verify the restore
        print("🔍 Verifying restored data...")
        cursor.execute("SELECT COUNT(*) FROM fruits")
        fruit_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = cursor.fetchone()[0]
        
        print(f"✅ Database restoration completed!")
        print(f"   🍓 Fruits: {fruit_count}")
        print(f"   📖 Recipes: {recipe_count}")
        print("   🌐 Real scraped data is now live!")
        
        conn.close()
        
        # Clean up - remove dump file and this script
        print("🧹 Cleaning up...")
        try:
            os.remove('db-dump.sql')
            print("✅ Dump file removed")
        except:
            pass
        
        try:
            os.remove(__file__)
            print("✅ Restore script removed")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Error restoring database: {e}")
        return False

if __name__ == "__main__":
    success = restore_from_dump()
    if not success:
        print("💥 Database restoration failed!")
        sys.exit(1)
    else:
        print("🎉 Database restoration completed successfully!")
