#!/usr/bin/env python3
"""
Detailed debug script to examine Serious Eats rating structure.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
import re
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def debug_serious_eats_ratings_detailed():
    """Debug Serious Eats rating structure in detail."""
    print("🔍 Detailed debugging of Serious Eats rating structure...")
    
    # Test with a known recipe URL
    recipe_url = "https://www.seriouseats.com/customizable-strawberry-jam-recipe"
    print(f"Testing recipe: {recipe_url}")
    
    # Get the HTML
    response = requests.get(recipe_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print(f"Response status: {response.status_code}")
    print(f"Response size: {len(response.text)} characters")
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for ALL JSON-LD scripts
    print("\n🔍 JSON-LD Script Analysis:")
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    print(f"Found {len(json_ld_scripts)} JSON-LD scripts")
    
    for i, script in enumerate(json_ld_scripts):
        print(f"\n--- JSON-LD Script {i+1} ---")
        try:
            data = json.loads(script.string)
            print(f"Type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'aggregateRating' in data:
                    print(f"aggregateRating: {data['aggregateRating']}")
                if 'review' in data:
                    print(f"review: {data['review']}")
                if '@type' in data:
                    print(f"@type: {data['@type']}")
                if 'name' in data:
                    print(f"name: {data['name']}")
                    
            elif isinstance(data, list):
                print(f"Array length: {len(data)}")
                for j, item in enumerate(data):
                    if isinstance(item, dict):
                        print(f"  Item {j+1} keys: {list(item.keys())}")
                        if 'aggregateRating' in item:
                            print(f"  Item {j+1} aggregateRating: {item['aggregateRating']}")
                        if 'review' in item:
                            print(f"  Item {j+1} review: {item['review']}")
                        if '@type' in item:
                            print(f"  Item {j+1} @type: {item['@type']}")
                        if 'name' in item:
                            print(f"  Item {j+1} name: {item['name']}")
                            
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing JSON: {e}")
            print(f"Script content preview: {script.string[:200]}...")
    
    # Look for rating-related text patterns
    print("\n🔍 Rating Text Pattern Search:")
    html = response.text.lower()
    
    # Search for specific rating patterns
    rating_patterns = [
        r'"ratingValue":\s*"([^"]+)"',
        r'"ratingCount":\s*"([^"]+)"',
        r'"ratingValue":\s*(\d+\.?\d*)',
        r'"ratingCount":\s*(\d+)',
        r'rating[:\s]*(\d+\.?\d*)',
        r'(\d+\.?\d*)\s*out\s*of\s*5',
        r'(\d+\.?\d*)\s*/\s*5',
        r'(\d+\.?\d*)\s*stars?'
    ]
    
    for pattern in rating_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"Pattern '{pattern}': {matches}")
    
    # Look for any script tags that might contain rating data
    print("\n🔍 Script Tag Analysis:")
    all_scripts = soup.find_all('script')
    rating_scripts = []
    
    for script in all_scripts:
        if script.string and any(word in script.string.lower() for word in ['rating', 'review', 'star', 'score']):
            rating_scripts.append(script)
    
    print(f"Found {len(rating_scripts)} scripts containing rating-related content")
    for i, script in enumerate(rating_scripts[:3]):  # Show first 3
        content = script.string[:300]
        print(f"Script {i+1} preview: {content}...")
    
    # Look for any elements with data attributes that might contain ratings
    print("\n🔍 Data Attribute Analysis:")
    elements_with_data = soup.find_all(attrs=lambda x: x and any(k.startswith('data-') for k in x.keys()))
    rating_elements = []
    
    for elem in elements_with_data:
        attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
        if any('rating' in str(v).lower() or 'review' in str(v).lower() or 'star' in str(v).lower() for v in attrs.values()):
            rating_elements.append((elem, attrs))
    
    print(f"Found {len(rating_elements)} elements with rating-related data attributes")
    for i, (elem, attrs) in enumerate(rating_elements[:5]):  # Show first 5
        print(f"Element {i+1}: {elem.name} | Data attrs: {attrs}")

if __name__ == "__main__":
    debug_serious_eats_ratings_detailed()
