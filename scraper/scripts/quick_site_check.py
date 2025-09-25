#!/usr/bin/env python3
"""
Quick Site Checker

This script quickly tests recipe sites to detect:
- Basic connectivity
- Common bot protection patterns
- Search functionality
- Response characteristics

Usage: python3 scraper/scripts/quick_site_check.py
"""

import requests
import time
from urllib.parse import quote_plus
from datetime import datetime

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD-HHMM format."""
    return datetime.utcnow().strftime("%Y-%m-%d-%H%M")

def test_site_connectivity(site_name, base_url, search_path, search_query="strawberry jam"):
    """
    Quick test of site connectivity and basic bot protection detection.
    
    Args:
        site_name (str): Name of the site
        base_url (str): Base URL of the site
        search_path (str): Search path/endpoint
        search_query (str): Test search query
        
    Returns:
        dict: Test results
    """
    print(f"\n🔍 Testing {site_name}...")
    
    results = {
        "site": site_name,
        "base_url": base_url,
        "search_url": f"{base_url}{search_path}",
        "connectivity": False,
        "search_works": False,
        "bot_protection": "unknown",
        "response_size": 0,
        "status_code": 0,
        "response_time": 0,
        "notes": []
    }
    
    # Test 1: Basic connectivity
    try:
        start_time = time.time()
        response = requests.get(base_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        response_time = time.time() - start_time
        
        results["connectivity"] = True
        results["status_code"] = response.status_code
        results["response_time"] = response_time
        results["response_size"] = len(response.text)
        
        print(f"  ✅ Connectivity: {response.status_code} ({response_time:.2f}s, {len(response.text)} chars)")
        
        # Check for common bot protection indicators
        content = response.text.lower()
        if any(indicator in content for indicator in [
            "cloudflare", "access denied", "blocked", "captcha", "challenge",
            "security check", "bot detection", "rate limit", "forbidden"
        ]):
            results["bot_protection"] = "detected"
            results["notes"].append("Bot protection indicators found in response")
            print(f"  ⚠️  Bot protection: DETECTED")
        else:
            results["bot_protection"] = "none_detected"
            print(f"  ✅ Bot protection: None detected")
            
    except requests.exceptions.RequestException as e:
        results["notes"].append(f"Connectivity failed: {e}")
        print(f"  ❌ Connectivity failed: {e}")
        return results
    
    # Test 2: Search functionality
    try:
        search_url = f"{base_url}{search_path}"
        if "?" in search_path:
            search_url += f"&q={quote_plus(search_query)}"
        else:
            search_url += f"?q={quote_plus(search_query)}"
            
        start_time = time.time()
        search_response = requests.get(search_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        search_time = time.time() - start_time
        
        if search_response.status_code == 200:
            results["search_works"] = True
            results["notes"].append(f"Search successful ({search_time:.2f}s)")
            print(f"  ✅ Search: Works ({search_time:.2f}s, {len(search_response.text)} chars)")
            
            # Check if search results contain the query
            search_content = search_response.text.lower()
            if search_query.lower() in search_content:
                results["notes"].append("Search query found in results")
                print(f"  ✅ Search results: Contains '{search_query}'")
            else:
                results["notes"].append("Search query not found in results")
                print(f"  ⚠️  Search results: Does not contain '{search_query}'")
        else:
            results["notes"].append(f"Search failed: {search_response.status_code}")
            print(f"  ❌ Search: Failed ({search_response.status_code})")
            
    except requests.exceptions.RequestException as e:
        results["notes"].append(f"Search failed: {e}")
        print(f"  ❌ Search failed: {e}")
    
    return results

def main():
    """Test multiple recipe sites quickly."""
    print(f"[{get_timestamp()}] Quick Site Checker - Testing Recipe Sites")
    print("=" * 60)
    
    # List of sites to test
    sites_to_test = [
        {
            "name": "AllRecipes",
            "base_url": "https://www.allrecipes.com",
            "search_path": "/search"
        },
        {
            "name": "Food.com",
            "base_url": "https://www.food.com",
            "search_path": "/search"
        },
        {
            "name": "Taste of Home",
            "base_url": "https://www.tasteofhome.com",
            "search_path": "/search"
        },
        {
            "name": "Food Network",
            "base_url": "https://www.foodnetwork.com",
            "search_path": "/search"
        },
        {
            "name": "Epicurious",
            "base_url": "https://www.epicurious.com",
            "search_path": "/search"
        },
        {
            "name": "Bon Appétit",
            "base_url": "https://www.bonappetit.com",
            "search_path": "/search"
        },
        {
            "name": "Serious Eats",
            "base_url": "https://www.seriouseats.com",
            "search_path": "/search"
        },
        {
            "name": "King Arthur Baking",
            "base_url": "https://www.kingarthurbaking.com",
            "search_path": "/search"
        }
    ]
    
    results = []
    
    for site in sites_to_test:
        result = test_site_connectivity(
            site["name"], 
            site["base_url"], 
            site["search_path"]
        )
        results.append(result)
        time.sleep(1)  # Be respectful with requests
    
    # Summary
    print(f"\n[{get_timestamp()}] SUMMARY")
    print("=" * 60)
    
    good_sites = []
    protected_sites = []
    failed_sites = []
    
    for result in results:
        if not result["connectivity"]:
            failed_sites.append(result["site"])
        elif result["bot_protection"] == "detected":
            protected_sites.append(result["site"])
        elif result["search_works"]:
            good_sites.append(result["site"])
        else:
            protected_sites.append(result["site"])  # Assume protection if search doesn't work
    
    print(f"✅ Good Sites ({len(good_sites)}): {', '.join(good_sites)}")
    print(f"⚠️  Protected Sites ({len(protected_sites)}): {', '.join(protected_sites)}")
    print(f"❌ Failed Sites ({len(failed_sites)}): {', '.join(failed_sites)}")
    
    # Recommendations
    print(f"\n[{get_timestamp()}] RECOMMENDATIONS")
    print("=" * 60)
    
    if good_sites:
        print(f"🎯 Focus on: {', '.join(good_sites[:2])} (fastest to implement)")
    
    if protected_sites:
        print(f"🤖 Consider Selenium for: {', '.join(protected_sites[:2])} (if worth the effort)")
    
    if failed_sites:
        print(f"❌ Skip: {', '.join(failed_sites)} (connectivity issues)")
    
    return results

if __name__ == "__main__":
    main()
