#!/usr/bin/env python3
"""
Test Google Images Scraper

Quick test with 2-3 fruits to verify everything works.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from scraper.images.adapters.google_images_adapter import GoogleImagesAdapter
from scraper.images.core.image_scraper import ImageScraper


def main():
    """
    Test Google Images scraper with a few fruits
    """
    print("🧪 Testing Google Images Scraper")
    print("=" * 50)
    
    # Test with just 3 fruits
    test_fruits = ["strawberry", "apple", "blueberry"]
    images_per_fruit = 25  # 25 total = 5 per search term
    
    print(f"\n🎯 Test fruits: {', '.join(test_fruits)}")
    print(f"📊 Images per fruit: {images_per_fruit}")
    print(f"📁 Output directory: test_images/")
    
    # Initialize adapter and scraper
    adapter = GoogleImagesAdapter()
    scraper = ImageScraper(output_dir="test_images", rate_limit=0.5, headless=True)  # Headless
    
    print(f"\n🚀 Starting test...")
    
    # Test with first fruit only
    fruit = test_fruits[0]
    print(f"\n🍓 Testing with: {fruit}")
    
    try:
        results = scraper.scrape_fruit_images(adapter, fruit, images_per_fruit)
        
        print(f"\n📊 Test Results for {fruit}:")
        print(f"  Found: {results['found']} images")
        print(f"  Downloaded: {results['downloaded']} images")
        print(f"  Failed: {results['failed']} images")
        
        if results['downloaded'] > 0:
            print(f"\n✅ Test successful! Check test_images/{fruit}/ for downloaded images")
        else:
            print(f"\n❌ Test failed - no images downloaded")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Always stop browser
        scraper.stop_browser()


if __name__ == "__main__":
    main()
