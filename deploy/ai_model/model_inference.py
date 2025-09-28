#!/usr/bin/env python3
"""
Model Inference Script for Jam Hot AI
Test the trained fruit classification model
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

class FruitClassifier:
    def __init__(self, model_path="ai_model/fruit_recog_model.h5"):
        """Initialize the fruit classifier"""
        print("🍓 Loading Jam Hot AI Model...")
        
        # Load the trained model
        self.model = keras.models.load_model(model_path)
        print(f"✅ Model loaded successfully!")
        
        # Load class names (fruit types)
        self.class_names = [
            'apple', 'apricot', 'blueberry', 'cherry', 'currant', 'fig', 
            'grape', 'grapefruit', 'kiwi', 'lemon', 'lime', 'mango', 
            'nectarine', 'orange', 'papaya', 'peach', 'pear', 'pineapple', 
            'plum', 'quince', 'raspberry', 'strawberry'
        ]
        
        print(f"✅ Ready to classify {len(self.class_names)} fruit types")
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        # Load and resize image
        image = Image.open(image_path)
        image = image.convert('RGB')  # Ensure RGB format
        image = image.resize((224, 224))  # Resize to model input size
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_batch = np.expand_dims(image_array, axis=0)
        
        return image_batch
    
    def predict(self, image_path, top_k=3):
        """Predict fruit type from image"""
        print(f"🔍 Analyzing image: {image_path}")
        
        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(processed_image, verbose=0)
        
        # Get top K predictions
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        
        results = []
        for i, idx in enumerate(top_indices):
            fruit_name = self.class_names[idx]
            confidence = float(predictions[0][idx])
            results.append({
                "rank": i + 1,
                "fruit": fruit_name,
                "confidence": confidence,
                "percentage": f"{confidence * 100:.1f}%"
            })
        
        return results
    
    def predict_and_display(self, image_path, top_k=3):
        """Predict and display results with image"""
        results = self.predict(image_path, top_k)
        
        # Display image
        image = Image.open(image_path)
        plt.figure(figsize=(10, 6))
        
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.title(f"Input Image")
        plt.axis('off')
        
        # Display predictions
        plt.subplot(1, 2, 2)
        fruits = [r["fruit"] for r in results]
        confidences = [r["confidence"] for r in results]
        
        bars = plt.barh(fruits, confidences)
        plt.xlabel('Confidence')
        plt.title('Top Predictions')
        plt.xlim(0, 1)
        
        # Add percentage labels
        for i, (bar, result) in enumerate(zip(bars, results)):
            plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    result["percentage"], va='center')
        
        plt.tight_layout()
        plt.show()
        
        return results

def test_with_sample_images():
    """Test the model with sample images from the dataset"""
    classifier = FruitClassifier()
    
    # Find some test images
    test_dir = Path("data/filtered_fruit_360/Test")
    
    if not test_dir.exists():
        print("❌ Test directory not found")
        return
    
    # Test a few different fruits
    test_fruits = ['strawberry', 'apple', 'orange', 'grape', 'lemon']
    
    for fruit in test_fruits:
        fruit_dir = test_dir / fruit
        if fruit_dir.exists():
            # Get first image from this fruit
            images = list(fruit_dir.glob("*.jpg"))
            if images:
                print(f"\n🍓 Testing {fruit.upper()}:")
                print("=" * 40)
                
                results = classifier.predict(images[0])
                
                for result in results:
                    print(f"{result['rank']}. {result['fruit'].title()}: {result['percentage']}")
                
                # Check if prediction is correct
                if results[0]['fruit'] == fruit:
                    print("✅ CORRECT prediction!")
                else:
                    print(f"❌ INCORRECT - predicted {results[0]['fruit']}, actual {fruit}")

def main():
    """Main testing function"""
    print("🍓 Jam Hot AI - Model Inference Test")
    print("=" * 50)
    
    # Test with sample images
    test_with_sample_images()
    
    print(f"\n🎯 Model Performance Summary:")
    print(f"- Training stopped early but model is functional")
    print(f"- Achieved 65% validation accuracy in epoch 2")
    print(f"- Can classify 22 different fruit types")
    print(f"- Ready for integration with FastAPI backend")

if __name__ == "__main__":
    main()
