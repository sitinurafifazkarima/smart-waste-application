# 🌍 Smart Waste Classifier

**Aplikasi Pembelajaran Machine Learning untuk Klasifikasi Sampah**

Aplikasi edukatif untuk siswa SMP yang mengajarkan konsep Artificial Intelligence sambil peduli lingkungan!

---

## ✨ Fitur Utama

### 📸 Tambah Data Training
- Upload foto sampah untuk memperkaya dataset
- 5 kategori: Cardboard, Glass, Metal, Paper, Plastic
- Automatic image processing & storage

### 🧠 Training Model Interaktif
- **Parameter yang dapat diatur:**
  - Jumlah Epoch (5-100)
  - Learning Rate (0.0001 - 0.01)
  - Batch Size (8, 16, 32, 64)
- **Visualisasi Real-time:**
  - Progress bar training
  - Live accuracy & loss graphs
  - Estimasi waktu training
- **Educational tooltips** untuk setiap parameter

### 🔍 Klasifikasi Sampah
- Upload foto untuk identifikasi otomatis
- Tampilkan confidence score
- Visualisasi distribusi prediksi
- Ikon kategori yang menarik

### ♻️ Rekomendasi Aksi
Untuk setiap jenis sampah, dapatkan:
- Aksi utama pengelolaan
- Tips praktis
- Dampak lingkungan
- Nilai ekonomis
- Fakta edukatif

### 🎮 Sistem Gamifikasi
- **AI Level System** berdasarkan accuracy:
  - 🥚 AI Telur (0-50%)
  - 🐣 AI Anak Ayam (50-70%)
  - 🐥 AI Ayam Muda (70-85%)
  - 🦅 AI Elang (85-95%)
  - 🚀 AI Roket (95-100%)
- Badge achievements
- Training progress tracking

### 🎓 Pusat Edukasi
- Penjelasan konsep AI (Epoch, Learning Rate, Accuracy, Loss)
- Panduan pengelolaan sampah
- Fakta menarik tentang daur ulang
- Dampak lingkungan

---

## 📁 Struktur Folder

```
app_pilahsampah/
├── app.py                      # ⭐ Aplikasi utama (Streamlit)
├── config.py                   # Konfigurasi aplikasi
├── requirements.txt            # Dependencies
├── keras_model.h5             # Model (akan diupdate saat training)
├── labels.txt                 # Label kategori
│
├── modules/                    # 🧩 Modul utama
│   ├── __init__.py
│   ├── classifier.py          # Klasifikasi gambar
│   ├── trainer.py             # Training model
│   ├── data_manager.py        # Manajemen dataset
│   └── recommender.py         # Sistem rekomendasi
│
├── utils/                      # 🔧 Utilities
│   ├── __init__.py
│   ├── image_processor.py     # Preprocessing gambar
│   └── visualizer.py          # Visualisasi data
│
├── assets/                     # 🎨 Asset (icons, styles)
│   └── icons/
│
├── dataset/                    # 📦 Dataset
│   ├── raw/                   # Data mentah (upload di sini)
│   │   ├── cardboard/
│   │   ├── glass/
│   │   ├── metal/
│   │   ├── paper/
│   │   └── plastic/
│   └── processed/             # Data terproses (auto-generated)
│       ├── train/
│       ├── test/
│       └── validation/
│
└── training_logs/              # 📝 Log training (auto-generated)
```

---

## 🚀 Cara Instalasi

### 1️⃣ Persiapan Environment

**Pastikan sudah terinstal:**
- Python 3.8 atau lebih baru
- pip (Python package manager)

### 2️⃣ Install Dependencies

Buka terminal di folder `app_pilahsampah`, lalu jalankan:

```powershell
pip install -r requirements.txt
```

**Dependencies yang akan diinstall:**
- `streamlit` - Framework UI
- `tensorflow` & `keras` - Machine Learning
- `pillow` - Image processing
- `matplotlib`, `plotly`, `seaborn` - Visualisasi
- `streamlit-option-menu` - Menu sidebar
- Dan lainnya...

### 3️⃣ Verifikasi Instalasi

```powershell
python -c "import streamlit; import tensorflow; print('✅ Instalasi berhasil!')"
```

---

## 🎯 Cara Menjalankan Aplikasi

### Metode 1: Command Line

```powershell
cd "d:\Materi KIR SMPITIK\app_pilahsampah"
streamlit run app.py
```

### Metode 2: Dengan Script

Buat file `run_app.ps1`:

```powershell
# run_app.ps1
Write-Host "🚀 Memulai Smart Waste Classifier..." -ForegroundColor Green
cd "d:\Materi KIR SMPITIK\app_pilahsampah"
streamlit run app.py
```

Lalu jalankan:
```powershell
.\run_app.ps1
```

### Aplikasi akan terbuka di browser:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## 📖 Panduan Penggunaan

### 1️⃣ **Tambah Data Training**

1. Klik menu **"📸 Tambah Data"**
2. Upload foto sampah (JPG/PNG)
3. Pilih kategori yang sesuai
4. Klik **"Tambah ke Dataset"**
5. Ulangi hingga setiap kategori memiliki minimal 10 gambar

