#!/usr/bin/env python3
"""
Food Network adapter for recipe scraping.

This adapter handles recipe extraction from Food Network website.
"""

import json
import re
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from scraper.adapters.base_adapter import BaseAdapter

class FoodNetworkAdapter(BaseAdapter):
    """Adapter for Food Network recipe scraping."""
    
    def get_site_name(self) -> str:
        """Return the name of the site this adapter scrapes."""
        return "Food Network"
    
    def get_scraping_method(self) -> str:
        """Return the scraping method this adapter needs."""
        return "requests"  # Food Network works with static HTML
    
    def search_for_fruit(self, fruit_name: str) -> str:
        """
        Generate search URL for a specific fruit on Food Network.
        
        Args:
            fruit_name (str): The fruit to search for (e.g., "strawberry")
            
        Returns:
            str: The search URL
        """
        # Food Network UK search URL format (working better than US site)
        search_query = f"{fruit_name} jam"
        encoded_query = search_query.replace(" ", "%20")
        return f"https://foodnetwork.co.uk/search?q={encoded_query}"
    
    def get_recipe_urls(self, search_results_html: str, count: int = 10) -> List[str]:
        """
        Extract recipe URLs from Food Network search results.
        
        Args:
            search_results_html (str): HTML content of search results page
            count (int): Maximum number of URLs to return
            
        Returns:
            List[str]: List of recipe URLs
        """
        soup = BeautifulSoup(search_results_html, 'html.parser')
        recipe_urls = []
        
        # Food Network recipe link selectors (to be determined)
        # Common selectors for recipe links
        recipe_selectors = [
            'a[href*="/recipes/"]',  # Links containing /recipes/
            '.recipe-card a',       # Recipe card links
            '.search-result a',     # Search result links
            'a[data-testid*="recipe"]',  # Data attribute recipe links
            'a[href*="recipe"]',    # Any link containing "recipe"
        ]
        
        for selector in recipe_selectors:
            links = soup.select(selector)
            if links:
                print(f"✅ Found {len(links)} recipe links using selector: {selector}")
                break
        
        if not links:
            print("❌ No recipe links found with any selector")
            return []
        
        for link in links:
            if len(recipe_urls) >= count:
                break
                
            href = link.get('href')
            if not href:
                continue
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = urljoin('https://www.foodnetwork.com', href)
            
            # Filter for actual recipe URLs
            if self._is_recipe_url(href):
                recipe_urls.append(href)
                print(f"Found recipe: {href}")
        
        return recipe_urls[:count]
    
    def _is_recipe_url(self, url: str) -> bool:
        """
        Check if URL is a recipe page.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL appears to be a recipe
        """
        # Food Network recipe URL patterns
        recipe_patterns = [
            r'/recipes/.*-recipe',
            r'/recipes/.*-recipes',
            r'/recipes/.*',
        ]
        
        for pattern in recipe_patterns:
            if re.search(pattern, url):
                return True
        
        return False
    
    def extract_recipe_data(self, recipe_html: str, recipe_url: str) -> Dict[str, Any]:
        """
        Extract recipe data from Food Network recipe page.
        
        Args:
            recipe_html (str): HTML content of recipe page
            recipe_url (str): URL of the recipe
            
        Returns:
            Dict[str, Any]: Extracted recipe data
        """
        soup = BeautifulSoup(recipe_html, 'html.parser')
        
        # Extract title
        title = self._extract_title(soup)
        
        # Extract ingredients
        ingredients = self._extract_ingredients(soup)
        
        # Extract instructions
        instructions = self._extract_instructions(soup)
        
        # Extract servings
        servings = self._extract_servings(soup)
        
        # Extract time info
        time_info = self._extract_time_info(soup)
        
        # Extract rating and review count
        rating, review_count = self._extract_rating_info(soup)
        
        # Extract image URL
        image_url = self._extract_image_url(soup)
        
        # Extract description
        description = self._extract_description(soup)
        
        recipe_data = {
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions,
            'servings': servings,
            'time_info': time_info,
            'rating': rating,
            'review_count': review_count,
            'image_url': image_url,
            'description': description,
            'source_url': recipe_url
        }
        
        # Validate that this is actually a jam recipe
        if not self._is_jam_recipe(recipe_data):
            print(f"⚠️  Recipe '{title}' failed jam validation:")
            print(f"    Title: {title}")
            print(f"    Description: {description[:100]}...")
            print(f"    Ingredients count: {len(ingredients)}")
            if ingredients:
                print(f"    First ingredient: {ingredients[0]}")
            raise ValueError(f"Recipe '{title}' is not a jam recipe")
        
        return recipe_data
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract recipe title."""
        # Food Network UK title selectors
        title_selectors = [
            'h1.p-name',  # Microdata title
            'h1.recipe-title',
            'h1[data-testid="recipe-title"]',
            '.recipe-title',
            'h1',
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()
        
        return "Unknown Recipe"
    
    def _extract_ingredients(self, soup: BeautifulSoup) -> List[str]:
        """Extract recipe ingredients."""
        ingredients = []
        
        # Food Network UK ingredient selectors
        ingredient_selectors = [
            '.p-ingredient',  # Microdata ingredients
            '.o-Ingredients__a-ListItem',
            '.ingredient',
            '.recipe-ingredients li',
            '.ingredients li',
            '[data-testid="ingredient"]',
        ]
        
        for selector in ingredient_selectors:
            ingredient_elems = soup.select(selector)
            if ingredient_elems:
                ingredients = [elem.get_text().strip() for elem in ingredient_elems]
                break
        
        return ingredients
    
    def _extract_instructions(self, soup: BeautifulSoup) -> List[str]:
        """Extract recipe instructions."""
        instructions = []
        
        # Food Network UK instruction selectors
        instruction_selectors = [
            '.e-instructions',  # Microdata instructions
            '.legacy-method.content',
            '.o-Method__m-Body p',
            '.recipe-instructions p',
            '.directions p',
            '.instructions p',
            '[data-testid="instruction"]',
        ]
        
        for selector in instruction_selectors:
            instruction_elems = soup.select(selector)
            if instruction_elems:
                # Split instructions by <BR> tags or newlines
                for elem in instruction_elems:
                    text = elem.get_text().strip()
                    if text:
                        # Split by <BR> tags or multiple newlines
                        parts = text.replace('<BR>', '\n').split('\n')
                        for part in parts:
                            part = part.strip()
                            if part:
                                instructions.append(part)
                if instructions:
                    break
        
        return instructions
    
    def _extract_servings(self, soup: BeautifulSoup) -> int:
        """Extract number of servings from JSON-LD structured data."""
        # Look for JSON-LD structured data first (most reliable)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    # Check for recipeYield field
                    if 'recipeYield' in data:
                        try:
                            yield_value = data['recipeYield']
                            if isinstance(yield_value, (int, float)):
                                return int(yield_value)
                            elif isinstance(yield_value, str):
                                # Extract number from text like "8" or "8 jars"
                                numbers = re.findall(r'\d+', yield_value)
                                if numbers:
                                    return int(numbers[0])
                        except (ValueError, TypeError):
                            pass
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Fallback to HTML selectors if JSON-LD didn't work
        serving_selectors = [
            '.o-RecipeInfo__m-Yield',
            '.recipe-yield',
            '.servings',
            '[data-testid="servings"]',
        ]
        
        for selector in serving_selectors:
            serving_elem = soup.select_one(selector)
            if serving_elem:
                serving_text = serving_elem.get_text().strip()
                # Extract number from text like "Serves 4" or "4 servings"
                numbers = re.findall(r'\d+', serving_text)
                if numbers:
                    return int(numbers[0])
        
        return 0
    
    def _extract_time_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract cooking time information from JSON-LD structured data."""
        time_info = {}
        
        # Look for JSON-LD structured data first (most reliable)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    # Check for prepTime field
                    if 'prepTime' in data:
                        time_info['prep_time'] = data['prepTime']
                    # Check for cookTime field
                    if 'cookTime' in data:
                        time_info['cook_time'] = data['cookTime']
                    # Check for totalTime field
                    if 'totalTime' in data:
                        time_info['total_time'] = data['totalTime']
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Fallback to HTML selectors if JSON-LD didn't work
        if not time_info:
            time_selectors = [
                '.o-RecipeInfo__m-Time',
                '.recipe-time',
                '.cook-time',
                '[data-testid="time"]',
            ]
            
            for selector in time_selectors:
                time_elem = soup.select_one(selector)
                if time_elem:
                    time_text = time_elem.get_text().strip()
                    # Parse time information
                    if 'prep' in time_text.lower():
                        time_info['prep_time'] = time_text
                    elif 'cook' in time_text.lower():
                        time_info['cook_time'] = time_text
                    elif 'total' in time_text.lower():
                        time_info['total_time'] = time_text
                    else:
                        time_info['time'] = time_text
        
        return time_info
    
    def _extract_rating_info(self, soup: BeautifulSoup) -> tuple:
        """Extract rating and review count from JSON-LD structured data."""
        rating = 0.0
        review_count = 0
        
        # Look for JSON-LD structured data first (most reliable)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    if 'aggregateRating' in data:
                        agg_rating = data['aggregateRating']
                        if isinstance(agg_rating, dict):
                            if 'ratingValue' in agg_rating:
                                try:
                                    rating = float(agg_rating['ratingValue'])
                                except (ValueError, TypeError):
                                    pass
                            if 'ratingCount' in agg_rating:
                                try:
                                    review_count = int(agg_rating['ratingCount'])
                                except (ValueError, TypeError):
                                    pass
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Fallback to HTML selectors if JSON-LD didn't work
        if rating == 0.0 and review_count == 0:
            # Food Network UK rating selectors - look for the rating display
            rating_selectors = [
                '.font-\\[700\\]',  # Rating number class
                '.recipe-rating',
                '.rating',
                '[data-testid="rating"]',
                '.stars',
            ]
            
            for selector in rating_selectors:
                rating_elems = soup.select(selector)
                for elem in rating_elems:
                    rating_text = elem.get_text().strip()
                    # Look for decimal numbers (ratings)
                    numbers = re.findall(r'\d+\.\d+', rating_text)
                    if numbers:
                        rating = float(numbers[0])
                        break
                if rating > 0:
                    break
            
            # Look for review count in parentheses
            review_selectors = [
                '.font-normal',  # Review count class
                '.review-count',
                '.reviews',
                '[data-testid="review-count"]',
            ]
            
            for selector in review_selectors:
                review_elems = soup.select(selector)
                for elem in review_elems:
                    review_text = elem.get_text().strip()
                    # Look for numbers in parentheses
                    if '(' in review_text and ')' in review_text:
                        numbers = re.findall(r'\((\d+)\)', review_text)
                        if numbers:
                            review_count = int(numbers[0])
                            break
                if review_count > 0:
                    break
        
        return rating, review_count
    
    def _extract_image_url(self, soup: BeautifulSoup) -> str:
        """Extract recipe image URL from JSON-LD structured data."""
        # Look for JSON-LD structured data first (most reliable)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    # Check for image field
                    if 'image' in data:
                        image_data = data['image']
                        if isinstance(image_data, str):
                            return image_data
                        elif isinstance(image_data, dict) and 'contentUrl' in image_data:
                            return image_data['contentUrl']
                    # Check for associatedMedia
                    if 'associatedMedia' in data:
                        media_data = data['associatedMedia']
                        if isinstance(media_data, dict) and 'contentUrl' in media_data:
                            return media_data['contentUrl']
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Fallback to HTML selectors if JSON-LD didn't work
        image_selectors = [
            '.recipe-image img',
            '.hero-image img',
            '.recipe-photo img',
            'img[data-testid="recipe-image"]',
        ]
        
        for selector in image_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                src = img_elem.get('src') or img_elem.get('data-src')
                if src:
                    return src
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract recipe description from JSON-LD structured data."""
        # Look for JSON-LD structured data first (most reliable)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    # Check for description field
                    if 'description' in data:
                        return data['description']
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Fallback to HTML selectors if JSON-LD didn't work
        description_selectors = [
            # Food Network UK specific selectors (most likely to work)
            '.p-summary',  # Microdata summary class
            'p.summary',
            '.recipe-info p',
            '.recipe-details p',
            '.summary p',
            # Generic selectors
            '.recipe-description',
            '.recipe-summary',
            '.description',
            '[data-testid="description"]',
        ]
        
        for selector in description_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                return desc_elem.get_text().strip()
        
        return ""
    
    def _is_jam_recipe(self, recipe_data: Dict[str, Any]) -> bool:
        """
        Validate that this is actually a jam recipe.
        
        Args:
            recipe_data (Dict[str, Any]): Recipe data to validate
            
        Returns:
            bool: True if this appears to be a jam recipe
        """
        title = recipe_data.get('title', '').lower()
        description = recipe_data.get('description', '').lower()
        ingredients = recipe_data.get('ingredients', [])
        
        # Check for jam-related keywords
        jam_keywords = ['jam', 'preserve', 'jelly', 'marmalade']
        has_jam_keyword = any(keyword in title for keyword in jam_keywords)
        
        # Check for non-jam keywords that should be filtered out
        non_jam_keywords = [
            'cake', 'cupcake', 'muffin', 'bread', 'cookie', 'pie', 'tart',
            'sandwich', 'toast', 'pancake', 'waffle', 'crepe', 'danish',
            'cheesecake', 'trifle', 'parfait', 'sundae', 'milkshake',
            'smoothie', 'cocktail', 'sauce', 'glaze', 'frosting', 'icing',
            'filling', 'topping', 'spread', 'dip', 'salad', 'dressing',
            'marinade', 'rub', 'seasoning', 'garnish', 'popsicle', 'frozen',
            'ice cream', 'sorbet', 'granita', 'sherbet'
        ]
        
        has_non_jam_keyword = any(keyword in title for keyword in non_jam_keywords)
        
        # Must have jam keyword and not have non-jam keywords
        return has_jam_keyword and not has_non_jam_keyword
    
    def extract_fruits_from_ingredients(self, ingredients: List[str]) -> List[str]:
        """
        Extract fruit names from a list of ingredients.
        
        Args:
            ingredients (List[str]): List of ingredient strings
            
        Returns:
            List[str]: List of fruit names found in the ingredients
        """
        # Import the fruit mapping system
        from scraper.fruit_mappings import extract_fruits_from_text
        
        # Combine all ingredients into a single text
        ingredients_text = " ".join(ingredients)
        
        # Extract fruits using the shared fruit mapping system
        fruits = extract_fruits_from_text(ingredients_text)
        
        return fruits
