# 🔧 TROUBLESHOOTING GUIDE - Smart Waste Classifier

## 📋 Daftar Masalah & Solusi

---

## 🚨 INSTALLATION ISSUES

### ❌ Error: "Python tidak ditemukan" / "python is not recognized"

**Penyebab:** Python belum terinstall atau tidak ada di PATH

**Solusi:**
1. Download Python dari: https://www.python.org/downloads/
2. Saat install, **CENTANG** "Add Python to PATH"
3. Restart terminal/PC
4. Test: `python --version`

---

### ❌ Error: "pip tidak ditemukan" / "pip is not recognized"

**Penyebab:** pip belum terinstall atau tidak di PATH

**Solusi:**
```powershell
# Download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Install pip
python get-pip.py

# Verify
pip --version
```

---

### ❌ Error saat `pip install -r requirements.txt`

**Penyebab:** Berbagai kemungkinan (network, permissions, dll)

**Solusi:**

**A. Network Issue:**
```powershell
# Gunakan mirror/proxy berbeda
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

**B. Permission Issue:**
```powershell
# Install untuk user saja (tanpa admin)
pip install -r requirements.txt --user
```

**C. Conflict Issue:**
```powershell
# Install satu per satu
pip install streamlit
pip install tensorflow
pip install pillow
# ... dst
```

**D. Outdated pip:**
```powershell
# Update pip dulu
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### ❌ Error: "Could not install TensorFlow"

**Penyebab:** TensorFlow butuh Python versi spesifik atau environment tertentu

**Solusi:**

**A. Cek Python version:**
```powershell
python --version
# TensorFlow 2.13+ butuh Python 3.8-3.11
```

**B. Install TensorFlow CPU version (lebih ringan):**
```powershell
pip install tensorflow-cpu
```

**C. Gunakan virtual environment:**
```powershell
# Buat venv
python -m venv venv

# Activate
.\venv\Scripts\activate

# Install
pip install -r requirements.txt
```

---

## 🚨 RUNTIME ISSUES

### ❌ Error: "streamlit: command not found"

**Penyebab:** Streamlit belum terinstall atau tidak di PATH

**Solusi:**
```powershell
# Install streamlit
pip install streamlit

# Atau jalankan langsung dengan python
python -m streamlit run app.py
```

---

### ❌ Error: "Model tidak ditemukan" / "keras_model.h5 not found"

**Penyebab:** Model belum di-training atau file hilang

**Solusi:**
1. Pastikan `keras_model.h5` ada di folder aplikasi
2. Atau lakukan training baru di menu "🧠 Training"
3. Tunggu hingga training selesai
4. Model akan auto-saved

---

### ❌ Error: "Dataset belum cukup untuk training"

**Penyebab:** Jumlah gambar kurang dari minimal requirement

**Solusi:**
1. Buka menu "📸 Tambah Data"
2. Upload minimal **10 gambar per kategori**
3. Total minimal: **50 gambar**
4. Cek di "Dataset Saat Ini" apakah sudah cukup

---

### ❌ Error: "No module named 'xxx'"

**Penyebab:** Module belum terinstall

**Solusi:**
```powershell
# Install module yang kurang
pip install [nama-module]

# Contoh:
pip install streamlit-option-menu
pip install plotly
```

---

### ❌ Training sangat lambat / stuck

**Penyebab:** Dataset besar, CPU lemah, atau parameter tidak optimal

**Solusi:**

**A. Kurangi kompleksitas:**
- Epochs: 10-20 (bukan 50+)
- Batch size: 8 atau 16 (bukan 32)

**B. Kurangi data:**
- Gunakan 20-30 gambar per kategori dulu untuk testing

**C. Close aplikasi lain:**
- Free up RAM & CPU

**D. Bersabar:**
- Training memang butuh waktu (5-30 menit normal)
- Jangan close aplikasi saat training!

**E. Monitor di terminal:**
- Lihat apakah ada error di terminal
- Cek CPU usage di Task Manager

---

