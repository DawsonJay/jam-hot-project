#!/usr/bin/env python3
"""
Create a simple database dump with just CREATE TABLE and INSERT statements.
"""

import os
import psycopg2
import json
from urllib.parse import urlparse

def get_database_connection():
    """Get database connection using .env values."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5433')
    database = os.getenv('DB_NAME', 'jam_hot')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'Glitter-Nebula-Frost')
    
    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

def create_simple_dump():
    """Create a simple dump file with just CREATE TABLE and INSERT statements."""
    print("Creating simple database dump...")
    
    conn = get_database_connection()
    cursor = conn.cursor()
    
    # Create deploy directory if it doesn't exist
    os.makedirs('deploy', exist_ok=True)
    
    with open('deploy/db-dump.sql', 'w') as f:
        f.write("-- Simple database dump\n")
        f.write("-- Created by create_simple_dump.py\n\n")
        
        # Get sequences first
        cursor.execute("""
            SELECT sequence_name 
            FROM information_schema.sequences 
            WHERE sequence_schema = 'public'
            ORDER BY sequence_name
        """)
        sequences = [row[0] for row in cursor.fetchall()]
        
        if sequences:
            f.write("-- Sequences\n")
            for seq in sequences:
                cursor.execute(f"SELECT last_value FROM {seq}")
                last_val = cursor.fetchone()[0]
                f.write(f"CREATE SEQUENCE public.{seq} START {last_val + 1};\n")
            f.write("\n")
        
        # Get table schemas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"Found tables: {tables}")
        
        # For each table, create the table structure and insert data
        for table in tables:
            print(f"Processing table: {table}")
            
            # Get table structure
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            
            # Create CREATE TABLE statement
            f.write(f"-- Table: {table}\n")
            f.write(f"CREATE TABLE public.{table} (\n")
            
            column_defs = []
            for col_name, data_type, is_nullable, col_default in columns:
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                default = f" DEFAULT {col_default}" if col_default else ""
                column_defs.append(f"    {col_name} {data_type} {nullable}{default}")
            
            f.write(",\n".join(column_defs))
            f.write("\n);\n\n")
            
            # Get and insert data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            if rows:
                # Get column names for INSERT
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' 
                    ORDER BY ordinal_position
                """)
                col_names = [row[0] for row in cursor.fetchall()]
                
                f.write(f"-- Data for table: {table}\n")
                for row in rows:
                    # Format values for SQL
                    formatted_values = []
                    for value in row:
                        if value is None:
                            formatted_values.append("NULL")
                        elif isinstance(value, str):
                            # Escape single quotes
                            escaped = value.replace("'", "''")
                            formatted_values.append(f"'{escaped}'")
                        elif isinstance(value, (list, dict)):
                            # JSON data
                            json_str = json.dumps(value).replace("'", "''")
                            formatted_values.append(f"'{json_str}'")
                        elif hasattr(value, 'isoformat'):  # datetime objects
                            # Format datetime as SQL timestamp
                            formatted_values.append(f"'{value.isoformat()}'")
                        else:
                            formatted_values.append(str(value))
                    
                    col_list = ", ".join(col_names)
                    val_list = ", ".join(formatted_values)
                    f.write(f"INSERT INTO public.{table} ({col_list}) VALUES ({val_list});\n")
                
                f.write("\n")
    
    cursor.close()
    conn.close()
    
    print("✅ Simple dump created: deploy/db-dump.sql")

if __name__ == "__main__":
    create_simple_dump()
