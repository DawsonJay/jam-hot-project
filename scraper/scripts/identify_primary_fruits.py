#!/usr/bin/env python3
"""
Primary fruit identification script for jam recipes.

This script identifies which fruits in recipes should be marked as primary vs secondary
based on recipe titles and supporting fruit classification.

Usage:
    python identify_primary_fruits.py --recipe-id 5          # Process specific recipe
    python identify_primary_fruits.py --all                  # Process all recipes
    python identify_primary_fruits.py --fruits strawberry,blueberry  # Process recipes with specific fruits
    python identify_primary_fruits.py --dry-run --all        # See changes without updating database
    python identify_primary_fruits.py --verbose --recipe-id 5 # Detailed output
"""

import sys
import os
import argparse
import psycopg2
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Set

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.fruit_mappings import extract_fruits_from_text, get_all_ai_names
from scraper.supporting_fruits import is_supporting_fruit
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

def extract_fruits_from_title(title: str) -> Set[str]:
    """
    Extract fruits mentioned in a recipe title.
    
    Args:
        title (str): Recipe title
        
    Returns:
        Set[str]: Set of fruit AI names found in the title
    """
    # Extract fruits from the title using our fruit mapping system
    fruits_in_title = set(extract_fruits_from_text(title))
    
    # Also look for compound fruits like "strawberry rhubarb"
    # Split on common separators and check each part
    title_parts = re.split(r'[,\s\-&]+', title.lower())
    for part in title_parts:
        part_fruits = extract_fruits_from_text(part)
        fruits_in_title.update(part_fruits)
    
    return fruits_in_title

def get_recipe_fruits(connection, recipe_id: int) -> Dict[str, Any]:
    """
    Get all fruits associated with a recipe.
    
    Args:
        connection: Database connection
        recipe_id: Recipe ID
        
    Returns:
        Dict with recipe info and associated fruits
    """
    cursor = connection.cursor()
    
    try:
        # Get recipe details
        cursor.execute("""
            SELECT r.id, r.title, r.ingredients, f.id as fruit_id, f.fruit_name, f.ai_identifier, rf.is_primary
            FROM recipes r
            LEFT JOIN recipe_fruits rf ON r.id = rf.recipe_id
            LEFT JOIN fruits f ON rf.fruit_id = f.id
            WHERE r.id = %s
        """, (recipe_id,))
        
        rows = cursor.fetchall()
        if not rows:
            return None
        
        # Parse the first row for recipe info
        recipe_id, title, ingredients, fruit_id, fruit_name, ai_identifier, is_primary = rows[0]
        
        recipe_info = {
            'id': recipe_id,
            'title': title,
            'ingredients': ingredients if ingredients else [],
            'fruits': []
        }
        
        # Parse all fruit relationships
        for row in rows:
            if row[3]:  # fruit_id is not None
                recipe_info['fruits'].append({
                    'fruit_id': row[3],
                    'fruit_name': row[4],
                    'ai_identifier': row[5],
                    'is_primary': row[6]
                })
        
        return recipe_info
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error fetching recipe fruits:")
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()

