"""
Serious Eats Adapter

This module implements the BaseAdapter interface for scraping recipes from Serious Eats.
It handles Serious Eats-specific HTML parsing and data extraction.
"""

import re
from typing import List, Dict, Any
from urllib.parse import quote_plus

from scraper.adapters.base_adapter import BaseAdapter


class SeriousEatsAdapter(BaseAdapter):
    """
    Adapter for scraping recipes from Serious Eats
    """
    
    def get_site_name(self) -> str:
        """Return the name of this site."""
        return "Serious Eats"
    
    def get_scraping_method(self) -> str:
        """Return the scraping method this adapter needs."""
        return "requests"  # Serious Eats works with static HTML (no bot protection detected)
    
    def search_for_fruit(self, fruit_name: str) -> str:
        """
        Generate a search URL for finding jam recipes containing this fruit on Serious Eats.
        
        Args:
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            str: The search URL for Serious Eats
        """
        # Serious Eats search URL format - search for fruit jam specifically
        search_query = f"{fruit_name} jam"
        encoded_query = quote_plus(search_query)
        return f"https://www.seriouseats.com/search?q={encoded_query}"
    
    def get_recipe_urls(self, search_results_html: str) -> List[str]:
        """
        Extract recipe URLs from Serious Eats search results HTML, filtering for jam recipes.
        
        Args:
            search_results_html (str): The HTML content of the search results page
            count (int): Number of jam recipe URLs to return (default: 10)
            
        Returns:
            List[str]: List of jam recipe URLs found on the search results page
        """
        from bs4 import BeautifulSoup
        import re
        
        soup = BeautifulSoup(search_results_html, 'html.parser')
        
        # Try multiple selectors for recipe links - Serious Eats specific
        recipe_links = []
        
        # Try different possible selectors for Serious Eats recipe links
        selectors_to_try = [
            'a[data-doc-id]',        # Serious Eats specific - recipe cards with data-doc-id
            '.card[data-doc-id]',    # Alternative selector for recipe cards
            '.card-list__item a',    # Card list item links
            'a[href*="seriouseats.com"][href*="recipe"]',  # Recipe links
            'a[href*="seriouseats.com"][href*="jam"]',     # Jam-specific links
            'a[href*="/recipes/"]',  # Direct recipe links
            'a[href*="/recipe/"]',   # Alternative recipe path
            '.recipe-card a',        # Recipe card links
            '.search-result a',      # Search result links
            'article a',             # Article links
            'h3 a, h4 a',            # Heading links
            '.post-title a',         # Post title links
            '.entry-title a',        # Entry title links
        ]
        
        for selector in selectors_to_try:
            links = soup.select(selector)
            if links:
                recipe_links = links
                print(f"✅ Found {len(recipe_links)} recipe links using selector: {selector}")
                break
        
        if not recipe_links:
            print("❌ No recipe links found with any selector")
            # Let's see what we actually have in the HTML
            print("HTML preview (first 2000 chars):")
            print(search_results_html[:2000])
            return []
        
        jam_recipe_urls = []
        
        for link in recipe_links:
            # Extract the URL
            url = link.get('href')
            if not url:
                continue
                
            if not url.startswith('http'):
                url = f"https://www.seriouseats.com{url}"
            
            # Extract the title from the link text or nearby elements
            title = link.get_text(strip=True)
            
            # If title is empty, try to find it in nearby elements
            if not title:
                # Look for title in parent or sibling elements
                parent = link.parent
                if parent:
                    title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                    else:
                        # Try alt text or other attributes
                        title = link.get('alt', link.get('title', ''))
            
            # Filter out navigation links
            navigation_keywords = ['recipes', 'dinner', 'easy', 'cuisines', 'cooking', 'dishes', 'ingredients', 'meal', 'techniques', 'add', 'login', 'see all', 'home', 'about', 'contact']
            is_navigation = any(keyword in title.lower() for keyword in navigation_keywords)
            
            # Check if this is a jam recipe (has "jam" in the title AND is actually making jam)
            # Filter out recipes that USE jam (like sandwiches, cakes) vs recipes that MAKE jam
            is_actual_jam_recipe = (
                title and 
                'jam' in title.lower() and 
                url not in jam_recipe_urls and 
                not is_navigation and
                self._is_actual_jam_recipe_title(title)
            )
            
            if is_actual_jam_recipe:
                jam_recipe_urls.append(url)
                print(f"Found jam recipe: {title[:50]}... -> {url}")
                
                # Stop when we have enough jam recipes (collect more to account for rejections)
                if len(jam_recipe_urls) >= 30:  # Collect 30 URLs to account for rejections
                    break
        
        return jam_recipe_urls
    
    def _is_actual_jam_recipe_title(self, title: str) -> bool:
        """
        Check if a title represents a recipe FOR making jam (not a recipe that USES jam).
        
        Args:
            title (str): The recipe title to check
            
        Returns:
            bool: True if this is a recipe for making jam, False otherwise
        """
        title_lower = title.lower()
        
        # Recipes that USE jam (should be filtered out)
        uses_jam_keywords = [
            'sandwich', 'sandwiches', 'cake', 'cupcake', 'muffin', 'bread', 'cookie', 'pie', 'tart',
            'toast', 'pancake', 'waffle', 'crepe', 'danish', 'croissant', 'biscuit', 'scone',
            'cheesecake', 'trifle', 'parfait', 'sundae', 'milkshake', 'smoothie', 'cocktail',
            'sauce', 'glaze', 'frosting', 'icing', 'filling', 'topping', 'spread', 'dip',
            'salad', 'dressing', 'marinade', 'rub', 'seasoning', 'garnish', 'garnish',
            'with jam', 'using jam', 'jam filled', 'jam topped', 'jam glazed'
        ]
        
        # Check if this is a recipe that USES jam
        if any(keyword in title_lower for keyword in uses_jam_keywords):
            return False
        
        # Recipes that MAKE jam (should be included)
        makes_jam_patterns = [
            'jam recipe', 'jam making', 'how to make', 'perfect jam', 'homemade jam',
            'jam from', 'jam with', 'jam and', 'jam or', 'jam of', 'jam for',
            'strawberry jam', 'cherry jam', 'blueberry jam', 'peach jam', 'apple jam',
            'rhubarb jam', 'blackberry jam', 'raspberry jam', 'grape jam', 'orange jam',
            'lemon jam', 'lime jam', 'apricot jam', 'plum jam', 'fig jam', 'pear jam'
        ]
        
        # Check if this is a recipe that MAKES jam
        if any(pattern in title_lower for pattern in makes_jam_patterns):
            return True
        
        # If it just has "jam" but doesn't clearly make or use jam, be conservative
        # Only include if it has fruit + jam pattern
        fruit_keywords = [
            'strawberry', 'cherry', 'blueberry', 'peach', 'apple', 'rhubarb', 'blackberry',
            'raspberry', 'grape', 'orange', 'lemon', 'lime', 'apricot', 'plum', 'fig', 'pear',
            'cranberry', 'elderberry', 'gooseberry', 'currant', 'mulberry', 'boysenberry'
        ]
        
        has_fruit = any(fruit in title_lower for fruit in fruit_keywords)
        has_jam = 'jam' in title_lower
        
        # Only include if it has both fruit and jam (likely a jam recipe)
        return has_fruit and has_jam
    
    def extract_recipe_data(self, recipe_html: str, recipe_url: str) -> Dict[str, Any]:
        """
        Extract recipe data from a Serious Eats recipe page HTML.
        
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
            print(f"⚠️  Recipe '{title}' failed jam validation:")
            print(f"    Title: {title}")
            print(f"    Description: {description[:100]}...")
            print(f"    Ingredients count: {len(ingredients)}")
            if ingredients:
                print(f"    First ingredient: {ingredients[0].get('name', '')}")
            raise ValueError(f"Recipe '{title}' is not a jam recipe")
        
        # Validate that this recipe has a rating (critical for quality assessment)
        if rating == 0.0:
            print(f"⚠️  Recipe '{title}' has no rating - rejecting:")
            print(f"    Title: {title}")
            print(f"    Rating: {rating} stars")
            print(f"    Review count: {review_count}")
            raise ValueError(f"Recipe '{title}' has no rating - cannot assess quality")
        
        return recipe_data
    
    def _extract_title(self, soup) -> str:
        """Extract recipe title from HTML."""
        # Try multiple selectors for title - Serious Eats specific
        title_selectors = [
            'h1.recipe-title',
            'h1[class*="title"]',
            'h1.entry-title',
            'h1.post-title',
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
        
        # Look for structured ingredients list - Serious Eats specific selectors
        ingredient_items = soup.select('.structured-ingredients__list-item, .recipe-ingredients li, .ingredients li, .ingredient-item, .recipe-ingredient, .mntl-structured-ingredients__list-item, .ingredient, .recipe-ingredients-list li')
        
        for item in ingredient_items:
            try:
                item_text = item.get_text(strip=True)
                if item_text:
                    # Try to parse quantity, unit, and name
                    # This is a simplified parser - Serious Eats might have different structure
                    ingredients.append({
                        "item": item_text,
                        "quantity": "",
                        "unit": "",
                        "name": item_text
                    })
            except Exception as e:
                # If parsing fails, just use the full text
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
        
        # Look for instruction steps in the recipe content - Serious Eats specific
        instruction_selectors = [
            '.mntl-sc-block-group--OL li',  # Serious Eats specific - ordered list for instructions
            'ol li',                        # General ordered list items
            '.recipe-instructions li',
            '.instructions li',
            '.recipe-steps li',
            '.cooking-instructions p',
            '.recipe-directions li',
            '.directions li'
        ]
        
        for selector in instruction_selectors:
            instruction_elements = soup.select(selector)
            for elem in instruction_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 10:  # Filter out very short text
                    instructions.append(text)
            
            if instructions:  # If we found instructions, break
                break
        
        return instructions
    
    def _extract_rating_info(self, soup) -> tuple:
        """Extract rating and review count from HTML."""
        rating = 0.0
        review_count = 0
        
        # Look for JSON-LD structured data first (Serious Eats uses this)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                import json
                data = json.loads(script.string)
                
                # Handle both single objects and arrays
                if isinstance(data, list):
                    for item in data:
                        rating, review_count = self._extract_rating_from_json_ld(item, rating, review_count)
                        if rating > 0.0 or review_count > 0:  # If we found data, break
                            break
                elif isinstance(data, dict):
                    rating, review_count = self._extract_rating_from_json_ld(data, rating, review_count)
                        
            except (json.JSONDecodeError, AttributeError):
                continue
        
        # Fallback to traditional selectors if JSON-LD didn't work
        if rating == 0.0 and review_count == 0:
            # Look for rating elements - Serious Eats specific
            rating_elem = soup.select_one('.rating, .recipe-rating, .star-rating, .review-rating')
            if rating_elem:
                try:
                    rating = float(rating_elem.get_text(strip=True))
                except ValueError:
                    pass
            
            # Look for review count
            review_elem = soup.select_one('.review-count, .reviews, .rating-count, .comment-count')
            if review_elem:
                review_text = review_elem.get_text(strip=True)
                # Extract number from text
                numbers = re.findall(r'\d+', review_text)
                if numbers:
                    try:
                        review_count = int(numbers[0])
                    except ValueError:
                        pass
        
        return rating, review_count
    
    def _extract_rating_from_json_ld(self, data: dict, current_rating: float, current_review_count: int) -> tuple:
        """Extract rating from JSON-LD structured data."""
        rating = current_rating
        review_count = current_review_count
        
        # Look for aggregateRating
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
        
        # Look for reviewRating in reviews (only if we don't have aggregateRating data)
        if 'review' in data and (rating == 0.0 or review_count == 0):
            reviews = data['review']
            if isinstance(reviews, list):
                # Count reviews and get average rating
                total_rating = 0
                review_count = len(reviews)
                for review in reviews:
                    if isinstance(review, dict) and 'reviewRating' in review:
                        review_rating = review['reviewRating']
                        if isinstance(review_rating, dict) and 'ratingValue' in review_rating:
                            try:
                                total_rating += float(review_rating['ratingValue'])
                            except (ValueError, TypeError):
                                pass
                if review_count > 0:
                    rating = total_rating / review_count
            elif isinstance(reviews, dict) and 'reviewRating' in reviews:
                review_rating = reviews['reviewRating']
                if isinstance(review_rating, dict) and 'ratingValue' in review_rating:
                    try:
                        rating = float(review_rating['ratingValue'])
                        review_count = 1
                    except (ValueError, TypeError):
                        pass
        
        return rating, review_count
    
    def _extract_image_url(self, soup) -> str:
        """Extract primary recipe image URL from HTML."""
        # Try multiple selectors for recipe image - Serious Eats specific
        image_selectors = [
            'meta[property="og:image"]',
            'meta[name="twitter:image"]',
            '.recipe-image img',
            '.recipe-photo img',
            '.main-image img',
            '.featured-image img',
            '.post-image img'
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
        
        # Look for serving patterns - Serious Eats specific
        serving_patterns = [
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
        
        return ""
    
    
    def _extract_description(self, soup) -> str:
        """Extract recipe description from HTML."""
        # Look for description in meta tags or intro content - Serious Eats specific
        desc_selectors = [
            'meta[name="description"]',
            '.recipe-description',
            '.recipe-intro p',
            '.recipe-summary',
            '.post-excerpt p',
            '.entry-summary p'
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