**Tips:**
- Gunakan foto yang jelas dan fokus
- Variasi angle dan kondisi cahaya
- Minimal 50 gambar total untuk hasil terbaik

### 2️⃣ **Training Model**

1. Klik menu **"🧠 Training"**
2. Baca penjelasan Epoch & Learning Rate
3. Atur parameter:
   - **Epoch**: Mulai dengan 20 (untuk pemula)
   - **Learning Rate**: 0.001 (recommended)
   - **Batch Size**: 32 (default)
4. Klik **"🚀 Mulai Training!"**
5. Tunggu hingga selesai (lihat progress real-time)

**Catatan:**
- Training pertama akan lebih lama (membuat model baru)
- Training selanjutnya lebih cepat (update model)
- Semakin banyak data dan epoch, semakin lama prosesnya

### 3️⃣ **Klasifikasi Sampah**

1. Klik menu **"🔍 Klasifikasi"**
2. Upload foto sampah yang ingin diidentifikasi
3. Klik **"🎯 Klasifikasikan!"**
4. Lihat hasil:
   - Jenis sampah
   - Confidence score
   - Grafik distribusi prediksi
   - Rekomendasi pengelolaan
   - Fakta edukatif

### 4️⃣ **Eksplorasi Edukasi**

1. Klik menu **"📚 Edukasi"**
2. Explore 3 tab:
   - **Tentang AI**: Konsep machine learning
   - **Tentang Sampah**: Panduan pengelolaan
   - **Level AI**: Sistem gamifikasi

---

## 🎓 Konsep Edukatif

### Apa itu Epoch? 🔄
**Epoch = 1 putaran lengkap AI mempelajari SEMUA data training**

Analogi: Seperti kamu belajar untuk ujian
- 1 epoch = baca semua materi 1 kali
- 10 epoch = baca 10 kali

💡 **Tips:** 
- Terlalu sedikit = AI belum paham
- Terlalu banyak = AI "menghafal" bukan "memahami" (overfitting)
- Ideal: 10-50 epoch

### Apa itu Learning Rate? ⚡
**Learning Rate = Kecepatan AI belajar**

Analogi: 
- Terlalu cepat (0.01) = ngebut, tidak paham
- Terlalu lambat (0.0001) = lama sekali belajarnya
- Pas (0.001) = belajar dengan nyaman

### Apa itu Accuracy? 🎯
**Accuracy = Persentase jawaban benar AI**

- 50% = AI masih belajar
- 70% = AI mulai paham
- 85% = AI sudah pintar
- 95%+ = AI sangat pintar!

### Apa itu Loss? 📉
**Loss = Tingkat kesalahan AI**

Semakin rendah = Semakin bagus!
- Loss turun terus = AI belajar dengan baik ✅
- Loss naik = Ada masalah ⚠️

---

## 🎨 Kustomisasi

### Ubah Tema Warna

Edit `config.py`, bagian `COLORS`:

```python
COLORS = {
    "primary": "#2ECC71",      # Hijau utama
    "secondary": "#27AE60",    # Hijau gelap
    "accent": "#F39C12",       # Oranye
    # ... ubah sesuai selera
}
```

### Tambah Kategori Sampah Baru

1. **Update `config.py`:**
```python
WASTE_CATEGORIES = {
    "cardboard": "Cardboard",
    "glass": "Glass",
    "metal": "Metal",
    "paper": "Paper",
    "plastic": "Plastic",
    "organic": "Organic"  # ← Tambah di sini
}
```

2. **Update rekomendasi** di `WASTE_RECOMMENDATIONS`

3. **Buat folder** `dataset/raw/organic/`

4. **Update `labels.txt`**

### Ubah Parameter Default

Edit `config.py`, bagian `DEFAULT_TRAINING_PARAMS`:

```python
DEFAULT_TRAINING_PARAMS = {
    "epochs": 30,              # Ubah default epochs
    "learning_rate": 0.0005,   # Ubah default learning rate
    "batch_size": 16,          # Ubah default batch size
    # ...
}
```

---

## 🐛 Troubleshooting

### ❌ Error: "Model tidak ditemukan"
**Solusi:** Training model terlebih dahulu di menu "🧠 Training"

### ❌ Error: "Dataset belum cukup"
**Solusi:** Tambahkan minimal 10 gambar per kategori (total 50 gambar)

### ❌ Error: ModuleNotFoundError
**Solusi:** Install dependencies:
```powershell
pip install -r requirements.txt
```

### ❌ Training sangat lambat
**Penyebab & Solusi:**
- **Banyak data:** Normal, tunggu saja
- **Epoch terlalu banyak:** Kurangi jumlah epoch
- **CPU lemah:** Gunakan batch_size lebih kecil (8 atau 16)

### ❌ Accuracy tidak meningkat
**Solusi:**
- Tambah lebih banyak data
- Coba learning rate berbeda
- Pastikan foto berkualitas baik
- Training lebih banyak epoch

