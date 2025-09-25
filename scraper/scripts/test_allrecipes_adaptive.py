#!/usr/bin/env python3
"""
Test script to verify AllRecipes works with the new AdaptiveScraper.

This script tests that AllRecipes still uses the fast requests method
and works correctly with the new adaptive architecture.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.adapters.allrecipes_adapter import AllRecipesAdapter
from scraper.core.adaptive_scraper import AdaptiveScraper

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD-HHMM format."""
    return datetime.utcnow().strftime("%Y-%m-%d-%H%M")

def test_allrecipes_adaptive():
    """Test AllRecipes with the adaptive scraper."""
    print(f"[{get_timestamp()}] Testing AllRecipes with AdaptiveScraper...")
    
    try:
        # Initialize the adaptive scraper and adapter
        print(f"[{get_timestamp()}] Step 1: Initializing adaptive scraper and adapter...")
        with AdaptiveScraper(headless=True) as scraper:
            adapter = AllRecipesAdapter()
            print(f"[{get_timestamp()}] ✅ Scraper and adapter initialized")
            print(f"[{get_timestamp()}] Adapter method: {adapter.get_scraping_method()}")
            
            # Test with strawberry jam search
            fruit_name = "strawberry"
            print(f"[{get_timestamp()}] Step 2: Testing adaptive scraping...")
            
            # This should automatically use requests since AllRecipesAdapter returns "requests"
            recipes = scraper.scrape_site(adapter, fruit_name)
            
            print(f"[{get_timestamp()}] ✅ Adaptive scraping completed!")
            print(f"[{get_timestamp()}] Found {len(recipes)} recipes")
            
            if recipes:
                print(f"[{get_timestamp()}] Sample recipe titles:")
                for i, recipe in enumerate(recipes[:3], 1):
                    title = recipe.get('title', 'Unknown')
                    print(f"    {i}. {title}")
                
                # Save sample recipe data for inspection
                import json
                sample_file = f"allrecipes_adaptive_sample_{fruit_name}.json"
                with open(sample_file, 'w', encoding='utf-8') as f:
                    json.dump(recipes[0] if recipes else {}, f, indent=2, ensure_ascii=False)
                print(f"[{get_timestamp()}] ✅ Sample recipe saved to {sample_file}")
                
                print(f"[{get_timestamp()}] 🎉 AllRecipes adaptive test successful!")
                return True
            else:
                print(f"[{get_timestamp()}] ⚠️  No recipes found.")
                return False
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ AllRecipes adaptive test failed:")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_allrecipes_adaptive()
    if success:
        print(f"[{get_timestamp()}] 🎉 Test completed successfully!")
    else:
        print(f"[{get_timestamp()}] 💥 Test failed!")
        sys.exit(1)
