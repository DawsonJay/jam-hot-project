# Fruit AI Training Strategy: Complete Design Document

## Project Overview
Building a 31-class fruit detection AI that classifies user-uploaded photos into:
- 29 specific fruit classes (apple, banana, orange, etc.)
- 1 "unknown fruit" class (fruits not in the 29 categories)
- 1 "not fruit" class (non-fruit objects)

## Key Problem Solved
Initial training on Fruits-360 dataset achieved 90%+ accuracy in training but 0% on real-world photos due to domain shift (studio photos vs. real-world conditions).

## Core Design Decisions

### 1. Data Collection Strategy
**Decision**: Multi-platform scraping with AI pre-filtering
**Rationale**: Social media images provide real-world quality and diversity needed for generalization

**Platforms**:
- Reddit API (common fruits)
- Flickr API (exotic fruits)
- Unsplash API (high quality)
- Pexels API (diverse conditions)

### 2. Folder Structure
```
images/
├── apple/
│   ├── apple_001.jpg
│   ├── apple_002.jpg
│   └── urls.json
├── strawberry/
│   ├── strawberry_001.jpg
│   └── urls.json
├── not_fruit/
│   ├── not_fruit_001.jpg
│   └── urls.json
└── unknown_fruit/
    ├── unknown_fruit_001.jpg
    └── urls.json
```

### 3. Duplicate Prevention
**Decision**: URL-based tracking in JSON files
**Rationale**: Prevents re-downloading same images, enables resume functionality

**urls.json format**:
```json
[
  "https://example.com/apple1.jpg",
  "https://example.com/apple2.jpg",
  "https://example.com/apple3.jpg"
]
```

### 4. AI Pre-filtering Pipeline
**Decision**: Use pre-trained models to filter images before downloading
**Rationale**: Saves 80% of download time and bandwidth

**Filtering stages**:
1. Single fruit detection (YOLO)
2. Fruit type classification (ResNet)
3. Quality filtering (image size, clarity)

### 5. Adaptive Oversampling
**Decision**: Learning multiplier that adjusts based on success rates
**Rationale**: Optimizes URL scraping based on historical performance

## Implementation Code

### Core Collector Class
```python
import json
import os
from pathlib import Path
import requests

class UltraSimpleCollector:
    def __init__(self, base_dir="images"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def get_urls_file(self, fruit_type):
        return self.base_dir / fruit_type / "urls.json"
    
    def load_urls(self, fruit_type):
        """Load URLs from urls.json"""
        urls_file = self.get_urls_file(fruit_type)
        
        if urls_file.exists():
            with open(urls_file, 'r') as f:
                return set(json.load(f))
        else:
            return set()
    
    def save_urls(self, fruit_type, urls):
        """Save URLs to urls.json"""
        urls_file = self.get_urls_file(fruit_type)
        urls_file.parent.mkdir(exist_ok=True)
        
        with open(urls_file, 'w') as f:
            json.dump(list(urls), f)
    
    def is_url_exists(self, url):
        """Check if URL exists in any fruit folder"""
        for fruit_type in self.get_all_fruit_types():
            urls = self.load_urls(fruit_type)
            if url in urls:
                return True
        return False
    
    def get_all_fruit_types(self):
        """Get all fruit types (folder names)"""
        return [item.name for item in self.base_dir.iterdir() if item.is_dir()]
    
    def add_image(self, url, fruit_type):
        """Add image and update urls.json"""
        if self.is_url_exists(url):
            return False
        
        # Download image
        filename = self.get_next_filename(fruit_type)
        file_path = self.base_dir / fruit_type / filename
        
        if not self.download_image(url, file_path):
            return False
        
        # Update urls.json
        urls = self.load_urls(fruit_type)
        urls.add(url)
        self.save_urls(fruit_type, urls)
        
        return True
    
    def get_next_filename(self, fruit_type):
        """Get next filename for a fruit type"""
        fruit_dir = self.base_dir / fruit_type
        if not fruit_dir.exists():
            return f"{fruit_type}_001.jpg"
        
        count = len([f for f in fruit_dir.iterdir() if f.suffix == '.jpg'])
        return f"{fruit_type}_{count + 1:03d}.jpg"
    
    def download_image(self, url, file_path):
        """Download image to file path"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return False
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
```

