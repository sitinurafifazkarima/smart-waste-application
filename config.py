"""
📋 KONFIGURASI APLIKASI SMART WASTE CLASSIFIER
File ini berisi semua konfigurasi penting untuk aplikasi
"""

import os
from pathlib import Path

# 📂 PATH KONFIGURASI
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
MODEL_PATH = BASE_DIR / "keras_model.h5"
LABELS_PATH = BASE_DIR / "labels.txt"

# 🏷️ KATEGORI SAMPAH
WASTE_CATEGORIES = {
    "cardboard": "Cardboard",
    "glass": "Glass",
    "metal": "Metal",
    "paper": "Paper",
    "plastic": "Plastic"
}

# 🎨 IKON UNTUK SETIAP KATEGORI
CATEGORY_ICONS = {
    "cardboard": "📦",
    "glass": "🫙",
    "metal": "🔩",
    "paper": "📄",
    "plastic": "🥤"
}

# ♻️ REKOMENDASI AKSI UNTUK SETIAP JENIS SAMPAH
WASTE_RECOMMENDATIONS = {
    "Cardboard": {
        "icon": "📦",
        "action": "Daur ulang karton",
        "description": "Cardboard dapat didaur ulang menjadi kertas atau karton baru. Pastikan bersih dan kering sebelum direcycle.",
        "tips": [
            "Lipat cardboard agar lebih mudah disimpan",
            "Pisahkan dari plastik atau stiker",
            "Setor ke tempat daur ulang terdekat"
        ],
        "impact": "🌳 Mengurangi penebangan pohon",
        "value": "ekonomis_rendah"
    },
    "Glass": {
        "icon": "🫙",
        "action": "Daur ulang di tempat khusus",
        "description": "Kaca dapat didaur ulang berkali-kali tanpa kehilangan kualitas. Namun harus ditangani dengan hati-hati.",
        "tips": [
            "Cuci bersih sebelum daur ulang",
            "Pisahkan berdasarkan warna",
            "Hati-hati dengan pecahan kaca"
        ],
        "impact": "⚡ Menghemat energi hingga 40%",
        "value": "ekonomis_sedang"
    },
    "Metal": {
        "icon": "🔩",
        "action": "Bernilai ekonomis - bisa dijual!",
        "description": "Logam sangat bernilai dan dapat didaur ulang berkali-kali. Setor ke bank sampah atau pengepul.",
        "tips": [
            "Pisahkan jenis logam (besi, aluminium)",
            "Bersihkan dari kotoran",
            "Kumpulkan hingga jumlah banyak untuk nilai jual lebih baik"
        ],
        "impact": "💰 Nilai ekonomi tinggi + ramah lingkungan",
        "value": "ekonomis_tinggi"
    },
    "Paper": {
        "icon": "📄",
        "action": "Daur ulang atau gunakan kembali",
        "description": "Kertas bekas dapat didaur ulang menjadi kertas baru atau digunakan ulang untuk kerajinan.",
        "tips": [
            "Pisahkan kertas putih dan berwarna",
            "Pastikan kertas kering dan bersih",
            "Gunakan dua sisi kertas sebelum direcycle"
        ],
        "impact": "🌳 1 ton kertas daur ulang = 17 pohon terselamatkan",
        "value": "ekonomis_rendah"
    },
    "Plastic": {
        "icon": "🥤",
        "action": "Kurangi penggunaan / setor ke bank sampah",
        "description": "Plastik sulit terurai. Prioritaskan mengurangi penggunaan, lalu daur ulang di bank sampah.",
        "tips": [
            "Cek kode recycle di kemasan (1-7)",
            "Cuci bersih dari sisa makanan",
            "Pilih plastik yang bisa didaur ulang",
            "Kurangi penggunaan plastik sekali pakai"
        ],
        "impact": "🌊 Mengurangi pencemaran laut dan tanah",
        "value": "ekonomis_rendah"
    }
}

