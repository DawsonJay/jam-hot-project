"""
Adaptive Scraper

This module provides an intelligent scraper that automatically chooses between
requests-based scraping (fast) and Selenium-based scraping (for JavaScript sites)
based on the adapter's requirements.
"""

import time
from typing import List, Dict, Any

from scraper.core.base_scraper import BaseScraper
from scraper.core.selenium_scraper import SeleniumScraper
from scraper.adapters.base_adapter import BaseAdapter


class AdaptiveScraper:
    """
    Intelligent scraper that automatically chooses the best scraping method
    based on the adapter's requirements.
    
    This scraper provides a unified interface while handling both static HTML
    sites (fast) and JavaScript-rendered sites (Selenium) transparently.
    """
    
    def __init__(self, rate_limit: float = 0.3, headless: bool = True):
        """
        Initialize the adaptive scraper.
        
        Args:
            rate_limit (float): Time to wait between requests in seconds
            headless (bool): Whether to run Selenium in headless mode
        """
        self.rate_limit = rate_limit
        self.headless = headless
        self.requests_scraper = BaseScraper(rate_limit)
        self.selenium_scraper = None  # Initialize lazily
    
    def _get_selenium_scraper(self) -> SeleniumScraper:
        """Get or create the Selenium scraper (lazy initialization)."""
        if self.selenium_scraper is None:
            self.selenium_scraper = SeleniumScraper(
                rate_limit=self.rate_limit,
                headless=self.headless
            )
        return self.selenium_scraper
    
    def scrape_site(self, adapter: BaseAdapter, fruit_name: str) -> List[Dict[str, Any]]:
        """
        Scrape recipes from a site using the appropriate method.
        
        Args:
            adapter (BaseAdapter): The site-specific adapter to use
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            List[Dict[str, Any]]: List of scraped recipe data
        """
        method = adapter.get_scraping_method()
        site_name = adapter.get_site_name()
        
        print(f"Scraping {site_name} for {fruit_name} recipes using {method} method...")
        
        try:
            if method == "requests":
                return self._scrape_with_requests(adapter, fruit_name)
            elif method == "selenium":
                return self._scrape_with_selenium(adapter, fruit_name)
            else:
                raise ValueError(f"Unknown scraping method: {method}")
                
        except Exception as e:
            print(f"Error scraping {site_name} with {method}: {e}")
            return []
    
    def _scrape_with_requests(self, adapter: BaseAdapter, fruit_name: str) -> List[Dict[str, Any]]:
        """Scrape using the fast requests-based method."""
        print(f"Using fast requests method for {adapter.get_site_name()}")
        return self.requests_scraper.scrape_site(adapter, fruit_name)
    
    def _scrape_with_selenium(self, adapter: BaseAdapter, fruit_name: str) -> List[Dict[str, Any]]:
        """Scrape using Selenium for JavaScript-rendered content."""
        print(f"Using Selenium method for {adapter.get_site_name()}")
        selenium_scraper = self._get_selenium_scraper()
        return selenium_scraper.scrape_site_with_selenium(adapter, fruit_name)
    
    def close(self):
        """Close any open resources (Selenium WebDriver)."""
        if self.selenium_scraper:
            self.selenium_scraper.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure resources are closed."""
        self.close()
