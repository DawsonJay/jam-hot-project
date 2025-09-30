# Scraper Module - Jam Hot Project

## Overview
This module handles all web scraping functionality for the Jam Hot project, organized into two main areas:

## 📁 Structure

### **Recipes Module** (`recipes/`)
Handles scraping of jam recipes from cooking websites:
- **Adapters**: Site-specific scrapers for recipe websites
- **Scripts**: Orchestration and data processing scripts
- **Target Sites**: AllRecipes, BBC Good Food, Food Network, Serious Eats

### **Images Module** (`images/`)
Handles collection of fruit images for AI training:
- **Adapters**: Site-specific scrapers for image sources
- **Scripts**: Image download and validation scripts
- **Target Sites**: Pinterest, Unsplash, and other image sources

### **Core Module** (`core/`)
Shared scraping infrastructure:
- **Base Classes**: Common scraping patterns and utilities
- **Selenium Integration**: Browser automation for complex sites
- **Validation**: Data quality and format checking

## 🎯 Current Focus: Pinterest Image Scraping

We're building a Pinterest adapter to collect realistic fruit photos for AI training:

### **Why Pinterest for AI Training:**
- Real user-submitted photos (matches app usage)
- Varied quality and composition
- Natural scenes and mixed objects
- Huge volume of fruit photos
- No licensing concerns (training use only)

### **Target Fruit Types (15):**
Strawberry, Apple, Raspberry, Blueberry, Peach, Plum, Cherry, Grape, Orange, Lemon, Lime, Fig, Apricot, Mango, Pear

### **Data Collection Strategy:**
- **Target**: 500+ images per fruit type (7,500+ total)
- **Quality Control**: Manual vetting of all downloaded images
- **Balancing**: Ensure similar counts across fruit types
- **Realism**: Focus on natural, user-submitted photos

## 🚀 Next Steps

1. **Build Pinterest Adapter** (`images/adapters/pinterest_adapter.py`)
2. **Create Image Downloader** (`images/scripts/download_fruit_images.py`)
3. **Implement Quality Control** (`images/scripts/validate_images.py`)
4. **Test with 1-2 Fruit Types** before mass collection

## 📊 Portfolio Value

This organized approach demonstrates:
- **Modular Architecture**: Clean separation of concerns
- **Scalable Design**: Easy to add new sites and adapters
- **Quality Focus**: Manual vetting process for training data
- **Engineering Judgment**: Recognizing when to pivot and reorganize

---

*This README was updated on 2025-09-29-0757 to reflect the new organized structure and Pinterest focus.*