### ❌ Training error: "Out of Memory" (OOM)

**Penyebab:** RAM tidak cukup

**Solusi:**
```powershell
# 1. Kurangi batch size
#    Di app: Set batch size = 8 (bukan 32)

# 2. Close aplikasi lain

# 3. Restart PC untuk free memory

# 4. Kalau masih error, kurangi data:
#    - 15-20 gambar per kategori cukup
```

---

### ❌ Aplikasi tidak muncul di browser

**Penyebab:** Port conflict, browser issue, atau network issue

**Solusi:**

**A. Buka manual:**
```
http://localhost:8501
```

**B. Gunakan IP address:**
```
http://127.0.0.1:8501
```

**C. Cek terminal - ada error?**
- Read error message
- Google error tersebut

**D. Port conflict - gunakan port lain:**
```powershell
streamlit run app.py --server.port 8502
```

**E. Clear browser cache:**
- Ctrl + Shift + Delete
- Clear cache & cookies

---

### ❌ Gambar tidak ter-upload

**Penyebab:** Format file salah, ukuran terlalu besar, atau permission issue

**Solusi:**

**A. Cek format file:**
- Hanya support: JPG, JPEG, PNG
- Rename file jika perlu

**B. Cek ukuran file:**
- Maksimal ~10MB per file
- Compress image jika terlalu besar

**C. Permission issue:**
- Run as Administrator
- Atau ubah permission folder dataset

---

### ❌ Error: "Unable to load image"

**Penyebab:** File corrupt, format tidak didukung

**Solusi:**
1. Buka file di image viewer dulu (cek corrupt atau tidak)
2. Convert ke JPG dengan tools lain
3. Re-upload

---

### ❌ Prediksi selalu salah / random

**Penyebab:** Model belum trained cukup atau data kurang bagus

**Solusi:**

**A. Re-training dengan data lebih banyak:**
- Minimal 20-30 gambar per kategori
- Foto berkualitas bagus

**B. Training lebih lama:**
- Tambah epochs (30-50)

**C. Cek data quality:**
- Apakah foto jelas?
- Apakah label benar?
- Apakah ada foto salah kategori?

**D. Data lebih variatif:**
- Berbagai angle
- Berbagai lighting
- Berbagai background

---

## 🚨 UI/UX ISSUES

### ❌ UI terlihat rusak / berantakan

**Penyebab:** Browser tidak support atau cache issue

**Solusi:**
1. **Clear browser cache:** Ctrl + Shift + Delete
2. **Gunakan browser modern:**
   - Chrome (recommended)
   - Firefox
   - Edge
3. **Reload:** Ctrl + F5 (hard reload)
4. **Zoom:** Pastikan zoom browser = 100%

---

### ❌ Chart tidak muncul / error

**Penyebab:** Plotly belum terinstall atau JavaScript issue

**Solusi:**
```powershell
# Install/reinstall plotly
pip install --upgrade plotly

# Restart aplikasi
```

---

### ❌ Progress bar tidak update

**Penyebab:** Browser cache atau streaming issue

**Solusi:**
1. Reload page (F5)
2. Clear cache
3. Wait - kadang delay beberapa detik normal

---

## 🚨 PERFORMANCE ISSUES

### ❌ Aplikasi lemot / lag

**Penyebab:** Resource terbatas atau terlalu banyak data

**Solusi:**

**A. Restart aplikasi:**
- Ctrl + C di terminal
- Run lagi

**B. Restart PC:**
- Free up memory

**C. Kurangi data:**
- Jangan terlalu banyak gambar (50-100 cukup untuk learning)

**D. Close browser tabs lain:**
- Free up RAM

---

### ❌ Training terlalu lama (>30 menit)

**Penyebab:** Data terlalu banyak atau parameter tidak optimal

**Solusi:**
1. **Stop training:** Ctrl + C (kalau perlu)
2. **Kurangi epochs:** 10-20 cukup
3. **Kurangi data:** 100-200 total gambar cukup
4. **Batch size kecil:** 8 atau 16

