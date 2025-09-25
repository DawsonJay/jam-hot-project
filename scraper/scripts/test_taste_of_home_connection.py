#!/usr/bin/env python3
"""
Test script to verify connection to Taste of Home and get HTML content.

This script follows the same incremental approach we used with AllRecipes:
1. First, just contact the site and get HTML
2. Then we'll add parsing and data extraction
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.adapters.taste_of_home_adapter import TasteOfHomeAdapter
from scraper.core.base_scraper import BaseScraper

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD-HHMM format."""
    return datetime.utcnow().strftime("%Y-%m-%d-%H%M")

def test_taste_of_home_connection():
    """Test basic connection to Taste of Home and get HTML content."""
    print(f"[{get_timestamp()}] Testing Taste of Home connection...")
    
    try:
        # Initialize the scraper and adapter
        print(f"[{get_timestamp()}] Step 1: Initializing scraper and adapter...")
        scraper = BaseScraper()
        adapter = TasteOfHomeAdapter()
        print(f"[{get_timestamp()}] ✅ Scraper and adapter initialized")
        
        # Test with strawberry jam search
        fruit_name = "strawberry"
        print(f"[{get_timestamp()}] Step 2: Testing search URL generation...")
        search_url = adapter.search_for_fruit(fruit_name)
        print(f"[{get_timestamp()}] Search URL: {search_url}")
        
        # Make the search request
        print(f"[{get_timestamp()}] Step 3: Making search request...")
        response = scraper.session.get(search_url)
        response.raise_for_status()
        search_html = response.text
        print(f"[{get_timestamp()}] ✅ Search request successful, got {len(search_html)} characters")
        
        # Save the HTML to a file for inspection
        output_file = f"taste_of_home_search_results_{fruit_name}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(search_html)
        print(f"[{get_timestamp()}] ✅ HTML saved to {output_file}")
        
        # Try to extract recipe URLs
        print(f"[{get_timestamp()}] Step 4: Extracting recipe URLs...")
        recipe_urls = adapter.get_recipe_urls(search_html, count=5)
        print(f"[{get_timestamp()}] Found {len(recipe_urls)} recipe URLs:")
        for i, url in enumerate(recipe_urls, 1):
            print(f"    {i}. {url}")
        
        if recipe_urls:
            # Test getting HTML from the first recipe
            print(f"[{get_timestamp()}] Step 5: Testing recipe page access...")
            first_recipe_url = recipe_urls[0]
            print(f"[{get_timestamp()}] Accessing: {first_recipe_url}")
            
            response = scraper.session.get(first_recipe_url)
            response.raise_for_status()
            recipe_html = response.text
            print(f"[{get_timestamp()}] ✅ Recipe page request successful, got {len(recipe_html)} characters")
            
            # Save the recipe HTML for inspection
            recipe_output_file = f"taste_of_home_recipe_{fruit_name}.html"
            with open(recipe_output_file, 'w', encoding='utf-8') as f:
                f.write(recipe_html)
            print(f"[{get_timestamp()}] ✅ Recipe HTML saved to {recipe_output_file}")
            
            print(f"[{get_timestamp()}] ✅ Taste of Home connection test completed successfully!")
            print(f"[{get_timestamp()}] Next steps:")
            print(f"    1. Inspect the HTML files to understand the structure")
            print(f"    2. Update the adapter selectors based on the actual HTML")
            print(f"    3. Test recipe data extraction")
        else:
            print(f"[{get_timestamp()}] ⚠️  No recipe URLs found. Check the HTML structure.")
            print(f"[{get_timestamp()}] Inspect {output_file} to see what we got.")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Taste of Home connection test failed:")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_taste_of_home_connection()
    if success:
        print(f"[{get_timestamp()}] 🎉 Test completed successfully!")
    else:
        print(f"[{get_timestamp()}] 💥 Test failed!")
        sys.exit(1)