def identify_primary_fruits_for_recipe(recipe_info: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Identify which fruits should be primary vs secondary for a recipe.
    
    Args:
        recipe_info: Recipe information with title, ingredients, and current fruits
        verbose: Whether to show detailed output
        
    Returns:
        Dict with analysis results and recommended changes
    """
    title = recipe_info['title']
    ingredients = recipe_info['ingredients']
    current_fruits = recipe_info['fruits']
    
    if verbose:
        print(f"    Analyzing recipe: '{title}'")
    
    # Extract fruits from title
    title_fruits = extract_fruits_from_title(title)
    if verbose:
        print(f"    Fruits in title: {list(title_fruits)}")
    
    # Extract fruits from ingredients
    ingredient_fruits = set()
    for ingredient in ingredients:
        if isinstance(ingredient, dict):
            ingredient_text = ingredient.get('ingredient', '') or ingredient.get('name', '')
        else:
            ingredient_text = str(ingredient)
        
        if ingredient_text:
            fruits = extract_fruits_from_text(ingredient_text)
            ingredient_fruits.update(fruits)
    
    if verbose:
        print(f"    Fruits in ingredients: {list(ingredient_fruits)}")
    
    # Determine primary vs secondary classification
    analysis = {
        'recipe_id': recipe_info['id'],
        'title': title,
        'title_fruits': list(title_fruits),
        'ingredient_fruits': list(ingredient_fruits),
        'recommendations': [],
        'changes_needed': False
    }
    
    # Process each fruit in the recipe
    for fruit_info in current_fruits:
        ai_identifier = fruit_info['ai_identifier']
        current_is_primary = fruit_info['is_primary']
        
        # Determine if this fruit should be primary
        should_be_primary = False
        
        # Rule 1: If fruit is in title, it's primary
        if ai_identifier in title_fruits:
            should_be_primary = True
            reason = "mentioned in title"
        
        # Rule 2: If fruit is in ingredients but not supporting, it's primary
        elif ai_identifier in ingredient_fruits and not is_supporting_fruit(ai_identifier):
            should_be_primary = True
            reason = "in ingredients and not a supporting fruit"
        
        # Rule 3: If fruit is supporting, it's secondary
        elif is_supporting_fruit(ai_identifier):
            should_be_primary = False
            reason = "supporting fruit (pectin/acidity/bulk)"
        
        # Rule 4: Default to secondary for any other case
        else:
            should_be_primary = False
            reason = "not in title and not clearly primary"
        
        # Check if change is needed
        if current_is_primary != should_be_primary:
            analysis['changes_needed'] = True
            analysis['recommendations'].append({
                'fruit_name': fruit_info['fruit_name'],
                'ai_identifier': ai_identifier,
                'current_primary': current_is_primary,
                'recommended_primary': should_be_primary,
                'reason': reason
            })
            
            if verbose:
                status_change = "primary → secondary" if current_is_primary else "secondary → primary"
                print(f"    {fruit_info['fruit_name']}: {status_change} ({reason})")
    
    return analysis

def update_recipe_fruit_relationships(connection, analysis: Dict[str, Any], dry_run: bool = False) -> int:
    """
    Update the recipe-fruit relationships based on analysis.
    
    Args:
        connection: Database connection
        analysis: Analysis results with recommendations
        dry_run: If True, don't actually update the database
        
    Returns:
        int: Number of relationships updated
    """
    if not analysis['changes_needed']:
        return 0
    
    if dry_run:
        print(f"    [DRY RUN] Would update {len(analysis['recommendations'])} relationships")
        return len(analysis['recommendations'])
    
    cursor = connection.cursor()
    updated_count = 0
    
    try:
        for rec in analysis['recommendations']:
            cursor.execute("""
                UPDATE recipe_fruits 
                SET is_primary = %s 
                WHERE recipe_id = %s AND fruit_id = (
                    SELECT id FROM fruits WHERE ai_identifier = %s
                )
            """, (rec['recommended_primary'], analysis['recipe_id'], rec['ai_identifier']))
            
            if cursor.rowcount > 0:
                updated_count += 1
        
        connection.commit()
        return updated_count
        
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error updating recipe-fruit relationships:")
        print(f"Error: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def process_recipe(connection, recipe_id: int, dry_run: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """
    Process a single recipe to identify primary fruits.
    
    Args:
        connection: Database connection
        recipe_id: Recipe ID to process
        dry_run: If True, don't actually update the database
        verbose: Whether to show detailed output
        
    Returns:
        Dict with processing results
    """
    if verbose:
        print(f"  Processing recipe ID {recipe_id}...")
    
    # Get recipe information
    recipe_info = get_recipe_fruits(connection, recipe_id)
    if not recipe_info:
        print(f"    ❌ Recipe ID {recipe_id} not found")
        return {'success': False, 'error': 'Recipe not found'}
    
    # Analyze the recipe
    analysis = identify_primary_fruits_for_recipe(recipe_info, verbose)
    
    # Update relationships if needed
    updated_count = 0
    if analysis['changes_needed']:
        updated_count = update_recipe_fruit_relationships(connection, analysis, dry_run)
        if not dry_run:
            print(f"    ✅ Updated {updated_count} relationships")
    
    return {
        'success': True,
        'recipe_id': recipe_id,
        'title': analysis['title'],
        'changes_needed': analysis['changes_needed'],
        'updated_count': updated_count,
        'recommendations': analysis['recommendations']
    }

def get_recipes_to_process(connection, recipe_id: Optional[int] = None, all_recipes: bool = False, fruit_names: Optional[List[str]] = None) -> List[int]:
    """
    Get list of recipe IDs to process based on criteria.
    
    Args:
        connection: Database connection
        recipe_id: Specific recipe ID
        all_recipes: Process all recipes
        fruit_names: Process recipes containing specific fruits
        
    Returns:
        List[int]: List of recipe IDs to process
    """
    cursor = connection.cursor()
    
    try:
        if recipe_id:
            # Check if specific recipe exists
            cursor.execute("SELECT id FROM recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone():
                return [recipe_id]
            else:
                return []
        
        elif all_recipes:
            # Get all recipe IDs
            cursor.execute("SELECT id FROM recipes ORDER BY id")
            return [row[0] for row in cursor.fetchall()]
        
        elif fruit_names:
            # Get recipes containing specific fruits
            placeholders = ','.join(['%s'] * len(fruit_names))
            cursor.execute(f"""
                SELECT DISTINCT r.id 
                FROM recipes r
                JOIN recipe_fruits rf ON r.id = rf.recipe_id
                JOIN fruits f ON rf.fruit_id = f.id
                WHERE f.ai_identifier IN ({placeholders})
                ORDER BY r.id
            """, fruit_names)
            return [row[0] for row in cursor.fetchall()]
        
        else:
            return []
            
    except psycopg2.Error as e:
        print(f"[{get_timestamp()}] ❌ Error getting recipes to process:")
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Identify primary vs secondary fruits in jam recipes')
    parser.add_argument('--recipe-id', type=int, help='Process specific recipe ID')
    parser.add_argument('--all', action='store_true', help='Process all recipes')
    parser.add_argument('--fruits', type=str, help='Process recipes containing specific fruits (comma-separated)')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without updating database')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.recipe_id, args.all, args.fruits]):
        print("Error: Must specify --recipe-id, --all, or --fruits")
        parser.print_help()
        sys.exit(1)
    
    print(f"[{get_timestamp()}] Primary fruit identification script starting...")
    
    if args.dry_run:
        print(f"[{get_timestamp()}] DRY RUN MODE - No database changes will be made")
    
    connection = None
    
    try:
        # Connect to database
        connection = connect_to_database()
        
        # Parse fruit names if provided
        fruit_names = None
        if args.fruits:
            fruit_names = [name.strip().lower() for name in args.fruits.split(',')]
            print(f"[{get_timestamp()}] Processing recipes containing fruits: {fruit_names}")
        
        # Get recipes to process
        recipe_ids = get_recipes_to_process(connection, args.recipe_id, args.all, fruit_names)
        
        if not recipe_ids:
            print(f"[{get_timestamp()}] No recipes found matching criteria")
            return
        
        print(f"[{get_timestamp()}] Found {len(recipe_ids)} recipes to process")
        
        # Process each recipe
        total_updated = 0
        recipes_with_changes = 0
        
        for recipe_id in recipe_ids:
            result = process_recipe(connection, recipe_id, args.dry_run, args.verbose)
            
            if result['success']:
                if result['changes_needed']:
                    recipes_with_changes += 1
                    total_updated += result['updated_count']
                    
                    if not args.verbose:
                        print(f"  Recipe {recipe_id}: {result['title']} - Updated {result['updated_count']} relationships")
        
        # Summary
        print(f"[{get_timestamp()}] ✅ Processing complete!")
        print(f"[{get_timestamp()}] Processed {len(recipe_ids)} recipes")
        print(f"[{get_timestamp()}] {recipes_with_changes} recipes had changes")
        print(f"[{get_timestamp()}] Total relationships updated: {total_updated}")
        
        if args.dry_run:
            print(f"[{get_timestamp()}] DRY RUN - No actual changes were made to the database")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Script failed:")
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if connection:
            connection.close()
            print(f"[{get_timestamp()}] Database connection closed")

if __name__ == "__main__":
    main()
