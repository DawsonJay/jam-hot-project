"""
AllRecipes.com Adapter

This module implements the BaseAdapter interface for scraping recipes from AllRecipes.com.
It handles AllRecipes-specific HTML parsing and data extraction.
"""

import re
from typing import List, Dict, Any
from urllib.parse import quote_plus

from scraper.adapters.base_adapter import BaseAdapter


class AllRecipesAdapter(BaseAdapter):
    """
    Adapter for scraping recipes from AllRecipes.com
    """
    
    def get_site_name(self) -> str:
        """Return the name of this site."""
        return "AllRecipes"
    
    def get_scraping_method(self) -> str:
        """Return the scraping method this adapter needs."""
        return "requests"  # AllRecipes works fine with static HTML
    
    def search_for_fruit(self, fruit_name: str) -> str:
        """
        Generate a search URL for finding jam recipes containing this fruit on AllRecipes.
        
        Args:
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            str: The search URL for AllRecipes
        """
        # AllRecipes search URL format - search for fruit jam specifically
        search_query = f"{fruit_name} jam"  # Search for "fruit jam" to get jam recipes
        encoded_query = quote_plus(search_query)
        return f"https://www.allrecipes.com/search?q={encoded_query}"
    
    def get_recipe_urls(self, search_results_html: str) -> List[str]:
        """
        Extract recipe URLs from AllRecipes search results HTML, filtering for jam recipes.
        
        Args:
            search_results_html (str): The HTML content of the search results page
            count (int): Number of jam recipe URLs to return (default: 10)
            
        Returns:
            List[str]: List of jam recipe URLs found on the search results page
        """
        from bs4 import BeautifulSoup
        import re
        
        soup = BeautifulSoup(search_results_html, 'html.parser')
        
        # Find all recipe cards/links
        recipe_links = soup.find_all('a', href=re.compile(r'/recipe/\d+/'))
        
        jam_recipe_urls = []
        
        for link in recipe_links:
            # Extract the URL
            url = link.get('href')
            if not url.startswith('http'):
                url = 'https://www.allrecipes.com' + url
            
            # Extract the title from the link text or nearby elements
            title = link.get_text(strip=True)
            
            # If title is empty, try to find it in nearby elements
            if not title:
                # Look for title in parent or sibling elements
                parent = link.parent
                if parent:
                    title_elem = parent.find(['h3', 'h4', 'span'], class_=re.compile(r'title|heading|name'))
                    if title_elem:
                        title = title_elem.get_text(strip=True)
            
            # Check if this is a jam recipe (has "jam" in the title)
            if title and 'jam' in title.lower():
                jam_recipe_urls.append(url)
                
                # Stop when we have enough jam recipes (limit to 10)
                if len(jam_recipe_urls) >= 10:
                    break
        
        return jam_recipe_urls
    
    def extract_recipe_data(self, recipe_html: str, recipe_url: str) -> Dict[str, Any]:
        """
        Extract recipe data from an AllRecipes recipe page HTML.
        
        Args:
            recipe_html (str): The HTML content of the recipe page
            recipe_url (str): The URL of the recipe page
            
        Returns:
            Dict[str, Any]: Dictionary containing the extracted recipe data
        """
        from bs4 import BeautifulSoup
        import re
        
        soup = BeautifulSoup(recipe_html, 'html.parser')
        
        # Extract title
        title = self._extract_title(soup)
        
        # Extract ingredients
        ingredients = self._extract_ingredients(soup)
        
        # Extract instructions
        instructions = self._extract_instructions(soup)
        
        # Extract rating and review count
        rating, review_count = self._extract_rating_info(soup)
        
        # Extract image URL
        image_url = self._extract_image_url(soup)
        
        # Extract servings/yield
        servings = self._extract_servings(soup)
        
        # Extract time information
        
        # Extract description
        description = self._extract_description(soup)
        
        recipe_data = {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "servings": servings,
            "rating": rating,
            "review_count": review_count,
            "source": self.get_site_name(),
            "source_url": recipe_url,
            "image_url": image_url,
            "description": description
        }
        
        # Validate that this is actually a jam recipe
        if not self._is_jam_recipe(recipe_data):
            raise ValueError(f"Recipe '{title}' is not a jam recipe")
        
        return recipe_data
    
    def _extract_title(self, soup) -> str:
        """Extract recipe title from HTML."""
        # Try multiple selectors for title
        title_selectors = [
            'h1.article-heading',
            'h1[class*="heading"]',
            'h1',
            'title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                # Clean up title (remove "Recipe" suffix if present)
                if title.endswith(' Recipe'):
                    title = title[:-7]
                return title
        
        return "Untitled Recipe"
    
    def _extract_ingredients(self, soup) -> List[Dict[str, Any]]:
        """Extract ingredients from HTML."""
        ingredients = []
        
        # Look for structured ingredients list
        ingredient_items = soup.select('.mm-recipes-structured-ingredients__list-item')
        
        for item in ingredient_items:
            try:
                # Extract quantity, unit, and name from structured data
                quantity_elem = item.select_one('[data-ingredient-quantity="true"]')
                unit_elem = item.select_one('[data-ingredient-unit="true"]')
                name_elem = item.select_one('[data-ingredient-name="true"]')
                
                if quantity_elem and unit_elem and name_elem:
                    quantity = quantity_elem.get_text(strip=True)
                    unit = unit_elem.get_text(strip=True)
                    name = name_elem.get_text(strip=True)
                    
                    # Create full item text
                    item_text = f"{quantity} {unit} {name}"
                    
                    ingredients.append({
                        "item": item_text,
                        "quantity": quantity,
                        "unit": unit,
                        "name": name
                    })
            except Exception as e:
                # If structured parsing fails, try to get the full text
                item_text = item.get_text(strip=True)
                if item_text:
                    ingredients.append({
                        "item": item_text,
                        "quantity": "",
                        "unit": "",
                        "name": item_text
                    })
        
        return ingredients
    
    def _extract_instructions(self, soup) -> List[str]:
        """Extract cooking instructions from HTML."""
        instructions = []
        
        # Look for instruction steps in the recipe content
        # AllRecipes uses specific selectors for instruction steps
        instruction_selectors = [
            '.mm-recipes-steps__content .mntl-sc-block-html',
            '.mntl-sc-block-html p',
            'ol.mntl-sc-block-html li'
        ]
        
        for selector in instruction_selectors:
            instruction_elements = soup.select(selector)
            for elem in instruction_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:  # Filter out very short text
                    instructions.append(text)
            
            if instructions:  # If we found instructions, break
                break
        
        # If no instructions found, try alternative approach
        if not instructions:
            # Look for any paragraph with cooking-related keywords
            all_paragraphs = soup.find_all('p', class_='mntl-sc-block-html')
            for p in all_paragraphs:
                text = p.get_text(strip=True)
                if any(keyword in text.lower() for keyword in ['combine', 'mix', 'cook', 'boil', 'heat', 'stir', 'add']):
                    if len(text) > 20:  # Reasonable instruction length
                        instructions.append(text)
        
        return instructions
    
    def _extract_rating_info(self, soup) -> tuple:
        """Extract rating and review count from HTML."""
        rating = 0.0
        review_count = 0
        
        # Look for rating elements
        rating_elem = soup.select_one('.mm-recipes-review-bar__rating')
        if rating_elem:
            try:
                rating = float(rating_elem.get_text(strip=True))
            except ValueError:
                pass
        
        # Look for review count
        review_elem = soup.select_one('.mm-recipes-review-bar__rating-count')
        if review_elem:
            review_text = review_elem.get_text(strip=True)
            # Extract number from text like "(948)"
            numbers = re.findall(r'\d+', review_text)
            if numbers:
                try:
                    review_count = int(numbers[0])
                except ValueError:
                    pass
        
        return rating, review_count
    
    def _extract_image_url(self, soup) -> str:
        """Extract primary recipe image URL from HTML."""
        # Try multiple selectors for recipe image
        image_selectors = [
            'meta[property="og:image"]',
            'meta[name="twitter:image"]',
            '.recipe-image img',
            '.mm-recipes-intro img'
        ]
        
        for selector in image_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                if img_elem.name == 'meta':
                    image_url = img_elem.get('content', '')
                else:
                    image_url = img_elem.get('src', '')
                
                if image_url and image_url.startswith('http'):
                    return image_url
        
        return ""
    
    def _extract_servings(self, soup) -> str:
        """Extract servings/yield information from HTML."""
        import re
        
        # Get all text from the page
        all_text = soup.get_text()
        
        # Look for clean serving patterns
        serving_patterns = [
            r'Original recipe \(1X\) yields (\d+) servings',
            r'(\d+)\s+servings?',
            r'yields?\s+(\d+)\s+servings?',
            r'makes?\s+(\d+)\s+servings?',
            r'(\d+)\s+\d*oz?\s+jars?',
            r'(\d+)\s+jars?'
        ]
        
        for pattern in serving_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                # Return the first match with "servings" or "jars"
                serving_count = matches[0]
                if 'jar' in pattern.lower():
                    return f"{serving_count} jars"
                else:
                    return f"{serving_count} servings"
        
        # Fallback: look for serving information in specific elements
        serving_selectors = [
            '.mm-recipes-serving-size-adjuster',
            '.recipe-serving',
            '.servings'
        ]
        
        for selector in serving_selectors:
            serving_elem = soup.select_one(selector)
            if serving_elem:
                serving_text = serving_elem.get_text(strip=True)
                # Clean up the text - look for just the serving number
                serving_match = re.search(r'(\d+)\s+(servings?|jars?)', serving_text, re.IGNORECASE)
                if serving_match:
                    return f"{serving_match.group(1)} {serving_match.group(2)}"
        
        return ""
    
    
    def _extract_description(self, soup) -> str:
        """Extract recipe description from HTML."""
        # Look for description in meta tags or intro content
        desc_selectors = [
            'meta[name="description"]',
            '.mm-recipes-intro__content p',
            '.recipe-description'
        ]
        
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                if desc_elem.name == 'meta':
                    description = desc_elem.get('content', '')
                else:
                    description = desc_elem.get_text(strip=True)
                
                if description and len(description) > 20:
                    return description
        
        return ""
    
    def extract_fruits_from_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract fruit names from a list of ingredients.
        
        Args:
            ingredients (List[Dict[str, Any]]): List of ingredient dictionaries
            
        Returns:
            List[Dict[str, Any]]: List of fruit dictionaries with name and primary flag
        """
        # Simple fruit detection - look for common fruit names
        fruits = []
        fruit_keywords = [
            "strawberry", "blueberry", "apple", "peach", "cherry", "grape",
            "raspberry", "blackberry", "orange", "lemon", "lime", "banana"
        ]
        
        for ingredient in ingredients:
            ingredient_name = ingredient.get("name", "").lower()
            for fruit in fruit_keywords:
                if fruit in ingredient_name:
                    # Check if this fruit is already in our list
                    if not any(f["fruit_name"] == fruit for f in fruits):
                        # Determine if it's primary (strawberry for strawberry jam)
                        is_primary = fruit == "strawberry"  # For now, assume strawberry is primary
                        fruits.append({"fruit_name": fruit, "is_primary": is_primary})
        
        return fruits
    
    def _is_jam_recipe(self, recipe_data: Dict[str, Any]) -> bool:
        """
        Validate that a recipe is actually a jam recipe using shared logic.
        
        Args:
            recipe_data: Dictionary containing recipe data
            
        Returns:
            bool: True if this is a jam recipe, False otherwise
        """
        from scraper.core.recipe_validator import is_jam_recipe
        return is_jam_recipe(recipe_data)
