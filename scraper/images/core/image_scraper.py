#!/usr/bin/env python3
"""
Image Scraper - Selenium-only scraper for image collection

This module provides a simplified scraper that only uses Selenium
for JavaScript-rendered image sites. All image sites use JavaScript,
so we don't need the complexity of requests vs Selenium logic.
"""

import time
import re
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from ..adapters.base_image_adapter import BaseImageAdapter


class ImageScraper:
    """
    Selenium-only image scraper for JavaScript sites.
    
    This scraper is designed specifically for image collection from
    JavaScript-rendered sites like Flickr, Reddit, etc.
    """
    
    def __init__(self, headless: bool = True, wait_timeout: int = 10, rate_limit: float = 0.5, max_workers: int = 3, adaptive_rate_limiting: bool = True):
        """
        Initialize the image scraper.
        
        Args:
            headless (bool): Whether to run browser in headless mode
            wait_timeout (int): Maximum time to wait for elements to load
            rate_limit (float): Base delay between requests in seconds (for respectful scraping)
            max_workers (int): Maximum number of parallel workers for photo page visits
            adaptive_rate_limiting (bool): Whether to use adaptive rate limiting
        """
        self.headless = headless
        self.wait_timeout = wait_timeout
        self.base_rate_limit = rate_limit
        self.max_workers = max_workers
        self.adaptive_rate_limiting = adaptive_rate_limiting
        
        # Adaptive rate limiting state
        self.success_rate = 0.0
        self.error_count = 0
        self.total_requests = 0
        
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
            
            # Set up ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            
        except Exception as e:
            raise Exception(f"Failed to set up Chrome WebDriver: {e}")
    
    def _get_adaptive_rate_limit(self) -> float:
        """
        Get the current rate limit based on success rate.
        
        Returns:
            float: Current rate limit in seconds
        """
        if not self.adaptive_rate_limiting or self.total_requests < 5:
            return self.base_rate_limit
        
        if self.success_rate > 0.8:
            return 0.1  # Much faster when successful
        elif self.success_rate > 0.5:
            return 0.3  # Normal rate
        else:
            return 1.0  # Slower when errors
    
    def _update_success_rate(self, success: bool):
        """
        Update the success rate based on request outcome.
        
        Args:
            success (bool): Whether the request was successful
        """
        self.total_requests += 1
        
        if success:
            self.success_rate = min(1.0, self.success_rate + 0.1)
        else:
            self.success_rate = max(0.0, self.success_rate - 0.2)
            self.error_count += 1
        
        # Print adaptive rate info every 10 requests
        if self.total_requests % 10 == 0:
            print(f"    📊 Adaptive Rate: {self.success_rate:.1%} success, {self._get_adaptive_rate_limit():.1f}s delay")
    
    def scrape_image_urls(self, adapter: BaseImageAdapter, fruit_name: str, max_urls: int, is_fruit: bool = True) -> dict:
        """
        Scrape image URLs from a site using Selenium.
        
        Args:
            adapter (BaseImageAdapter): The site-specific adapter to use
            fruit_name (str): The name of the fruit/object to search for
            max_urls (int): Maximum number of image URLs to collect
            is_fruit (bool): Whether this is a fruit (multiple searches) or not-fruit (single search)
            
        Returns:
            dict: Dictionary with 'fruit' and 'not_fruit' URL lists
        """
        print(f"🔍 Scraping {adapter.get_source_name()} for {fruit_name} images...")
        
        results = {
            'fruit': [],
            'not_fruit': []
        }
        
        if is_fruit:
            # For fruits: use multiple search term variations
            search_terms = adapter.get_fruit_search_terms(fruit_name)
            urls_per_term = max(1, max_urls // len(search_terms)) if len(search_terms) > 0 else max_urls
            
            print(f"🍎 Scraping {max_urls} fruit URLs using {len(search_terms)} search variations...")
            for search_term in search_terms:
                print(f"  Searching for '{search_term}'...")
                try:
                    # Create search URL for this term
                    search_url = adapter.create_search_url(search_term)
                    
                    # Get HTML using Selenium
                    html_content = self.get_page_html(search_url)
                    
                    # Extract photo page URLs using adapter
                    photo_page_urls = adapter.get_image_urls(html_content, urls_per_term)
                    print(f"  Found {len(photo_page_urls)} photo page URLs for '{search_term}'")
                    
                    # Visit photo pages in parallel to get actual image URLs
                    actual_image_urls = self._visit_photo_pages_parallel(photo_page_urls, urls_per_term)
                    
                    results['fruit'].extend(actual_image_urls)
                    print(f"  ✅ Found {len(actual_image_urls)} actual image URLs for '{search_term}'")
                except Exception as e:
                    print(f"  ❌ Error scraping for '{search_term}': {e}")
        else:
            # For not-fruits: use single search with exact term
            print(f"🍽️ Scraping {max_urls} not-fruit URLs using single search...")
            print(f"  Searching for '{fruit_name}'...")
            try:
                # Create search URL for this term
                search_url = adapter.create_search_url(fruit_name)
                
                # Get HTML using Selenium
                html_content = self.get_page_html(search_url)
                
                # Extract photo page URLs using adapter (same as fruit search)
                photo_page_urls = adapter.get_image_urls(html_content, max_urls)
                print(f"  Found {len(photo_page_urls)} photo page URLs for '{fruit_name}'")
                
                # Visit photo pages in parallel to get actual image URLs
                actual_image_urls = self._visit_photo_pages_parallel(photo_page_urls, max_urls)
                
                results['not_fruit'].extend(actual_image_urls)
                print(f"  ✅ Found {len(actual_image_urls)} actual image URLs for '{fruit_name}'")
            except Exception as e:
                print(f"  ❌ Error scraping for '{fruit_name}': {e}")
        
        return results
    
    def _extract_image_urls_from_photo_page(self, photo_html: str) -> List[str]:
        """Extract high-quality image URLs from a Flickr photo page."""
        image_urls = []
        seen = set()
        
        try:
            # Pattern 1: Look for high-quality image URLs in the photo page
            # These are usually in meta tags or JSON data
            high_quality_pattern = r'https://live\.staticflickr\.com/[^"\s]+\.jpg'
            high_quality_matches = re.findall(high_quality_pattern, photo_html)
            
            for url in high_quality_matches:
                if url not in seen:
                    # Filter for high-quality images (not thumbnails)
                    if '_n.jpg' not in url and '_m.jpg' not in url and '_s.jpg' not in url:
                        image_urls.append(url)
                        seen.add(url)
            
            # Pattern 2: Look for image URLs in src attributes
            if len(image_urls) == 0:
                src_pattern = r'src="(https://live\.staticflickr\.com/[^"]+\.jpg)"'
                src_matches = re.findall(src_pattern, photo_html)
                
                for url in src_matches:
                    if url not in seen:
                        if '_n.jpg' not in url and '_m.jpg' not in url and '_s.jpg' not in url:
                            image_urls.append(url)
                            seen.add(url)
            
            # Pattern 3: Look for any Flickr image URLs as fallback
            if len(image_urls) == 0:
                flickr_pattern = r'https://live\.staticflickr\.com/[^"\s]+\.jpg'
                flickr_matches = re.findall(flickr_pattern, photo_html)
                
                for url in flickr_matches:
                    if url not in seen:
                        image_urls.append(url)
                        seen.add(url)
        
        except Exception as e:
            print(f"    ❌ Error extracting image URLs from photo page: {e}")
        
        return image_urls
    
    def get_photo_page_html(self, url: str) -> str:
        """
        Get HTML content from a photo page (fast, no scrolling needed).
        
        Args:
            url (str): The photo page URL to scrape
            
        Returns:
            str: The HTML content of the page
        """
        try:
            self.driver.get(url)
            
            # Just wait for basic page load (optimized - no unnecessary delays)
            time.sleep(0.5)  # Minimal wait for page to load
            
            return self.driver.page_source
            
        except TimeoutException:
            print(f"⏰ Timeout loading photo page {url}")
            return self.driver.page_source
        except WebDriverException as e:
            print(f"❌ WebDriver error on photo page {url}: {e}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error on photo page {url}: {e}")
            raise
    
    def get_page_html(self, url: str, wait_for_element: Optional[str] = None) -> str:
        """
        Get HTML content from a URL using Selenium with optimized timing.
        
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
            
            # Wait for search results to load dynamically (optimized - no initial delay)
            print("⏳ Waiting for search results to load...")
            # REMOVED: time.sleep(1) - unnecessary since we wait for elements
            
            # Try to wait for Flickr-specific elements
            try:
                wait = WebDriverWait(self.driver, 5)  # Wait for Flickr elements
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='photo-list-view'], [class*='photo-list-photo-view']")))
                print("✅ Flickr photo elements detected")
            except TimeoutException:
                print("⚠️  Flickr photo elements may not have loaded completely")
            
            # Also wait for any images
            try:
                wait = WebDriverWait(self.driver, 3)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img")))
                print("✅ Images detected")
            except TimeoutException:
                print("⚠️  Images may not have loaded completely")
            
            # Scroll to trigger lazy loading (Flickr loads images on scroll)
            print("📜 Scrolling to load more images...")
            max_scrolls = 4  # Stop after 4 scrolls to avoid "Load more results" button
            
            for i in range(max_scrolls):
                # Scroll to bottom of page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(f"   Scroll {i+1}/{max_scrolls} completed")
                
                # Wait for loading animation to disappear
                print("   ⏳ Waiting for loading animation to finish...")
                self._wait_for_loading_animation()
                
                # Check if "Load more results" button appeared (stop if it did)
                try:
                    load_more_button = self.driver.find_element(By.CSS_SELECTOR, "[class*='load-more'], [class*='load-more-results'], button[class*='load']")
                    if load_more_button.is_displayed():
                        print("   🛑 'Load more results' button detected - stopping scroll")
                        break
                except:
                    # No "Load more" button found, continue scrolling
                    pass
                
                # Check if we're at the bottom and no new content is loading
                current_height = self.driver.execute_script("return document.body.scrollHeight")
                scroll_position = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
                
                if scroll_position >= current_height - 100:  # Within 100px of bottom
                    print("   📍 Reached bottom of page")
                    break
            
            # OPTIMIZED: No final delay - lazy loading is already complete
            print("   ✅ Lazy loading complete - no additional delays needed")
            
            return self.driver.page_source
            
        except TimeoutException:
            print(f"⏰ Timeout waiting for element {wait_for_element} on {url}")
            return self.driver.page_source
        except WebDriverException as e:
            print(f"❌ WebDriver error on {url}: {e}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error on {url}: {e}")
            raise
    
    def _visit_photo_pages_parallel(self, photo_page_urls: List[str], target_urls: int) -> List[str]:
        """
        Visit photo pages in parallel to extract image URLs.
        
        Args:
            photo_page_urls (List[str]): List of photo page URLs to visit
            target_urls (int): Target number of image URLs to collect
            
        Returns:
            List[str]: List of actual image URLs found
        """
        if not photo_page_urls:
            return []
        
        actual_image_urls = []
        max_pages_to_visit = len(photo_page_urls)
        
        print(f"  🚀 Visiting {max_pages_to_visit} photo pages in parallel (max {self.max_workers} workers)...")
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all photo page visits
            future_to_url = {
                executor.submit(self._visit_single_photo_page, photo_url): photo_url 
                for photo_url in photo_page_urls[:max_pages_to_visit]
            }
            
            # Process completed futures
            completed_count = 0
            for future in as_completed(future_to_url):
                completed_count += 1
                photo_url = future_to_url[future]
                
                try:
                    image_urls = future.result()
                    if image_urls:
                        for img_url in image_urls:
                            if img_url not in actual_image_urls:
                                actual_image_urls.append(img_url)
                    
                    # Progress tracking
                    print(f"    📊 Progress: {completed_count}/{max_pages_to_visit} photo pages completed, {len(actual_image_urls)}/{target_urls} URLs collected")
                    
                    # Early termination if we have enough URLs
                    if len(actual_image_urls) >= target_urls:
                        print(f"  ✅ Early termination: collected {len(actual_image_urls)}/{target_urls} URLs")
                        break
                        
                except Exception as e:
                    print(f"      ❌ Error processing photo page {photo_url}: {e}")
                    continue
        
        return actual_image_urls[:target_urls]  # Limit to target number
    
    def _visit_single_photo_page(self, photo_url: str) -> List[str]:
        """
        Visit a single photo page and extract image URLs with retry logic.
        
        Args:
            photo_url (str): The photo page URL to visit
            
        Returns:
            List[str]: List of image URLs found on this page
        """
        return self._retry_with_backoff(
            lambda: self._visit_photo_page_once(photo_url),
            max_retries=3
        )
    
    def _visit_photo_page_once(self, photo_url: str) -> List[str]:
        """
        Visit a single photo page once (no retry logic).
        
        Args:
            photo_url (str): The photo page URL to visit
            
        Returns:
            List[str]: List of image URLs found on this page
        """
        # Get the full URL
        full_photo_url = f"https://www.flickr.com{photo_url}"
        
        # Visit the photo page and extract image URLs
        photo_html = self.get_photo_page_html(full_photo_url)
        image_urls = self._extract_image_urls_from_photo_page(photo_html)
        
        # Update success rate
        self._update_success_rate(success=True)
        
        # Apply adaptive rate limiting
        adaptive_delay = self._get_adaptive_rate_limit()
        if adaptive_delay > 0:
            time.sleep(adaptive_delay)
        
        return image_urls
    
    def _retry_with_backoff(self, func, max_retries: int = 3):
        """
        Retry function with exponential backoff.
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retries
            
        Returns:
            Result of function or raises exception after max retries
        """
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    # Final attempt failed, update success rate and raise
                    self._update_success_rate(success=False)
                    raise
                
                # Calculate backoff delay: 1s, 2s, 4s
                wait_time = 2 ** attempt
                print(f"      ⏳ Retry {attempt + 1}/{max_retries} in {wait_time}s: {e}")
                time.sleep(wait_time)
    
    def _wait_for_loading_animation(self):
        """Wait for Flickr's loading animation to disappear."""
        try:
            # Look for common loading animation selectors
            loading_selectors = [
                "[class*='loading']",
                "[class*='spinner']", 
                "[class*='loader']",
                "[class*='loading-animation']",
                ".loading",
                ".spinner"
            ]
            
            # Wait for any loading animation to disappear
            for selector in loading_selectors:
                try:
                    wait = WebDriverWait(self.driver, 1)  # Short wait
                    wait.until_not(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                except:
                    # No loading animation found with this selector, continue
                    pass
            
            # Additional wait to ensure content is loaded
            time.sleep(1)
            
        except Exception as e:
            # If we can't detect loading animation, just wait a bit
            time.sleep(2)
    
    def close(self):
        """Close the WebDriver and clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                print("🔒 WebDriver closed")
            except Exception as e:
                print(f"❌ Error closing WebDriver: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure WebDriver is closed."""
        self.close()
