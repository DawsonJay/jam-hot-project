#!/usr/bin/env python3
"""
Fruit extraction script for scraped recipes.

This script processes existing recipes in the database to extract fruits
from ingredients and create recipe-fruit relationships.
"""

import sys
import os
import psycopg2
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.fruit_mappings import extract_fruits_from_text, get_all_ai_names
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

def get_all_recipes(connection):
    """
    Get all recipes from the database.
    
    Args:
        connection: Database connection
        
    Returns:
        List[Dict]: List of recipe dictionaries
    """
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT id, title, ingredients, source_url 
            FROM recipes 
            ORDER BY id
        """)
        
        recipes = []
        for row in cursor.fetchall():
            # Ingredients are already stored as JSON in the database
            ingredients = row[2] if row[2] else []
            if isinstance(ingredients, str):
                ingredients = json.loads(ingredients)
            
            recipe = {
                'id': row[0],
                'title': row[1],
                'ingredients': ingredients,
                'source_url': row[3]
            }
            recipes.append(recipe)
        
        return recipes
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error fetching recipes:")
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()

def extract_fruits_from_recipe(recipe):
    """
    Extract fruits from a recipe's ingredients.
    
    Args:
        recipe: Recipe dictionary with ingredients
        
    Returns:
        List[str]: List of unique fruit AI names found
    """
    all_fruits = set()
    
    # Extract fruits from each ingredient
    for ingredient in recipe['ingredients']:
        # Handle both old format ('ingredient') and new format ('name')
        if isinstance(ingredient, dict):
            ingredient_text = ingredient.get('ingredient', '') or ingredient.get('name', '')
        else:
            # Handle case where ingredient is a string
            ingredient_text = str(ingredient)
        
        if ingredient_text:
            fruits = extract_fruits_from_text(ingredient_text)
            all_fruits.update(fruits)
    
    return list(all_fruits)

def insert_recipe_fruits(connection, recipe_id, fruits, recipe_title=""):
    """
    Insert recipe-fruit relationships into the database with proper primary fruit identification.
    
    Args:
        connection: Database connection
        recipe_id: Recipe ID
        fruits: List of fruit AI names
        recipe_title: Recipe title for primary fruit identification
        
    Returns:
        int: Number of relationships inserted
    """
    cursor = connection.cursor()
    
    try:
        inserted_count = 0
        
        # Import supporting fruits logic
        from scraper.supporting_fruits import is_supporting_fruit
        
        for fruit_name in fruits:
            # Check if fruit exists in fruits table
            cursor.execute("SELECT id FROM fruits WHERE ai_identifier = %s", (fruit_name,))
            fruit_row = cursor.fetchone()
            
            if fruit_row:
                fruit_id = fruit_row[0]
                
                # Check if relationship already exists
                cursor.execute("""
                    SELECT recipe_id FROM recipe_fruits 
                    WHERE recipe_id = %s AND fruit_id = %s
                """, (recipe_id, fruit_id))
                
                if not cursor.fetchone():
                    # Determine if this fruit should be primary
                    is_primary = not is_supporting_fruit(fruit_name)
                    
                    # Insert new relationship with proper primary status
                    cursor.execute("""
                        INSERT INTO recipe_fruits (recipe_id, fruit_id, is_primary)
                        VALUES (%s, %s, %s)
                    """, (recipe_id, fruit_id, is_primary))
                    inserted_count += 1
            else:
                print(f"[{get_timestamp()}] ⚠️  Fruit '{fruit_name}' not found in fruits table")
        
        connection.commit()
        return inserted_count
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error inserting recipe-fruit relationships:")
        print(f"Error: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def ensure_fruits_exist(connection):
    """
    Ensure all fruits from the mapping exist in the fruits table.
    
    Args:
        connection: Database connection
    """
    cursor = connection.cursor()
    
    try:
        all_ai_names = get_all_ai_names()
        inserted_count = 0
        
        for ai_name in all_ai_names:
            # Check if fruit exists
            cursor.execute("SELECT id FROM fruits WHERE ai_identifier = %s", (ai_name,))
            if not cursor.fetchone():
                # Insert new fruit
                cursor.execute("""
                    INSERT INTO fruits (fruit_name, ai_identifier)
                    VALUES (%s, %s)
                """, (ai_name.replace('_', ' ').title(), ai_name))
                inserted_count += 1
        
        connection.commit()
        print(f"[{get_timestamp()}] ✅ Ensured {inserted_count} fruits exist in database")
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error ensuring fruits exist:")
        print(f"Error: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def extract_fruits_from_all_recipes():
    """
    Extract fruits from all recipes in the database.
    """
    print(f"[{get_timestamp()}] Starting fruit extraction from all recipes...")
    
    connection = None
    
    try:
        # Connect to database
        connection = connect_to_database()
        
        # Ensure all fruits exist in the database
        ensure_fruits_exist(connection)
        
        # Get all recipes
        recipes = get_all_recipes(connection)
        print(f"[{get_timestamp()}] Found {len(recipes)} recipes to process")
        
        total_relationships = 0
        
        # Process each recipe
        for i, recipe in enumerate(recipes, 1):
            print(f"[{get_timestamp()}] Processing recipe {i}/{len(recipes)}: {recipe['title']}")
            
            # Extract fruits from ingredients
            fruits = extract_fruits_from_recipe(recipe)
            
            if fruits:
                print(f"[{get_timestamp()}] Found fruits: {fruits}")
                
                # Insert recipe-fruit relationships with proper primary identification
                inserted_count = insert_recipe_fruits(connection, recipe['id'], fruits, recipe.get('title', ''))
                total_relationships += inserted_count
                
                print(f"[{get_timestamp()}] ✅ Inserted {inserted_count} fruit relationships")
            else:
                print(f"[{get_timestamp()}] ⚠️  No fruits found in ingredients")
        
        print(f"[{get_timestamp()}] ✅ Fruit extraction complete!")
        print(f"[{get_timestamp()}] Total recipe-fruit relationships created: {total_relationships}")
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Fruit extraction failed:")
        print(f"Error: {e}")
        raise
    finally:
        if connection:
            connection.close()
            print(f"[{get_timestamp()}] Database connection closed")

def main():
    """Main function for testing the script."""
    print(f"[{get_timestamp()}] Fruit extraction script starting...")
    
    try:
        extract_fruits_from_all_recipes()
        print(f"[{get_timestamp()}] Test completed successfully!")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Test failed:")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
