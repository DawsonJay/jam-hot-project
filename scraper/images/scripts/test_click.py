#!/usr/bin/env python3
"""Test clicking a thumbnail and see what happens"""

import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.google.com/search?q=strawberry+fruit&tbm=isch&hl=en")
    time.sleep(3)
    
    # Scroll to load images
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    
    # Find thumbnails
    thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img[width]')
    print(f"Found {len(thumbnails)} thumbnails")
    
    if thumbnails:
        # Try clicking the first few thumbnails
        for i in range(min(3, len(thumbnails))):
            print(f"\n--- Clicking thumbnail {i+1} ---")
            
            try:
                # Click the thumbnail
                driver.execute_script("arguments[0].click();", thumbnails[i])
                time.sleep(2)  # Wait for panel to load
                
                # Check for /imgres links
                html = driver.page_source
                imgres_matches = re.findall(r'href="(/imgres\?[^"]+)"', html)
                print(f"Found {len(imgres_matches)} /imgres links after clicking")
                
                if imgres_matches:
                    print("First /imgres link:")
                    print(f"  {imgres_matches[0][:150]}...")
                    
                    # Try to extract imgurl
                    from urllib.parse import urlparse, parse_qs
                    try:
                        imgres_url = imgres_matches[0].replace('&amp;', '&')
                        parsed = urlparse(imgres_url)
                        params = parse_qs(parsed.query)
                        if 'imgurl' in params:
                            print(f"  imgurl: {params['imgurl'][0][:100]}...")
                    except Exception as e:
                        print(f"  Error parsing: {e}")
                else:
                    print("No /imgres links found")
                    
            except Exception as e:
                print(f"Error clicking thumbnail {i+1}: {e}")
    
finally:
    driver.quit()
