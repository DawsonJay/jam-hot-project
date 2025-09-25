#!/usr/bin/env python3
"""
Test script to verify Serious Eats adapter works correctly.

This script tests that Serious Eats works with the adaptive scraper.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.adapters.serious_eats_adapter import SeriousEatsAdapter
from scraper.core.adaptive_scraper import AdaptiveScraper

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD-HHMM format."""
    return datetime.utcnow().strftime("%Y-%m-%d-%H%M")

def test_serious_eats_connectivity():
    """Test Serious Eats connectivity and basic functionality."""
    print(f"[{get_timestamp()}] Testing Serious Eats connectivity...")
    
    try:
        # Test 1: Basic adapter initialization
        print(f"[{get_timestamp()}] Step 1: Testing adapter initialization...")
        adapter = SeriousEatsAdapter()
        print(f"[{get_timestamp()}] ✅ Adapter initialized: {adapter.get_site_name()}")
        print(f"[{get_timestamp()}] Scraping method: {adapter.get_scraping_method()}")
        
        # Test 2: Search URL generation
        print(f"[{get_timestamp()}] Step 2: Testing search URL generation...")
        search_url = adapter.search_for_fruit("strawberry")
        print(f"[{get_timestamp()}] ✅ Search URL: {search_url}")
        
        # Test 3: Test with adaptive scraper
        print(f"[{get_timestamp()}] Step 3: Testing with adaptive scraper...")
        with AdaptiveScraper(headless=True) as scraper:
            recipes = scraper.scrape_site(adapter, "strawberry")
            
            print(f"[{get_timestamp()}] ✅ Scraping completed!")
            print(f"[{get_timestamp()}] Found {len(recipes)} recipes")
            
            if recipes:
                print(f"[{get_timestamp()}] Sample recipe titles:")
                for i, recipe in enumerate(recipes[:3], 1):
                    title = recipe.get('title', 'Unknown')
                    print(f"    {i}. {title}")
                
                # Save sample recipe data for inspection
                import json
                sample_file = f"serious_eats_sample_strawberry.json"
                with open(sample_file, 'w', encoding='utf-8') as f:
                    json.dump(recipes[0] if recipes else {}, f, indent=2, ensure_ascii=False)
                print(f"[{get_timestamp()}] ✅ Sample recipe saved to {sample_file}")
                
                print(f"[{get_timestamp()}] 🎉 Serious Eats test successful!")
                return True
            else:
                print(f"[{get_timestamp()}] ⚠️  No recipes found.")
                return False
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Serious Eats test failed:")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_serious_eats_connectivity()
    if success:
        print(f"[{get_timestamp()}] 🎉 Test completed successfully!")
    else:
        print(f"[{get_timestamp()}] 💥 Test failed!")
        sys.exit(1)
