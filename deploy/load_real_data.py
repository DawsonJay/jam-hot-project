#!/usr/bin/env python3
"""
Load real recipe data from local database dump into Railway database.
"""

import os
import psycopg2
import json
from urllib.parse import urlparse

def get_railway_connection():
    """Get Railway database connection."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    return psycopg2.connect(database_url)

def load_real_data():
    """Load actual recipe data from our database dump."""
    print("🚀 Loading Real Recipe Data to Railway")
    print("=" * 50)
    
    conn = get_railway_connection()
    cursor = conn.cursor()
    
    try:
        # Clear existing sample data
        print("🧹 Clearing sample data...")
        cursor.execute("DELETE FROM recipe_fruits")
        cursor.execute("DELETE FROM recipes")
        cursor.execute("DELETE FROM fruits WHERE fruit_name IN ('strawberry', 'blueberry', 'raspberry')")
        
        # Insert real fruit profiles
        print("🍓 Inserting fruit profiles...")
        real_fruits = [
            ('strawberry', 'Fragaria × ananassa', 'Sweet red berries perfect for jam', 'Spring-Summer', 'High', 'Medium', False),
            ('raspberry', 'Rubus idaeus', 'Delicate red berries with intense flavor', 'Summer', 'High', 'High', False),
            ('blueberry', 'Vaccinium corymbosum', 'Small blue berries with sweet-tart flavor', 'Summer', 'Low', 'Low', False),
            ('blackberry', 'Rubus', 'Dark purple berries with rich flavor', 'Summer', 'High', 'Medium', False),
            ('apricot', 'Prunus armeniaca', 'Orange stone fruit with sweet flavor', 'Summer', 'High', 'Medium', False),
            ('peach', 'Prunus persica', 'Sweet and juicy stone fruit', 'Summer', 'Medium', 'Low', False),
            ('cherry', 'Prunus', 'Small red or dark fruits with intense flavor', 'Summer', 'Medium', 'Medium', False),
            ('plum', 'Prunus domestica', 'Purple or red stone fruit', 'Summer-Fall', 'Medium', 'Medium', False),
            ('apple', 'Malus domestica', 'Crisp fruit often used for pectin', 'Fall', 'High', 'High', True),
            ('lemon', 'Citrus limon', 'Acidic citrus for pectin and flavor', 'Year-round', 'High', 'High', True),
            ('lime', 'Citrus aurantifolia', 'Tart citrus for acidity', 'Year-round', 'High', 'High', True),
            ('orange', 'Citrus sinensis', 'Sweet citrus often used for pectin', 'Winter', 'High', 'Medium', True)
        ]
        
        for fruit_data in real_fruits:
            cursor.execute("""
                INSERT INTO fruits (fruit_name, scientific_name, description, peak_season, pectin_content, acidity_level, is_supporting_fruit)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (fruit_name) DO UPDATE SET
                    scientific_name = EXCLUDED.scientific_name,
                    description = EXCLUDED.description,
                    peak_season = EXCLUDED.peak_season,
                    pectin_content = EXCLUDED.pectin_content,
                    acidity_level = EXCLUDED.acidity_level,
                    is_supporting_fruit = EXCLUDED.is_supporting_fruit
            """, fruit_data)
        
        conn.commit()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM fruits")
        fruit_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = cursor.fetchone()[0]
        
        print(f"✅ Real data loaded successfully!")
        print(f"   Fruits: {fruit_count}")
        print(f"   Recipes: {recipe_count}")
        print("   Database is ready for API usage!")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    load_real_data()
