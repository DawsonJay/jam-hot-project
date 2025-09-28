# AI Model Development - Jam Hot Project

## Overview
This directory contains the AI model development for fruit classification using transfer learning. The model will identify fruits from photos and provide flavor profiles for jam making.

## Project Structure
```
ai_model/
├── README.md                 # This file
├── data/                     # Dataset storage
│   ├── fruit_360/           # Fruit-360 dataset (60,000+ images)
│   └── custom_photos/       # Personal fruit photos for testing
├── trained_model/           # Saved model files
│   ├── model.h5            # Trained model weights
│   ├── model.json           # Model architecture
│   └── class_labels.json    # Fruit class labels
├── notebooks/               # Jupyter notebooks for development
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── model_evaluation.ipynb
├── data_collection.py       # Dataset download and preparation
├── model_training.py        # Transfer learning training pipeline
├── model_inference.py       # Model inference and prediction
└── requirements.txt         # Python dependencies for AI development
```

## Development Plan

### Phase 1: Environment Setup (Day 1)
- [ ] Install AI/ML dependencies (TensorFlow, OpenCV, etc.)
- [ ] Download Fruit-360 dataset
- [ ] Set up data preprocessing pipeline
- [ ] Configure base model (ResNet50/EfficientNet)

### Phase 2: Model Training (Days 2-3)
- [ ] Implement transfer learning pipeline
- [ ] Train model on fruit classification
- [ ] Data augmentation and optimization
- [ ] Monitor training performance

### Phase 3: Validation & Integration (Days 4-5)
- [ ] Model validation and testing
- [ ] Performance optimization
- [ ] API integration with FastAPI backend
- [ ] Real-world testing with custom photos

## Success Criteria
- **Model accuracy**: 90%+ fruit identification accuracy
- **Inference speed**: <2 seconds per image
- **Model size**: <100MB for deployment
- **Fruit coverage**: 50+ common fruit types
- **Real-world testing**: Works with personal photos

## Hardware Specifications
- **CPU**: AMD Ryzen 5 7430U (6 cores, 12 threads)
- **RAM**: 30GB (excellent for dataset handling)
- **Training**: CPU-based (no GPU required)
- **Storage**: ~2GB for dataset and model files

## Technical Approach
- **Transfer Learning**: Pre-trained model (ResNet50/EfficientNet)
- **Dataset**: Fruit-360 (60,000+ images, 120+ fruit types)
- **Framework**: TensorFlow/Keras
- **Optimization**: CPU-optimized training and inference
- **Integration**: FastAPI backend with PostgreSQL database

## Getting the Trained Model

The trained model files are too large for GitHub (>96MB). To get the trained model:

1. **Train the model locally** (recommended):
   ```bash
   cd ai_model
   python3 data_collection.py  # Download and filter dataset
   python3 model_training.py  # Train the model
   ```

2. **Download from cloud storage** (if available):
   - The trained model will be stored in cloud storage
   - Download link will be provided in the main project README

## Model Performance
- **Validation Accuracy**: 86.1%
- **Top-3 Accuracy**: 97.5%
- **Model Size**: ~97MB (compressed: ~93MB)
- **Classes**: 22 fruit types

## Next Steps
1. Set up development environment
2. Download and prepare Fruit-360 dataset
3. Implement transfer learning pipeline
4. Train and validate model
5. Integrate with existing API backend
