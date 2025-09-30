#!/usr/bin/env python3
"""
Fruit Classifier Training Script

Trains a CNN model on real-world fruit images for the Jam-Hot project.
This model will classify 29 types of fruits plus an "unknown" class.
"""

import os
import sys
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "scraper" / "images" / "data"
OUTPUT_DIR = PROJECT_ROOT / "ai_model" / "trained_model"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


def check_dataset():
    """Check the dataset structure and count images."""
    print("\n" + "="*60)
    print("📊 DATASET ANALYSIS")
    print("="*60)
    
    if not DATA_DIR.exists():
        print(f"❌ Error: Dataset directory not found: {DATA_DIR}")
        sys.exit(1)
    
    # Count classes and images
    classes = []
    total_images = 0
    
    for class_dir in sorted(DATA_DIR.iterdir()):
        if class_dir.is_dir():
            images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.jpeg")) + list(class_dir.glob("*.png"))
            if images:
                classes.append(class_dir.name)
                count = len(images)
                total_images += count
                print(f"  {class_dir.name:20} - {count:4} images")
    
    print(f"\n  Total classes: {len(classes)}")
    print(f"  Total images: {total_images:,}")
    
    if len(classes) == 0:
        print(f"❌ Error: No image classes found in {DATA_DIR}")
        sys.exit(1)
    
    return classes, total_images


def create_datasets():
    """Create training and validation datasets with augmentation."""
    print("\n" + "="*60)
    print("🔄 CREATING DATASETS")
    print("="*60)
    
    # Data augmentation for training
    train_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=VALIDATION_SPLIT,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation (no augmentation)
    val_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=VALIDATION_SPLIT
    )
    
    # Create training dataset
    train_dataset = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Create validation dataset
    val_dataset = val_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print(f"  Training samples: {train_dataset.samples}")
    print(f"  Validation samples: {val_dataset.samples}")
    print(f"  Number of classes: {len(train_dataset.class_indices)}")
    
    # Save class indices
    class_indices_path = OUTPUT_DIR / "class_indices.txt"
    with open(class_indices_path, 'w') as f:
        for class_name, index in sorted(train_dataset.class_indices.items(), key=lambda x: x[1]):
            f.write(f"{index}: {class_name}\n")
    print(f"  ✅ Class indices saved to: {class_indices_path}")
    
    return train_dataset, val_dataset


def build_model(num_classes):
    """Build the CNN model using transfer learning."""
    print("\n" + "="*60)
    print("🏗️  BUILDING MODEL")
    print("="*60)
    
    # Load pre-trained ResNet50 (more stable than EfficientNetB0)
    base_model = ResNet50(
        include_top=False,
        weights='imagenet',
        input_shape=(*IMAGE_SIZE, 3)
    )
    
    # Freeze base model layers initially
    base_model.trainable = False
    
    # Build model
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print(f"  Base model: EfficientNetB0 (frozen)")
    print(f"  Output classes: {num_classes}")
    print(f"  Total parameters: {model.count_params():,}")
    
    return model


def create_callbacks():
    """Create training callbacks."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            OUTPUT_DIR / f"best_model_{timestamp}.h5",
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    return callbacks


def plot_training_history(history, output_dir):
    """Plot and save training history."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy plot
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.plot(history.history['top_3_accuracy'], label='Training Top-3 Accuracy')
    ax1.plot(history.history['val_top_3_accuracy'], label='Validation Top-3 Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Loss plot
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.set_title('Model Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'training_history.png')
    print(f"  ✅ Training history plot saved")


def fine_tune_model(model, train_dataset, val_dataset, callbacks):
    """Fine-tune the model by unfreezing some layers."""
    print("\n" + "="*60)
    print("🎯 FINE-TUNING MODEL")
    print("="*60)
    
    # Unfreeze the base model
    model.layers[0].trainable = True
    
    # Freeze all layers except the last 20
    for layer in model.layers[0].layers[:-20]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print(f"  Unfrozen layers: 20 (out of {len(model.layers[0].layers)})")
    print(f"  Learning rate: {LEARNING_RATE/10}")
    
    # Fine-tune
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=20,  # Fewer epochs for fine-tuning
        callbacks=callbacks,
        verbose=1
    )
    
    return history


def main():
    """Main training function."""
    print("\n" + "="*60)
    print("🍓 FRUIT CLASSIFIER TRAINING")
    print("   Jam-Hot Project - Real-World Image Training")
    print("="*60)
    
    # Check GPU availability
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"✅ GPU available: {len(gpus)} device(s)")
    else:
        print("⚠️  No GPU detected - training will be slower")
    
    # Check dataset
    classes, total_images = check_dataset()
    
    # Create datasets
    train_dataset, val_dataset = create_datasets()
    
    # Build model
    num_classes = len(train_dataset.class_indices)
    model = build_model(num_classes)
    
    # Create callbacks
    callbacks = create_callbacks()
    
    # Train model (initial phase)
    print("\n" + "="*60)
    print("🚀 TRAINING - PHASE 1 (Transfer Learning)")
    print("="*60)
    
    history1 = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Fine-tune model (phase 2)
    history2 = fine_tune_model(model, train_dataset, val_dataset, callbacks)
    
    # Combine histories
    combined_history = {}
    for key in history1.history.keys():
        combined_history[key] = history1.history[key] + history2.history[key]
    
    # Create a mock History object
    class MockHistory:
        def __init__(self, history_dict):
            self.history = history_dict
    
    combined_history_obj = MockHistory(combined_history)
    
    # Plot training history
    plot_training_history(combined_history_obj, OUTPUT_DIR)
    
    # Final evaluation
    print("\n" + "="*60)
    print("📊 FINAL EVALUATION")
    print("="*60)
    
    val_loss, val_accuracy, val_top3_accuracy = model.evaluate(val_dataset, verbose=0)
    
    print(f"  Validation Loss: {val_loss:.4f}")
    print(f"  Validation Accuracy: {val_accuracy*100:.2f}%")
    print(f"  Validation Top-3 Accuracy: {val_top3_accuracy*100:.2f}%")
    
    # Save final model
    final_model_path = OUTPUT_DIR / "final_model.h5"
    model.save(final_model_path)
    print(f"\n  ✅ Final model saved to: {final_model_path}")
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print(f"📈 Training history plot: {OUTPUT_DIR / 'training_history.png'}")
    print(f"🤖 Best model: {OUTPUT_DIR / 'best_model_*.h5'}")
    print(f"🤖 Final model: {final_model_path}")
    print(f"📋 Class indices: {OUTPUT_DIR / 'class_indices.txt'}")
    
    print("\n🎯 Next steps:")
    print("  1. Review the training history plot")
    print("  2. Test the model with real fruit photos")
    print("  3. Deploy to production if satisfied with results")


if __name__ == "__main__":
    main()
