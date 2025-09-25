"""
Selenium Scraper

This module extends the BaseScraper to handle JavaScript-rendered content using Selenium.
It provides browser automation capabilities for modern websites that require JavaScript execution.
"""

import time
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from scraper.core.base_scraper import BaseScraper
from scraper.adapters.base_adapter import BaseAdapter


class SeleniumScraper(BaseScraper):
    """
    Enhanced scraper that uses Selenium for JavaScript-rendered content.
    
    This class extends BaseScraper to handle modern websites that require
    JavaScript execution to load content dynamically.
    """
    
    def __init__(self, rate_limit: float = 0.3, headless: bool = True, wait_timeout: int = 10):
        """
        Initialize the Selenium scraper.
        
        Args:
            rate_limit (float): Time to wait between requests in seconds
            headless (bool): Whether to run browser in headless mode
            wait_timeout (int): Maximum time to wait for elements to load
        """
        super().__init__(rate_limit)
        self.headless = headless
        self.wait_timeout = wait_timeout
        self.driver = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Set up the Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Add common Chrome options for better compatibility
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Disable images and CSS for faster loading (optional)
            # chrome_options.add_argument("--disable-images")
            # chrome_options.add_argument("--disable-css")
            
            # Set up ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            
        except Exception as e:
            raise Exception(f"Failed to set up Chrome WebDriver: {e}")
    
    def get_page_html(self, url: str, wait_for_element: Optional[str] = None) -> str:
        """
        Get HTML content from a URL using Selenium.
        
        Args:
            url (str): The URL to scrape
            wait_for_element (str, optional): CSS selector to wait for before returning HTML
            
        Returns:
            str: The HTML content of the page
        """
        try:
            self.driver.get(url)
            
            # Wait for specific element if provided
            if wait_for_element:
                wait = WebDriverWait(self.driver, self.wait_timeout)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element)))
            
            # Wait longer for search results to load dynamically
            print("Waiting for search results to load...")
            time.sleep(5)  # Give more time for dynamic content
            
            # Try to wait for search results specifically
            try:
                # Wait for recipe cards or search results to appear
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='recipe-card'], .recipe-card, div[class*='recipe'], .search-results, .results")))
                print("✅ Search results detected")
            except TimeoutException:
                print("⚠️  Search results may not have loaded completely")
            
            # Additional wait for any remaining JavaScript
            time.sleep(3)
            
            return self.driver.page_source
            
        except TimeoutException:
            print(f"Timeout waiting for element {wait_for_element} on {url}")
            return self.driver.page_source
        except WebDriverException as e:
            print(f"WebDriver error on {url}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error on {url}: {e}")
            raise
    
    def scrape_site_with_selenium(self, adapter: BaseAdapter, fruit_name: str) -> List[Dict[str, Any]]:
        """
        Scrape recipes from a site using Selenium for JavaScript-rendered content.
        
        Args:
            adapter (BaseAdapter): The site-specific adapter to use
            fruit_name (str): The name of the fruit to search for
            
        Returns:
            List[Dict[str, Any]]: List of scraped recipe data
        """
        print(f"Scraping {adapter.get_site_name()} for {fruit_name} recipes using Selenium...")
        
        try:
            # Step 1: Get search URL from adapter
            search_url = adapter.search_for_fruit(fruit_name)
            print(f"Search URL: {search_url}")
            
            # Step 2: Get search results HTML using Selenium
            print("Loading search results with Selenium...")
            # Wait for search results to load - try multiple possible elements
            search_html = self.get_page_html(search_url, wait_for_element="[data-testid='recipe-card'], .recipe-card, div[class*='recipe'], .search-results")
            print(f"Search request successful, got {len(search_html)} characters")
            
            # Step 3: Get recipe URLs from adapter
            recipe_urls = adapter.get_recipe_urls(search_html)
            print(f"Found {len(recipe_urls)} recipe URLs")
            
            if not recipe_urls:
                print("No recipe URLs found. The site might use different selectors or require different wait conditions.")
                return []
            
            # Step 4: Scrape each recipe
            recipes = []
            for i, recipe_url in enumerate(recipe_urls):
                print(f"Scraping recipe {i+1}/{len(recipe_urls)}: {recipe_url}")
                
                try:
                    # Get recipe page HTML using Selenium
                    recipe_html = self.get_page_html(recipe_url, wait_for_element="body")
                    
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
            
            print(f"Selenium scraping complete. Got {len(recipes)} recipes from {adapter.get_site_name()}")
            return recipes
            
        except Exception as e:
            print(f"Error in Selenium scraping: {e}")
            return []
    
    def close(self):
        """Close the WebDriver and clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error closing WebDriver: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure WebDriver is closed."""
        self.close()
