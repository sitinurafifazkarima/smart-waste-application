"""
🧠 MODUL TRAINER - TRAINING MODEL MACHINE LEARNING
Modul untuk melatih model dengan parameter yang dapat diatur pengguna
Dengan visualisasi real-time!
"""

import os
import numpy as np
from pathlib import Path
from typing import Dict, Callable
import time

# Lazy import TensorFlow to avoid slow startup
_tf = None
_keras = None
_layers = None
_ImageDataGenerator = None
_Callback = None
_EarlyStopping = None
_ReduceLROnPlateau = None

def _get_tf():
    global _tf
    if _tf is None:
        import tensorflow as tf
        _tf = tf
    return _tf

def _get_keras():
    global _keras
    if _keras is None:
        tf = _get_tf()
        _keras = tf.keras
    return _keras

def _get_keras_layers():
    global _layers
    if _layers is None:
        keras = _get_keras()
        _layers = keras.layers
    return _layers

def _get_image_data_generator():
    global _ImageDataGenerator
    if _ImageDataGenerator is None:
        keras = _get_keras()
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        _ImageDataGenerator = ImageDataGenerator
    return _ImageDataGenerator

def _get_callback():
    global _Callback
    if _Callback is None:
        keras = _get_keras()
        from tensorflow.keras.callbacks import Callback
        _Callback = Callback
    return _Callback

def _get_early_stopping():
    global _EarlyStopping
    if _EarlyStopping is None:
        keras = _get_keras()
        from tensorflow.keras.callbacks import EarlyStopping
        _EarlyStopping = EarlyStopping
    return _EarlyStopping

def _get_reduce_lr_on_plateau():
    global _ReduceLROnPlateau
    if _ReduceLROnPlateau is None:
        keras = _get_keras()
        from tensorflow.keras.callbacks import ReduceLROnPlateau
        _ReduceLROnPlateau = ReduceLROnPlateau
    return _ReduceLROnPlateau
import json
from datetime import datetime

class TrainingProgressCallback(Callback):
    """
    📊 Custom callback untuk tracking progress training
    Digunakan untuk update UI real-time di Streamlit
    """
    
    def __init__(self, total_epochs: int, progress_callback: Callable = None):
        super().__init__()
        self.total_epochs = total_epochs
        self.progress_callback = progress_callback
        self.epoch_logs = []
        self.start_time = None
        
    def on_train_begin(self, logs=None):
        self.start_time = time.time()
        
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        
        # Hitung waktu
        elapsed_time = time.time() - self.start_time
        avg_time_per_epoch = elapsed_time / (epoch + 1)
        eta = avg_time_per_epoch * (self.total_epochs - epoch - 1)
        
        # Store logs
        epoch_data = {
            "epoch": epoch + 1,
            "loss": float(logs.get("loss", 0)),
            "accuracy": float(logs.get("accuracy", 0)),
            "val_loss": float(logs.get("val_loss", 0)),
            "val_accuracy": float(logs.get("val_accuracy", 0)),
            "elapsed_time": elapsed_time,
            "eta": eta
        }
        
        self.epoch_logs.append(epoch_data)
        
        # Call progress callback untuk update UI
        if self.progress_callback:
            self.progress_callback(epoch_data)


