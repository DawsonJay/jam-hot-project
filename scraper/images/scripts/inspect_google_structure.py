#!/usr/bin/env python3
"""Inspect Google Images page structure after clicking"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.google.com/search?q=strawberry+fruit&tbm=isch&hl=en")
    time.sleep(3)
    
    # Find all image container elements
    print("Looking for image elements...")
    
    # Try different selectors
    selectors = [
        ('a[jsname]', 'Links with jsname'),
        ('div[jsname]', 'Divs with jsname'),
        ('img[jsname]', 'Images with jsname'),
        ('a[href^="/imgres"]', 'Links starting with /imgres'),
        ('div[data-id]', 'Divs with data-id'),
    ]
    
    for selector, desc in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"\n{desc} ({selector}): {len(elements)} found")
        if elements and len(elements) > 0:
            print(f"  First element HTML: {elements[0].get_attribute('outerHTML')[:200]}...")
    
    # Try clicking on first clickable image
    print("\n\nAttempting to click first image...")
    try:
        first_link = driver.find_elements(By.CSS_SELECTOR, 'a[jsname]')[0]
        driver.execute_script("arguments[0].click();", first_link)
        time.sleep(2)
        
        print("Clicked! Looking for full-size image...")
        
        # Find the large image that appears
        large_img = driver.find_elements(By.CSS_SELECTOR, 'img.sFlh5c, img.iPVvYb, img[data-atf="true"]')
        print(f"Found {len(large_img)} large images")
        if large_img:
            for idx, img in enumerate(large_img[:3]):
                src = img.get_attribute('src')
                print(f"  {idx+1}. {src[:100] if src else 'None'}...")
        
        # Also check for any href with imgurl
        import re
        html = driver.page_source
        imgurl_matches = re.findall(r'imgurl=(https[^&]+)', html)
        print(f"\nFound {len(imgurl_matches)} imgurl parameters in HTML")
        if imgurl_matches:
            from urllib.parse import unquote
            for i, match in enumerate(imgurl_matches[:3], 1):
                decoded = unquote(match)
                print(f"  {i}. {decoded[:100]}...")
        
    except Exception as e:
        print(f"Error clicking: {e}")
    
    print("\n\nPress Enter to close browser...")
    input()
    
finally:
    driver.quit()
