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
        
        # Parse and execute SQL statements and COPY data
        print("📊 Parsing and executing dump file...")
        
        lines = dump_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip psql meta-commands and comments
            if (line.startswith('\\') or 
                line.startswith('--') or 
                line.startswith('SET ') or
                line.startswith('SELECT pg_catalog') or
                line == ''):
                i += 1
                continue
            
            # Handle COPY statements (these contain the actual data!)
            if line.startswith('COPY '):
                print(f"   Processing COPY statement...")
                # Execute the COPY statement
                cursor.execute(line)
                
                # Read data lines until we hit a period
                i += 1
                data_lines = []
                while i < len(lines) and lines[i].strip() != '\\.':
                    data_lines.append(lines[i])
                    i += 1
                
                # Insert data using INSERT statements instead of COPY
                if data_lines:
                    # Parse the COPY statement to get table and columns
                    copy_parts = line.split('(')
                    table_part = copy_parts[0].replace('COPY ', '').strip()
                    columns_part = copy_parts[1].replace(')', '').strip()
                    columns = [col.strip() for col in columns_part.split(',')]
                    
                    # Convert COPY data to INSERT statements
                    for data_line in data_lines:
                        if data_line.strip():
                            values = data_line.split('\t')
                            if len(values) == len(columns):
                                placeholders = ', '.join(['%s'] * len(values))
                                insert_sql = f"INSERT INTO {table_part} ({columns_part}) VALUES ({placeholders})"
                                cursor.execute(insert_sql, values)
                
                i += 1
                continue
                
            # Handle regular SQL statements (only CREATE, ALTER, DROP, etc.)
            if (line.endswith(';') and 
                (line.startswith('CREATE ') or 
                 line.startswith('ALTER ') or 
                 line.startswith('DROP ') or
                 line.startswith('INSERT ') or
                 line.startswith('UPDATE ') or
                 line.startswith('DELETE '))):
                print(f"   Executing SQL statement...")
                cursor.execute(line)
            
            i += 1
        
        print("✅ Dump file processed successfully")
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
