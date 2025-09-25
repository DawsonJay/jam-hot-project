#!/usr/bin/env python3
"""
Debug script to examine Serious Eats HTML structure.
"""

import sys
import os
import requests
from urllib.parse import quote_plus

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.adapters.serious_eats_adapter import SeriousEatsAdapter

def debug_serious_eats():
    """Debug Serious Eats HTML structure."""
    print("🔍 Debugging Serious Eats HTML structure...")
    
    adapter = SeriousEatsAdapter()
    search_url = adapter.search_for_fruit("strawberry")
    print(f"Search URL: {search_url}")
    
    # Get the HTML
    response = requests.get(search_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print(f"Response status: {response.status_code}")
    print(f"Response size: {len(response.text)} characters")
    
    # Save HTML to file for inspection
    with open("serious_eats_debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✅ HTML saved to serious_eats_debug.html")
    
    # Look for common patterns
    html = response.text.lower()
    
    # Check for common link patterns
    patterns_to_check = [
        'href="/recipes/',
        'href="/recipe/',
        'class="recipe',
        'class="post',
        'class="article',
        'data-testid',
        'strawberry',
        'jam'
    ]
    
    print("\n🔍 Pattern analysis:")
    for pattern in patterns_to_check:
        count = html.count(pattern)
        print(f"  {pattern}: {count} occurrences")
    
    # Look for specific selectors
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("\n🔍 Selector analysis:")
    selectors_to_test = [
        'a[href*="/recipes/"]',
        'a[href*="/recipe/"]',
        'a[href*="seriouseats.com"]',
        '.recipe-card',
        '.post-card',
        '.article-card',
        '[data-testid*="recipe"]',
        '[data-testid*="post"]',
        'article',
        'h3 a',
        'h4 a',
        '.title a',
        '.headline a'
    ]
    
    for selector in selectors_to_test:
        elements = soup.select(selector)
        if elements:
            print(f"  ✅ {selector}: {len(elements)} elements")
            # Show first few examples
            for i, elem in enumerate(elements[:3]):
                if elem.name == 'a':
                    href = elem.get('href', '')
                    text = elem.get_text(strip=True)[:50]
                    print(f"    {i+1}. {text} -> {href}")
                else:
                    text = elem.get_text(strip=True)[:50]
                    print(f"    {i+1}. {text}")
        else:
            print(f"  ❌ {selector}: 0 elements")

if __name__ == "__main__":
    debug_serious_eats()
