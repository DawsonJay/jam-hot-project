#!/usr/bin/env python3
"""
Database restoration script for Railway deployment.
Restores the database dump to the Railway PostgreSQL instance.
"""

import os
import subprocess
import sys
import psycopg2
from urllib.parse import urlparse

def get_database_url():
    """Get the database URL from environment variables."""
    # Railway provides DATABASE_URL automatically
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Fallback to individual components
        host = os.getenv('PGHOST', 'localhost')
        port = os.getenv('PGPORT', '5432')
        database = os.getenv('PGDATABASE', 'jam_hot')
        user = os.getenv('PGUSER', 'postgres')
        password = os.getenv('PGPASSWORD', '')
        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    return database_url

def parse_database_url(database_url):
    """Parse database URL into components."""
    parsed = urlparse(database_url)
    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:],  # Remove leading slash
        'user': parsed.username,
        'password': parsed.password
    }

def test_connection(db_config):
    """Test database connection."""
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def restore_database():
    """Restore database from dump file."""
    print("🗄️  Starting database restoration...")
    
    # Get database configuration
    database_url = get_database_url()
    db_config = parse_database_url(database_url)
    
    print(f"📡 Connecting to: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    
    # Test connection
    if not test_connection(db_config):
        print("❌ Failed to connect to database")
        return False
    
    print("✅ Database connection successful")
    
    # Check if dump file exists
    dump_file = os.path.join(os.path.dirname(__file__), 'database_dump.sql')
    if not os.path.exists(dump_file):
        print(f"❌ Dump file not found: {dump_file}")
        return False
    
    print(f"📄 Found dump file: {os.path.basename(dump_file)}")
    
    # Set environment variables for psql
    env = os.environ.copy()
    env['PGHOST'] = str(db_config['host'])
    env['PGPORT'] = str(db_config['port'])
    env['PGDATABASE'] = db_config['database']
    env['PGUSER'] = db_config['user']
    env['PGPASSWORD'] = db_config['password']
    
    try:
        # Run psql to restore the dump
        print("🔄 Restoring database...")
        result = subprocess.run(
            ['psql', '-f', dump_file],
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Database restoration completed successfully!")
            print("📊 Checking restored data...")
            
            # Verify restoration by counting records
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
            
            cur = conn.cursor()
            
            # Count recipes
            cur.execute("SELECT COUNT(*) FROM recipes")
            recipe_count = cur.fetchone()[0]
            
            # Count fruit profiles
            cur.execute("SELECT COUNT(*) FROM fruit_profiles")
            fruit_count = cur.fetchone()[0]
            
            # Count recipe-fruit relationships
            cur.execute("SELECT COUNT(*) FROM recipe_fruits")
            relationship_count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            print(f"📈 Restored data:")
            print(f"   - Recipes: {recipe_count}")
            print(f"   - Fruit profiles: {fruit_count}")
            print(f"   - Recipe-fruit relationships: {relationship_count}")
            
            return True
        else:
            print(f"❌ Database restoration failed:")
            print(f"   Return code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ psql command not found. Make sure PostgreSQL client is installed.")
        return False
    except Exception as e:
        print(f"❌ Restoration failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Jam Hot Database Restoration")
    print("=" * 40)
    
    success = restore_database()
    
    if success:
        print("\n🎉 Database restoration completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Database restoration failed!")
        sys.exit(1)
