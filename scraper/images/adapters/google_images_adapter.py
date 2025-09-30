"""
Google Images Adapter

Adapter for scraping images from Google Images search.
"""

import requests
import re
import json
from typing import List, Dict, Any
from pathlib import Path
from urllib.parse import quote_plus

from scraper.images.adapters.base_image_adapter import BaseImageAdapter


class GoogleImagesAdapter(BaseImageAdapter):
    """
    Adapter for scraping images from Google Images.
    """
    
    def __init__(self):
        """Initialize the Google Images adapter"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def get_source_name(self) -> str:
        """Return the name of this image source"""
        return "Google Images"
    
    def search_for_fruit(self, fruit_name: str, max_images: int = 100) -> str:
        """
        Generate a Google Images search URL for this fruit.
        
        Args:
            fruit_name (str): The name of the fruit to search for
            max_images (int): Maximum number of images (not used in URL but kept for interface)
            
        Returns:
            str: The Google Images search URL
        """
        # Create search query
        search_query = f"{fruit_name} fruit"
        encoded_query = quote_plus(search_query)
        
        # Google Images search URL
        # tbm=isch means "Images" tab
        return f"https://www.google.com/search?q={encoded_query}&tbm=isch&hl=en"
    
    def get_image_urls(self, search_results_html: str, max_images: int = 100) -> List[str]:
        """
        Extract full-size image URLs from Google Images search results HTML.
        Extracts from /imgres links which contain the imgurl parameter.
        
        Args:
            search_results_html (str): The HTML content of the search results page
            max_images (int): Maximum number of image URLs to extract
            
        Returns:
            List[str]: List of full-size image URLs found
        """
        image_urls = []
        seen = set()
        
        try:
            from urllib.parse import urlparse, parse_qs, unquote
            
            # Method 1: Extract from /imgres links (contains imgurl parameter with full-size image)
            # Pattern: href="/imgres?imgurl=https://...&..."
            imgres_pattern = r'href="(/imgres\?[^"]+)"'
            imgres_matches = re.findall(imgres_pattern, search_results_html)
            
            for imgres_url in imgres_matches:
                try:
                    # Decode HTML entities
                    imgres_url = imgres_url.replace('&amp;', '&')
                    
                    # Parse the query string
                    parsed = urlparse(imgres_url)
                    params = parse_qs(parsed.query)
                    
                    # Extract the imgurl parameter (this is the full-size image URL)
                    if 'imgurl' in params:
                        full_image_url = params['imgurl'][0]
                        
                        if full_image_url not in seen:
                            # Basic validation - check if it looks like an image URL
                            if any(ext in full_image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) or \
                               not full_image_url.startswith('data:'):
                                image_urls.append(full_image_url)
                                seen.add(full_image_url)
                                
                                if len(image_urls) >= max_images:
                                    break
                except Exception as e:
                    # Skip malformed URLs
                    continue
            
            # Method 2: Fallback to thumbnails if we didn't get enough full-size images
            if len(image_urls) < max_images:
                thumb_pattern = r'"(https://encrypted-tbn\d\.gstatic\.com/images[^"]+)"'
                thumb_matches = re.findall(thumb_pattern, search_results_html)
                
                for url in thumb_matches:
                    if url not in seen and len(image_urls) < max_images:
                        image_urls.append(url)
                        seen.add(url)
        
        except Exception as e:
            print(f"Error extracting image URLs: {e}")
            import traceback
            traceback.print_exc()
        
        return image_urls[:max_images]
    
    def download_image(self, image_url: str, save_path: str) -> Dict[str, Any]:
        """
        Download an image from the given URL.
        
        Args:
            image_url (str): The URL of the image to download
            save_path (str): The local path where the image should be saved
            
        Returns:
            Dict[str, Any]: Download results
        """
        try:
            # Decode unicode escape sequences in URL
            if '\\u' in image_url:
                image_url = image_url.encode('utf-8').decode('unicode_escape')
            
            # Make request for the image
            response = self.session.get(image_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type.lower():
                return {
                    'success': False,
                    'url': image_url,
                    'path': save_path,
                    'error': f'Not an image (Content-Type: {content_type})'
                }
            
            # Save the image
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Get file size
            file_size = Path(save_path).stat().st_size
            
            return {
                'success': True,
                'url': image_url,
                'path': save_path,
                'size': file_size
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'url': image_url,
                'path': save_path,
                'error': f'Request error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'url': image_url,
                'path': save_path,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def get_scraping_method(self) -> str:
        """Return the scraping method needed for Google Images"""
        # Google Images loads content dynamically, so we need Selenium
        return "selenium"
    
    def get_search_terms(self, fruit_name: str) -> List[str]:
        """
        Generate search term variations for better image diversity.
        Mix of professional reference images (20%) and amateur realistic images (80%).
        
        Args:
            fruit_name (str): The base fruit name
            
        Returns:
            List[str]: List of search term variations
        """
        return [
            f"{fruit_name} fruit close up fresh",     # Clear fruit photos
            f"{fruit_name} picking hands harvest",    # Real picking context
            f"{fruit_name} market fresh produce",     # Market context
            f"{fruit_name} tree branch ripe",         # Natural growing
            f"{fruit_name} bowl kitchen fresh"        # Food preparation
        ]