# 🎓 KONTEN EDUKATIF
EDUCATIONAL_CONTENT = {
    "epoch": {
        "title": "Apa itu Epoch? 🔄",
        "description": "Epoch adalah 1 kali putaran lengkap AI mempelajari SEMUA data training. Semakin banyak epoch, AI semakin belajar - tapi hati-hati overfitting!",
        "analogy": "Seperti kamu belajar menghadapi ujian. 1 epoch = baca semua materi 1 kali. 10 epoch = baca 10 kali.",
        "tips": "📚 Biasanya 10-50 epoch cukup. Terlalu banyak bisa bikin AI 'menghafal' bukan 'memahami'."
    },
    "learning_rate": {
        "title": "Apa itu Learning Rate? 📊",
        "description": "Learning rate mengatur seberapa cepat AI belajar. Terlalu cepat = AI bingung. Terlalu lambat = lama belajarnya.",
        "analogy": "Seperti kecepatan belajar. Terlalu ngebut = nggak paham. Terlalu pelan = bosan.",
        "tips": "⚡ Nilai ideal: 0.001 - 0.01. Mulai dengan 0.001 untuk aman."
    },
    "accuracy": {
        "title": "Accuracy (Akurasi) 🎯",
        "description": "Persentase jawaban benar AI dari total prediksi. Semakin tinggi = semakin pintar!",
        "levels": {
            "0-50": "🥚 AI Pemula - Masih belajar",
            "50-70": "🐣 AI Berkembang - Mulai memahami",
            "70-85": "🐥 AI Kompeten - Cukup pintar",
            "85-95": "🦅 AI Ahli - Sangat pintar!",
            "95-100": "🚀 AI Master - Luar biasa!"
        }
    },
    "loss": {
        "title": "Loss (Kesalahan) 📉",
        "description": "Tingkat kesalahan AI. Semakin rendah = semakin bagus! AI belajar untuk meminimalkan nilai loss.",
        "tips": "🎯 Target: Loss mendekati 0. Kalau loss turun terus = AI belajar dengan baik!"
    }
}

# 🎮 SISTEM GAMIFIKASI
AI_LEVELS = {
    "level_1": {"name": "🥚 AI Telur", "accuracy": 0, "badge": "Baru Menetas"},
    "level_2": {"name": "🐣 AI Anak Ayam", "accuracy": 50, "badge": "Mulai Belajar"},
    "level_3": {"name": "🐥 AI Ayam Muda", "accuracy": 70, "badge": "Semakin Pintar"},
    "level_4": {"name": "🦅 AI Elang", "accuracy": 85, "badge": "Ahli Klasifikasi"},
    "level_5": {"name": "🚀 AI Roket", "accuracy": 95, "badge": "Master AI"}
}

# 🎨 TEMA WARNA (Eco-Green)
COLORS = {
    "primary": "#2ECC71",      # Hijau utama
    "secondary": "#27AE60",    # Hijau gelap
    "accent": "#F39C12",       # Oranye (peringatan)
    "success": "#28B463",      # Hijau sukses
    "info": "#3498DB",         # Biru info
    "warning": "#F39C12",      # Oranye warning
    "danger": "#E74C3C",       # Merah bahaya
    "background": "#E8F8F5",   # Hijau muda latar
    "text": "#2C3E50"          # Text gelap
}

# ⚙️ PARAMETER TRAINING DEFAULT
DEFAULT_TRAINING_PARAMS = {
    "epochs": 20,
    "learning_rate": 0.001,
    "batch_size": 32,
    "validation_split": 0.2,
    "image_size": (224, 224)
}

# 📊 PARAMETER MODEL
MODEL_CONFIG = {
    "input_shape": (224, 224, 3),
    "num_classes": 5,
    "optimizer": "adam",
    "loss": "categorical_crossentropy",
    "metrics": ["accuracy"]
}

# 📝 PESAN APLIKASI
MESSAGES = {
    "welcome": "🌍 **Selamat datang di Smart Waste Classifier!** Mari belajar memilah sampah dengan AI 🤖",
    "upload_success": "✅ Gambar berhasil ditambahkan ke dataset!",
    "training_start": "🚀 Training dimulai! AI sedang belajar...",
    "training_complete": "🎉 Training selesai! AI kamu semakin pintar!",
    "classification_success": "✨ Klasifikasi berhasil!",
    "error": "❌ Terjadi kesalahan. Coba lagi ya!"
}
