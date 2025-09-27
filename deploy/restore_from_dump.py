#!/usr/bin/env python3
"""
Simple script to restore database from the dump file.
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse
import subprocess

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
    
    # Get database connection details
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    parsed = urlparse(database_url)
    
    # Set environment variables for psql
    env = os.environ.copy()
    env['PGPASSWORD'] = parsed.password
    
    print("🧹 Clearing existing data...")
    try:
        conn = get_railway_connection()
        cursor = conn.cursor()
        
        # Drop all tables to start fresh
        cursor.execute("DROP TABLE IF EXISTS recipe_fruits CASCADE")
        cursor.execute("DROP TABLE IF EXISTS recipes CASCADE")
        cursor.execute("DROP TABLE IF EXISTS profiles CASCADE")
        cursor.execute("DROP TABLE IF EXISTS fruits CASCADE")
        
        conn.commit()
        conn.close()
        print("✅ Existing tables cleared")
        
    except Exception as e:
        print(f"❌ Error clearing tables: {e}")
        return False
    
    # Restore from dump file
    print("📊 Restoring from dump file...")
    try:
        cmd = [
            'psql',
            f'--host={parsed.hostname}',
            f'--port={parsed.port or 5432}',
            f'--username={parsed.username}',
            f'--dbname={parsed.path[1:]}',  # Remove leading slash
            '--file=db-dump.sql',
            '--quiet'
        ]
        
        print(f"🔧 Running: {' '.join(cmd[:4])}...")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database dump restored successfully!")
        else:
            print(f"❌ psql failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ psql command not found - trying Python approach...")
        return restore_with_python()
    except Exception as e:
        print(f"❌ Error running psql: {e}")
        return False
    
    # Verify the restore
    print("🔍 Verifying restored data...")
    try:
        conn = get_railway_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM fruits")
        fruit_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipe_fruits")
        link_count = cursor.fetchone()[0]
        
        print(f"✅ Database restoration verified!")
        print(f"   🍓 Fruits: {fruit_count}")
        print(f"   📖 Recipes: {recipe_count}")
        print(f"   🔗 Recipe-Fruit Links: {link_count}")
        print("   🌐 Real scraped data is now live!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def restore_with_python():
    """Fallback: restore using Python if psql is not available."""
    print("🐍 Using Python fallback for restoration...")
    
    try:
        # Read the dump file
        with open('db-dump.sql', 'r') as f:
            dump_content = f.read()
        
        conn = get_railway_connection()
        cursor = conn.cursor()
        
        # Execute the dump (this is a simplified approach)
        cursor.execute(dump_content)
        conn.commit()
        conn.close()
        
        print("✅ Database restored using Python!")
        return True
        
    except Exception as e:
        print(f"❌ Python restoration failed: {e}")
        return False

if __name__ == "__main__":
    success = restore_from_dump()
    if not success:
        print("💥 Database restoration failed!")
        sys.exit(1)
    else:
        print("🎉 Database restoration completed successfully!")
