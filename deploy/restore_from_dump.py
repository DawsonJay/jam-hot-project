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
    print("🚀 Restoring Database from Dump File (Updated)")
    print("=" * 50)
    
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
        
        # Execute SQL statements in proper order
        print("📊 Executing SQL statements...")
        
        # Split into individual statements
        statements = [stmt.strip() for stmt in dump_content.split(';') if stmt.strip()]
        
        # Collect statements by type for proper ordering
        create_statements = []
        alter_statements = []
        insert_statements = []
        
        for statement in statements:
            # Clean up the statement (remove extra whitespace and newlines)
            clean_statement = ' '.join(statement.split())
            
            # Skip comments, SET statements, and psql meta-commands
            if (clean_statement.startswith('--') or 
                clean_statement.startswith('SET ') or
                clean_statement.startswith('SELECT pg_catalog') or
                clean_statement.startswith('\\') or
                not clean_statement):
                continue
                
            # Collect statements by type
            if clean_statement.startswith('CREATE '):
                create_statements.append(clean_statement)
            elif clean_statement.startswith('ALTER '):
                alter_statements.append(clean_statement)
            elif clean_statement.startswith('INSERT '):
                insert_statements.append(clean_statement)
        
        # Execute statements in proper order: CREATE first, then ALTER, then INSERT
        executed_count = 0
        
        # Execute CREATE statements first
        print(f"   Executing {len(create_statements)} CREATE statements...")
        for statement in create_statements:
            cursor.execute(statement)
            executed_count += 1
        
        # Execute ALTER statements second
        print(f"   Executing {len(alter_statements)} ALTER statements...")
        for statement in alter_statements:
            cursor.execute(statement)
            executed_count += 1
        
        # Execute INSERT statements last
        print(f"   Executing {len(insert_statements)} INSERT statements...")
        for statement in insert_statements:
            cursor.execute(statement)
            executed_count += 1
            if executed_count % 20 == 0:
                print(f"   Executed {executed_count} statements...")
                    
        print(f"✅ Executed {executed_count} SQL statements successfully")
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
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = restore_from_dump()
    if not success:
        print("💥 Database restoration failed!")
        sys.exit(1)
    else:
        print("🎉 Database restoration completed successfully!")
