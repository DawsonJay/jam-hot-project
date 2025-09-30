#!/usr/bin/env python3
"""Check what links are available on Google Images"""

import time
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
    
    # Check for /imgres links
    imgres_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/imgres"]')
    print(f"Found {len(imgres_links)} /imgres links")
    
    if imgres_links:
        print("\nFirst 3 /imgres links:")
        for i, link in enumerate(imgres_links[:3], 1):
            href = link.get_attribute('href')
            print(f"\n{i}. {href[:150]}...")
            
            # Try to extract imgurl
            if 'imgurl=' in href:
                from urllib.parse import urlparse, parse_qs
                try:
                    parsed = urlparse(href)
                    params = parse_qs(parsed.query)
                    if 'imgurl' in params:
                        print(f"   imgurl: {params['imgurl'][0][:100]}...")
                except Exception as e:
                    print(f"   Error parsing: {e}")
    else:
        print("\nNo /imgres links found. Checking for other link patterns...")
        
        # Check for any links with href
        all_links = driver.find_elements(By.CSS_SELECTOR, 'a[href]')
        print(f"Found {len(all_links)} total links with href")
        
        # Look for links that might contain image URLs
        for i, link in enumerate(all_links[:10], 1):
            href = link.get_attribute('href')
            if href and ('img' in href.lower() or 'image' in href.lower() or 'photo' in href.lower()):
                print(f"\n{i}. {href[:100]}...")
    
finally:
    driver.quit()
