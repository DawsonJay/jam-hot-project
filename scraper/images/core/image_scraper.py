"""
Image Scraper Core

This module contains the core image scraper that orchestrates the image downloading process.
It uses source-specific adapters to scrape images from different sources.
"""

import time
import random
import os
from typing import List, Dict, Any
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

from scraper.images.adapters.base_image_adapter import BaseImageAdapter


class ImageScraper:
    """
    Core image scraper that orchestrates the image downloading process.
    
    This class handles the common functionality like HTTP requests, rate limiting,
    and image downloading, while delegating source-specific logic to adapters.
    """
    
    def __init__(self, output_dir: str = "image_data", rate_limit: float = 1.0, headless: bool = True):
        """
        Initialize the image scraper.
        
        Args:
            output_dir (str): Directory to save downloaded images
            rate_limit (float): Time to wait between requests in seconds
            headless (bool): Whether to run browser in headless mode
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.rate_limit = rate_limit
        self.headless = headless
        self.driver = None
    
    def start_browser(self):
        """Start the Selenium browser"""
        if self.driver:
            return
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Browser started successfully")
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            print("💡 Make sure Chrome and chromedriver are installed")
    
    def stop_browser(self):
        """Stop the Selenium browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✅ Browser stopped")
    
    def validate_image(self, image_path: str) -> tuple[bool, str]:
        """
        Validate image quality and content.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            tuple[bool, str]: (is_valid, reason)
        """
        try:
            # Check file size (reject tiny images)
            file_size = os.path.getsize(image_path)
            if file_size < 5000:  # Less than 5KB = likely icon/placeholder
                return False, "File too small (< 5KB)"
            
            # Check image dimensions using PIL
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Reject tiny images
                if width < 100 or height < 100:
                    return False, f"Image too small ({width}x{height})"
                
                # Reject extremely wide/tall images (likely banners/text)
                aspect_ratio = max(width, height) / min(width, height)
                if aspect_ratio > 5:
                    return False, f"Unusual aspect ratio ({aspect_ratio:.1f}:1)"
                
                # Additional quality checks
                # Check if image is too dark (likely poor quality)
                img_gray = img.convert('L')
                avg_brightness = sum(img_gray.getdata()) / (width * height)
                if avg_brightness < 30:  # Very dark image
                    return False, f"Image too dark (brightness: {avg_brightness:.1f})"
                
                # Check for very low contrast (likely poor quality)
                import numpy as np
                img_array = np.array(img_gray)
                contrast = np.std(img_array)
                if contrast < 20:  # Very low contrast
                    return False, f"Image too low contrast ({contrast:.1f})"
            
            return True, "Valid"
            
        except Exception as e:
            return False, f"Cannot open image: {str(e)}"
    
    def scrape_fruit_images(self, adapter: BaseImageAdapter, fruit_name: str, max_images: int = 100) -> Dict[str, Any]:
        """
        Scrape images for a fruit using the provided adapter.
        Uses multiple search terms to get diverse, realistic images.
        
        Args:
            adapter (BaseImageAdapter): The source-specific adapter to use
            fruit_name (str): The name of the fruit to search for
            max_images (int): Maximum number of images to download
            
        Returns:
            Dict[str, Any]: Results of the scraping operation
        """
        print(f"\n🍓 Scraping {adapter.get_source_name()} for {fruit_name} images...")
        print("-" * 60)
        
        results = {
            'fruit': fruit_name,
            'source': adapter.get_source_name(),
            'requested': max_images,
            'found': 0,
            'downloaded': 0,
            'validated': 0,
            'rejected': 0,
            'failed': 0,
            'images': []
        }
        
        # Create fruit directory
        fruit_dir = self.output_dir / fruit_name
        fruit_dir.mkdir(exist_ok=True, parents=True)
        
        # Check if we need browser
        if adapter.get_scraping_method() == "selenium":
            self.start_browser()
            if not self.driver:
                print("❌ Cannot scrape without browser")
                return results
        
        try:
            # Get multiple search terms for diversity
            search_terms = adapter.get_search_terms(fruit_name)
            
            # Weight the terms: 80% amateur, 20% professional
            # Term 1: "fruit" (professional) - 20%
            # Terms 2-5: amateur contexts - 80%
            professional_images = max(1, int(max_images * 0.2))  # 20%
            amateur_images_per_term = max(1, int((max_images - professional_images) / 4))  # 80% / 4 terms
            
            print(f"📋 Using {len(search_terms)} search terms:")
            print(f"   Professional (fruit): {professional_images} images")
            print(f"   Amateur (forage/shopping/market/gardening): {amateur_images_per_term} each")
            
            all_image_urls = []
            
            # Search with each term (with different weights)
            for term_idx, search_term in enumerate(search_terms, 1):
                # Determine how many images to get for this term
                if term_idx == 1:  # First term is "fruit" (professional)
                    target_images = professional_images
                else:  # Terms 2-5 are amateur contexts
                    target_images = amateur_images_per_term
                
                print(f"\n🔍 [{term_idx}/{len(search_terms)}] Searching: \"{search_term}\" ({target_images} images)")
                
                # Build search URL with custom term
                from urllib.parse import quote_plus
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                
                encoded_query = quote_plus(search_term)
                search_url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&hl=en"
                
                # Load search results
                if adapter.get_scraping_method() == "selenium":
                    self.driver.get(search_url)
                    time.sleep(2)
                    
                    # Scroll to load more images
                    for _ in range(3):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.5)
                    
                    # Use the working thumbnail approach
                    try:
                        # Get page HTML and extract thumbnail URLs
                        search_results_html = self.driver.page_source
                        term_image_urls = adapter.get_image_urls(search_results_html, target_images)
                        
                        all_image_urls.extend(term_image_urls)
                        print(f"   Found {len(term_image_urls)} images")
                        
                    except Exception as e:
                        print(f"   Error extracting images: {e}")
                        # Fallback to old method
                        search_results_html = self.driver.page_source
                        term_image_urls = adapter.get_image_urls(search_results_html, target_images)
                        all_image_urls.extend(term_image_urls)
                        print(f"   Found {len(term_image_urls)} images (fallback)")
                else:
                    import requests
                    response = requests.get(search_url)
                    response.raise_for_status()
                    search_results_html = response.text
                    term_image_urls = adapter.get_image_urls(search_results_html, target_images)
                    all_image_urls.extend(term_image_urls)
                    print(f"   Found {len(term_image_urls)} images")
                
                # Small delay between searches
                if term_idx < len(search_terms):
                    time.sleep(1)
            
            results['found'] = len(all_image_urls)
            print(f"\n🖼️  Total found: {len(all_image_urls)} image URLs")
            
            if not all_image_urls:
                print("❌ No image URLs found")
                return results
            
            # Step 4: Download and validate images with retry logic
            good_images = 0
            attempts = 0
            max_attempts = len(all_image_urls) + (max_images * 2)  # Allow extra attempts
            url_index = 0
            
            print(f"\n📥 Downloading and validating images...")
            print(f"   Target: {max_images} good images")
            
            while good_images < max_images and url_index < len(all_image_urls):
                image_url = all_image_urls[url_index]
                url_index += 1
                attempts += 1
                
                # Generate filename
                timestamp = int(time.time())
                random_id = random.randint(1000, 9999)
                filename = f"{adapter.get_source_name().lower().replace(' ', '_')}_{fruit_name}_{timestamp}_{random_id}.jpg"
                save_path = fruit_dir / filename
                
                print(f"\n[{good_images}/{max_images}] Attempt {attempts}...")
                print(f"   URL: {image_url[:80]}...")
                
                # Download image
                download_result = adapter.download_image(image_url, str(save_path))
                
                if download_result['success']:
                    results['downloaded'] += 1
                    
                    # Validate the image
                    is_valid, reason = self.validate_image(str(save_path))
                    
                    if is_valid:
                        good_images += 1
                        results['validated'] += 1
                        size_mb = download_result['size'] / (1024 * 1024)
                        print(f"   ✅ Valid: {filename} ({size_mb:.2f} MB)")
                    else:
                        results['rejected'] += 1
                        # Delete invalid image
                        os.remove(str(save_path))
                        print(f"   ❌ Rejected: {reason}")
                else:
                    results['failed'] += 1
                    print(f"   ❌ Failed: {download_result.get('error', 'Unknown error')}")
                
                results['images'].append(download_result)
                
                # Rate limiting
                time.sleep(self.rate_limit + random.uniform(0, 0.5))
            
            # Summary of validation
            if good_images < max_images:
                print(f"\n⚠️  Only got {good_images}/{max_images} valid images from available URLs")
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
        
        print(f"\n✅ Scraping complete for {fruit_name}")
        print(f"   URLs found: {results['found']}")
        print(f"   Downloaded: {results['downloaded']}")
        print(f"   Validated: {results['validated']}")
        print(f"   Rejected: {results['rejected']}")
        print(f"   Failed: {results['failed']}")
        
        return results
    
    def scrape_multiple_fruits(self, adapter: BaseImageAdapter, fruit_names: List[str], max_images_per_fruit: int = 100) -> Dict[str, Any]:
        """
        Scrape images for multiple fruits.
        
        Args:
            adapter (BaseImageAdapter): The source-specific adapter to use
            fruit_names (List[str]): List of fruit names to scrape
            max_images_per_fruit (int): Maximum number of images per fruit
            
        Returns:
            Dict[str, Any]: Results for all fruits
        """
        all_results = {}
        
        try:
            for fruit_name in fruit_names:
                results = self.scrape_fruit_images(adapter, fruit_name, max_images_per_fruit)
                all_results[fruit_name] = results
                
                # Longer delay between different fruits
                if fruit_name != fruit_names[-1]:
                    print(f"\n⏸️  Waiting 5 seconds before next fruit...")
                    time.sleep(5)
        
        finally:
            # Always stop browser when done
            self.stop_browser()
        
        # Summary
        total_requested = sum(r['requested'] for r in all_results.values())
        total_found = sum(r['found'] for r in all_results.values())
        total_downloaded = sum(r['downloaded'] for r in all_results.values())
        total_failed = sum(r['failed'] for r in all_results.values())
        
        print(f"\n📊 FINAL SUMMARY")
        print("=" * 60)
        print(f"Fruits processed: {len(fruit_names)}")
        print(f"Images requested: {total_requested}")
        print(f"Images found: {total_found}")
        print(f"Images downloaded: {total_downloaded}")
        print(f"Downloads failed: {total_failed}")
        print(f"Success rate: {(total_downloaded/total_found*100):.1f}%" if total_found > 0 else "N/A")
        
        return all_results
