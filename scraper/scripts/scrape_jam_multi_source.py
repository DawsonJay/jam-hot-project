#!/usr/bin/env python3
"""
Multi-source jam recipe scraper and database inserter.

This script orchestrates the complete pipeline for scraping jam recipes
from multiple sources (AllRecipes, Serious Eats, etc.) and inserting them into the database.
"""

import sys
import os
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.core.adaptive_scraper import AdaptiveScraper
from scraper.adapters.allrecipes_adapter import AllRecipesAdapter
from scraper.adapters.serious_eats_adapter import SeriousEatsAdapter
from scraper.scripts.insert_recipes import insert_recipes, connect_to_database

def get_timestamp():
    """Get current timestamp for logging."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def scrape_jam_multi_source(fruit_name: str, sources: List[str] = None, recipes_per_source: int = 10) -> List[int]:
    """
    Scrape jam recipes from multiple sources for a specific fruit and insert into database.
    
    Args:
        fruit_name (str): The fruit to search for (e.g., "strawberry")
        sources (List[str]): List of sources to scrape from (default: ["allrecipes", "serious_eats"])
        recipes_per_source (int): Number of recipes to scrape from each source (default: 10)
        
    Returns:
        List[int]: List of recipe IDs inserted into database
        
    Raises:
        Exception: If scraping or insertion fails
    """
    if sources is None:
        sources = ["allrecipes", "serious_eats"]
    
    print(f"[{get_timestamp()}] Starting multi-source jam scraping for: {fruit_name}")
    print(f"[{get_timestamp()}] Sources: {', '.join(sources)}")
    print(f"[{get_timestamp()}] Recipes per source: {recipes_per_source}")
    
    all_scraped_recipes = []
    
    try:
        # Step 1: Initialize adaptive scraper
        print(f"[{get_timestamp()}] Step 1: Initializing adaptive scraper...")
        with AdaptiveScraper(headless=True) as scraper:
            print(f"[{get_timestamp()}] ✅ Adaptive scraper initialized")
            
            # Step 2: Scrape from each source
            for source in sources:
                print(f"[{get_timestamp()}] Step 2: Scraping from {source}...")
                
                try:
                    # Get the appropriate adapter
                    if source == "allrecipes":
                        adapter = AllRecipesAdapter()
                    elif source == "serious_eats":
                        adapter = SeriousEatsAdapter()
                    else:
                        print(f"[{get_timestamp()}] ⚠️  Unknown source: {source}, skipping...")
                        continue
                    
                    print(f"[{get_timestamp()}] Using {adapter.get_site_name()} adapter")
                    print(f"[{get_timestamp()}] Scraping method: {adapter.get_scraping_method()}")
                    
                    # Scrape recipes from this source
                    source_recipes = scraper.scrape_site(adapter, fruit_name)
                    
                    print(f"[{get_timestamp()}] ✅ {source} scraping complete! Got {len(source_recipes)} recipes")
                    
                    # Add source information to recipes
                    for recipe in source_recipes:
                        recipe['source'] = adapter.get_site_name()
                    
                    all_scraped_recipes.extend(source_recipes)
                    
                except Exception as e:
                    print(f"[{get_timestamp()}] ❌ Error scraping from {source}: {e}")
                    print(f"[{get_timestamp()}] Continuing with other sources...")
                    continue
        
        print(f"[{get_timestamp()}] ✅ Multi-source scraping complete!")
        print(f"[{get_timestamp()}] Total recipes collected: {len(all_scraped_recipes)}")
        
        if not all_scraped_recipes:
            print(f"[{get_timestamp()}] ❌ No recipes collected from any source!")
            return []
        
        # Step 3: Sort by popularity (rating first, then review count as tiebreaker)
        print(f"[{get_timestamp()}] Step 3: Sorting by popularity (rating first, then review count)...")
        all_scraped_recipes.sort(key=lambda r: (r.get('rating', 0), r.get('review_count', 0)), reverse=True)
        
        # Show top recipes
        print(f"[{get_timestamp()}] Top recipes by popularity:")
        for i, recipe in enumerate(all_scraped_recipes[:5], 1):
            title = recipe.get('title', 'Unknown')
            rating = recipe.get('rating', 0.0)
            review_count = recipe.get('review_count', 0)
            source = recipe.get('source', 'Unknown')
            print(f"    {i}. {title} - {rating} stars ({review_count} reviews) from {source}")
        
        # Step 4: Insert recipes into database
        print(f"[{get_timestamp()}] Step 4: Inserting recipes into database...")
        recipe_ids = insert_recipes(all_scraped_recipes)
        
        # Step 5: Extract fruits and identify primary fruits
        print(f"[{get_timestamp()}] Step 5: Extracting fruits and identifying primary fruits...")
        if recipe_ids:
            # Import the fruit extraction and primary identification functions
            from scraper.scripts.extract_fruits import extract_fruits_from_all_recipes
            from scraper.scripts.identify_primary_fruits import process_recipe
            
            # Extract fruits from the newly inserted recipes
            print(f"[{get_timestamp()}] Extracting fruits from {len(recipe_ids)} new recipes...")
            extract_fruits_from_all_recipes()
            
            # Identify primary fruits for the newly inserted recipes
            print(f"[{get_timestamp()}] Identifying primary fruits for new recipes...")
            db_connection = connect_to_database()
            for recipe_id in recipe_ids:
                process_recipe(db_connection, recipe_id, dry_run=False, verbose=False)
            db_connection.close()
            
            print(f"[{get_timestamp()}] ✅ Fruit extraction and primary identification complete!")
        
        print(f"[{get_timestamp()}] ✅ Multi-source scraping pipeline complete!")
        print(f"[{get_timestamp()}] Successfully processed {len(recipe_ids)} recipes for {fruit_name}")
        
        return recipe_ids
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Multi-source scraping pipeline failed:")
        print(f"Error: {e}")
        raise

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Scrape jam recipes from multiple sources")
    parser.add_argument("--fruit", "-f", required=True, help="Fruit name to search for (e.g., cherry, strawberry)")
    parser.add_argument("--sources", "-s", nargs="+", default=["allrecipes", "serious_eats"], 
                       help="Sources to scrape from (default: allrecipes serious_eats)")
    parser.add_argument("--count", "-c", type=int, default=10, 
                       help="Number of recipes to scrape from each source (default: 10)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    
    args = parser.parse_args()
    
    print(f"[{get_timestamp()}] Multi-source jam scraper starting...")
    print(f"[{get_timestamp()}] Fruit: {args.fruit}")
    print(f"[{get_timestamp()}] Sources: {', '.join(args.sources)}")
    print(f"[{get_timestamp()}] Count per source: {args.count}")
    
    try:
        recipe_ids = scrape_jam_multi_source(
            fruit_name=args.fruit,
            sources=args.sources,
            recipes_per_source=args.count
        )
        
        if recipe_ids:
            print(f"[{get_timestamp()}] 🎉 Success! Inserted {len(recipe_ids)} recipes")
            print(f"[{get_timestamp()}] Recipe IDs: {recipe_ids}")
        else:
            print(f"[{get_timestamp()}] ⚠️  No recipes were inserted")
            
    except Exception as e:
        print(f"[{get_timestamp()}] 💥 Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
