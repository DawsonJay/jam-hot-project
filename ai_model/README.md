# AI Model Development - Jam Hot Project

## Overview
This directory contains the AI model development for the Jam Hot project - an AI-powered fruit classification system for jam making.

## Current Status
**🔄 PIVOTING TO GOOGLE IMAGES-BASED TRAINING**

The previous AI model training using the Fruit-360 dataset failed completely on real-world images (0% accuracy despite 83.4% validation accuracy). We're now implementing a Google Images-based scraping strategy for realistic training data.

### Why the Previous Approach Failed:
- **Dataset Mismatch**: Fruit-360 images are clean, isolated fruits on white backgrounds
- **Real-World Gap**: User photos are complex scenes with natural lighting and mixed objects
- **Overconfidence Problem**: Model gave 71-100% confidence on completely wrong predictions
- **Domain Gap**: No transfer learning between artificial and real-world images

## New Google Images-Based Strategy

### Why Google Images is Perfect:
- **Real User Photos**: Matches expected app usage patterns
- **Varied Quality**: Phone photos, different lighting, natural scenes
- **Huge Volume**: Thousands of fruit photos available
- **No Licensing Issues**: Training use only, no deployment concerns

### New Training Workflow:
1. **Google Images Scraping**: Collect realistic fruit photos using web scraper
2. **Manual Vetting**: Download images locally for quality review
3. **Dataset Curation**: Ensure balance across 29 target fruit types
4. **Model Retraining**: Use curated realistic dataset

## Target Fruit Types (29 Most Common for Jam)
- Strawberry, Apple, Raspberry, Blueberry, Peach, Plum, Cherry, Grape, Orange, Lemon, Lime
- Fig, Apricot, Mango, Pear, Blackberry, Cranberry, Currant, Elderberry, Gooseberry, Grapefruit
- Kiwi, Nectarine, Papaya, Passion Fruit, Pineapple, Quince, Rhubarb, Dragon Fruit

## Project Structure
```
ai_model/
├── README.md                    # This file
├── ai_env/                      # Virtual environment (reusable)
├── train_fruit_classifier.py   # Training script
└── trained_model/              # Model outputs
    ├── final_model.h5
    ├── class_indices.json
    └── training_history.png

scraper/images/
├── adapters/                    # Image source adapters
│   └── google_images_adapter.py
├── core/                        # Core scraping logic
│   └── image_scraper.py
├── scripts/                     # Download scripts
│   └── download_training_images.py
└── data/                        # Image storage (organized by fruit)
    ├── strawberry/
    ├── apple/
    └── ... (29 fruit types + unknown)
```

## Technical Approach

### Data Collection Strategy:
- **Target**: 500+ images per fruit type (7,500+ total)
- **Quality Control**: Manual vetting of all downloaded images
- **Balancing**: Ensure similar counts across fruit types
- **Realism**: Focus on natural, user-submitted photos

### Model Architecture:
- **Base Model**: ResNet50 (proven architecture)
- **Input Size**: 224x224 RGB images
- **Output**: 15 fruit classes
- **Transfer Learning**: Fine-tune on realistic data
- **Regularization**: Dropout, early stopping, data augmentation

### Performance Targets:
- **Real-World Accuracy**: >80% on user photos
- **Inference Speed**: <2 seconds per image
- **Confidence Calibration**: Accurate confidence scores
- **Robustness**: Handle varied lighting and composition

## Implementation Plan

### Phase 1: Pinterest Scraper (1 day)
- Build Pinterest image collection adapter
- Implement URL extraction and validation
- Test with 1-2 fruit types

### Phase 2: Mass Data Collection (1-2 days)
- Scrape 500+ images for 15 target fruits
- Download and organize into local folders
- Manual vetting and dataset balancing

### Phase 3: Model Retraining (1-2 days)
- Train ResNet50 on curated Pinterest dataset
- Validate on real user photos
- Achieve >80% accuracy on realistic images

**Total Timeline**: 4-5 days for working model

## Portfolio Value

This pivot demonstrates valuable professional skills:
- **Problem Diagnosis**: Systematic analysis of AI training failures
- **Adaptability**: Pivoting strategy when initial approach fails
- **Data Engineering**: Designing custom data collection pipeline
- **Quality Focus**: Manual vetting process for training data
- **ML Understanding**: Recognizing domain gap and dataset mismatch

## Next Steps
1. Build Pinterest image scraper
2. Collect and vet realistic training data
3. Retrain model on curated dataset
4. Validate on real-world photos
5. Deploy working AI model

---

*This README was updated on 2025-09-29-0757 to reflect the pivot to Pinterest-based training approach.*