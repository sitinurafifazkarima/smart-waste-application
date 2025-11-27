# ⚡ QUICK START GUIDE - Smart Waste Classifier

## 🎯 Panduan Cepat untuk Memulai (5 Menit!)

---

### 📋 Yang Kamu Butuhkan:
- ✅ Python 3.8+ sudah terinstall
- ✅ Koneksi internet (untuk install dependencies)
- ✅ 1GB space kosong

---

## 🚀 Langkah-Langkah:

### 1️⃣ Buka Terminal PowerShell

Tekan `Win + X` → Pilih "Windows PowerShell"

### 2️⃣ Pindah ke Folder Aplikasi

```powershell
cd "d:\Materi KIR SMPITIK\app_pilahsampah"
```

### 3️⃣ Install Dependencies (Hanya Sekali)

```powershell
pip install -r requirements.txt
```

⏱️ **Waktu:** 3-5 menit  
☕ Sabar ya, ini hanya dilakukan sekali!

### 4️⃣ Jalankan Aplikasi

**Opsi A - Via Script (RECOMMENDED):**
```powershell
.\run_app.ps1
```

**Opsi B - Manual:**
```powershell
streamlit run app.py
```

### 5️⃣ Buka Browser

Aplikasi akan otomatis terbuka di:
```
http://localhost:8501
```

Jika tidak otomatis, buka browser dan ketik URL di atas.

---

## 🎓 Alur Penggunaan Pertama Kali:

### Step 1: Tambah Data (10 menit)
1. Klik menu **"📸 Tambah Data"**
2. Upload minimal 10 foto per kategori
3. Total minimal: **50 foto**

**Tips foto yang bagus:**
- ✅ Fokus jelas
- ✅ Cahaya cukup
- ✅ Objek terlihat penuh
- ❌ Jangan blur/gelap

### Step 2: Training Model (5-15 menit)
1. Klik menu **"🧠 Training"**
2. Baca penjelasan Epoch & Learning Rate
3. Set parameter:
   - **Epoch:** 20 (untuk pemula)
   - **Learning Rate:** 0.001
   - **Batch Size:** 32
4. Klik **"🚀 Mulai Training!"**
5. Tunggu hingga selesai (lihat grafik real-time)

**Hasil yang bagus:**
- ✅ Accuracy > 80%
- ✅ Loss terus menurun
- ✅ Level AI: 🐥 atau lebih tinggi

### Step 3: Klasifikasi (1 menit)
1. Klik menu **"🔍 Klasifikasi"**
2. Upload foto sampah
3. Klik **"🎯 Klasifikasikan!"**
4. Lihat hasil:
   - Jenis sampah
   - Confidence score
   - Rekomendasi pengelolaan

### Step 4: Eksplorasi Edukasi (Optional)
1. Klik menu **"📚 Edukasi"**
2. Pelajari tentang AI & sampah
3. Lihat level AI kamu

---

## 🆘 Troubleshooting Cepat

### ❌ Error: "Python tidak ditemukan"
**Solusi:** Install Python dari https://www.python.org/downloads/

### ❌ Error: "streamlit not found"
**Solusi:** 
```powershell
pip install streamlit
```

### ❌ Error: "Dataset belum cukup"
**Solusi:** Tambahkan minimal 50 foto (10 per kategori)

### ❌ Training sangat lambat
**Solusi:** 
- Kurangi epoch jadi 10
- Batch size jadi 16
- Atau tunggu saja (normal untuk CPU)

### ❌ Aplikasi tidak muncul
**Solusi:**
1. Cek terminal, ada error?
2. Buka manual: http://localhost:8501
3. Restart: Ctrl+C, lalu run lagi

---

## 💡 Tips Sukses:

### Untuk Hasil Training Terbaik:
1. **Data Berkualitas** > Kuantitas
   - 20 foto bagus > 100 foto buruk
2. **Variasi Data**
   - Berbagai angle
   - Berbagai pencahayaan
   - Background berbeda
3. **Patience!**
   - Training butuh waktu
   - Jangan close saat training
   - Lihat grafik untuk monitoring

### Untuk Pembelajaran Optimal:
1. **Eksperimen!**
   - Coba epoch berbeda
   - Coba learning rate berbeda
   - Lihat perbedaannya
2. **Catat Hasil**
   - Screenshot grafik
   - Bandingkan antar training
3. **Diskusi**
   - Diskusikan dengan teman
   - Kenapa AI salah klasifikasi?
   - Bagaimana improve?

---

## 🎯 Checklist Pemula

Sebelum mulai training, pastikan:
- [ ] Sudah install dependencies
- [ ] Punya minimal 50 foto
- [ ] Foto berkualitas bagus
- [ ] Sudah baca penjelasan epoch & learning rate
- [ ] Punya waktu 15-30 menit

---

## 📞 Butuh Bantuan?

1. Baca **README.md** untuk detail lengkap
2. Baca **ARCHITECTURE.md** untuk penjelasan teknis
3. Check **test_modules.py** untuk test semua modul
4. Lihat komentar di code (banyak penjelasan!)

---

## 🎉 Selamat Belajar!

**Remember:**
- 🧠 AI belajar dari data yang kamu beri
- 🔄 Practice makes perfect
- 🌍 Belajar AI sambil peduli lingkungan
- 🎯 Jangan takut eksperimen!

---

## ⚡ One-Liner Commands

Jalankan aplikasi:
```powershell
cd "d:\Materi KIR SMPITIK\app_pilahsampah" ; streamlit run app.py
```

Test semua modul:
```powershell
python test_modules.py
```

Install dependencies:
```powershell
pip install streamlit tensorflow keras pillow matplotlib plotly seaborn streamlit-option-menu
```

---

**Status Aplikasi:**
- ✅ Siap digunakan
- ✅ Sudah terintegrasi dengan kode existing
- ✅ UI Modern & Edukatif
- ✅ Real-time visualization
- ✅ Sistem rekomendasi lengkap
- ✅ Gamifikasi (AI Levels)

**Dibuat dengan ❤️ untuk pendidikan siswa SMP**

---

🚀 **HAPPY LEARNING & CODING!** 🌍