---

## 🚨 DATA ISSUES

### ❌ Dataset statistics tidak update

**Penyebab:** Perlu reload atau cache

**Solusi:**
1. Reload page (F5)
2. Restart aplikasi jika perlu
3. Cek folder `dataset/raw/` manual - ada gambar?

---

### ❌ Gambar hilang dari dataset

**Penyebab:** Terhapus atau dipindah

**Solusi:**
1. Cek Recycle Bin
2. Re-upload gambar
3. Check permission folder

---

### ❌ Dataset split error

**Penyebab:** Gambar kurang atau folder permission

**Solusi:**
1. Pastikan minimal 10 gambar per kategori
2. Check folder permission
3. Run as Administrator

---

## 🚨 ADVANCED TROUBLESHOOTING

### 🔍 Debug Mode

Jalankan dengan debug info:
```powershell
streamlit run app.py --logger.level=debug
```

### 🔍 Check Module Import

Test manual:
```powershell
python -c "import streamlit; import tensorflow; import PIL; print('All OK!')"
```

### 🔍 Check Dataset

Test data manager:
```powershell
python test_modules.py
```

### 🔍 Check File Paths

```python
# Di Python terminal
import os
print(os.path.exists("keras_model.h5"))  # Should be True
print(os.path.exists("dataset/raw/"))    # Should be True
```

### 🔍 Check Port Availability

```powershell
# Cek port 8501 digunakan atau tidak
netstat -ano | findstr :8501

# Kill process jika perlu (ganti PID)
taskkill /PID [PID] /F
```

---

## 💡 TIPS PREVENTIF

### ✅ Best Practices untuk Menghindari Error:

1. **Install Python 3.8-3.11** (bukan 3.12+ atau <3.8)
2. **Gunakan virtual environment**
3. **Install semua dependencies sebelum run**
4. **Pastikan minimal 4GB RAM free**
5. **Close aplikasi berat lain saat training**
6. **Backup dataset regular**
7. **Jangan close aplikasi saat training**
8. **Gunakan Chrome/Firefox (bukan IE)**
9. **Data berkualitas > kuantitas**
10. **Update dependencies regular**

---

## 📞 Masih Error?

### Langkah Diagnosis:

1. **Baca error message lengkap**
   - Screenshot error
   - Google error message

2. **Cek terminal output**
   - Biasanya ada info detail di sini

3. **Test module individual**
   ```powershell
   python test_modules.py
   ```

4. **Fresh start**
   - Delete venv (kalau ada)
   - Re-install semua dependencies
   - Restart PC

5. **Check environment**
   - Python version: `python --version`
   - Pip version: `pip --version`
   - Streamlit version: `streamlit --version`

---

## 🆘 Emergency Reset

Kalau semua gagal, nuclear option:

```powershell
# 1. Backup data penting (dataset)
# 2. Delete semua kecuali:
#    - dataset/raw/
#    - labels.txt
#    - keras_model.h5 (kalau ada)

# 3. Download ulang aplikasi
# 4. Install fresh
pip install -r requirements.txt

# 5. Test
python test_modules.py

# 6. Run
streamlit run app.py
```

---

## 📚 Resources Tambahan

### Documentation:
- Streamlit: https://docs.streamlit.io/
- TensorFlow: https://www.tensorflow.org/
- Keras: https://keras.io/

### Community:
- Stack Overflow: Tag `streamlit`, `tensorflow`
- GitHub Issues: Report bugs

### Learning:
- Python basics: https://www.python.org/about/gettingstarted/
- ML basics: https://www.coursera.org/learn/machine-learning

---

**💡 Pro Tip:** Sebagian besar error bisa solved dengan:
1. Read error message carefully
2. Google error message
3. Restart aplikasi/PC
4. Re-install dependencies

**🎯 90% masalah adalah:**
- Dependencies belum install
- Python version salah
- Data kurang
- RAM/CPU terbatas

**Jangan menyerah! Debugging adalah bagian dari pembelajaran! 💪**
