#!/usr/bin/env python3
"""
Data Collection Script for Jam Hot AI Model
Downloads and prepares Fruit-360 dataset for our 29 target fruits
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path
import json
from tqdm import tqdm

# Our 29 target fruits (matching database)
TARGET_FRUITS = [
    'apple', 'apricot', 'blackberry', 'blueberry', 'cherry',
    'cranberry', 'currant', 'dragon_fruit', 'elderberry', 'fig',
    'gooseberry', 'grape', 'grapefruit', 'kiwi', 'lemon',
    'lime', 'mango', 'nectarine', 'orange', 'papaya',
    'passion_fruit', 'peach', 'pear', 'pineapple', 'plum',
    'quince', 'raspberry', 'rhubarb', 'strawberry'
]

# Fruit-360 dataset mapping (some names might be different)
FRUIT_360_MAPPING = {
    'apple': 'Apple Braeburn',  # We'll need to check actual folder names
    'apricot': 'Apricot',
    'blackberry': 'Blackberry',
    'blueberry': 'Blueberry',
    'cherry': 'Cherry 1',
    'cranberry': 'Cranberry',
    'currant': 'Currant Red',
    'dragon_fruit': 'Dragon Fruit',
    'elderberry': 'Elderberry',
    'fig': 'Fig',
    'gooseberry': 'Gooseberry',
    'grape': 'Grape Blue',
    'grapefruit': 'Grapefruit Pink',
    'kiwi': 'Kiwi',
    'lemon': 'Lemon',
    'lime': 'Lime',
    'mango': 'Mango',
    'nectarine': 'Nectarine',
    'orange': 'Orange',
    'papaya': 'Papaya',
    'passion_fruit': 'Passion Fruit',
    'peach': 'Peach',
    'pear': 'Pear',
    'pineapple': 'Pineapple',
    'plum': 'Plum',
    'quince': 'Quince',
    'raspberry': 'Raspberry',
    'rhubarb': 'Rhubarb',
    'strawberry': 'Strawberry'
}

def download_file(url, filename):
    """Download a file with progress bar"""
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))
    
    print(f"✅ Downloaded {filename}")

def extract_zip(zip_path, extract_to):
    """Extract zip file"""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extracted to {extract_to}")

def download_fruit_360():
    """Download Fruit-360 dataset"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Fruit-360 dataset URLs (we'll need to find the actual URLs)
    # For now, let's create a placeholder structure
    fruit_360_dir = data_dir / "fruit_360"
    fruit_360_dir.mkdir(exist_ok=True)
    
    print("📁 Created fruit_360 directory structure")
    print("⚠️  Note: You'll need to manually download the Fruit-360 dataset")
    print("   Dataset available at: https://www.kaggle.com/moltean/fruits")
    print("   Or: https://github.com/Horea94/Fruit-Images-Dataset")
    
    return fruit_360_dir

def scan_available_fruits(fruit_360_dir):
    """Scan what fruits are actually available in the dataset"""
    training_dir = fruit_360_dir / "Training"
    if not training_dir.exists():
        print("❌ Training directory not found. Please download Fruit-360 dataset first.")
        return []
    
    available_fruits = []
    for fruit_dir in training_dir.iterdir():
        if fruit_dir.is_dir():
            available_fruits.append(fruit_dir.name)
    
    print(f"📊 Found {len(available_fruits)} fruit types in dataset")
    return sorted(available_fruits)

def map_our_fruits_to_dataset(available_fruits):
    """Map our target fruits to available dataset fruits"""
    mapping = {}
    
    for our_fruit in TARGET_FRUITS:
        # Try exact match first
        exact_matches = [f for f in available_fruits if our_fruit.lower() in f.lower()]
        
        if exact_matches:
            # Use the first match (we can refine this later)
            mapping[our_fruit] = exact_matches[0]
            print(f"✅ {our_fruit} → {exact_matches[0]}")
        else:
            print(f"❌ No match found for {our_fruit}")
    
    return mapping

def create_filtered_dataset(fruit_360_dir, mapping):
    """Create a filtered dataset with only our target fruits"""
    training_dir = fruit_360_dir / "Training"
    test_dir = fruit_360_dir / "Test"
    
    # Create our filtered dataset structure
    filtered_dir = Path("data/filtered_fruit_360")
    filtered_dir.mkdir(exist_ok=True)
    
    filtered_train = filtered_dir / "Training"
    filtered_test = filtered_dir / "Test"
    filtered_train.mkdir(exist_ok=True)
    filtered_test.mkdir(exist_ok=True)
    
    stats = {}
    
    for our_fruit, dataset_fruit in mapping.items():
        print(f"Processing {our_fruit} ({dataset_fruit})...")
        
        # Copy training images
        src_train = training_dir / dataset_fruit
        dst_train = filtered_train / our_fruit
        
        if src_train.exists():
            shutil.copytree(src_train, dst_train, dirs_exist_ok=True)
            train_count = len(list(dst_train.glob("*.jpg")))
        else:
            train_count = 0
        
        # Copy test images
        src_test = test_dir / dataset_fruit
        dst_test = filtered_test / our_fruit
        
        if src_test.exists():
            shutil.copytree(src_test, dst_test, dirs_exist_ok=True)
            test_count = len(list(dst_test.glob("*.jpg")))
        else:
            test_count = 0
        
        stats[our_fruit] = {
            "training_images": train_count,
            "test_images": test_count,
            "total_images": train_count + test_count
        }
        
        print(f"  ✅ {train_count} training + {test_count} test = {train_count + test_count} total images")
    
    # Save statistics
    with open(filtered_dir / "dataset_stats.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n📊 Dataset Statistics:")
    total_images = sum(s["total_images"] for s in stats.values())
    print(f"Total fruits: {len(stats)}")
    print(f"Total images: {total_images}")
    print(f"Average per fruit: {total_images // len(stats) if stats else 0}")
    
    return filtered_dir, stats

def main():
    """Main data collection process"""
    print("🍓 Jam Hot AI - Data Collection")
    print("=" * 50)
    
    # Step 1: Download/setup Fruit-360 dataset
    fruit_360_dir = download_fruit_360()
    
    # Step 2: Scan available fruits
    available_fruits = scan_available_fruits(fruit_360_dir)
    
    if not available_fruits:
        print("\n⚠️  Please download the Fruit-360 dataset first:")
        print("1. Go to: https://www.kaggle.com/moltean/fruits")
        print("2. Download the dataset")
        print("3. Extract to: data/fruit_360/")
        print("4. Run this script again")
        return
    
    # Step 3: Map our fruits to dataset
    mapping = map_our_fruits_to_dataset(available_fruits)
    
    if not mapping:
        print("❌ No fruit mappings found. Check dataset structure.")
        return
    
    # Step 4: Create filtered dataset
    filtered_dir, stats = create_filtered_dataset(fruit_360_dir, mapping)
    
    print(f"\n✅ Data collection complete!")
    print(f"Filtered dataset created at: {filtered_dir}")
    print(f"Ready for model training with {len(stats)} fruit types")

if __name__ == "__main__":
    main()
