# AI Model Specification - Jam Hot Project

## Overview
The AI model component uses transfer learning to identify fruits from photos and provide flavor profiles. This demonstrates real AI/ML skills including transfer learning, computer vision, and model optimization. The model focuses on fruits only - herbs, spices, and other ingredients are not identified.

## Technical Approach

### Transfer Learning Strategy
- **Base Model**: Pre-trained model (ResNet50 or EfficientNet)
- **Fine-tuning**: Adapt to fruit classification task
- **Data**: Fruit-360 dataset (60,000+ images, 120+ fruit types)
- **Custom Data**: Personal fruit photos for testing

### Why Transfer Learning
- **Real AI skills**: Not just API integration
- **Faster development**: 2-3 weeks vs months for custom training
- **Industry standard**: What companies actually do
- **Portfolio value**: Demonstrates genuine ML expertise

## Data Strategy

### Primary Dataset
- **Fruit-360**: 60,000+ fruit images, 120+ fruit types
- **Quality**: High-resolution, well-labeled images
- **Diversity**: Various angles, lighting, ripeness levels
- **Preprocessing**: Resize, normalize, augment

### Data Augmentation
- **Rotation**: Random rotations for robustness
- **Flipping**: Horizontal flips for variety
- **Brightness**: Adjust lighting conditions
- **Contrast**: Enhance image variations

### Custom Data Collection
- **Personal photos**: Real fruit photos for testing
- **Wild fruits**: Peak District foraging photos
- **Supermarket fruits**: Common commercial varieties
- **Validation set**: Manual testing with real photos

## Model Architecture

### Base Model Options
1. **ResNet50**: Proven performance, good balance
2. **EfficientNet**: More efficient, better accuracy
3. **MobileNet**: Lighter for deployment

### Transfer Learning Process
1. **Load pre-trained weights**: ImageNet trained model
2. **Replace final layer**: Custom fruit classification head
3. **Freeze early layers**: Keep learned features
4. **Fine-tune later layers**: Adapt to fruit data
5. **Full fine-tuning**: Optional final training

### Model Output
- **Fruit identification**: Top 5 predictions with confidence scores
- **Flavor profile**: Sweet, tart, acidic, etc.
- **Ripeness level**: Unripe, ripe, overripe
- **Best uses**: Jam, preserves, fresh eating
- **Scope limitation**: Only identifies fruits, ignores herbs/spices/other ingredients
- **Confidence handling**: Present options if multiple likely candidates, ask for better photo if unclear

## Technical Implementation

### Training Pipeline
```python
# Model training process:
1. Data loading and preprocessing
2. Train/validation split
3. Data augmentation
4. Model compilation with custom loss
5. Transfer learning fine-tuning
6. Model validation and testing
7. Performance optimization
```

### Inference API
```python
# Model inference interface:
- Load trained model
- Preprocess input image
- Run inference
- Post-process results
- Return structured output
```

### Model Optimization
- **Quantization**: Reduce model size for deployment
- **Pruning**: Remove unnecessary weights
- **Optimization**: TensorFlow Lite for mobile deployment
- **Caching**: Preload model for faster inference

## Project Structure
```
ai_model/
├── data_collection.py
├── model_training.py
├── model_inference.py
├── data/
│   ├── fruit_360/
│   └── custom_photos/
└── trained_model/
    ├── model.h5
    ├── model.json
    └── class_labels.json
```

## Success Criteria
- **Model accuracy**: 90%+ fruit identification accuracy
- **Inference speed**: <2 seconds per image
- **Model size**: <100MB for deployment
- **Fruit coverage**: 50+ common fruit types
- **Real-world testing**: Works with personal photos
- **Confidence handling**: Present options for ambiguous cases
- **Error handling**: Graceful handling of unrecognizable images
- **Reliability**: Consistent performance across different image types

## Portfolio Value
- **Transfer learning**: Real ML skills, not just API calls
- **Computer vision**: Image preprocessing and classification
- **Model optimization**: Production-ready deployment
- **Data engineering**: Dataset collection and preprocessing
- **End-to-end ML**: From data to deployed model

## Development Timeline
- **Week 2, Days 1-2**: Set up transfer learning pipeline
- **Week 2, Days 3-4**: Train model on fruit data
- **Week 2, Day 5**: Validate and optimize model performance

## Technical Dependencies
- **Python packages**: tensorflow, numpy, PIL, matplotlib
- **Data**: Fruit-360 dataset download
- **Hardware**: GPU recommended for training
- **Storage**: ~2GB for dataset and model files

## Integration Points
- **Backend API**: Model runs on server, not frontend
- **Single Database**: Query fruits, profiles, and recipes from one PostgreSQL database
- **Coverage Tracking**: Check which fruits have profiles (LEFT JOIN profiles table)
- **Smart Status**: Return appropriate status based on coverage and recipe availability
- **Frontend**: Receives results via API calls
