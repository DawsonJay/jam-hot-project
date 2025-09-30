#!/usr/bin/env python3
"""
Database insertion script for scraped recipes.

This script handles inserting scraped recipe data into the PostgreSQL database,
including duplicate checking and error handling.
"""

import sys
import os
import psycopg2
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def get_timestamp():
    """Get current timestamp for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def connect_to_database():
    """
    Connect to the PostgreSQL database.
    
    Returns:
        psycopg2.connection: Database connection object
        
    Raises:
        psycopg2.Error: If connection fails
    """
    print(f"[{get_timestamp()}] Connecting to database...")
    
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5433")),
            database=os.getenv("DB_NAME", "jam_hot"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD")
        )
        
        # Test the connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        
        print(f"[{get_timestamp()}] ✅ Database connection successful")
        return connection
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Database connection failed:")
        print(f"Error: {e}")
        raise

def check_duplicate_recipe(connection, recipe_data: Dict[str, Any]) -> bool:
    """
    Check if a recipe already exists in the database.
    
    Args:
        connection: Database connection
        recipe_data: Recipe data dictionary
        
    Returns:
        bool: True if duplicate exists, False otherwise
    """
    cursor = connection.cursor()
    
    try:
        # Check for duplicates by source_url OR title
        # Same URL = same recipe (even if title differs)
        # Same title = same recipe (even if URL differs)
        cursor.execute("""
            SELECT id FROM recipes 
            WHERE source_url = %s OR title = %s
        """, (recipe_data['source_url'], recipe_data['title']))
        
        result = cursor.fetchone()
        return result is not None
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error checking for duplicates:")
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()

def insert_recipe(connection, recipe_data: Dict[str, Any]) -> int:
    """
    Insert a single recipe into the database.
    
    Args:
        connection: Database connection
        recipe_data: Recipe data dictionary
        
    Returns:
        int: The ID of the inserted recipe
        
    Raises:
        psycopg2.Error: If insertion fails
    """
    cursor = connection.cursor()
    
    try:
        # Check for duplicates first
        if check_duplicate_recipe(connection, recipe_data):
            print(f"[{get_timestamp()}] ⚠️  Duplicate recipe found: {recipe_data['title']}")
            print(f"[{get_timestamp()}] ⚠️  Skipping duplicate recipe")
            return None
        
        # Prepare the insert query
        insert_query = """
            INSERT INTO recipes (
                title, ingredients, instructions, rating, review_count,
                source, source_url, image_url, servings, prep_time, cook_time, total_time
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
        """
        
        # Extract time info
        time_info = recipe_data.get('time_info', {})
        prep_time = time_info.get('prep_time', '')
        cook_time = time_info.get('cook_time', '')
        total_time = time_info.get('total_time', '')
        
        # Prepare data for insertion
        values = (
            recipe_data['title'],
            json.dumps(recipe_data['ingredients']),  # Convert to JSONB
            json.dumps(recipe_data['instructions']),  # Convert to JSONB
            recipe_data['rating'],
            recipe_data['review_count'],
            recipe_data['source'],
            recipe_data['source_url'],
            recipe_data['image_url'],
            recipe_data.get('servings', ''),
            prep_time,
            cook_time,
            total_time
        )
        
        # Execute the insert
        cursor.execute(insert_query, values)
        recipe_id = cursor.fetchone()[0]
        
        # Commit the transaction
        connection.commit()
        
        print(f"[{get_timestamp()}] ✅ Recipe inserted successfully: {recipe_data['title']} (ID: {recipe_id})")
        return recipe_id
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error inserting recipe:")
        print(f"Error: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def insert_recipes(recipes: List[Dict[str, Any]]) -> List[int]:
    """
    Insert multiple recipes into the database.
    
    Args:
        recipes: List of recipe data dictionaries
        
    Returns:
        List[int]: List of inserted recipe IDs
        
    Raises:
        psycopg2.Error: If any insertion fails
    """
    print(f"[{get_timestamp()}] Starting recipe insertion...")
    print(f"[{get_timestamp()}] Processing {len(recipes)} recipes")
    
    connection = None
    recipe_ids = []
    
    try:
        # Connect to database
        connection = connect_to_database()
        
        # Insert each recipe
        for i, recipe in enumerate(recipes, 1):
            print(f"[{get_timestamp()}] Processing recipe {i}/{len(recipes)}: {recipe['title']}")
            
            recipe_id = insert_recipe(connection, recipe)
            if recipe_id:
                recipe_ids.append(recipe_id)
        
        print(f"[{get_timestamp()}] ✅ Recipe insertion complete!")
        print(f"[{get_timestamp()}] Successfully inserted {len(recipe_ids)} recipes")
        
        return recipe_ids
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Recipe insertion failed:")
        print(f"Error: {e}")
        raise
    finally:
        if connection:
            connection.close()
            print(f"[{get_timestamp()}] Database connection closed")

def main():
    """Main function for testing the script."""
    print(f"[{get_timestamp()}] Database insertion script starting...")
    
    # Test with sample data - same title, different URL
    sample_recipe = {
        "title": "Test Strawberry Jam",  # Same title as existing
        "ingredients": [
            {
                "item": "2 pounds fresh strawberries, hulled",
                "quantity": "2",
                "unit": "pounds",
                "name": "fresh strawberries, hulled"
            }
        ],
        "instructions": [
            "Gather all ingredients.",
            "Crush strawberries in a wide bowl."
        ],
        "rating": 4.5,
        "review_count": 100,
        "source": "Test",
        "source_url": "https://test.com/recipe/2",  # Different URL
        "image_url": "https://test.com/image.jpg",
        "servings": "40 servings",
        "time_info": {}
    }
    
    try:
        recipe_ids = insert_recipes([sample_recipe])
        print(f"[{get_timestamp()}] Test completed successfully!")
        print(f"[{get_timestamp()}] Inserted recipe IDs: {recipe_ids}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Test failed:")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
