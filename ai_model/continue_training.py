#!/usr/bin/env python3
"""
Continue Training Script for Jam Hot AI
Resume training from the saved model to improve accuracy
"""

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import matplotlib.pyplot as plt

def create_data_generators(data_dir):
    """Create data generators (same as before)"""
    print("🔄 Creating data generators...")
    
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # Validation data
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        data_dir / 'Training',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    validation_generator = val_datagen.flow_from_directory(
        data_dir / 'Training',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    print(f"✅ Training samples: {train_generator.samples}")
    print(f"✅ Validation samples: {validation_generator.samples}")
    
    return train_generator, validation_generator

def create_callbacks(model_dir):
    """Create training callbacks"""
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            model_dir / 'improved_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=15,  # More patience for better results
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=7,
            min_lr=1e-7,
            verbose=1
        ),
        keras.callbacks.CSVLogger(
            model_dir / 'continued_training_log.csv',
            append=True
        )
    ]
    
    return callbacks

def main():
    """Continue training from saved model"""
    print("🍓 Jam Hot AI - Continue Training")
    print("=" * 50)
    
    # Setup paths
    data_dir = Path("data/filtered_fruit_360")
    model_dir = Path("trained_model")
    
    if not (model_dir / 'best_model.h5').exists():
        print("❌ No saved model found. Run model_training.py first.")
        return
    
    # Load the existing model
    print("📂 Loading existing model...")
    model = keras.models.load_model(model_dir / 'best_model.h5')
    print(f"✅ Model loaded! Current architecture:")
    model.summary()
    
    # Create data generators
    train_gen, val_gen = create_data_generators(data_dir)
    
    # Recompile model with lower learning rate for fine-tuning
    print("🔧 Recompiling model with lower learning rate...")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),  # Lower LR
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    # Create callbacks
    callbacks = create_callbacks(model_dir)
    
    # Continue training
    print("🚀 Continuing training...")
    print("Target: Improve from 65% to 80-90% accuracy")
    
    history = model.fit(
        train_gen,
        epochs=30,  # Additional epochs
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Plot training history
    print("📊 Plotting training progress...")
    
    plt.figure(figsize=(12, 4))
    
    # Accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy (Continued Training)')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    # Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss (Continued Training)')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(model_dir / 'continued_training_history.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Load best model and evaluate
    print("🔍 Loading best model for final evaluation...")
    best_model = keras.models.load_model(model_dir / 'improved_model.h5')
    
    # Test on validation set
    val_loss, val_accuracy, val_top3 = best_model.evaluate(val_gen, verbose=0)
    
    print(f"\n🎉 Training Complete!")
    print(f"✅ Final Validation Accuracy: {val_accuracy:.1%}")
    print(f"✅ Top-3 Accuracy: {val_top3:.1%}")
    print(f"✅ Improved model saved as: improved_model.h5")
    
    if val_accuracy >= 0.80:
        print("🏆 Excellent! Achieved 80%+ accuracy target!")
    elif val_accuracy >= 0.75:
        print("🎯 Good! Solid improvement achieved!")
    else:
        print("📈 Progress made! Consider more training or data augmentation.")

if __name__ == "__main__":
    main()
