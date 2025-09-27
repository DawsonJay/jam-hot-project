#!/usr/bin/env python3
"""
Test database connection and create tables manually.
"""

import os
import psycopg2
from urllib.parse import urlparse

def test_connection():
    """Test database connection and create tables."""
    print("🔍 Testing database connection...")
    
    # Get DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    print(f"📡 DATABASE_URL: {database_url[:20]}...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        print("✅ Database connection successful!")
        
        cursor = conn.cursor()
        
        # Create a simple test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO test_table (name) VALUES ('test') ON CONFLICT DO NOTHING")
        
        # Query test data
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]
        
        print(f"✅ Test table created and populated! Records: {count}")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
