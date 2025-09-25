#!/usr/bin/env python3
"""
Debug script to examine Serious Eats ingredient structure.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def debug_serious_eats_ingredients():
    """Debug Serious Eats ingredient structure."""
    print("🔍 Debugging Serious Eats ingredient structure...")
    
    # Test with a known recipe URL
    recipe_url = "https://www.seriouseats.com/customizable-strawberry-jam-recipe"
    print(f"Testing recipe: {recipe_url}")
    
    # Get the HTML
    response = requests.get(recipe_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print(f"Response status: {response.status_code}")
    print(f"Response size: {len(response.text)} characters")
    
    # Save HTML to file for inspection
    with open("serious_eats_recipe_debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✅ HTML saved to serious_eats_recipe_debug.html")
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for ingredient-related patterns
    html = response.text.lower()
    
    print("\n🔍 Ingredient pattern analysis:")
    patterns_to_check = [
        'ingredient',
        'recipe-ingredient',
        'structured-ingredient',
        'mntl-structured',
        'sugar',
        'strawberry',
        'pectin'
    ]
    
    for pattern in patterns_to_check:
        count = html.count(pattern)
        print(f"  {pattern}: {count} occurrences")
    
    # Look for specific selectors
    print("\n🔍 Ingredient selector analysis:")
    selectors_to_test = [
        '.recipe-ingredients li',
        '.ingredients li',
        '.ingredient-item',
        '.recipe-ingredient',
        '.mntl-structured-ingredients__list-item',
        '.structured-ingredients__list-item',
        '.ingredient',
        '.recipe-ingredients-list li',
        '[class*="ingredient"]',
        '[class*="recipe-ingredient"]',
        'li[class*="ingredient"]'
    ]
    
    for selector in selectors_to_test:
        elements = soup.select(selector)
        if elements:
            print(f"  ✅ {selector}: {len(elements)} elements")
            # Show first few examples
            for i, elem in enumerate(elements[:3]):
                text = elem.get_text(strip=True)[:100]
                print(f"    {i+1}. {text}")
        else:
            print(f"  ❌ {selector}: 0 elements")
    
    # Look for any list items that might contain ingredients
    print("\n🔍 General list analysis:")
    all_lis = soup.find_all('li')
    print(f"Total <li> elements: {len(all_lis)}")
    
    # Look for li elements that might contain ingredients
    ingredient_like_lis = []
    for li in all_lis:
        text = li.get_text(strip=True).lower()
        if any(word in text for word in ['sugar', 'strawberry', 'pectin', 'lemon', 'cup', 'tablespoon', 'teaspoon']):
            ingredient_like_lis.append(li)
    
    print(f"LI elements that look like ingredients: {len(ingredient_like_lis)}")
    for i, li in enumerate(ingredient_like_lis[:5]):
        text = li.get_text(strip=True)[:100]
        classes = li.get('class', [])
        print(f"  {i+1}. {text} (classes: {classes})")

if __name__ == "__main__":
    debug_serious_eats_ingredients()
