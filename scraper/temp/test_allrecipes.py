#!/usr/bin/env python3
"""
Test Script for AllRecipes Scraper

This is a disposable test script to validate that our core scraper and
AllRecipes adapter can get data from AllRecipes.com.

Usage:
    python test_allrecipes.py
"""

import sys
import os

# Add the parent directory of 'scraper' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.core.base_scraper import BaseScraper
from scraper.adapters.allrecipes_adapter import AllRecipesAdapter


def test_allrecipes_scraper():
    """Test the AllRecipes scraper with a simple strawberry jam search."""
    
    print("=" * 60)
    print("Testing AllRecipes Scraper")
    print("=" * 60)
    
    # Create the scraper and adapter
    scraper = BaseScraper(rate_limit=0.5)  # Slower rate limit for testing
    adapter = AllRecipesAdapter()
    
    # Test scraping strawberry jam recipes
    fruit_name = "strawberry"
    print(f"Testing with fruit: {fruit_name}")
    print()
    
    # Scrape the site
    recipes = scraper.scrape_site(adapter, fruit_name)
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if recipes:
        print(f"Successfully scraped {len(recipes)} recipe(s):")
        print()
        
        for i, recipe in enumerate(recipes, 1):
            print(f"Recipe {i}:")
            print(f"  Title: {recipe.get('title', 'N/A')}")
            print(f"  Source: {recipe.get('source', 'N/A')}")
            print(f"  Rating: {recipe.get('rating', 'N/A')}")
            print(f"  Review Count: {recipe.get('review_count', 'N/A')}")
            print(f"  URL: {recipe.get('source_url', 'N/A')}")
            print(f"  Ingredients: {len(recipe.get('ingredients', []))} items")
            print(f"  Instructions: {len(recipe.get('instructions', []))} steps")
            print()
    else:
        print("No recipes were scraped.")
    
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_allrecipes_scraper()


