#!/usr/bin/env python3
"""
Debug Script - Save AllRecipes HTML

This script will save the HTML we get from AllRecipes so we can examine it.
"""

import sys
import os

# Add the scraper directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.base_scraper import BaseScraper
from adapters.allrecipes_adapter import AllRecipesAdapter


def save_allrecipes_html():
    """Save the HTML from AllRecipes search results to a file."""
    
    print("Getting HTML from AllRecipes...")
    
    # Create the scraper and adapter
    scraper = BaseScraper(rate_limit=0.5)
    adapter = AllRecipesAdapter()
    
    # Get search URL
    search_url = adapter.search_for_fruit("strawberry")
    print(f"Search URL: {search_url}")
    
    # Make the request
    try:
        response = scraper.session.get(search_url)
        response.raise_for_status()
        html_content = response.text
        
        # Save to file
        with open('allrecipes_search_results.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML saved to allrecipes_search_results.html")
        print(f"HTML length: {len(html_content)} characters")
        print(f"First 500 characters:")
        print("-" * 50)
        print(html_content[:500])
        print("-" * 50)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    save_allrecipes_html()


