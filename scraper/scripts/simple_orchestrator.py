#!/usr/bin/env python3
"""
Simple Recipe Orchestrator

A clean, simple orchestrator that:
1. Takes a list of adapters
2. Calls each adapter with a fruit name
3. Gets back a list of recipes (standardized format)
4. Inserts all recipes into database
5. Runs post-processing
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

from scraper.adapters.allrecipes_adapter import AllRecipesAdapter
from scraper.adapters.serious_eats_adapter import SeriousEatsAdapter
from scraper.adapters.food_network_adapter import FoodNetworkAdapter
from scraper.adapters.bbc_good_food_adapter import BBCGoodFoodAdapter
from scraper.scripts.insert_recipes import insert_recipes, connect_to_database

def get_timestamp():
    """Get current timestamp for logging."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_adapter(source_name: str):
    """Get the appropriate adapter for a source."""
    if source_name == "allrecipes":
        return AllRecipesAdapter()
    elif source_name == "serious_eats":
        return SeriousEatsAdapter()
    elif source_name == "food_network":
        return FoodNetworkAdapter()
    elif source_name == "bbc_good_food":
        return BBCGoodFoodAdapter()
    else:
        raise ValueError(f"Unknown source: {source_name}")

def scrape_fruit_recipes(fruit_name: str, sources: List[str], count_per_source: int = 10) -> List[Dict[str, Any]]:
    """
    Scrape recipes for a fruit from multiple sources.
    
    Args:
        fruit_name: The fruit to search for
        sources: List of source names
        count_per_source: Number of recipes to get from each source
        
    Returns:
        List of recipe dictionaries
    """
    all_recipes = []
    
    for source in sources:
        try:
            print(f"[{get_timestamp()}] Scraping {source} for {fruit_name}...")
            adapter = get_adapter(source)
            
            # Get recipe URLs
            recipe_urls = adapter.search_for_fruit_urls(fruit_name, count_per_source)
            print(f"[{get_timestamp()}] Found {len(recipe_urls)} URLs from {source}")
            
            # Scrape each recipe
            for i, url in enumerate(recipe_urls):
                try:
                    print(f"[{get_timestamp()}] Scraping recipe {i+1}/{len(recipe_urls)} from {source}: {url}")
                    recipe = adapter.scrape_recipe(url)
                    
                    if recipe:
                        # Add source information
                        recipe['source'] = adapter.get_site_name()
                        all_recipes.append(recipe)
                        print(f"[{get_timestamp()}] ✅ Successfully scraped: {recipe['title']}")
                    else:
                        print(f"[{get_timestamp()}] ❌ Failed to scrape recipe from {url}")
                        
                except Exception as e:
                    print(f"[{get_timestamp()}] ❌ Error scraping {url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"[{get_timestamp()}] ❌ Error with {source}: {e}")
            continue
    
    print(f"[{get_timestamp()}] Total recipes collected: {len(all_recipes)}")
    return all_recipes

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Simple recipe orchestrator")
    parser.add_argument("--fruit", "-f", required=True, help="Fruit name to search for")
    parser.add_argument("--sources", "-s", nargs="+", default=["allrecipes", "serious_eats", "food_network", "bbc_good_food"], 
                       help="Sources to scrape from")
    parser.add_argument("--count", "-c", type=int, default=10, 
                       help="Number of recipes per source")
    
    args = parser.parse_args()
    
    print(f"[{get_timestamp()}] Simple Recipe Orchestrator")
    print(f"[{get_timestamp()}] Fruit: {args.fruit}")
    print(f"[{get_timestamp()}] Sources: {', '.join(args.sources)}")
    print(f"[{get_timestamp()}] Count per source: {args.count}")
    
    try:
        # Step 1: Scrape recipes
        recipes = scrape_fruit_recipes(args.fruit, args.sources, args.count)
        
        if not recipes:
            print(f"[{get_timestamp()}] ⚠️  No recipes found")
            return
        
        # Step 2: Insert into database
        print(f"[{get_timestamp()}] Inserting {len(recipes)} recipes into database...")
        recipe_ids = insert_recipes(recipes)
        
        if recipe_ids:
            print(f"[{get_timestamp()}] ✅ Successfully inserted {len(recipe_ids)} recipes")
            print(f"[{get_timestamp()}] Recipe IDs: {recipe_ids}")
        else:
            print(f"[{get_timestamp()}] ⚠️  No recipes were inserted")
            
    except Exception as e:
        print(f"[{get_timestamp()}] 💥 Orchestrator failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
