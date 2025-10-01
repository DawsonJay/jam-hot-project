#!/usr/bin/env python3
"""
Comprehensive Fruit Classifier Training Script

Trains a CNN model on fruit images with proper handling of:
- Single fruits (29 main classes)
- Mixed fruits (multiple fruits in one image)
- Not fruits (objects like knives, spoons, etc.)
- Unknown fruits (exotic fruits)

This addresses the issues from previous training attempts.
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
OUTPUT_DIR = PROJECT_ROOT / "ai_model" / "trained_model_comprehensive"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


def check_dataset():
    """
    Check if the dataset is properly organized with all required classes.
    """
    print("🔍 Checking dataset structure...")
    
    if not DATA_DIR.exists():
        print(f"❌ Data directory not found: {DATA_DIR}")
        return False
    
    # Expected classes
    main_fruits = [
        "strawberry", "apple", "raspberry", "blueberry", "peach",
        "plum", "cherry", "grape", "orange", "lemon", "lime",
        "fig", "apricot", "mango", "pear", "blackberry", "cranberry",
        "currant", "elderberry", "gooseberry", "grapefruit", "kiwi",
        "nectarine", "papaya", "passion_fruit", "pineapple", "quince",
        "rhubarb", "dragon_fruit"
    ]
    
    special_classes = ["mixed_fruits", "not_fruit", "unknown_fruit"]
    all_classes = main_fruits + special_classes
    
    print(f"📋 Expected classes: {len(all_classes)}")
    print(f"   Main fruits: {len(main_fruits)}")
    print(f"   Special classes: {len(special_classes)}")
    
    # Check each class
    missing_classes = []
    total_images = 0
    
    for class_name in all_classes:
        class_dir = DATA_DIR / class_name
        if class_dir.exists():
            image_count = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.jpeg"))) + len(list(class_dir.glob("*.png")))
            total_images += image_count
            print(f"   ✅ {class_name}: {image_count} images")
        else:
            missing_classes.append(class_name)
            print(f"   ❌ {class_name}: Missing")
    
    print(f"\n📊 Dataset Summary:")
    print(f"   Total images: {total_images}")
    print(f"   Missing classes: {len(missing_classes)}")
    
    if missing_classes:
        print(f"   Missing: {missing_classes}")
        return False
    
    return True


def setup_data_generators(data_dir, image_size, batch_size):
    """
    Sets up data generators for training and validation with augmentation.
    """
    print("\n--- Setting up Data Generators ---")
    
    # Data Augmentation for Training
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=VALIDATION_SPLIT
    )
    
    # No Augmentation for Validation (only rescaling)
    val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=VALIDATION_SPLIT
    )
    
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        seed=42
    )
    
    validation_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        seed=42
    )
    
    print(f"Found {train_generator.num_classes} classes.")
    print(f"Training images: {train_generator.samples}")
    print(f"Validation images: {validation_generator.samples}")
    
    return train_generator, validation_generator


def build_model(num_classes, image_size):
    """
    Builds the ResNet50 model with custom top layers for comprehensive fruit classification.
    """
    print("\n--- Building Model ---")
    
    # Load pre-trained ResNet50 model
    base_model = ResNet50(
        include_top=False,
        weights='imagenet',
        input_shape=(*image_size, 3)
    )
    
    # Add custom top layers
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(1024, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    predictions = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs=base_model.input, outputs=predictions)
    
    print("Model built successfully using ResNet50.")
    return model, base_model


def train_model(model, base_model, train_generator, validation_generator, num_classes):
    """
    Trains the model in two phases: frozen base and fine-tuning.
    """
    print("\n--- Starting Training ---")
    
    # Callbacks
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    checkpoint_filepath = OUTPUT_DIR / f'best_model_{timestamp}.h5'
    
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7),
        ModelCheckpoint(filepath=str(checkpoint_filepath), monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
    ]
    
    # --- Phase 1: Train only the top layers (freeze base model) ---
    print("\n--- Phase 1: Training top layers (frozen base) ---")
    for layer in base_model.layers:
        layer.trainable = False
    
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                  loss='categorical_crossentropy',
                  metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')])
    
    history1 = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // BATCH_SIZE,
        callbacks=callbacks
    )
    
    # --- Phase 2: Fine-tune the entire model (unfreeze some layers) ---
    print("\n--- Phase 2: Fine-tuning entire model (unfreeze last 20 layers) ---")
    for layer in base_model.layers[-20:]:  # Unfreeze last 20 layers of ResNet50
        layer.trainable = True
    
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
                  loss='categorical_crossentropy',
                  metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')])
    
    history2 = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // BATCH_SIZE,
        callbacks=callbacks
    )
    
    return history1, history2, model


def plot_history(history1, history2):
    """
    Plots training and validation accuracy and loss.
    """
    print("\n--- Plotting Training History ---")
    
    hist = {}
    for key in history1.history.keys():
        hist[key] = history1.history[key] + history2.history[key]
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(hist['accuracy'], label='Training Accuracy')
    plt.plot(hist['val_accuracy'], label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(hist['loss'], label='Training Loss')
    plt.plot(hist['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plot_path = OUTPUT_DIR / 'training_history.png'
    plt.savefig(plot_path)
    print(f"Training history plot saved to {plot_path}")


def save_class_indices(generator, save_dir):
    """
    Saves the class_indices mapping to a JSON file.
    """
    import json
    class_indices_path = save_dir / 'class_indices.json'
    with open(class_indices_path, 'w') as f:
        json.dump(generator.class_indices, f)
    print(f"Class indices saved to {class_indices_path}")


def main():
    print("🚀 Starting Comprehensive Fruit Classifier Training 🚀")
    print("=" * 60)
    
    # Check dataset
    if not check_dataset():
        print("❌ Dataset check failed. Please ensure all classes are present.")
        return
    
    # Setup data generators
    train_generator, validation_generator = setup_data_generators(DATA_DIR, IMAGE_SIZE, BATCH_SIZE)
    num_classes = train_generator.num_classes
    
    # Build model
    model, base_model = build_model(num_classes, IMAGE_SIZE)
    
    # Train model
    history1, history2, final_model = train_model(model, base_model, train_generator, validation_generator, num_classes)
    
    # Plot history
    plot_history(history1, history2)
    
    # Save class indices
    save_class_indices(train_generator, OUTPUT_DIR)
    
    # Save final model
    final_model_path = OUTPUT_DIR / 'final_model.h5'
    final_model.save(final_model_path)
    print(f"\nFinal trained model saved to {final_model_path}")
    
    print("\n✅ Comprehensive AI Training Complete!")
    print("This model can now handle:")
    print("  - Single fruit identification (29 classes)")
    print("  - Mixed fruit detection")
    print("  - Not-fruit detection")
    print("  - Unknown fruit detection")


if __name__ == "__main__":
    main()