class ModelTrainer:
    """
    🎓 Kelas untuk training model klasifikasi sampah
    
    Fitur:
    - Training dengan parameter custom (epochs, learning rate)
    - Visualisasi real-time
    - Data augmentation
    - Model checkpoint & early stopping
    """
    
    def __init__(self, processed_data_dir: str, model_save_path: str):
        """
        Inisialisasi trainer
        
        Args:
            processed_data_dir: Path ke folder dataset/processed
            model_save_path: Path untuk save model hasil training
        """
        self.processed_data_dir = Path(processed_data_dir)
        self.model_save_path = model_save_path
        self.train_dir = self.processed_data_dir / "train"
        self.test_dir = self.processed_data_dir / "test"
        self.val_dir = self.processed_data_dir / "validation"
        
        self.model = None
        self.history = None
    
    def create_model(self, learning_rate: float = 0.001) -> keras.Model:
        """
        🏗️ Buat arsitektur model CNN
        
        Arsitektur:
        - Convolutional layers untuk ekstraksi fitur
        - MaxPooling untuk downsampling
        - Dropout untuk mencegah overfitting
        - Dense layers untuk klasifikasi
        
        Args:
            learning_rate: Learning rate untuk optimizer
            
        Returns:
            keras.Model yang sudah di-compile
        """
        
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=(224, 224, 3)),
            
            # Block 1: Convolutional + Pooling
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 2: Lebih banyak filter untuk fitur kompleks
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3: Fitur high-level
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten untuk input ke Dense layer
            layers.Flatten(),
            
            # Fully connected layers
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            
            # Output layer: 5 kelas dengan softmax
            layers.Dense(5, activation='softmax')
        ])
        
        # Compile model
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def prepare_data_generators(self, batch_size: int = 32):
        """
        📦 Prepare data generators dengan augmentation
        
        Data Augmentation untuk training:
        - Rotation: rotasi gambar untuk variasi
        - Shift: geser gambar
        - Flip: flip horizontal
        - Zoom: zoom in/out
        
        Args:
            batch_size: Ukuran batch untuk training
            
        Returns:
            Tuple (train_generator, validation_generator, test_generator)
        """
        
        # Data augmentation untuk training (untuk variasi data)
        train_datagen = ImageDataGenerator(
            rescale=1./127.5,           # Normalisasi [-1, 1]
            rotation_range=20,          # Rotasi random ±20 derajat
            width_shift_range=0.2,      # Geser horizontal 20%
            height_shift_range=0.2,     # Geser vertikal 20%
            shear_range=0.2,            # Shear transformation
            zoom_range=0.2,             # Zoom ±20%
            horizontal_flip=True,       # Flip horizontal
            fill_mode='nearest',        # Isi pixel kosong
            preprocessing_function=lambda x: x - 1  # Shift ke range [-1, 1]
        )
        
        # Hanya rescale untuk validation & test (no augmentation)
        val_test_datagen = ImageDataGenerator(
            rescale=1./127.5,
            preprocessing_function=lambda x: x - 1
        )
        
        # Create generators
        train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=True
        )
        
        validation_generator = val_test_datagen.flow_from_directory(
            self.val_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        test_generator = val_test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        return train_generator, validation_generator, test_generator
    
    def train(self, 
              epochs: int = 20, 
              learning_rate: float = 0.001,
              batch_size: int = 32,
              progress_callback: Callable = None) -> Dict[str, any]:
        """
        🚀 Mulai training model!
        
        Args:
            epochs: Jumlah epoch untuk training
            learning_rate: Learning rate optimizer
            batch_size: Ukuran batch
            progress_callback: Fungsi callback untuk update progress (untuk UI)
            
        Returns:
            Dict dengan hasil training
        """
        try:
            print(f"\n{'='*50}")
            print(f"🚀 MEMULAI TRAINING MODEL")
            print(f"{'='*50}")
            print(f"📊 Parameter:")
            print(f"   - Epochs: {epochs}")
            print(f"   - Learning Rate: {learning_rate}")
            print(f"   - Batch Size: {batch_size}")
            print(f"{'='*50}\n")
            
            # Prepare data
            train_gen, val_gen, test_gen = self.prepare_data_generators(batch_size)
            
            print(f"📦 Data berhasil di-load:")
            print(f"   - Training: {train_gen.samples} gambar")
            print(f"   - Validation: {val_gen.samples} gambar")
            print(f"   - Test: {test_gen.samples} gambar\n")
            
            # Create model
            print("🏗️ Membuat model...")
            self.model = self.create_model(learning_rate)
            print(f"✅ Model siap! Total parameters: {self.model.count_params():,}\n")
            
            # Callbacks
            callbacks_list = []
            
            # Progress callback
            if progress_callback:
                progress_cb = TrainingProgressCallback(epochs, progress_callback)
                callbacks_list.append(progress_cb)
            
            # Early stopping (stop jika tidak ada improvement)
            early_stop = EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            )
            callbacks_list.append(early_stop)
            
            # Reduce learning rate jika stuck
            reduce_lr = ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            )
            callbacks_list.append(reduce_lr)
            
            # TRAINING!
            print("🧠 Training dimulai...\n")
            start_time = time.time()
            
            self.history = self.model.fit(
                train_gen,
                epochs=epochs,
                validation_data=val_gen,
                callbacks=callbacks_list,
                verbose=1
            )
            
            training_time = time.time() - start_time
            
            # Evaluate on test set
            print("\n📊 Evaluating on test set...")
            test_loss, test_accuracy = self.model.evaluate(test_gen, verbose=0)
            
            # Save model
            print(f"\n💾 Menyimpan model ke {self.model_save_path}...")
            self.model.save(self.model_save_path)
            
            # Get final metrics
            final_train_acc = self.history.history['accuracy'][-1]
            final_val_acc = self.history.history['val_accuracy'][-1]
            final_train_loss = self.history.history['loss'][-1]
            final_val_loss = self.history.history['val_loss'][-1]
            
            print(f"\n{'='*50}")
            print(f"🎉 TRAINING SELESAI!")
            print(f"{'='*50}")
            print(f"⏱️  Waktu training: {training_time:.2f} detik")
            print(f"🎯 Final Training Accuracy: {final_train_acc*100:.2f}%")
            print(f"✅ Final Validation Accuracy: {final_val_acc*100:.2f}%")
            print(f"🧪 Test Accuracy: {test_accuracy*100:.2f}%")
            print(f"{'='*50}\n")
            
            # Return hasil
            result = {
                "success": True,
                "training_time": training_time,
                "final_train_accuracy": float(final_train_acc),
                "final_val_accuracy": float(final_val_acc),
                "test_accuracy": float(test_accuracy),
                "final_train_loss": float(final_train_loss),
                "final_val_loss": float(final_val_loss),
                "test_loss": float(test_loss),
                "epochs_completed": len(self.history.history['accuracy']),
                "history": {
                    "accuracy": [float(x) for x in self.history.history['accuracy']],
                    "val_accuracy": [float(x) for x in self.history.history['val_accuracy']],
                    "loss": [float(x) for x in self.history.history['loss']],
                    "val_loss": [float(x) for x in self.history.history['val_loss']]
                }
            }
            
            # Save training log
            self._save_training_log(result)
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error during training: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
    
    def _save_training_log(self, result: Dict):
        """
        📝 Save training log ke file
        """
        log_dir = Path("training_logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"training_log_{timestamp}.json"
        
        with open(log_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"📝 Training log disimpan di {log_file}")


# 🧪 TESTING
if __name__ == "__main__":
    from config import PROCESSED_DATA_DIR, MODEL_PATH
    
    trainer = ModelTrainer(PROCESSED_DATA_DIR, MODEL_PATH)
    
    # Test training dengan parameter minimal
    result = trainer.train(epochs=2, learning_rate=0.001, batch_size=16)
    
    if result["success"]:
        print("\n✅ Training berhasil!")
        print(f"🎯 Test Accuracy: {result['test_accuracy']*100:.2f}%")
    else:
        print(f"\n❌ Training gagal: {result.get('error', 'Unknown error')}")
