"""
Base Image Adapter Interface

This module defines the base interface that all image source adapters must implement.
The image scraper uses this interface to work with any image source without knowing
the specific implementation details.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseImageAdapter(ABC):
    """
    Abstract base class for all image source adapters.
    
    This defines the interface that all site-specific image adapters must implement.
    The image scraper uses this interface to work with any image source.
    """
    
    @abstractmethod
    def get_source_name(self) -> str:
        """
        Return the name of this image source.
        
        Returns:
            str: The name of the source (e.g., "Flickr", "Reddit", "Unsplash")
        """
        pass
    
    @abstractmethod
    def create_search_url(self, search_term: str) -> str:
        """
        Create a search URL for a specific search term.
        
        This method is used by the scraper to create URLs for each search term.
        Each adapter can customize how search terms are converted to URLs.
        
        Args:
            search_term (str): The specific term to search for
            
        Returns:
            str: The search URL for this source
        """
        pass
    
    @abstractmethod
    def get_image_urls(self, search_results_html: str, max_images: int = 100) -> List[str]:
        """
        Extract image URLs from search results HTML.
        
        Args:
            search_results_html (str): The HTML content of the search results page
            max_images (int): Maximum number of image URLs to extract
            
        Returns:
            List[str]: List of image URLs found on the search results page
        """
        pass
    
    def get_fruit_search_terms(self, fruit_name: str) -> List[str]:
        """
        Generate search term variations for a specific fruit, optimized for jam making.
        
        The scraper will divide the target URL count across all search terms
        to ensure variety in the collected images.
        
        Args:
            fruit_name (str): The base fruit name
            
        Returns:
            List[str]: List of search term variations for fruits
        """
        return [
            f"{fruit_name} fruit",           # Main fruit search
            f"{fruit_name} fresh",           # Fresh produce
            f"{fruit_name} ripe",            # Ripe fruits (best for jam)
            f"{fruit_name} organic",         # Organic produce
            f"{fruit_name} close up",        # Close-up shots
            f"{fruit_name} natural",        # Natural lighting
            f"{fruit_name} harvest",         # Harvest time (peak ripeness)
            f"{fruit_name} picking"          # Picking (fresh from source)
        ]
    
    def get_not_fruit_search_terms(self) -> List[str]:
        """
        Generate search terms for non-fruit images to create a balanced dataset.
        
        Returns:
            List[str]: List of search terms for not-fruit images
        """
        return [
            "hands holding",                 # Hands (common in fruit photos)
            "kitchen utensils",              # Kitchen tools
            "cooking tools",                 # Cooking equipment
            "cutting board",                 # Cutting boards
            "spoon fork knife",              # Utensils
            "kitchen counter",               # Kitchen surfaces
            "cooking ingredients"            # General cooking items
        ]