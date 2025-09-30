#!/usr/bin/env python3
"""
Test Stricter Image Validation

Tests the enhanced validation system with stricter quality checks.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from scraper.images.adapters.google_images_adapter import GoogleImagesAdapter
from scraper.images.core.image_scraper import ImageScraper


def test_stricter_validation():
    """
    Test the stricter validation system
    """
    print("🧪 Testing Stricter Image Validation")
    print("=" * 60)
    print("\n🎯 Enhanced Validation:")
    print("  ✅ File size check (≥ 5KB)")
    print("  ✅ Dimension check (≥ 100x100)")
    print("  ✅ Aspect ratio check (≤ 5:1)")
    print("  ✅ Brightness check (≥ 30)")
    print("  ✅ Contrast check (≥ 20)")
    print("  ✅ Better search terms")
    
    # Test with apple (had issues before)
    test_fruit = "apple"
    target_images = 20  # Smaller test batch
    
    print(f"\n📊 Test Configuration:")
    print(f"  Fruit: {test_fruit}")
    print(f"  Target: {target_images} validated images")
    print(f"  Output: test_strict_validation/{test_fruit}/")
    
    # Clean up previous test
    test_output_dir = Path("test_strict_validation") / test_fruit
    if test_output_dir.exists():
        import shutil
        shutil.rmtree(test_output_dir.parent)
        print(f"\n🗑️  Cleaned up previous test")
    
    # Initialize adapter and scraper
    adapter = GoogleImagesAdapter()
    scraper = ImageScraper(
        output_dir="test_strict_validation",
        rate_limit=0.5,  # Faster for testing
        headless=True
    )
    
    print(f"\n🚀 Starting stricter validation test...")
    print("-" * 60)
    
    # Run scraper
    results = scraper.scrape_fruit_images(adapter, test_fruit, target_images)
    
    # Detailed results
    print(f"\n\n{'='*60}")
    print(f"📊 STRICT VALIDATION RESULTS FOR {test_fruit.upper()}")
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
        
        print(f"\n✅ Test successful! Check test_strict_validation/{test_fruit}/ for results")
        print(f"\n🔍 Manual Review Recommended:")
        print(f"  - Check for cartoon/illustration images")
        print(f"  - Verify fruit is clearly visible")
        print(f"  - Look for text-only or sign images")
        print(f"  - Ensure images show actual {test_fruit} fruit")
    else:
        print(f"\n❌ Test failed - no valid images")
    
    print(f"{'='*60}")


if __name__ == "__main__":
    test_stricter_validation()
