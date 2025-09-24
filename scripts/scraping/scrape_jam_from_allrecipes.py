#!/usr/bin/env python3
"""
AllRecipes jam recipe scraper and database inserter.

This script orchestrates the complete pipeline for scraping jam recipes
from AllRecipes and inserting them into the database.
"""

import sys
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.core.base_scraper import BaseScraper
from scraper.adapters.allrecipes_adapter import AllRecipesAdapter
from scripts.scraping.insert_recipes import insert_recipes

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
        
        # Import the duplicate checking function
        from scripts.scraping.insert_recipes import check_duplicate_recipe, connect_to_database
        
        # Connect to database for duplicate checking
        db_connection = connect_to_database()
        
        # Filter out duplicates
        print(f"[{get_timestamp()}] Checking for duplicates...")
        non_duplicate_recipes = []
        duplicate_count = 0
        
        for recipe in all_scraped_recipes:
            if check_duplicate_recipe(db_connection, recipe):
                print(f"[{get_timestamp()}] ⚠️  Duplicate found: {recipe.get('title', 'Untitled')}")
                duplicate_count += 1
            else:
                non_duplicate_recipes.append(recipe)
        
        # Close database connection
        db_connection.close()
        
        print(f"[{get_timestamp()}] Found {duplicate_count} duplicates, {len(non_duplicate_recipes)} unique recipes")
        
        # Sort by popularity (rating first, then review count as tiebreaker)
        print(f"[{get_timestamp()}] Sorting by popularity (rating first, then review count)...")
        non_duplicate_recipes.sort(key=lambda r: (r['rating'], r['review_count']), reverse=True)
        
        # Take top N recipes
        scraped_recipes = non_duplicate_recipes[:insert_count]
        print(f"[{get_timestamp()}] Selected top {len(scraped_recipes)} most popular recipes for insertion")
        
        # Step 3: Insert recipes into database
        print(f"[{get_timestamp()}] Step 3: Inserting recipes into database...")
        if not scraped_recipes:
            print(f"[{get_timestamp()}] ❌ No recipes to insert!")
            return []
        
        recipe_ids = insert_recipes(scraped_recipes)
        
        print(f"[{get_timestamp()}] ✅ AllRecipes scraping pipeline complete!")
        print(f"[{get_timestamp()}] Successfully processed {len(recipe_ids)} recipes for {fruit_name}")
        
        return recipe_ids
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ AllRecipes scraping pipeline failed:")
        print(f"Error: {e}")
        raise

def main():
    """Main function for testing the script."""
    print(f"[{get_timestamp()}] AllRecipes jam scraper starting...")
    
    try:
        # Test with strawberry
        fruit_name = "strawberry"
        scrape_count = 10  # Scrape 10 recipes from search results
        insert_count = 5   # Insert top 5 non-duplicate recipes
        
        print(f"[{get_timestamp()}] Testing with fruit: {fruit_name}")
        print(f"[{get_timestamp()}] Will scrape {scrape_count} recipes, insert top {insert_count} non-duplicates")
        
        recipe_ids = scrape_jam_from_allrecipes(fruit_name, scrape_count, insert_count)
        
        print(f"[{get_timestamp()}] Test completed successfully!")
        print(f"[{get_timestamp()}] Recipe IDs inserted: {recipe_ids}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Test failed:")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
