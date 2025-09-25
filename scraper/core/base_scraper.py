"""
Base Scraper

This module contains the core scraper that orchestrates the scraping process.
It uses site-specific adapters to scrape recipes from different websites.
"""

import requests
import time
from typing import List, Dict, Any
from urllib.parse import urljoin

from scraper.adapters.base_adapter import BaseAdapter


class BaseScraper:
    """
    Core scraper that orchestrates the recipe scraping process.
    
    This class handles the common functionality like HTTP requests, rate limiting,
    and data processing, while delegating site-specific logic to adapters.
    """
    
    def __init__(self, rate_limit: float = 0.3):
        """
        Initialize the base scraper.
        
        Args:
            rate_limit (float): Time to wait between requests in seconds
        """
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_site(self, adapter: BaseAdapter, fruit_name: str) -> List[Dict[str, Any]]:
        """
        Scrape recipes from a site using the provided adapter.
        
        Args:
            adapter (BaseAdapter): The site-specific adapter to use
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            List[Dict[str, Any]]: List of scraped recipe data
        """
        print(f"Scraping {adapter.get_site_name()} for {fruit_name} recipes...")
        
        # Step 1: Get search URL from adapter
        search_url = adapter.search_for_fruit(fruit_name)
        print(f"Search URL: {search_url}")
        
        # Step 2: Make search request
        try:
            response = self.session.get(search_url)
            response.raise_for_status()
            search_results_html = response.text
            print(f"Search request successful, got {len(search_results_html)} characters")
        except requests.RequestException as e:
            print(f"Error making search request: {e}")
            return []
        
        # Step 3: Get recipe URLs from adapter
        recipe_urls = adapter.get_recipe_urls(search_results_html)
        print(f"Found {len(recipe_urls)} recipe URLs")
        
        # Step 4: Scrape each recipe
        recipes = []
        for i, recipe_url in enumerate(recipe_urls):
            print(f"Scraping recipe {i+1}/{len(recipe_urls)}: {recipe_url}")
            
            try:
                # Make request for recipe page
                response = self.session.get(recipe_url)
                response.raise_for_status()
                recipe_html = response.text
                
                # Extract recipe data using adapter
                recipe_data = adapter.extract_recipe_data(recipe_html, recipe_url)
                recipes.append(recipe_data)
                
                print(f"Successfully scraped recipe: {recipe_data.get('title', 'Unknown')}")
                
                # Rate limiting
                if i < len(recipe_urls) - 1:  # Don't wait after the last request
                    time.sleep(self.rate_limit)
                    
            except Exception as e:
                print(f"Error scraping recipe {recipe_url}: {e}")
                continue
        
        print(f"Scraping complete. Got {len(recipes)} recipes from {adapter.get_site_name()}")
        return recipes
    
    def scrape_multiple_sites(self, adapters: List[BaseAdapter], fruit_name: str) -> List[Dict[str, Any]]:
        """
        Scrape recipes from multiple sites.
        
        Args:
            adapters (List[BaseAdapter]): List of site-specific adapters
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            List[Dict[str, Any]]: List of all scraped recipe data
        """
        all_recipes = []
        
        for adapter in adapters:
            try:
                recipes = self.scrape_site(adapter, fruit_name)
                all_recipes.extend(recipes)
            except Exception as e:
                print(f"Error scraping {adapter.get_site_name()}: {e}")
                continue
        
        print(f"Total recipes scraped: {len(all_recipes)}")
        return all_recipes
