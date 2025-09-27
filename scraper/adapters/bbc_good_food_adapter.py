#!/usr/bin/env python3
"""
BBC Good Food adapter for jam recipe scraping.

This adapter scrapes jam recipes from BBC Good Food website.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
import time
import random

from .base_adapter import BaseAdapter

class BBCGoodFoodAdapter(BaseAdapter):
    """Adapter for scraping BBC Good Food jam recipes."""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bbcgoodfood.com"
        self.search_url = "https://www.bbcgoodfood.com/search"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_for_fruit(self, fruit_name: str) -> str:
        """Generate search URL for fruit."""
        search_query = f"{fruit_name} jam"
        return f"{self.search_url}?q={search_query}"
    
    def get_recipe_urls(self, search_results_html: str) -> List[str]:
        """Extract recipe URLs from search results, filtering out collection pages."""
        soup = BeautifulSoup(search_results_html, 'html.parser')
        urls = []
        
        # Look for recipe links
        recipe_links = soup.select('a[href*="/recipes/"]')
        for link in recipe_links:
            href = link.get('href')
            if href and '/recipes/' in href:
                # Filter out collection and category pages
                if any(keyword in href.lower() for keyword in ['collection', 'category']):
                    continue
                    
                # Only include individual recipe pages
                full_url = urljoin(self.base_url, href)
                if full_url not in urls:
                    urls.append(full_url)
        
        print(f"Found {len(urls)} individual recipe URLs (filtered out collection pages)")
        return urls
    
    def extract_recipe_data(self, recipe_html: str, recipe_url: str) -> Dict[str, Any]:
        """Extract recipe data from HTML."""
        soup = BeautifulSoup(recipe_html, 'html.parser')
        
        # Extract all recipe data
        recipe_data = {
            'title': self._extract_title(soup),
            'description': self._extract_description(soup),
            'ingredients': self._extract_ingredients(soup),
            'instructions': self._extract_instructions(soup),
            'rating': self._extract_rating(soup),
            'review_count': self._extract_review_count(soup),
            'image_url': self._extract_image_url(soup),
            'servings': self._extract_servings(soup),
            'source_url': recipe_url
        }
        
        # Validate that this is actually a jam recipe
        title = recipe_data.get('title', '')
        if not self._is_jam_recipe(recipe_data):
            raise ValueError(f"Recipe '{title}' is not a jam recipe")
        
        return recipe_data
    
    def get_site_name(self) -> str:
        """Get the name of this site."""
        return "BBC Good Food"
    
    def _is_jam_related_url(self, url: str, fruit_name: str) -> bool:
        """Check if URL is likely to be a jam recipe."""
        url_lower = url.lower()
        fruit_lower = fruit_name.lower()
        
        # Must contain the fruit name
        if fruit_lower not in url_lower:
            return False
        
        # Must contain jam-related keywords
        jam_keywords = ['jam', 'jelly', 'preserve', 'marmalade', 'conserve']
        return any(keyword in url_lower for keyword in jam_keywords)
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract recipe title."""
        selectors = [
            'h1.recipe-header__title',
            'h1[data-test-id="recipe-title"]',
            'h1.recipe-title',
            'h1'
        ]
        
        for selector in selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text(strip=True)
        
        return "Unknown Recipe"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract recipe description."""
        # First try JSON-LD
        json_ld_desc = self._extract_description_from_json_ld(soup)
        if json_ld_desc:
            return json_ld_desc
        
        selectors = [
            '.recipe-header__description',
            '.recipe-description',
            '[data-test-id="recipe-description"]',
            '.recipe-intro'
        ]
        
        for selector in selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                return desc_elem.get_text(strip=True)
        
        return ""
    
    def _extract_ingredients(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract ingredients list."""
        ingredients = []
        
        # Try to find ingredients list
        ingredient_selectors = [
            '.ingredients-list__item',
            '.recipe-ingredients__item',
            '.recipe-ingredients li',
            '[data-test-id="ingredient"]'
        ]
        
        for selector in ingredient_selectors:
            ingredient_elems = soup.select(selector)
            if ingredient_elems:
                for elem in ingredient_elems:
                    text = elem.get_text(strip=True)
                    if text:
                        ingredients.append({
                            'name': text,
                            'amount': '',
                            'unit': ''
                        })
                break
        
        return ingredients
    
    def _extract_instructions(self, soup: BeautifulSoup) -> List[str]:
        """Extract cooking instructions."""
        instructions = []
        
        # First try JSON-LD
        json_ld_instructions = self._extract_instructions_from_json_ld(soup)
        if json_ld_instructions:
            return json_ld_instructions
        
        # Try to find instructions
        instruction_selectors = [
            '.recipe-method__item',
            '.method-list__item',
            '.recipe-method li',
            '[data-test-id="method-step"]'
        ]
        
        for selector in instruction_selectors:
            instruction_elems = soup.select(selector)
            if instruction_elems:
                for elem in instruction_elems:
                    text = elem.get_text(strip=True)
                    if text:
                        instructions.append(text)
                break
        
        return instructions
    
    def _extract_instructions_from_json_ld(self, soup: BeautifulSoup) -> List[str]:
        """Extract instructions from JSON-LD structured data."""
        try:
            json_scripts = soup.select('script[type="application/ld+json"]')
            for script in json_scripts:
                data = json.loads(script.string)
                if data.get('@type') == 'Recipe' and 'recipeInstructions' in data:
                    instructions = []
                    for instruction in data['recipeInstructions']:
                        if isinstance(instruction, dict) and 'text' in instruction:
                            instructions.append(instruction['text'])
                        elif isinstance(instruction, str):
                            instructions.append(instruction)
                    return instructions
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        return []
    
    def _extract_rating(self, soup: BeautifulSoup) -> float:
        """Extract recipe rating."""
        # First try JSON-LD
        json_ld_rating = self._extract_rating_from_json_ld(soup)
        if json_ld_rating > 0:
            return json_ld_rating
        
        # Look for rating in various formats
        rating_selectors = [
            '.rating__value',
            '[data-test-id="rating"]',
            '.recipe-rating',
            '.star-rating'
        ]
        
        for selector in rating_selectors:
            rating_elem = soup.select_one(selector)
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                # Extract number from text
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    return float(rating_match.group(1))
        
        return 0.0
    
    def _extract_rating_from_json_ld(self, soup: BeautifulSoup) -> float:
        """Extract rating from JSON-LD structured data."""
        try:
            json_scripts = soup.select('script[type="application/ld+json"]')
            for script in json_scripts:
                data = json.loads(script.string)
                if 'aggregateRating' in data:
                    rating_data = data['aggregateRating']
                    if isinstance(rating_data, dict) and 'ratingValue' in rating_data:
                        return float(rating_data['ratingValue'])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass
        return 0.0
    
    def _extract_review_count(self, soup: BeautifulSoup) -> int:
        """Extract number of reviews."""
        # First try JSON-LD
        json_ld_reviews = self._extract_review_count_from_json_ld(soup)
        if json_ld_reviews > 0:
            return json_ld_reviews
        
        # Look for review count
        review_selectors = [
            '.rating__count',
            '[data-test-id="review-count"]',
            '.recipe-reviews'
        ]
        
        for selector in review_selectors:
            review_elem = soup.select_one(selector)
            if review_elem:
                review_text = review_elem.get_text(strip=True)
                # Extract number from text
                review_match = re.search(r'(\d+)', review_text)
                if review_match:
                    return int(review_match.group(1))
        
        return 0
    
    def _extract_review_count_from_json_ld(self, soup: BeautifulSoup) -> int:
        """Extract review count from JSON-LD structured data."""
        try:
            json_scripts = soup.select('script[type="application/ld+json"]')
            for script in json_scripts:
                data = json.loads(script.string)
                if 'aggregateRating' in data:
                    rating_data = data['aggregateRating']
                    if isinstance(rating_data, dict) and 'reviewCount' in rating_data:
                        return int(rating_data['reviewCount'])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass
        return 0
    
    def _extract_image_url(self, soup: BeautifulSoup) -> str:
        """Extract recipe image URL."""
        # First try JSON-LD
        json_ld_image = self._extract_image_url_from_json_ld(soup)
        if json_ld_image:
            return json_ld_image
        
        # Look for recipe image
        img_selectors = [
            '.recipe-header__image img',
            '.recipe-image img',
            '[data-test-id="recipe-image"] img',
            '.hero-image img'
        ]
        
        for selector in img_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                src = img_elem.get('src') or img_elem.get('data-src')
                if src:
                    return urljoin(self.base_url, src)
        
        return ""
    
    def _extract_servings(self, soup: BeautifulSoup) -> int:
        """Extract number of servings."""
        # First try JSON-LD
        json_ld_servings = self._extract_servings_from_json_ld(soup)
        if json_ld_servings > 0:
            return json_ld_servings
        
        # Look for servings information
        serving_selectors = [
            '.recipe-details__servings',
            '[data-test-id="servings"]',
            '.recipe-servings'
        ]
        
        for selector in serving_selectors:
            serving_elem = soup.select_one(selector)
            if serving_elem:
                serving_text = serving_elem.get_text(strip=True)
                # Extract number from text
                serving_match = re.search(r'(\d+)', serving_text)
                if serving_match:
                    return int(serving_match.group(1))
        
        return 0
    
    
    def _is_jam_recipe(self, recipe_data: Dict[str, Any]) -> bool:
        """
        Validate that this is actually a jam recipe using shared logic.
        
        Args:
            recipe_data (Dict[str, Any]): Recipe data to validate
            
        Returns:
            bool: True if this appears to be a jam recipe
        """
        from scraper.core.recipe_validator import is_jam_recipe
        return is_jam_recipe(recipe_data)
    
    def extract_fruits_from_ingredients(self, ingredients: List[Dict[str, str]]) -> List[str]:
        """
        Extract fruit names from ingredients list.
        
        Args:
            ingredients: List of ingredient dictionaries
            
        Returns:
            List of fruit AI names found in ingredients
        """
        from scraper.fruit_mappings import extract_fruits_from_text
        
        fruits = set()
        for ingredient in ingredients:
            ingredient_text = ingredient.get('name', '')
            if ingredient_text:
                found_fruits = extract_fruits_from_text(ingredient_text)
                fruits.update(found_fruits)
        
        return list(fruits)
    
    def _extract_description_from_json_ld(self, soup: BeautifulSoup) -> str:
        """Extract description from JSON-LD structured data."""
        try:
            json_scripts = soup.select('script[type="application/ld+json"]')
            for script in json_scripts:
                data = json.loads(script.string)
                if data.get('@type') == 'Recipe' and 'description' in data:
                    return data['description']
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        return ""
    
    def _extract_image_url_from_json_ld(self, soup: BeautifulSoup) -> str:
        """Extract image URL from JSON-LD structured data."""
        try:
            json_scripts = soup.select('script[type="application/ld+json"]')
            for script in json_scripts:
                data = json.loads(script.string)
                if data.get('@type') == 'Recipe' and 'image' in data:
                    image_data = data['image']
                    if isinstance(image_data, list) and len(image_data) > 0:
                        image_obj = image_data[0]
                        if isinstance(image_obj, dict) and 'url' in image_obj:
                            return image_obj['url']
                    elif isinstance(image_data, dict) and 'url' in image_data:
                        return image_data['url']
                    elif isinstance(image_data, str):
                        return image_data
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        return ""
    
    def _extract_servings_from_json_ld(self, soup: BeautifulSoup) -> int:
        """Extract servings from JSON-LD structured data."""
        try:
            json_scripts = soup.select('script[type="application/ld+json"]')
            for script in json_scripts:
                data = json.loads(script.string)
                if data.get('@type') == 'Recipe' and 'recipeYield' in data:
                    yield_data = data['recipeYield']
                    if isinstance(yield_data, (int, float)):
                        return int(yield_data)
                    elif isinstance(yield_data, str):
                        # Extract number from string like "Makes 3-4 jars"
                        import re
                        match = re.search(r'(\d+)', yield_data)
                        if match:
                            return int(match.group(1))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            pass
        return 0
    
