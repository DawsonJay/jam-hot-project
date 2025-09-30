#!/usr/bin/env python3
"""Check if /imgres links are in the HTML"""

import sys
import re
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://www.google.com/search?q=strawberry+fruit&tbm=isch&hl=en")
        time.sleep(3)
        
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        
        html = driver.page_source
        
        # Search for /imgres
        imgres_matches = re.findall(r'href="(/imgres\?[^"]{0,200})', html)
        print(f"Found {len(imgres_matches)} /imgres links")
        
        if imgres_matches:
            print("\nFirst 3 examples:")
            for i, match in enumerate(imgres_matches[:3], 1):
                print(f"\n{i}. {match[:200]}...")
                
                # Try to extract imgurl parameter
                from urllib.parse import parse_qs, urlparse
                try:
                    parsed = urlparse(match.replace('&amp;', '&'))
                    params = parse_qs(parsed.query)
                    if 'imgurl' in params:
                        print(f"   → Full image URL: {params['imgurl'][0][:100]}...")
                except:
                    pass
        else:
            print("\n❌ No /imgres links found!")
            print("\nSearching for 'imgurl' in HTML...")
            imgurl_matches = re.findall(r'imgurl[^&]{0,100}', html)
            print(f"Found {len(imgurl_matches)} mentions of 'imgurl'")
            if imgurl_matches:
                for match in imgurl_matches[:3]:
                    print(f"  {match}")
    
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
