#!/usr/bin/env python3
"""
Debug Image URL Extraction

This script helps us see what URLs are actually in the Google Images HTML
"""

import sys
import re
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


def main():
    """Debug URL extraction from Google Images"""
    print("🔍 Debugging Google Images URL Extraction")
    print("=" * 60)
    
    # Start browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Search for strawberries
        search_url = "https://www.google.com/search?q=strawberry+fruit&tbm=isch&hl=en"
        print(f"\n🔍 Loading: {search_url}")
        
        driver.get(search_url)
        time.sleep(3)
        
        # Scroll to load images
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        
        html = driver.page_source
        print(f"📄 Got {len(html):,} characters of HTML")
        
        # Try different patterns
        print("\n" + "=" * 60)
        print("Testing different URL extraction patterns:")
        print("=" * 60)
        
        # Pattern 1: Original URLs (ou)
        print("\n1️⃣  Original URLs (ou pattern):")
        ou_pattern = r'"ou":"(https?://[^"]+)"'
        ou_matches = re.findall(ou_pattern, html)
        print(f"   Found {len(ou_matches)} matches")
        if ou_matches:
            for i, url in enumerate(ou_matches[:5], 1):
                print(f"   {i}. {url[:100]}...")
        
        # Pattern 2: Thumbnail URLs
        print("\n2️⃣  Thumbnail URLs (encrypted-tbn):")
        thumb_pattern = r'"(https://encrypted-tbn\d\.gstatic\.com/images[^"]+)"'
        thumb_matches = re.findall(thumb_pattern, html)
        print(f"   Found {len(thumb_matches)} matches")
        if thumb_matches:
            for i, url in enumerate(thumb_matches[:5], 1):
                print(f"   {i}. {url[:100]}...")
        
        # Pattern 3: Look for JSON-like structures with image metadata
        print("\n3️⃣  Looking for AF_initDataCallback structures:")
        af_pattern = r'AF_initDataCallback\({[^}]*?"(\w+)"[^}]*?\}[^;]*?;'
        af_matches = re.findall(af_pattern, html)
        print(f"   Found {len(af_matches)} AF_initDataCallback entries")
        
        # Pattern 4: Look for data-src or similar attributes
        print("\n4️⃣  Image src attributes:")
        src_pattern = r'<img[^>]+src="([^"]+)"'
        src_matches = re.findall(src_pattern, html)
        print(f"   Found {len(src_matches)} img src attributes")
        if src_matches:
            for i, url in enumerate(src_matches[:5], 1):
                if 'http' in url:
                    print(f"   {i}. {url[:100]}...")
        
        # Save a sample of HTML for manual inspection
        sample_file = Path(__file__).parent.parent.parent.parent / "test_html_sample.txt"
        with open(sample_file, 'w') as f:
            # Save first 50,000 chars
            f.write(html[:50000])
        print(f"\n💾 Saved HTML sample to: {sample_file}")
        print("   (First 50,000 characters for manual inspection)")
        
    finally:
        driver.quit()
        print("\n✅ Browser stopped")


if __name__ == "__main__":
    main()
