#!/usr/bin/env python3
"""
Debug script to examine Serious Eats instruction structure.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def debug_serious_eats_instructions():
    """Debug Serious Eats instruction structure."""
    print("🔍 Debugging Serious Eats instruction structure...")
    
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
    with open("serious_eats_instructions_debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("✅ HTML saved to serious_eats_instructions_debug.html")
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for instruction-related patterns
    html = response.text.lower()
    
    print("\n🔍 Instruction pattern analysis:")
    patterns_to_check = [
        'instruction',
        'step',
        'direction',
        'method',
        'procedure',
        'cooking',
        'preparation',
        'directions',
        'steps',
        'how to',
        'process'
    ]
    
    for pattern in patterns_to_check:
        count = html.count(pattern)
        print(f"  {pattern}: {count} occurrences")
    
    # Look for specific selectors
    print("\n🔍 Instruction selector analysis:")
    selectors_to_test = [
        '.recipe-instructions li',
        '.instructions li',
        '.recipe-steps li',
        '.cooking-instructions p',
        '.recipe-directions li',
        '.directions li',
        '.mntl-sc-block-group--OL li',
        '.mntl-sc-block-group--UL li',
        'ol li',
        'ul li',
        '[class*="instruction"]',
        '[class*="step"]',
        '[class*="direction"]',
        'li[class*="instruction"]',
        'li[class*="step"]',
        'p[class*="instruction"]',
        'p[class*="step"]'
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
    
    # Look for any ordered or unordered lists that might contain instructions
    print("\n🔍 General list analysis:")
    all_ols = soup.find_all('ol')
    all_uls = soup.find_all('ul')
    print(f"Total <ol> elements: {len(all_ols)}")
    print(f"Total <ul> elements: {len(all_uls)}")
    
    # Look for ol/ul elements that might contain instructions
    instruction_like_lists = []
    for ol in all_ols:
        text = ol.get_text(strip=True).lower()
        if any(word in text for word in ['heat', 'cook', 'simmer', 'boil', 'stir', 'add', 'combine', 'mix', 'place', 'remove']):
            instruction_like_lists.append(ol)
    
    for ul in all_uls:
        text = ul.get_text(strip=True).lower()
        if any(word in text for word in ['heat', 'cook', 'simmer', 'boil', 'stir', 'add', 'combine', 'mix', 'place', 'remove']):
            instruction_like_lists.append(ul)
    
    print(f"Lists that look like instructions: {len(instruction_like_lists)}")
    for i, list_elem in enumerate(instruction_like_lists[:3]):
        text = list_elem.get_text(strip=True)[:200]
        classes = list_elem.get('class', [])
        print(f"  {i+1}. {text} (classes: {classes})")

if __name__ == "__main__":
    debug_serious_eats_instructions()
