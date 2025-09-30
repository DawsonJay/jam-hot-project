#!/usr/bin/env python3
"""Debug what selectors work for Google Images thumbnails"""

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
    
    # Try different selectors for image thumbnails
    selectors = [
        ('img.rg_i', 'img.rg_i'),
        ('img[alt]', 'img with alt'),
        ('img[src*="encrypted-tbn"]', 'img with encrypted-tbn'),
        ('img[jsname]', 'img with jsname'),
        ('a img', 'img inside a tag'),
        ('div img', 'img inside div'),
        ('img[width]', 'img with width'),
        ('img[height]', 'img with height'),
    ]
    
    for selector, desc in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"\n{desc} ({selector}): {len(elements)} found")
        if elements:
            first = elements[0]
            print(f"  src: {first.get_attribute('src')[:80] if first.get_attribute('src') else 'None'}...")
            print(f"  alt: {first.get_attribute('alt')}")
            print(f"  class: {first.get_attribute('class')}")
            print(f"  jsname: {first.get_attribute('jsname')}")
    
    # Also try to find any clickable elements that might be images
    print(f"\n\nLooking for clickable elements...")
    clickable = driver.find_elements(By.CSS_SELECTOR, 'a, div[onclick], div[jsaction]')
    print(f"Found {len(clickable)} clickable elements")
    
    # Look for elements with strawberry-related content
    strawberry_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'strawberry') or contains(@alt, 'strawberry')]")
    print(f"Found {len(strawberry_elements)} elements with 'strawberry' text/alt")
    
finally:
    driver.quit()
