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
        
        # Drop test table if it exists
        cursor.execute("DROP TABLE IF EXISTS test_table")
        
        # Test basic connection with a simple query
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()[0]
        
        print(f"✅ Database connection test passed! Query result: {result}")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
