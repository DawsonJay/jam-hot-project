#!/usr/bin/env python3
"""Find image elements on Google Images"""

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
    
    # Look for actual image thumbnails
    thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i, img[alt]')
    print(f"Found {len(thumbnails)} thumbnail images")
    
    if thumbnails:
        print(f"\nFirst 3 thumbnail attributes:")
        for i, img in enumerate(thumbnails[:3], 1):
            print(f"\n{i}.")
            print(f"  src: {img.get_attribute('src')[:80] if img.get_attribute('src') else 'None'}...")
            print(f"  alt: {img.get_attribute('alt')}")
            print(f"  parent tag: {img.find_element(By.XPATH, '..').tag_name}")
            
            # Get parent's parent (the link)
            try:
                grandparent = img.find_element(By.XPATH, '../..')
                print(f"  grandparent tag: {grandparent.tag_name}")
                if grandparent.tag_name == 'a':
                    print(f"  grandparent href: {grandparent.get_attribute('href')[:80] if grandparent.get_attribute('href') else 'None'}...")
            except:
                pass
        
        # Try clicking first image's container
        print("\n\nTrying to click first image...")
        try:
            first_img = thumbnails[0]
            # Find the clickable parent (usually an <a>)
            clickable = first_img.find_element(By.XPATH, '../..')
            driver.execute_script("arguments[0].click();", clickable)
            time.sleep(2)
            
            print("Clicked! Checking for full image...")
            
            # After clicking, look for the large image
            import re
            html = driver.page_source
            
            # Save sample for inspection
            with open('after_click.html', 'w') as f:
                f.write(html[:100000])
            print("Saved after_click.html (first 100k chars)")
            
            # Look for imgurl in the HTML after clicking
            imgurl_matches = re.findall(r'imgurl=(https?[^&"\s]+)', html)
            print(f"\nFound {len(imgurl_matches)} imgurl matches")
            if imgurl_matches:
                from urllib.parse import unquote
                for match in imgurl_matches[:3]:
                    print(f"  {unquote(match)[:100]}...")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
finally:
    driver.quit()