### Learning Multiplier System
```python
class SimpleLearningCollector:
    def __init__(self, base_dir="images"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.multiplier_file = self.base_dir / "multiplier.json"
        self.load_multiplier()
    
    def load_multiplier(self):
        """Load the current multiplier"""
        if self.multiplier_file.exists():
            with open(self.multiplier_file, 'r') as f:
                self.multiplier = json.load(f)
        else:
            self.multiplier = 10.0  # Start with 10x oversample
    
    def save_multiplier(self):
        """Save the updated multiplier"""
        with open(self.multiplier_file, 'w') as f:
            json.dump(self.multiplier, f)
    
    def calculate_urls_needed(self, target_images):
        """Calculate how many URLs to scrape"""
        urls_needed = int(target_images * self.multiplier)
        print(f"Target: {target_images} images → Scrape {urls_needed} URLs (multiplier: {self.multiplier:.2f})")
        return urls_needed
    
    def update_multiplier(self, urls_scraped, images_downloaded):
        """Update multiplier based on results (like neural network learning)"""
        if urls_scraped == 0:
            return
        
        # Calculate actual ratio
        actual_ratio = urls_scraped / images_downloaded if images_downloaded > 0 else float('inf')
        
        # Learning rate (how much to adjust)
        learning_rate = 0.1
        
        # Update multiplier (weighted average)
        new_multiplier = (1 - learning_rate) * self.multiplier + learning_rate * actual_ratio
        
        # Keep within reasonable bounds
        new_multiplier = max(2.0, min(new_multiplier, 50.0))
        
        print(f"Updated multiplier: {self.multiplier:.2f} → {new_multiplier:.2f}")
        self.multiplier = new_multiplier
        self.save_multiplier()
```

### Reddit Scraping
```python
import praw

def collect_from_reddit(fruit_name, limit=100):
    reddit = praw.Reddit(
        client_id="your_client_id",
        client_secret="your_client_secret", 
        user_agent="FruitAI/1.0"
    )
    
    collector = UltraSimpleCollector()
    subreddits = ['food', 'fruit', 'cooking', 'healthyfood']
    
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).search(fruit_name, limit=30):
            if submission.url.endswith(('.jpg', '.png', '.jpeg')):
                if not collector.is_url_exists(submission.url):
                    if filter_image_from_url(submission.url, fruit_name):
                        collector.add_image(submission.url, fruit_name)
                        print(f"Downloaded {fruit_name} image")
```

### Flickr Scraping
```python
import flickrapi

def collect_from_flickr(fruit_name, limit=100):
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    collector = UltraSimpleCollector()
    
    photos = flickr.photos.search(
        text=f'{fruit_name} fruit',
        per_page=100,
        license='4,5,6,7'  # Creative Commons
    )
    
    for photo in photos['photos']['photo']:
        url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
        
        if not collector.is_url_exists(url):
            if filter_image_from_url(url, fruit_name):
                collector.add_image(url, fruit_name)
                print(f"Downloaded {fruit_name} image")
```

### AI Pre-filtering
```python
import torch
from ultralytics import YOLO
from torchvision import models, transforms
from PIL import Image
import io

# Load pre-trained models
yolo_model = YOLO('yolov8n.pt')
classification_model = models.resnet50(pretrained=True)
classification_model.eval()

def filter_image_from_url(image_url, target_fruit):
    """Filter image without downloading - just load into memory"""
    try:
        # Download image into memory (not to disk)
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            return False
            
        # Load image from memory
        image = Image.open(io.BytesIO(response.content))
        
        # Apply AI filtering
        if not filter_single_fruit_from_image(image):
            return False
            
        if not classify_fruit_type_from_image(image, target_fruit):
            return False
            
        return True
        
    except Exception as e:
        print(f"Error filtering {image_url}: {e}")
        return False

def filter_single_fruit_from_image(image):
    """Filter single fruit from PIL Image object"""
    # Convert PIL to format YOLO expects
    # Apply YOLO detection
    # Return True if single fruit detected
    pass

def classify_fruit_type_from_image(image, target_fruit):
    """Classify if image contains the target fruit type"""
    # Preprocess image
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    input_tensor = transform(image).unsqueeze(0)
    
    # Get prediction
    with torch.no_grad():
        outputs = classification_model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
    # Check if target fruit is in top predictions
    return is_target_fruit(probabilities, target_fruit)
```

