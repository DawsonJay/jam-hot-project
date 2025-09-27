#!/usr/bin/env python3
"""
Restore the real database dump to Railway PostgreSQL.
This replaces the sample data with actual scraped recipe data.
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

def restore_real_database():
    """Restore the real database dump to Railway."""
    print("🚀 Restoring Real Database to Railway")
    print("=" * 50)
    
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
        
        # Clear existing data but keep table structure
        cursor.execute("DELETE FROM recipe_fruits")
        cursor.execute("DELETE FROM recipes") 
        cursor.execute("DELETE FROM profiles")
        cursor.execute("DELETE FROM fruits")
        
        conn.commit()
        conn.close()
        print("✅ Existing data cleared")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        return False
    
    # Restore from dump file
    print("📊 Restoring real database dump...")
    try:
        cmd = [
            'psql',
            f'--host={parsed.hostname}',
            f'--port={parsed.port or 5432}',
            f'--username={parsed.username}',
            f'--dbname={parsed.path[1:]}',  # Remove leading slash
            '--file=real_database_dump.sql',
            '--quiet'
        ]
        
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
        with open('real_database_dump.sql', 'r') as f:
            dump_content = f.read()
        
        conn = get_railway_connection()
        cursor = conn.cursor()
        
        # Execute the dump (this is a simplified approach)
        # In production, you'd want more sophisticated SQL parsing
        cursor.execute(dump_content)
        conn.commit()
        conn.close()
        
        print("✅ Database restored using Python!")
        return True
        
    except Exception as e:
        print(f"❌ Python restoration failed: {e}")
        return False

if __name__ == "__main__":
    success = restore_real_database()
    if not success:
        print("💥 Database restoration failed!")
        sys.exit(1)
    else:
        print("🎉 Database restoration completed successfully!")
