#!/usr/bin/env python3
"""
Debug script to examine Serious Eats rating structure.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
import re

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def debug_serious_eats_ratings():
    """Debug Serious Eats rating structure."""
    print("🔍 Debugging Serious Eats rating structure...")
    
    # Test with a known recipe URL
    recipe_url = "https://www.seriouseats.com/rustic-apricot-jam-recipe"
    print(f"Testing recipe: {recipe_url}")
    
    # Get the HTML
    response = requests.get(recipe_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print(f"Response status: {response.status_code}")
    print(f"Response size: {len(response.text)} characters")
    
    # Save HTML to file for inspection
    with open("serious_eats_ratings_debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✅ HTML saved to serious_eats_ratings_debug.html")
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for rating-related patterns
    html = response.text.lower()
    
    print("\n🔍 Rating pattern analysis:")
    patterns_to_check = [
        'rating',
        'star',
        'review',
        'score',
        'vote',
        'rate',
        'out of',
        'stars',
        'reviews',
        'votes',
        'rating:',
        'score:',
        '4.5',
        '4.0',
        '5.0',
        '3.5',
        '3.0'
    ]
    
    for pattern in patterns_to_check:
        count = html.count(pattern)
        if count > 0:
            print(f"  {pattern}: {count} occurrences")
    
    # Look for specific selectors
    print("\n🔍 Rating selector analysis:")
    selectors_to_test = [
        '.rating',
        '.recipe-rating',
        '.star-rating',
        '.review-rating',
        '.rating-value',
        '.rating-score',
        '.rating-stars',
        '.review-count',
        '.reviews',
        '.rating-count',
        '.comment-count',
        '.vote-count',
        '.score',
        '[class*="rating"]',
        '[class*="star"]',
        '[class*="review"]',
        '[class*="score"]',
        '[class*="vote"]',
        '[data-rating]',
        '[data-score]',
        '[data-reviews]',
        '[data-votes]'
    ]
    
    for selector in selectors_to_test:
        elements = soup.select(selector)
        if elements:
            print(f"  ✅ {selector}: {len(elements)} elements")
            # Show first few examples
            for i, elem in enumerate(elements[:3]):
                text = elem.get_text(strip=True)
                classes = elem.get('class', [])
                attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
                print(f"    {i+1}. Text: '{text}' | Classes: {classes} | Data attrs: {attrs}")
        else:
            print(f"  ❌ {selector}: 0 elements")
    
    # Look for any elements that might contain rating information
    print("\n🔍 General rating search:")
    
    # Search for common rating patterns in text
    rating_patterns = [
        r'(\d+\.?\d*)\s*out\s*of\s*5',
        r'(\d+\.?\d*)\s*/\s*5',
        r'(\d+\.?\d*)\s*stars?',
        r'rating[:\s]*(\d+\.?\d*)',
        r'score[:\s]*(\d+\.?\d*)',
        r'(\d+)\s*reviews?',
        r'(\d+)\s*votes?',
        r'(\d+)\s*ratings?'
    ]
    
    for pattern in rating_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"  Pattern '{pattern}': {matches}")
    
    # Look for any elements containing numbers that might be ratings
    print("\n🔍 Number-containing elements:")
    all_elements = soup.find_all(text=re.compile(r'\d+\.?\d*'))
    rating_like_elements = []
    
    for elem in all_elements:
        text = elem.strip()
        if re.match(r'^\d+\.?\d*$', text) and float(text) <= 5.0:
            parent = elem.parent
            if parent:
                parent_text = parent.get_text(strip=True)
                if any(word in parent_text.lower() for word in ['rating', 'star', 'review', 'score', 'vote']):
                    rating_like_elements.append((text, parent_text[:100]))
    
    print(f"Found {len(rating_like_elements)} rating-like elements:")
    for rating, context in rating_like_elements[:5]:
        print(f"  Rating: {rating} | Context: {context}")

if __name__ == "__main__":
    debug_serious_eats_ratings()
