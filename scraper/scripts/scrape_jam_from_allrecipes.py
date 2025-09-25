#!/usr/bin/env python3
"""
AllRecipes jam recipe scraper and database inserter.

This script orchestrates the complete pipeline for scraping jam recipes
from AllRecipes and inserting them into the database.
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

from scraper.core.base_scraper import BaseScraper
from scraper.adapters.allrecipes_adapter import AllRecipesAdapter
from scraper.scripts.insert_recipes import insert_recipes, connect_to_database

def get_timestamp():
    """Get current timestamp for logging."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def scrape_jam_from_allrecipes(fruit_name: str, scrape_count: int = 10, insert_count: int = 5) -> List[int]:
    """
    Scrape jam recipes from AllRecipes for a specific fruit and insert into database.
    
    Args:
        fruit_name (str): The fruit to search for (e.g., "strawberry")
        scrape_count (int): Number of recipes to scrape from search results (default: 10)
        insert_count (int): Number of non-duplicate recipes to insert (default: 5)
        
    Returns:
        List[int]: List of recipe IDs inserted into database
        
    Raises:
        Exception: If scraping or insertion fails
    """
    print(f"[{get_timestamp()}] Starting AllRecipes jam scraping for: {fruit_name}")
    
    try:
        # Step 1: Initialize scraper and adapter
        print(f"[{get_timestamp()}] Step 1: Initializing scraper and adapter...")
        scraper = BaseScraper()
        allrecipes_adapter = AllRecipesAdapter()
        print(f"[{get_timestamp()}] ✅ Scraper and adapter initialized")
        
        # Step 2: Scrape recipes (get top 10 to have backups for duplicates)
        print(f"[{get_timestamp()}] Step 2: Scraping recipes from AllRecipes...")
        print(f"[{get_timestamp()}] Searching for: {fruit_name} jam")
        
        # Get search URL and scrape
        search_url = allrecipes_adapter.search_for_fruit(fruit_name)
        print(f"[{get_timestamp()}] Search URL: {search_url}")
        
        # Make request to search page
        response = scraper.session.get(search_url)
        response.raise_for_status()
        search_results_html = response.text
        print(f"[{get_timestamp()}] Search request successful, got {len(search_results_html)} characters")
        
        # Extract recipe URLs
        recipe_urls = allrecipes_adapter.get_recipe_urls(search_results_html, scrape_count)
        print(f"[{get_timestamp()}] Found {len(recipe_urls)} recipe URLs")
        
        # Scrape all recipes first
        print(f"[{get_timestamp()}] Scraping all {len(recipe_urls)} recipes...")
        all_scraped_recipes = []
        
        for i, recipe_url in enumerate(recipe_urls, 1):
            print(f"[{get_timestamp()}] Scraping recipe {i}/{len(recipe_urls)}: {recipe_url}")
            try:
                response = scraper.session.get(recipe_url)
                response.raise_for_status()
                recipe_html = response.text
                recipe_data = allrecipes_adapter.extract_recipe_data(recipe_html, recipe_url)
                all_scraped_recipes.append(recipe_data)
                print(f"[{get_timestamp()}] ✅ Successfully scraped: {recipe_data.get('title', 'Untitled')}")
                
            except Exception as e:
                print(f"[{get_timestamp()}] ❌ Error scraping recipe {recipe_url}: {e}")
                # Continue with next recipe instead of failing completely
                continue
        
        print(f"[{get_timestamp()}] ✅ Recipe scraping complete! Got {len(all_scraped_recipes)} recipes")
        
        # Sort by popularity (rating first, then review count as tiebreaker)
        print(f"[{get_timestamp()}] Sorting by popularity (rating first, then review count)...")
        all_scraped_recipes.sort(key=lambda r: (r['rating'], r['review_count']), reverse=True)
        
        # Take top N recipes (no duplicate checking - let post-processing handle it)
        scraped_recipes = all_scraped_recipes[:insert_count]
        print(f"[{get_timestamp()}] Selected top {len(scraped_recipes)} most popular recipes for insertion")
        
        # Step 3: Insert recipes into database
        print(f"[{get_timestamp()}] Step 3: Inserting recipes into database...")
        if not scraped_recipes:
            print(f"[{get_timestamp()}] ❌ No recipes to insert!")
            return []
        
        recipe_ids = insert_recipes(scraped_recipes)
        
        # Step 4: Extract fruits and identify primary fruits
        print(f"[{get_timestamp()}] Step 4: Extracting fruits and identifying primary fruits...")
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
        
        print(f"[{get_timestamp()}] ✅ AllRecipes scraping pipeline complete!")
        print(f"[{get_timestamp()}] Successfully processed {len(recipe_ids)} recipes for {fruit_name}")
        
        return recipe_ids
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ AllRecipes scraping pipeline failed:")
        print(f"Error: {e}")
        raise

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Scrape jam recipes from AllRecipes")
    parser.add_argument("--fruit", "-f", required=True, help="Fruit name to search for (e.g., cherry, strawberry)")
    parser.add_argument("--count", "-c", type=int, default=10, help="Number of recipes to scrape (default: 10)")
    parser.add_argument("--insert", "-i", type=int, default=5, help="Number of recipes to insert (default: 5)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    
    args = parser.parse_args()
    
    print(f"[{get_timestamp()}] AllRecipes jam scraper starting...")
    print(f"[{get_timestamp()}] Verbose mode: {'ON' if args.verbose else 'OFF'}")
    
    try:
        fruit_name = args.fruit
        scrape_count = args.count
        insert_count = args.insert
        
        print(f"[{get_timestamp()}] Scraping {fruit_name} jam recipes...")
        print(f"[{get_timestamp()}] Will scrape {scrape_count} recipes, insert top {insert_count}")
        
        recipe_ids = scrape_jam_from_allrecipes(fruit_name, scrape_count, insert_count)
        
        print(f"[{get_timestamp()}] Scraping completed successfully!")
        print(f"[{get_timestamp()}] Recipe IDs inserted: {recipe_ids}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Scraping failed:")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
