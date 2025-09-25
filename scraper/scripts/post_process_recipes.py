#!/usr/bin/env python3
"""
Post-processing script for recipe filtering.

This script processes recipes after all orchestrators have completed:
1. Groups recipes by primary fruit combinations
2. Removes exact duplicates (keeps highest rated)
3. Keeps best 5 recipes per combination (by popularity)
4. Deletes excess recipes from database
"""

import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Set

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.scripts.insert_recipes import connect_to_database
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_timestamp():
    """Get current timestamp for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_primary_fruit_combinations(connection) -> Dict[Tuple[str, ...], List[Tuple[int, str, float, int]]]:
    """
    Get all unique combinations of primary fruits from recipes.
    
    Args:
        connection: Database connection
        
    Returns:
        Dict mapping fruit combinations to list of (recipe_id, title, rating, review_count)
    """
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT r.id, r.title, r.rating, r.review_count,
                   ARRAY_AGG(f.ai_identifier ORDER BY f.ai_identifier) as primary_fruits
            FROM recipes r
            JOIN recipe_fruits rf ON r.id = rf.recipe_id
            JOIN fruits f ON rf.fruit_id = f.id
            WHERE rf.is_primary = true
            GROUP BY r.id, r.title, r.rating, r.review_count
            ORDER BY r.id
        """)
        
        combinations = {}
        for recipe_id, title, rating, review_count, fruits in cursor.fetchall():
            fruit_combo = tuple(fruits)  # e.g., ('strawberry',) or ('strawberry', 'gooseberry')
            if fruit_combo not in combinations:
                combinations[fruit_combo] = []
            combinations[fruit_combo].append((recipe_id, title, rating, review_count))
        
        return combinations
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Error getting primary fruit combinations: {e}")
        raise
    finally:
        cursor.close()

def remove_exact_duplicates(recipes: List[Tuple[int, str, float, int]]) -> List[Tuple[int, str, float, int]]:
    """
    Remove recipes with identical titles, keeping the highest rated one.
    
    Args:
        recipes: List of (recipe_id, title, rating, review_count)
        
    Returns:
        List of unique recipes with highest ratings
    """
    title_groups = {}
    for recipe_id, title, rating, review_count in recipes:
        if title not in title_groups:
            title_groups[title] = []
        title_groups[title].append((recipe_id, rating, review_count))
    
    # Keep only the highest rated recipe for each title
    unique_recipes = []
    for title, recipe_list in title_groups.items():
        if len(recipe_list) > 1:
            # Multiple recipes with same title - keep the best one
            best_recipe = max(recipe_list, key=lambda x: x[1] * x[2])  # rating * review_count
            unique_recipes.append((best_recipe[0], title, best_recipe[1], best_recipe[2]))
        else:
            # Only one recipe with this title
            recipe_id, rating, review_count = recipe_list[0]
            unique_recipes.append((recipe_id, title, rating, review_count))
    
    return unique_recipes

def calculate_popularity_score(rating, review_count) -> float:
    """
    Calculate popularity score for recipe ranking.
    
    Uses a rating-aware approach:
    - 4-5 stars: More reviews = better (high quality confirmed by many)
    - 3 stars: Neutral (more reviews don't help or hurt)
    - 1-2 stars: More reviews = worse (bad quality confirmed by many)
    
    Args:
        rating: Recipe rating (1-5 scale) - can be float or Decimal
        review_count: Number of reviews - can be int or Decimal
        
    Returns:
        Popularity score (higher is better)
    """
    # Convert to float to handle Decimal types from database
    rating = float(rating)
    review_count = float(review_count)
    
    # Base score from rating (0-25 scale)
    base_score = rating ** 2
    
    # Review multiplier based on rating quality
    if rating >= 4.0:
        # 4-5 stars: More reviews = better (logarithmic to prevent extreme values)
        review_multiplier = 1 + (review_count ** 0.3) / 10
    elif rating >= 3.0:
        # 3 stars: Neutral (reviews don't significantly help or hurt)
        review_multiplier = 1 + (review_count ** 0.1) / 50
    else:
        # 1-2 stars: More reviews = worse (penalty for bad recipes with many reviews)
        review_multiplier = 1 - (review_count ** 0.3) / 20
    
    return base_score * review_multiplier

