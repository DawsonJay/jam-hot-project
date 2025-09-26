#!/usr/bin/env python3
"""
Test script for Food Network adapter.

This script tests the Food Network adapter to see if it can successfully
scrape recipes from Food Network.
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.adapters.food_network_adapter import FoodNetworkAdapter
from scraper.core.adaptive_scraper import AdaptiveScraper

def get_timestamp():
    return datetime.utcnow().strftime('%Y-%m-%d-%H%M')

def test_food_network_connection():
    """Test the Food Network adapter."""
    print(f'[{get_timestamp()}] Testing Food Network adapter...')
    
    try:
        with AdaptiveScraper(headless=True) as scraper:
            adapter = FoodNetworkAdapter()
            print(f'[{get_timestamp()}] ✅ Adapter initialized: {adapter.get_site_name()}')
            print(f'[{get_timestamp()}] Scraping method: {adapter.get_scraping_method()}')
            
            # Test with strawberry jam
            fruit_name = "strawberry"
            print(f'[{get_timestamp()}] Testing with {fruit_name} jam...')
            
            recipes = scraper.scrape_site(adapter, fruit_name)
            
            print(f'[{get_timestamp()}] ✅ Scraping completed!')
            print(f'[{get_timestamp()}] Found {len(recipes)} {fruit_name} jam recipes')
            
            if recipes:
                print(f'[{get_timestamp()}] Recipe titles:')
                for i, recipe in enumerate(recipes, 1):
                    title = recipe.get('title', 'Unknown')
                    rating = recipe.get('rating', 0.0)
                    review_count = recipe.get('review_count', 0)
                    print(f'    {i}. {title}')
                    print(f'       Rating: {rating} stars ({review_count} reviews)')
                
                # Save a sample recipe for inspection
                sample_file = f"food_network_sample_{fruit_name}.json"
                with open(sample_file, 'w', encoding='utf-8') as f:
                    json.dump(recipes[0], f, indent=4)
                print(f'[{get_timestamp()}] ✅ Sample recipe saved to {sample_file}')
                
                print(f'[{get_timestamp()}] 🎉 Food Network test successful!')
            else:
                print(f'[{get_timestamp()}] ⚠️  No recipes found.')
                print(f'[{get_timestamp()}] 💥 Test failed!')
                sys.exit(1)
                
    except Exception as e:
        print(f'[{get_timestamp()}] ❌ Food Network test failed:')
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
        print(f'[{get_timestamp()}] 💥 Test failed!')
        sys.exit(1)

if __name__ == "__main__":
    test_food_network_connection()
