#!/usr/bin/env python3
"""
Model Training Script for Jam Hot AI
Implements transfer learning for fruit classification
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Configuration
CONFIG = {
    'image_size': (224, 224),
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'validation_split': 0.2,
    'base_model': 'ResNet50',  # Reliable and proven
    'fine_tune_layers': 20,  # Number of layers to fine-tune
}

def create_data_generators(data_dir):
    """Create data generators with augmentation"""
    print("🔄 Creating data generators...")
    
    # Training data augmentation (aggressive for better generalization)
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
        validation_split=CONFIG['validation_split']
    )
    
    # Validation data (no augmentation, just rescaling)
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=CONFIG['validation_split']
    )
    
    # Test data (no augmentation)
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        data_dir / 'Training',
        target_size=CONFIG['image_size'],
        batch_size=CONFIG['batch_size'],
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    validation_generator = val_datagen.flow_from_directory(
        data_dir / 'Training',
        target_size=CONFIG['image_size'],
        batch_size=CONFIG['batch_size'],
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    # Test generator
    test_generator = test_datagen.flow_from_directory(
        data_dir / 'Test',
        target_size=CONFIG['image_size'],
        batch_size=CONFIG['batch_size'],
        class_mode='categorical',
        shuffle=False
    )
    
    print(f"✅ Training samples: {train_generator.samples}")
    print(f"✅ Validation samples: {validation_generator.samples}")
    print(f"✅ Test samples: {test_generator.samples}")
    print(f"✅ Number of classes: {train_generator.num_classes}")
    
    return train_generator, validation_generator, test_generator

def create_model(num_classes):
    """Create transfer learning model"""
    print(f"🧠 Creating {CONFIG['base_model']} model...")
    
    # Load pre-trained base model
    if CONFIG['base_model'] == 'ResNet50':
        base_model = keras.applications.ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=CONFIG['image_size'] + (3,)
        )
    elif CONFIG['base_model'] == 'EfficientNetB2':
        base_model = keras.applications.EfficientNetB2(
            weights='imagenet',
            include_top=False,
            input_shape=CONFIG['image_size'] + (3,)
        )
    else:
        raise ValueError(f"Unsupported base model: {CONFIG['base_model']}")
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Add custom classification head
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    print(f"✅ Model created with {num_classes} classes")
    print(f"✅ Total parameters: {model.count_params():,}")
    
    return model, base_model

def compile_model(model, learning_rate=None):
    """Compile model with optimizer and loss"""
    lr = learning_rate or CONFIG['learning_rate']
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print(f"✅ Model compiled with learning rate: {lr}")

def create_callbacks(model_dir):
    """Create training callbacks"""
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            model_dir / 'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        keras.callbacks.CSVLogger(
            model_dir / 'training_log.csv',
            append=True
        )
    ]
    
    return callbacks

def plot_training_history(history, model_dir):
    """Plot training history"""
    print("📊 Plotting training history...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Accuracy
    axes[0, 0].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0, 0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0, 0].set_title('Model Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    
    # Loss
    axes[0, 1].plot(history.history['loss'], label='Training Loss')
    axes[0, 1].plot(history.history['val_loss'], label='Validation Loss')
    axes[0, 1].set_title('Model Loss')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    
    # Top-3 Accuracy
    axes[1, 0].plot(history.history['top_3_accuracy'], label='Training Top-3 Accuracy')
    axes[1, 0].plot(history.history['val_top_3_accuracy'], label='Validation Top-3 Accuracy')
    axes[1, 0].set_title('Model Top-3 Accuracy')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Top-3 Accuracy')
    axes[1, 0].legend()
    
    # Learning Rate
    if 'lr' in history.history:
        axes[1, 1].plot(history.history['lr'], label='Learning Rate')
        axes[1, 1].set_title('Learning Rate Schedule')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Learning Rate')
        axes[1, 1].set_yscale('log')
        axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig(model_dir / 'training_history.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Training history saved to {model_dir / 'training_history.png'}")

def evaluate_model(model, test_generator, class_names, model_dir):
    """Evaluate model on test set"""
    print("🔍 Evaluating model on test set...")
    
    # Get predictions
    test_generator.reset()
    predictions = model.predict(test_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Get true labels
    true_classes = test_generator.classes
    
    # Classification report
    report = classification_report(
        true_classes, 
        predicted_classes, 
        target_names=class_names,
        output_dict=True
    )
    
    # Save classification report
    with open(model_dir / 'classification_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    accuracy = report['accuracy']
    print(f"✅ Test Accuracy: {accuracy:.4f}")
    print(f"✅ Macro Avg F1-Score: {report['macro avg']['f1-score']:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(true_classes, predicted_classes)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(model_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Confusion matrix saved to {model_dir / 'confusion_matrix.png'}")
    
    return accuracy, report

def save_model_artifacts(model, class_names, model_dir):
    """Save model and related artifacts"""
    print("💾 Saving model artifacts...")
    
    # Save model
    model.save(model_dir / 'final_model.h5')
    
    # Save class names
    with open(model_dir / 'class_names.json', 'w') as f:
        json.dump(class_names, f, indent=2)
    
    # Save config
    with open(model_dir / 'config.json', 'w') as f:
        json.dump(CONFIG, f, indent=2)
    
    print(f"✅ Model artifacts saved to {model_dir}")

def main():
    """Main training process"""
    print("🍓 Jam Hot AI - Model Training")
    print("=" * 50)
    
    # Setup paths
    data_dir = Path("data/filtered_fruit_360")
    model_dir = Path("trained_model")
    model_dir.mkdir(exist_ok=True)
    
    if not data_dir.exists():
        print("❌ Dataset not found. Run data_collection.py first.")
        return
    
    # Create data generators
    train_gen, val_gen, test_gen = create_data_generators(data_dir)
    class_names = list(train_gen.class_indices.keys())
    num_classes = len(class_names)
    
    print(f"🎯 Training on {num_classes} fruit classes:")
    for i, name in enumerate(class_names):
        print(f"  {i}: {name}")
    
    # Create model
    model, base_model = create_model(num_classes)
    compile_model(model)
    
    # Print model summary
    print("\n📋 Model Summary:")
    model.summary()
    
    # Phase 1: Train classification head
    print("\n🚀 Phase 1: Training classification head...")
    callbacks = create_callbacks(model_dir)
    
    history1 = model.fit(
        train_gen,
        epochs=20,  # Initial training
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Phase 2: Fine-tune some layers
    print(f"\n🔧 Phase 2: Fine-tuning top {CONFIG['fine_tune_layers']} layers...")
    base_model.trainable = True
    
    # Freeze early layers, unfreeze later layers
    for layer in base_model.layers[:-CONFIG['fine_tune_layers']]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    compile_model(model, learning_rate=CONFIG['learning_rate'] / 10)
    
    history2 = model.fit(
        train_gen,
        epochs=CONFIG['epochs'] - 20,  # Continue training
        initial_epoch=20,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    # Combine histories
    history = keras.utils.History()
    for key in history1.history:
        history.history[key] = history1.history[key] + history2.history[key]
    
    # Plot training history
    plot_training_history(history, model_dir)
    
    # Load best model
    model = keras.models.load_model(model_dir / 'best_model.h5')
    
    # Evaluate model
    accuracy, report = evaluate_model(model, test_gen, class_names, model_dir)
    
    # Save final artifacts
    save_model_artifacts(model, class_names, model_dir)
    
    print(f"\n🎉 Training Complete!")
    print(f"✅ Final Test Accuracy: {accuracy:.4f}")
    print(f"✅ Model saved to: {model_dir}")
    
    if accuracy >= 0.95:
        print("🏆 Excellent! Achieved 95%+ accuracy target!")
    elif accuracy >= 0.90:
        print("🎯 Good! Achieved 90%+ accuracy target!")
    else:
        print("⚠️  Consider more training or data augmentation to reach 95% target")

if __name__ == "__main__":
    main()