def delete_recipes(connection, recipe_ids: List[int]) -> bool:
    """
    Delete recipes and their associated data from the database.
    
    Args:
        connection: Database connection
        recipe_ids: List of recipe IDs to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not recipe_ids:
        return True
    
    cursor = connection.cursor()
    
    try:
        # Delete recipe_fruits relationships first (foreign key constraint)
        cursor.execute("DELETE FROM recipe_fruits WHERE recipe_id = ANY(%s)", (recipe_ids,))
        
        # Delete the recipes
        cursor.execute("DELETE FROM recipes WHERE id = ANY(%s)", (recipe_ids,))
        
        connection.commit()
        return True
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Error deleting recipes: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def process_combination(connection, fruit_combo: Tuple[str, ...], recipes: List[Tuple[int, str, float, int]], 
                       verbose: bool = False) -> Tuple[int, int]:
    """
    Process a single fruit combination.
    
    Args:
        connection: Database connection
        fruit_combo: Tuple of fruit names
        recipes: List of (recipe_id, title, rating, review_count)
        verbose: Whether to show detailed logging
        
    Returns:
        Tuple of (kept_count, removed_count)
    """
    combo_name = " + ".join(fruit_combo)
    
    if verbose:
        print(f"[{get_timestamp()}] Processing {combo_name} combination ({len(recipes)} recipes)...")
    
    # Remove exact duplicates
    unique_recipes = remove_exact_duplicates(recipes)
    duplicates_removed = len(recipes) - len(unique_recipes)
    
    if duplicates_removed > 0 and verbose:
        print(f"[{get_timestamp()}]   Removed {duplicates_removed} exact duplicates")
    
    # Select best 5
    if len(unique_recipes) > 5:
        # Sort by popularity (rating * review_count)
        sorted_recipes = sorted(unique_recipes, 
                              key=lambda x: calculate_popularity_score(x[2], x[3]),
                              reverse=True)
        kept_recipes = sorted_recipes[:5]
        removed_recipes = sorted_recipes[5:]
        
        if verbose:
            print(f"[{get_timestamp()}]   KEPT ({len(kept_recipes)} recipes):")
            for recipe_id, title, rating, review_count in kept_recipes:
                popularity = calculate_popularity_score(rating, review_count)
                print(f"[{get_timestamp()}]     ✅ {title} (rating: {rating}, reviews: {review_count}, popularity: {popularity:.1f})")
            
            print(f"[{get_timestamp()}]   REMOVED ({len(removed_recipes)} recipes):")
            for recipe_id, title, rating, review_count in removed_recipes:
                popularity = calculate_popularity_score(rating, review_count)
                print(f"[{get_timestamp()}]     ❌ {title} (rating: {rating}, reviews: {review_count}, popularity: {popularity:.1f})")
        
        # Delete removed recipes
        recipe_ids_to_delete = [r[0] for r in removed_recipes]
        if delete_recipes(connection, recipe_ids_to_delete):
            return len(kept_recipes), len(removed_recipes)
        else:
            print(f"[{get_timestamp()}] ❌ Failed to delete recipes for {combo_name}")
            return len(kept_recipes), 0
    else:
        # Keep all recipes for this combination
        if verbose:
            print(f"[{get_timestamp()}]   KEPT ALL ({len(unique_recipes)} recipes):")
            for recipe_id, title, rating, review_count in unique_recipes:
                popularity = calculate_popularity_score(rating, review_count)
                print(f"[{get_timestamp()}]     ✅ {title} (rating: {rating}, reviews: {review_count}, popularity: {popularity:.1f})")
        
        return len(unique_recipes), 0

def post_process_recipes(verbose: bool = False):
    """
    Main post-processing function.
    
    Args:
        verbose: Whether to show detailed logging
    """
    print(f"[{get_timestamp()}] Starting post-processing...")
    
    connection = None
    
    try:
        # Connect to database
        connection = connect_to_database()
        
        # Get all primary fruit combinations
        combinations = get_primary_fruit_combinations(connection)
        print(f"[{get_timestamp()}] Found {len(combinations)} unique fruit combinations")
        
        if not combinations:
            print(f"[{get_timestamp()}] No recipes found to process")
            return
        
        # Process each combination
        total_kept = 0
        total_removed = 0
        
        for fruit_combo, recipes in combinations.items():
            kept, removed = process_combination(connection, fruit_combo, recipes, verbose)
            total_kept += kept
            total_removed += removed
        
        # Summary
        print(f"[{get_timestamp()}] ✅ Post-processing complete!")
        print(f"[{get_timestamp()}] Total kept: {total_kept} recipes")
        print(f"[{get_timestamp()}] Total removed: {total_removed} recipes")
        
        # Show final statistics
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM recipes")
        final_recipe_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM recipe_fruits")
        final_relationship_count = cursor.fetchone()[0]
        cursor.close()
        
        print(f"[{get_timestamp()}] Final database state:")
        print(f"[{get_timestamp()}]   Recipes: {final_recipe_count}")
        print(f"[{get_timestamp()}]   Recipe-fruit relationships: {final_relationship_count}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Post-processing failed:")
        print(f"Error: {e}")
        raise
    finally:
        if connection:
            connection.close()
            print(f"[{get_timestamp()}] Database connection closed")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Post-process recipes to keep best 5 per primary fruit combination")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Show detailed logging of kept/removed recipes")
    
    args = parser.parse_args()
    
    print(f"[{get_timestamp()}] Post-processing script starting...")
    print(f"[{get_timestamp()}] Verbose mode: {'ON' if args.verbose else 'OFF'}")
    
    try:
        post_process_recipes(verbose=args.verbose)
        print(f"[{get_timestamp()}] Script completed successfully!")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Script failed:")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
