#!/usr/bin/env python3
"""
Download Training Images Script

This script downloads fruit images for AI training using the Google Images adapter.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from scraper.images.adapters.google_images_adapter import GoogleImagesAdapter
from scraper.images.core.image_scraper import ImageScraper


def main():
    """
    Download fruit images for AI training
    """
    print("🍓 Fruit Image Downloader for AI Training")
    print("=" * 60)
    
    # Main fruits (29 fruits from database) - 172 images each
    main_fruits = [
        "strawberry", "apple", "raspberry", "blueberry", "peach",
        "plum", "cherry", "grape", "orange", "lemon", "lime",
        "fig", "apricot", "mango", "pear", "blackberry", "cranberry",
        "currant", "elderberry", "gooseberry", "grapefruit", "kiwi",
        "nectarine", "papaya", "passion_fruit", "pineapple", "quince",
        "rhubarb", "dragon_fruit"
    ]
    
    # Exotic fruits for "unknown" class - 25 images each
    exotic_fruits = [
        "starfruit", "persimmon", "pomegranate", "lychee", "rambutan",
        "durian", "jackfruit", "mangosteen", "longan", "custard_apple",
        "soursop", "breadfruit", "plantain", "tamarind", "guava",
        "feijoa", "cherimoya", "sapodilla", "sugar_apple", "monk_fruit",
        "horned_melon", "kiwano", "ugli_fruit", "yuzu", "kumquat"
    ]
    
    print(f"\n🎯 Main fruits ({len(main_fruits)}):")
    for i, fruit in enumerate(main_fruits, 1):
        print(f"  {i:2}. {fruit}")
    
    print(f"\n🌴 Exotic fruits for 'unknown' class ({len(exotic_fruits)}):")
    for i, fruit in enumerate(exotic_fruits, 1):
        print(f"  {i:2}. {fruit}")
    
    # Configuration
    main_images_per_fruit = 172  # Main fruits: 172 each
    exotic_images_per_fruit = 25  # Exotic fruits: 25 each
    output_dir = "scraper/images/data"
    
    total_main_images = len(main_fruits) * main_images_per_fruit
    total_exotic_images = len(exotic_fruits) * exotic_images_per_fruit
    total_images = total_main_images + total_exotic_images
    
    print(f"\n⚙️  Configuration:")
    print(f"  Main fruits: {len(main_fruits)} × {main_images_per_fruit} = {total_main_images:,} images")
    print(f"  Exotic fruits: {len(exotic_fruits)} × {exotic_images_per_fruit} = {total_exotic_images:,} images")
    print(f"  Total images: {total_images:,}")
    print(f"  Output directory: {output_dir}")
    
    # Auto-proceed for automated execution
    print("\n✅ Auto-proceeding with download...")
    
    # Initialize adapter and scraper
    adapter = GoogleImagesAdapter()
    scraper = ImageScraper(output_dir=output_dir, rate_limit=1.0, headless=True)
    
    # Download main fruits first
    print(f"\n🍓 Downloading main fruits...")
    main_results = scraper.scrape_multiple_fruits(
        adapter=adapter,
        fruit_names=main_fruits,
        max_images_per_fruit=main_images_per_fruit
    )
    
    # Download exotic fruits to 'unknown' folder
    print(f"\n🌴 Downloading exotic fruits to 'unknown' folder...")
    scraper.output_dir = Path(output_dir) / "unknown"
    scraper.output_dir.mkdir(exist_ok=True, parents=True)
    
    exotic_results = scraper.scrape_multiple_fruits(
        adapter=adapter,
        fruit_names=exotic_fruits,
        max_images_per_fruit=exotic_images_per_fruit
    )
    
    # Combine results
    results = {**main_results['fruit_results'], **exotic_results['fruit_results']}
    
    # Detailed results
    print(f"\n📋 DETAILED RESULTS")
    print("-" * 60)
    print(f"🍓 MAIN FRUITS:")
    for fruit in main_fruits:
        if fruit in results:
            result = results[fruit]
            success_rate = (result['downloaded']/result['found']*100) if result['found'] > 0 else 0
            print(f"  {fruit:15}: {result['downloaded']:3}/{result['found']:3} downloaded ({success_rate:.0f}%)")
    
    print(f"\n🌴 EXOTIC FRUITS (unknown class):")
    for fruit in exotic_fruits:
        if fruit in results:
            result = results[fruit]
            success_rate = (result['downloaded']/result['found']*100) if result['found'] > 0 else 0
            print(f"  {fruit:15}: {result['downloaded']:3}/{result['found']:3} downloaded ({success_rate:.0f}%)")
    
    # Summary
    total_downloaded = sum(result['downloaded'] for result in results.values())
    total_found = sum(result['found'] for result in results.values())
    overall_success_rate = (total_downloaded/total_found*100) if total_found > 0 else 0
    
    print(f"\n📊 SUMMARY:")
    print(f"  Total images found: {total_found:,}")
    print(f"  Total images downloaded: {total_downloaded:,}")
    print(f"  Overall success rate: {overall_success_rate:.1f}%")
    
    print(f"\n✅ Download complete!")
    print(f"📁 Main fruits saved to: {output_dir}/[fruit_name]/")
    print(f"📁 Exotic fruits saved to: {output_dir}/unknown/")
    print(f"\n📋 NEXT STEPS:")
    print("1. Review downloaded images in each fruit folder")
    print("2. Delete any misclassified or low-quality images")
    print("3. Run AI training on the curated dataset")
    print("4. The 'unknown' folder will serve as the 'unknown fruit' class for training")


if __name__ == "__main__":
    main()
