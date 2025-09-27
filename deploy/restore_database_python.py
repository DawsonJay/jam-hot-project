#!/usr/bin/env python3
"""
Python-based database restoration script for Railway deployment.
Creates tables and inserts data using Python instead of psql.
"""

import os
import psycopg2
from urllib.parse import urlparse
import json

def get_database_url():
    """Get the database URL from environment variables."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return None
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

def create_connection():
    """Create database connection."""
    database_url = get_database_url()
    if not database_url:
        return None
    
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def create_tables(conn):
    """Create the database tables."""
    print("🏗️  Creating database tables...")
    
    cursor = conn.cursor()
    
    # Create fruits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fruits (
            id SERIAL PRIMARY KEY,
            fruit_name VARCHAR(100) UNIQUE NOT NULL,
            scientific_name VARCHAR(200),
            description TEXT,
            peak_season VARCHAR(100),
            pectin_content VARCHAR(50),
            acidity_level VARCHAR(50),
            color VARCHAR(50),
            flavor_profile TEXT,
            best_for_jam BOOLEAN DEFAULT true,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create recipes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            ingredients TEXT,
            instructions TEXT,
            rating DECIMAL(3,2),
            review_count INTEGER,
            source VARCHAR(100),
            source_url TEXT,
            image_url TEXT,
            servings VARCHAR(50),
            prep_time VARCHAR(50),
            cook_time VARCHAR(50),
            total_time VARCHAR(50),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create recipe_fruits table (many-to-many relationship)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_fruits (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
            fruit_id INTEGER REFERENCES fruits(id) ON DELETE CASCADE,
            is_primary BOOLEAN DEFAULT false,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(recipe_id, fruit_id)
        )
    """)
    
    conn.commit()
    print("✅ Database tables created successfully!")
    return True

def insert_sample_data(conn):
    """Insert sample data for testing."""
    print("📊 Inserting sample data...")
    
    cursor = conn.cursor()
    
    # Insert sample fruits
    sample_fruits = [
        ('strawberry', 'Fragaria × ananassa', 'Sweet red berries perfect for jam', 'Spring-Summer', 'High', 'Medium', 'Red', 'Sweet and tangy'),
        ('blueberry', 'Vaccinium corymbosum', 'Small blue berries with intense flavor', 'Summer', 'Low', 'Low', 'Blue', 'Sweet and slightly tart'),
        ('raspberry', 'Rubus idaeus', 'Delicate red berries', 'Summer', 'High', 'High', 'Red', 'Tart and sweet')
    ]
    
    for fruit_data in sample_fruits:
        cursor.execute("""
            INSERT INTO fruits (fruit_name, scientific_name, description, peak_season, pectin_content, acidity_level, color, flavor_profile)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (fruit_name) DO NOTHING
        """, fruit_data)
    
    # Insert sample recipes
    sample_recipes = [
        ('Strawberry Jam', '["strawberries", "sugar", "lemon juice"]', '["Wash and hull strawberries", "Combine with sugar", "Cook until thickened"]', 4.5, 25, 'AllRecipes', 'https://example.com/strawberry-jam', 'https://example.com/strawberry.jpg', '4 jars', '15 min', '20 min', '35 min'),
        ('Blueberry Jam', '["blueberries", "sugar", "lemon juice", "pectin"]', '["Wash blueberries", "Mash slightly", "Add sugar and pectin", "Boil until set"]', 4.8, 18, 'BBC Good Food', 'https://example.com/blueberry-jam', 'https://example.com/blueberry.jpg', '3 jars', '10 min', '15 min', '25 min')
    ]
    
    for recipe_data in sample_recipes:
        cursor.execute("""
            INSERT INTO recipes (title, ingredients, instructions, rating, review_count, source, source_url, image_url, servings, prep_time, cook_time, total_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, recipe_data)
    
    conn.commit()
    print("✅ Sample data inserted successfully!")
    return True

def main():
    """Main restoration function."""
    print("🚀 Jam Hot Database Setup")
    print("=" * 40)
    
    # Create connection
    conn = create_connection()
    if not conn:
        print("💥 Database setup failed!")
        return False
    
    print("✅ Database connection successful")
    
    # Create tables
    if not create_tables(conn):
        print("💥 Table creation failed!")
        return False
    
    # Insert sample data
    if not insert_sample_data(conn):
        print("💥 Sample data insertion failed!")
        return False
    
    # Test the setup
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fruits")
    fruit_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM recipes")
    recipe_count = cursor.fetchone()[0]
    
    print(f"📊 Database setup complete!")
    print(f"   Fruits: {fruit_count}")
    print(f"   Recipes: {recipe_count}")
    
    conn.close()
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
