#!/usr/bin/env python3
"""
Test Improved Google Images Scraper

Tests the new validation and retry logic with better search terms.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from scraper.images.adapters.google_images_adapter import GoogleImagesAdapter
from scraper.images.core.image_scraper import ImageScraper


def test_improved_scraper():
    """
    Test the improved scraper with validation and retry logic
    """
    print("🧪 Testing Improved Google Images Scraper")
    print("=" * 60)
    print("\n🎯 Changes:")
    print("  ✅ Image validation (size, dimensions, aspect ratio)")
    print("  ✅ Auto-retry until target reached")
    print("  ✅ Better search terms (more specific)")
    print("  ✅ Auto-rejection of bad images")
    
    # Test with apple (had issues before)
    test_fruit = "apple"
    target_images = 50  # Try for 50 good images
    
    print(f"\n📊 Test Configuration:")
    print(f"  Fruit: {test_fruit}")
    print(f"  Target: {target_images} validated images")
    print(f"  Output: test_images_improved/{test_fruit}/")
    
    # Clean up previous test
    test_output_dir = Path("test_images_improved") / test_fruit
    if test_output_dir.exists():
        import shutil
        shutil.rmtree(test_output_dir.parent)
        print(f"\n🗑️  Cleaned up previous test")
    
    # Initialize adapter and scraper
    adapter = GoogleImagesAdapter()
    scraper = ImageScraper(
        output_dir="test_images_improved",
        rate_limit=0.5,  # Faster for testing
        headless=True
    )
    
    print(f"\n🚀 Starting improved scraper...")
    print("-" * 60)
    
    # Run scraper
    results = scraper.scrape_fruit_images(adapter, test_fruit, target_images)
    
    # Detailed results
    print(f"\n\n{'='*60}")
    print(f"📊 TEST RESULTS FOR {test_fruit.upper()}")
    print(f"{'='*60}")
    print(f"  URLs found: {results['found']}")
    print(f"  Downloaded: {results['downloaded']}")
    print(f"  ✅ Validated: {results['validated']}")
    print(f"  ❌ Rejected: {results['rejected']}")
    print(f"  ⚠️  Failed: {results['failed']}")
    print(f"  Target: {target_images}")
    print(f"  Success: {'YES' if results['validated'] >= target_images else 'PARTIAL'}")
    
    if results['validated'] > 0:
        quality_rate = (results['validated'] / results['downloaded'] * 100) if results['downloaded'] > 0 else 0
        print(f"  Quality rate: {quality_rate:.1f}%")
        
        # Check actual files
        downloaded_files = list(test_output_dir.iterdir())
        total_size = sum(f.stat().st_size for f in downloaded_files)
        avg_size = total_size / len(downloaded_files) if downloaded_files else 0
        
        print(f"\n📁 Files on disk: {len(downloaded_files)}")
        print(f"  Total size: {total_size / (1024*1024):.2f} MB")
        print(f"  Average size: {avg_size / 1024:.2f} KB")
        
        print(f"\n✅ Test successful! Check test_images_improved/{test_fruit}/ for results")
    else:
        print(f"\n❌ Test failed - no valid images")
    
    print(f"{'='*60}")


if __name__ == "__main__":
    test_improved_scraper()