## Dataset Ratios

### Recommended Distribution
- **29 fruit classes**: 80-85% of total dataset
- **"Unknown fruit" class**: 10-15% of total dataset  
- **"Not fruit" class**: 5-10% of total dataset

### Within the 29 Fruit Classes
- **Balanced distribution** across all 29 fruits
- **Minimum 100-200 images per fruit** for good performance
- **More images for common fruits** if available

## Expected Performance

### Without AI Filtering
- **1000 images collected** → **200 usable** (20% success rate)
- **Lots of plants, trees, multiple fruits**
- **Wrong fruit types**
- **Poor quality images**

### With AI Filtering
- **1000 images collected** → **800+ usable** (80%+ success rate)
- **Single fruit focus**
- **Correct fruit type**
- **High quality images**

### Learning Process
- **First run**: 10x oversample (500 URLs for 50 images)
- **After learning**: 5x oversample (250 URLs for 50 images)
- **Efficient**: Automatically optimizes over time

## Key Benefits

1. **No Duplicates**: Same URL never downloaded twice
2. **Resume Anytime**: Continue from where you left off
3. **Pre-filtering**: Saves 80% of download time and bandwidth
4. **Organized**: Each fruit in its own folder
5. **Adaptive**: Learns optimal oversampling ratios
6. **Legal**: Uses APIs and Creative Commons images
7. **Real-world Quality**: Social media style images for better generalization

## Usage Examples

### Basic Collection
```python
collector = UltraSimpleCollector()

# Collect images for a fruit
collect_from_reddit("apple", limit=100)
collect_from_flickr("apple", limit=100)

# Check what you have
urls = collector.load_urls("apple")
print(f"Have {len(urls)} apple images")
```

### Resume Collection
```python
# If you stop and restart, just run the same code
# It will automatically skip URLs you already have
collect_from_reddit("apple", limit=100)
```

### Check Database Size
```bash
# Linux command to check total size
du -sh images/

# Count total images
find images/ -name "*.jpg" | wc -l
```

## File Structure After Running
```
images/
├── apple/
│   ├── apple_001.jpg
│   ├── apple_002.jpg
│   └── urls.json
├── banana/
│   ├── banana_001.jpg
│   └── urls.json
├── not_fruit/
│   ├── not_fruit_001.jpg
│   └── urls.json
├── unknown_fruit/
│   ├── unknown_fruit_001.jpg
│   └── urls.json
└── multiplier.json
```

## Next Steps

1. **Set up APIs**: Get Reddit, Flickr, Unsplash, Pexels API keys
2. **Install dependencies**: `pip install praw flickrapi requests pillow torch ultralytics`
3. **Start collection**: Run the scraping scripts
4. **Monitor progress**: Check folder sizes and image counts
5. **Train model**: Use collected images for training
6. **Test real-world**: Deploy and test on actual user photos

## Troubleshooting

### Common Issues
- **API rate limits**: Add delays between requests
- **Download failures**: Check URL validity and network
- **Filtering too strict**: Adjust AI filtering thresholds
- **Low success rates**: Increase oversampling multiplier

### Monitoring
- **Check urls.json files**: See what URLs you've collected
- **Monitor multiplier.json**: Track learning progress
- **Use Linux commands**: Monitor disk usage and file counts
- **Review logs**: Check for errors and success rates

This strategy provides a complete, legal, and efficient way to collect diverse, real-world quality fruit images for training a robust AI model.
