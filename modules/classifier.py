"""
🔍 MODUL CLASSIFIER - KLASIFIKASI GAMBAR SAMPAH
Modul ini mengintegrasikan kode klasifikasi existing dengan improvement
"""

import numpy as np
from PIL import Image, ImageOps
import os
from pathlib import Path
from typing import Tuple, Dict

# Lazy import TensorFlow to avoid slow startup
_tf = None
_keras = None

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

class WasteClassifier:
    """
    Kelas untuk klasifikasi gambar sampah menggunakan model deep learning
    
    🧠 Cara Kerja:
    1. Load model yang sudah dilatih
    2. Preprocess gambar input (resize + normalisasi)
    3. Prediksi kelas dan confidence score
    """
    
    def __init__(self, model_path: str, labels_path: str):
        """
        Inisialisasi classifier
        
        Args:
            model_path: Path ke file model (.h5)
            labels_path: Path ke file labels (.txt)
        """
        self.model_path = model_path
        self.labels_path = labels_path
        self.model = None
        self.class_names = []
        
        # Disable scientific notation untuk clarity
        np.set_printoptions(suppress=True)
        
        # Load model dan labels
        self._load_model_and_labels()
    
    def _load_model_and_labels(self):
        """
        🔄 Load model dan labels dari file
        Private method untuk inisialisasi
        """
        try:
            # Load model Keras
            if os.path.exists(self.model_path):
                keras = _get_keras()
                self.model = keras.models.load_model(self.model_path, compile=False)
                print(f"✅ Model berhasil dimuat dari {self.model_path}")
            else:
                raise FileNotFoundError(f"Model tidak ditemukan di {self.model_path}")
            
            # Load class labels
            if os.path.exists(self.labels_path):
                with open(self.labels_path, "r") as f:
                    self.class_names = f.readlines()
                print(f"✅ Labels berhasil dimuat: {len(self.class_names)} kelas")
            else:
                raise FileNotFoundError(f"Labels tidak ditemukan di {self.labels_path}")
                
        except Exception as e:
            print(f"❌ Error loading model/labels: {e}")
            raise
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        📸 Preprocess gambar untuk input model
        
        Tahapan:
        1. Load gambar dan convert ke RGB
        2. Resize ke 224x224 (sesuai input model)
        3. Normalisasi pixel values ke range [-1, 1]
        
        Args:
            image_path: Path ke file gambar
            
        Returns:
            np.ndarray: Array gambar yang sudah dipreprocess
        """
        try:
            # Load dan convert gambar ke RGB
            image = Image.open(image_path).convert("RGB")
            
            # Resize gambar ke 224x224 dengan cropping dari center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            
            # Convert ke numpy array
            image_array = np.asarray(image)
            
            # Normalisasi: ubah range [0, 255] ke [-1, 1]
            # Formula: (pixel / 127.5) - 1
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            
            # Reshape untuk batch: (1, 224, 224, 3)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array
            
            return data
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            raise
    
    def predict(self, image_path: str) -> Dict[str, any]:
        """
        🎯 Prediksi kelas sampah dari gambar
        
        Args:
            image_path: Path ke file gambar yang akan diprediksi
            
        Returns:
            Dict dengan keys:
                - class_name: Nama kelas (str)
                - confidence: Confidence score (float 0-1)
                - confidence_percent: Confidence dalam persen (float)
                - class_index: Index kelas (int)
                - all_predictions: Semua prediksi untuk visualisasi (dict)
        """
        try:
            # Preprocess gambar
            processed_image = self.preprocess_image(image_path)
            
            # Prediksi menggunakan model
            prediction = self.model.predict(processed_image, verbose=0)
            
            # Ambil kelas dengan confidence tertinggi
            class_index = np.argmax(prediction)
            confidence_score = float(prediction[0][class_index])
            
            # Parse nama kelas (format: "0 Cardboard\n")
            class_name = self.class_names[class_index].strip()
            # Ambil nama kelas saja (skip index di awal)
            if " " in class_name:
                class_name = class_name.split(" ", 1)[1]
            
            # Buat dictionary untuk semua prediksi (untuk visualisasi)
            all_predictions = {}
            for idx, score in enumerate(prediction[0]):
                label = self.class_names[idx].strip()
                if " " in label:
                    label = label.split(" ", 1)[1]
                all_predictions[label] = float(score)
            
            # Return hasil prediksi
            result = {
                "class_name": class_name,
                "confidence": confidence_score,
                "confidence_percent": confidence_score * 100,
                "class_index": int(class_index),
                "all_predictions": all_predictions
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            raise
    
    def predict_from_pil_image(self, pil_image: Image.Image) -> Dict[str, any]:
        """
        🖼️ Prediksi dari PIL Image object (untuk Streamlit upload)
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            Dict hasil prediksi (sama seperti method predict)
        """
        try:
            # Preprocess PIL Image
            image = pil_image.convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array
            
            # Prediksi
            prediction = self.model.predict(data, verbose=0)
            class_index = np.argmax(prediction)
            confidence_score = float(prediction[0][class_index])
            
            class_name = self.class_names[class_index].strip()
            if " " in class_name:
                class_name = class_name.split(" ", 1)[1]
            
            all_predictions = {}
            for idx, score in enumerate(prediction[0]):
                label = self.class_names[idx].strip()
                if " " in label:
                    label = label.split(" ", 1)[1]
                all_predictions[label] = float(score)
            
            result = {
                "class_name": class_name,
                "confidence": confidence_score,
                "confidence_percent": confidence_score * 100,
                "class_index": int(class_index),
                "all_predictions": all_predictions
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            raise
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        📊 Kategorisasi tingkat confidence
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            str: Kategori confidence
        """
        if confidence >= 0.9:
            return "Sangat Yakin 🎯"
        elif confidence >= 0.75:
            return "Yakin ✅"
        elif confidence >= 0.5:
            return "Cukup Yakin 🤔"
        else:
            return "Kurang Yakin ⚠️"
    
    def reload_model(self):
        """
        🔄 Reload model (setelah training baru)
        """
        print("🔄 Reloading model...")
        self._load_model_and_labels()
        print("✅ Model berhasil di-reload!")


# 🧪 TESTING
if __name__ == "__main__":
    # Test classifier
    model_path = "../keras_model.h5"
    labels_path = "../labels.txt"
    
    try:
        classifier = WasteClassifier(model_path, labels_path)
        print("\n✅ Classifier berhasil diinisialisasi!")
        print(f"📊 Jumlah kelas: {len(classifier.class_names)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
