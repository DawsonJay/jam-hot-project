"""
Base Adapter Interface for Recipe Scrapers

This module defines the base interface that all site-specific adapters must implement.
The core scraper uses this interface to work with any site adapter without knowing
the specific implementation details.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAdapter(ABC):
    """
    Abstract base class for all recipe site adapters.
    
    This defines the interface that all site-specific adapters must implement.
    The core scraper uses this interface to work with any site adapter.
    """
    
    @abstractmethod
    def get_site_name(self) -> str:
        """
        Return the name of this site.
        
        Returns:
            str: The name of the site (e.g., "AllRecipes", "Ball Canning")
        """
        pass
    
    @abstractmethod
    def search_for_fruit(self, fruit_name: str) -> str:
        """
        Generate a search URL for finding recipes containing this fruit.
        
        Args:
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            str: The search URL for this site
        """
        pass
    
    @abstractmethod
    def get_recipe_urls(self, search_results_html: str) -> List[str]:
        """
        Extract recipe URLs from search results HTML.
        
        Args:
            search_results_html (str): The HTML content of the search results page
            
        Returns:
            List[str]: List of recipe URLs found on the search results page
        """
        pass
    
    @abstractmethod
    def extract_recipe_data(self, recipe_html: str, recipe_url: str) -> Dict[str, Any]:
        """
        Extract recipe data from a recipe page HTML.
        
        Args:
            recipe_html (str): The HTML content of the recipe page
            recipe_url (str): The URL of the recipe page
            
        Returns:
            Dict[str, Any]: Dictionary containing the extracted recipe data
        """
        pass
    
    @abstractmethod
    def extract_fruits_from_ingredients(self, ingredients: List[str]) -> List[str]:
        """
        Extract fruit names from a list of ingredients.
        
        Args:
            ingredients (List[str]): List of ingredient strings
            
        Returns:
            List[str]: List of fruit names found in the ingredients
        """
        pass