### ❌ Aplikasi tidak muncul di browser
**Solusi:**
1. Pastikan tidak ada aplikasi lain di port 8501
2. Coba buka manual: `http://localhost:8501`
3. Restart terminal dan coba lagi

---

## 📊 Tips untuk Hasil Terbaik

### 1. Dataset Berkualitas
✅ **DO:**
- Foto jelas dan fokus
- Variasi angle & pencahayaan
- Minimal 20 gambar per kategori
- Background yang bersih

❌ **DON'T:**
- Foto blur/buram
- Terlalu gelap/terang
- Objek terlalu kecil
- Background berantakan

### 2. Parameter Training
**Untuk Pemula:**
- Epochs: 20-30
- Learning Rate: 0.001
- Batch Size: 32

**Untuk Dataset Besar (100+ gambar):**
- Epochs: 50-100
- Learning Rate: 0.0005
- Batch Size: 32

**Untuk CPU Lemah:**
- Epochs: 10-20
- Learning Rate: 0.001
- Batch Size: 8-16

### 3. Evaluasi Model
- **Accuracy > 85%** = Sangat baik! ✅
- **Accuracy 70-85%** = Bagus, bisa ditingkatkan 👍
- **Accuracy < 70%** = Perlu lebih banyak data 📚

---

## 🎯 Objektif Pembelajaran

Aplikasi ini dirancang untuk mengajarkan:

### Konsep Teknis:
- ✅ Machine Learning basics
- ✅ Image classification
- ✅ Training & testing
- ✅ Model evaluation
- ✅ Data preprocessing

### Konsep Lingkungan:
- ✅ Jenis-jenis sampah
- ✅ Metode daur ulang
- ✅ Dampak lingkungan
- ✅ Nilai ekonomis sampah
- ✅ Pemilahan sampah

### Soft Skills:
- ✅ Problem solving
- ✅ Data collection
- ✅ Experimentation
- ✅ Critical thinking
- ✅ Environmental awareness

---

## 🤝 Untuk Guru/Pendidik

### Skenario Pembelajaran

**Pertemuan 1: Pengenalan AI & Dataset**
- Intro AI dan Machine Learning
- Demo aplikasi
- Siswa upload 5-10 foto per kategori
- Diskusi: Mengapa data penting?

**Pertemuan 2: Training Model**
- Jelaskan konsep Epoch & Learning Rate
- Demo training dengan parameter berbeda
- Siswa training model mereka
- Observasi: Grafik accuracy & loss

**Pertemuan 3: Evaluasi & Klasifikasi**
- Uji model dengan foto baru
- Analisis confidence score
- Diskusi: Kapan AI salah? Mengapa?
- Hubungkan dengan pengelolaan sampah

**Pertemuan 4: Project & Presentasi**
- Siswa improve model mereka
- Dokumentasi proses
- Presentasi hasil
- Diskusi dampak lingkungan

### Penilaian
- **Keaktifan:** Kontribusi data (20%)
- **Pemahaman:** Penjelasan konsep AI (30%)
- **Eksperimen:** Testing parameter berbeda (20%)
- **Presentasi:** Dokumentasi & presentasi (30%)

---

## 📝 Changelog

### Version 1.0.0 (2025-11-26)
✨ **Initial Release**
- ✅ Upload & manage dataset
- ✅ Training dengan parameter custom
- ✅ Real-time visualization
- ✅ Klasifikasi gambar
- ✅ Sistem rekomendasi
- ✅ Gamifikasi (AI Levels)
- ✅ Pusat edukasi
- ✅ UI eco-green theme

---

## 📞 Support

Jika ada pertanyaan atau masalah:
1. Baca troubleshooting di atas
2. Check dokumentasi di aplikasi (menu Edukasi)
3. Review kode (ada banyak komentar edukatif)

---

## 🌟 Credits

**Dibuat untuk:** Siswa SMP - Pembelajaran AI & Lingkungan

**Tech Stack:**
- Python 3.x
- Streamlit (UI Framework)
- TensorFlow/Keras (Machine Learning)
- Plotly (Interactive Visualization)
- Pillow (Image Processing)

**Dataset:** User-contributed (siswa upload sendiri)

---

## 📄 License

Educational use only. Dibuat untuk tujuan pembelajaran.

---

## 🎉 Selamat Belajar!

Aplikasi ini adalah alat untuk **belajar sambil peduli lingkungan**.

**Remember:**
- 🧠 AI belajar dari data yang kamu beri
- 🌍 Setiap sampah punya cara pengelolaan yang tepat
- 🎯 Practice makes perfect - semakin sering training, semakin paham!

**Mari bersama-sama:**
- Belajar teknologi AI
- Peduli lingkungan
- Ciptakan masa depan lebih baik

---

## 🚀 Quick Start Commands

```powershell
# Install dependencies
pip install -r requirements.txt

# Run aplikasi
streamlit run app.py

# Test modul individual
python modules/classifier.py
python modules/data_manager.py
python modules/trainer.py
python modules/recommender.py
```

---

**Happy Learning! 🎓♻️🤖**
