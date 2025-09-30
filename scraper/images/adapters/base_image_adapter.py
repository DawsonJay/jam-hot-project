"""
Base Image Adapter Interface

This module defines the base interface that all image source adapters must implement.
The core image scraper uses this interface to work with any image source without knowing
the specific implementation details.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseImageAdapter(ABC):
    """
    Abstract base class for all image source adapters.
    
    This defines the interface that all site-specific image adapters must implement.
    The core image scraper uses this interface to work with any image source.
    """
    
    @abstractmethod
    def get_source_name(self) -> str:
        """
        Return the name of this image source.
        
        Returns:
            str: The name of the source (e.g., "Google Images", "Flickr")
        """
        pass
    
    @abstractmethod
    def search_for_fruit(self, fruit_name: str, max_images: int = 100) -> str:
        """
        Generate a search URL for finding images of this fruit.
        
        Args:
            fruit_name (str): The name of the fruit to search for
            max_images (int): Maximum number of images to retrieve
            
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
    
    @abstractmethod
    def download_image(self, image_url: str, save_path: str) -> Dict[str, Any]:
        """
        Download an image from the given URL and save it to the specified path.
        
        Args:
            image_url (str): The URL of the image to download
            save_path (str): The local path where the image should be saved
            
        Returns:
            Dict[str, Any]: Dictionary containing download results
                - success (bool): Whether the download was successful
                - url (str): The original image URL
                - path (str): The local save path
                - size (int): File size in bytes (if successful)
                - error (str): Error message (if failed)
        """
        pass
    
    def get_scraping_method(self) -> str:
        """
        Return the scraping method this adapter needs.
        
        Returns:
            str: The scraping method ("requests" for static HTML, "selenium" for JavaScript-rendered content)
        """
        return "requests"  # Default to fast method
    
    def get_search_terms(self, fruit_name: str) -> List[str]:
        """
        Generate search term variations for better image diversity.
        
        Args:
            fruit_name (str): The base fruit name
            
        Returns:
            List[str]: List of search term variations
        """
        return [
            f"{fruit_name}",
            f"{fruit_name} fruit",
            f"fresh {fruit_name}",
            f"{fruit_name} photo"
        ]
