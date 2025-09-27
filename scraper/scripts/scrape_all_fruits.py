#!/usr/bin/env python3
"""
Batch scraper for all fruits with profiles.

This script scrapes jam recipes for every fruit that has a profile in the database.
"""

import sys
import os
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.scripts.scrape_jam_multi_source import scrape_jam_multi_source
from scraper.scripts.insert_recipes import connect_to_database
from scraper.scripts.post_process_recipes import post_process_recipes

def get_timestamp():
    """Get current timestamp for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_fruits_with_profiles() -> List[str]:
    """
    Get all fruits that have profiles in the database.
    
    Returns:
        List[str]: List of fruit AI identifiers
    """
    connection = connect_to_database()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT f.ai_identifier 
            FROM fruits f 
            JOIN profiles p ON f.id = p.fruit_id 
            ORDER BY f.ai_identifier;
        """)
        
        fruits = [row[0] for row in cursor.fetchall()]
        return fruits
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Error getting fruits with profiles: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def scrape_all_fruits(sources: List[str] = None, recipes_per_source: int = 5, 
                     start_from: str = None, skip_fruits: List[str] = None) -> Dict[str, List[int]]:
    """
    Scrape jam recipes for all fruits with profiles.
    
    Args:
        sources: List of sources to scrape from (default: ["allrecipes", "serious_eats", "food_network"])
        recipes_per_source: Number of recipes to scrape from each source (default: 5)
        start_from: Fruit to start from (resume from this fruit)
        skip_fruits: List of fruits to skip
        
    Returns:
        Dict[str, List[int]]: Mapping of fruit names to recipe IDs inserted
    """
    if sources is None:
        sources = ["allrecipes", "serious_eats", "food_network"]
    
    if skip_fruits is None:
        skip_fruits = []
    
    print(f"[{get_timestamp()}] Starting batch scraping for all fruits with profiles")
    print(f"[{get_timestamp()}] Sources: {', '.join(sources)}")
    print(f"[{get_timestamp()}] Recipes per source: {recipes_per_source}")
    
    # Get all fruits with profiles
    fruits = get_fruits_with_profiles()
    print(f"[{get_timestamp()}] Found {len(fruits)} fruits with profiles")
    
    # Filter fruits if needed
    if start_from:
        try:
            start_index = fruits.index(start_from)
            fruits = fruits[start_index:]
            print(f"[{get_timestamp()}] Starting from {start_from} (fruit {start_index + 1}/{len(fruits)})")
        except ValueError:
            print(f"[{get_timestamp()}] ⚠️  Fruit '{start_from}' not found, starting from beginning")
    
    if skip_fruits:
        fruits = [f for f in fruits if f not in skip_fruits]
        print(f"[{get_timestamp()}] Skipping {len(skip_fruits)} fruits: {', '.join(skip_fruits)}")
        print(f"[{get_timestamp()}] Remaining fruits: {len(fruits)}")
    
    # Scrape each fruit
    results = {}
    total_recipes = 0
    
    for i, fruit in enumerate(fruits, 1):
        print(f"\n[{get_timestamp()}] 🍓 Scraping {fruit} ({i}/{len(fruits)})")
        print(f"[{get_timestamp()}] {'='*50}")
        
        try:
            recipe_ids = scrape_jam_multi_source(
                fruit_name=fruit,
                sources=sources,
                recipes_per_source=recipes_per_source
            )
            
            results[fruit] = recipe_ids
            total_recipes += len(recipe_ids)
            
            print(f"[{get_timestamp()}] ✅ {fruit}: {len(recipe_ids)} recipes inserted")
            
        except Exception as e:
            print(f"[{get_timestamp()}] ❌ {fruit}: Failed - {e}")
            results[fruit] = []
            continue
    
    # Summary
    print(f"\n[{get_timestamp()}] 🎉 Batch scraping complete!")
    print(f"[{get_timestamp()}] {'='*50}")
    print(f"[{get_timestamp()}] Total fruits processed: {len(fruits)}")
    print(f"[{get_timestamp()}] Total recipes inserted: {total_recipes}")
    
    # Show results by fruit
    print(f"\n[{get_timestamp()}] Results by fruit:")
    for fruit, recipe_ids in results.items():
        if recipe_ids:
            print(f"  ✅ {fruit}: {len(recipe_ids)} recipes")
        else:
            print(f"  ❌ {fruit}: 0 recipes")
    
    # Run post-processing if we have recipes
    if total_recipes > 0:
        print(f"\n[{get_timestamp()}] 🔧 Running post-processing...")
        print(f"[{get_timestamp()}] {'='*50}")
        try:
            post_process_recipes(verbose=False)
            print(f"[{get_timestamp()}] ✅ Post-processing complete!")
        except Exception as e:
            print(f"[{get_timestamp()}] ❌ Post-processing failed: {e}")
            print(f"[{get_timestamp()}] Continuing without post-processing...")
    else:
        print(f"[{get_timestamp()}] ⚠️  No recipes to post-process")
    
    return results

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Scrape jam recipes for all fruits with profiles")
    parser.add_argument("--sources", "-s", nargs="+", default=["allrecipes", "serious_eats", "food_network", "bbc_good_food"],
                       help="Sources to scrape from (default: allrecipes serious_eats food_network bbc_good_food)")
    parser.add_argument("--count", "-c", type=int, default=10,
                        help="Number of recipes to scrape from each source (default: 10)")
    parser.add_argument("--start-from", "-f", type=str,
                       help="Fruit to start from (resume from this fruit)")
    parser.add_argument("--skip", "-k", nargs="+", default=[],
                       help="Fruits to skip")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    
    args = parser.parse_args()
    
    print(f"[{get_timestamp()}] Batch fruit scraper starting...")
    print(f"[{get_timestamp()}] Sources: {', '.join(args.sources)}")
    print(f"[{get_timestamp()}] Count per source: {args.count}")
    if args.start_from:
        print(f"[{get_timestamp()}] Starting from: {args.start_from}")
    if args.skip:
        print(f"[{get_timestamp()}] Skipping: {', '.join(args.skip)}")
    
    try:
        results = scrape_all_fruits(
            sources=args.sources,
            recipes_per_source=args.count,
            start_from=args.start_from,
            skip_fruits=args.skip
        )
        
        # Final summary
        successful_fruits = [fruit for fruit, recipe_ids in results.items() if recipe_ids]
        failed_fruits = [fruit for fruit, recipe_ids in results.items() if not recipe_ids]
        
        print(f"\n[{get_timestamp()}] 📊 Final Summary:")
        print(f"[{get_timestamp()}] ✅ Successful: {len(successful_fruits)} fruits")
        print(f"[{get_timestamp()}] ❌ Failed: {len(failed_fruits)} fruits")
        
        if failed_fruits:
            print(f"[{get_timestamp()}] Failed fruits: {', '.join(failed_fruits)}")
        
        # Show final database state
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM recipes")
            final_recipe_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM recipe_fruits")
            final_relationship_count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            
            print(f"\n[{get_timestamp()}] 🗄️  Final Database State:")
            print(f"[{get_timestamp()}]   Recipes: {final_recipe_count}")
            print(f"[{get_timestamp()}]   Recipe-fruit relationships: {final_relationship_count}")
        except Exception as e:
            print(f"[{get_timestamp()}] ⚠️  Could not get final database state: {e}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] 💥 Batch scraping failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
