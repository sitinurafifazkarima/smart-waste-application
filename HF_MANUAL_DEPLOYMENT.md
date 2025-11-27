# 🚀 CARA DEPLOY KE HUGGING FACE - MANUAL METHOD

## ⚠️ Problem: Files tab tidak muncul di Space Settings

Jika Anda tidak menemukan opsi "Import from GitHub" di Hugging Face Space, gunakan method ini:

---

## 📋 LANGKAH DEPLOYMENT MANUAL

### Step 1: Create Hugging Face Space (Baru/Kosong)

1. **Login ke Hugging Face**
   - URL: https://huggingface.co/
   
2. **Create New Space**
   - Klik profile → **New Space**
   - Space name: `smart-waste-classifier`
   - License: MIT
   - **Space SDK: Docker** ← PENTING!
   - Space hardware: CPU basic (FREE)
   - Visibility: Public
   - Klik **Create Space**

3. **Anda akan dibawa ke Space yang baru dibuat**
   - URL: `https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier`

### Step 2: Clone HF Space Repository ke Local

Di terminal/PowerShell:

```powershell
# Navigate ke parent folder
cd "D:\Materi KIR SMPITIK"

# Clone HF Space (akan create folder baru)
git clone https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier hf_space

# Masuk ke folder
cd hf_space
```

**Note:** Replace `sitinurafifazkarima` dengan username Hugging Face Anda yang sebenarnya.

### Step 3: Copy Project Files dari GitHub Project

```powershell
# Copy semua files dari project ke HF space folder
Copy-Item "D:\Materi KIR SMPITIK\app_pilahsampah_ver3\*" -Destination "D:\Materi KIR SMPITIK\hf_space" -Recurse -Force -Exclude @('.git', 'venv', '__pycache__', 'backend')

# Verify files copied
ls "D:\Materi KIR SMPITIK\hf_space"
```

Files yang HARUS ada:
- ✅ `app_hf.py`
- ✅ `Dockerfile`
- ✅ `README.md` (dengan metadata header)
- ✅ `requirements_hf.txt`
- ✅ `model/keras_model.h5` (via Git LFS)
- ✅ `model/labels.txt`
- ✅ `modules/` folder
- ✅ `frontend/` folder
- ✅ `.gitattributes` (untuk Git LFS)

### Step 4: Setup Git LFS di HF Space

```powershell
cd "D:\Materi KIR SMPITIK\hf_space"

# Install Git LFS (jika belum)
git lfs install

# Track model files
git lfs track "*.h5"
git lfs track "model/*.h5"

# Add gitattributes
git add .gitattributes
```

### Step 5: Add & Commit Files

```powershell
# Add all files
git add .

# Commit
git commit -m "Initial deployment to Hugging Face Spaces"

# Check status
git status
```

### Step 6: Push ke Hugging Face

```powershell
# Push ke HF
git push origin main

# atau jika branch-nya master:
git push origin master
```

**Authentication:**
- Username: Hugging Face username Anda
- Password: **Hugging Face Access Token** (BUKAN password biasa!)

**Cara buat Access Token:**
1. Hugging Face → Settings → Access Tokens
2. New token → Name: "deployment" → Role: write
3. Copy token → Paste saat diminta password

### Step 7: Wait for Build

1. Buka HF Space: `https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier`
2. Anda akan lihat **"Building..."** status
3. Tunggu 10-15 menit untuk:
   - Clone repository
   - Download LFS files (model 312MB)
   - Build Docker image
   - Start container

4. Status akan berubah menjadi **"Running"**
5. App accessible di URL space!

---

## 🔧 ALTERNATIVE METHOD - Copy Files Manual via Web UI

Jika git push gagal, upload files manual via web:

### Via Hugging Face Web Interface:

1. **Buka Space Anda**
   - https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier

2. **Klik "Files" tab**

3. **Upload files satu per satu:**
   - README.md (copy content dari README_HF.md)
   - Dockerfile (copy dari Dockerfile_HF)
   - requirements.txt (copy dari requirements_hf.txt)
   - app_hf.py

4. **Create folders dan upload:**
   - `model/` folder:
     - Upload `labels.txt` (small)
     - Upload `keras_model.h5` (large, via Git LFS)
   
   - `modules/` folder:
     - Upload semua .py files
   
   - `frontend/` folder:
     - Upload `templates/index.html`
     - Upload `static/css/style.css`
     - Upload `static/js/app.js`

5. **Commit changes** setiap kali upload

---

## 🎯 SIMPLIFIED METHOD - Tanpa Model (Rebuild di Server)

Jika upload model 312MB terlalu lama, deploy dulu tanpa model:

### Step 1: Deploy Tanpa Model

Upload semua files KECUALI `model/keras_model.h5`

### Step 2: Rebuild Model di Server

Setelah app running, akses Shell via Hugging Face:

```bash
# Di HF Space → Settings → Container → Open Shell

cd /app

# Install dependencies jika belum
pip install tensorflow keras pillow numpy

# Download model dari Google Drive atau rebuild
# Option A: Download dari Google Drive
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID' -O model/keras_model.h5

# Option B: Rebuild dari dataset
python -c "
from modules.trainer import ModelTrainer
trainer = ModelTrainer('./dataset_private/processed', './model/keras_model.h5')
trainer.train(epochs=20)
"
```

---

## ✅ VERIFY DEPLOYMENT

### Test Endpoints:

```bash
# Health check
curl https://sitinurafifazkarima-smart-waste-classifier.hf.space/health

# API status
curl https://sitinurafifazkarima-smart-waste-classifier.hf.space/api/status

# Categories
curl https://sitinurafifazkarima-smart-waste-classifier.hf.space/api/categories
```

### Test via Browser:

```
https://sitinurafifazkarima-smart-waste-classifier.hf.space
```

Anda akan lihat frontend UI dengan 5 pages:
- 🏠 Home
- 🔍 Classify
- 📤 Upload Data
- 🧠 Train Model
- 📚 Education

---

## 🆘 TROUBLESHOOTING

### Error: "Authentication failed"

**Solution:**
```powershell
# Use Access Token instead of password
# Get token: https://huggingface.co/settings/tokens

# Configure git credential helper
git config credential.helper store

# Re-push
git push origin main
```

### Error: "Large file detected"

**Solution:**
```powershell
# Pastikan Git LFS terinstall
git lfs install

# Re-track files
git lfs track "*.h5"
git add .gitattributes
git add model/keras_model.h5
git commit --amend --no-edit
git push origin main --force
```

### Error: "Build failed - Out of memory"

**Solution:**
- Edit `requirements_hf.txt`:
  ```
  # Gunakan tensorflow-cpu bukan tensorflow
  tensorflow-cpu==2.15.0
  ```
- Commit dan push ulang

### Error: "Container failed to start"

**Solution:**
1. Check logs di HF Space → Logs tab
2. Verify Dockerfile syntax
3. Test locally:
   ```powershell
   docker build -t test -f Dockerfile .
   docker run -p 7860:7860 test
   ```

---

## 📊 DEPLOYMENT CHECKLIST

- [ ] Hugging Face account created
- [ ] New Space created (SDK: Docker)
- [ ] Access Token generated
- [ ] Git LFS installed locally
- [ ] HF Space repository cloned
- [ ] Files copied from GitHub project
- [ ] .gitattributes configured
- [ ] Model tracked with Git LFS
- [ ] Files committed
- [ ] Pushed to Hugging Face
- [ ] Build successful (check Logs)
- [ ] App running (status: Running)
- [ ] Public URL accessible
- [ ] API endpoints working
- [ ] Frontend UI displaying

---

## 🎉 SUCCESS!

**Your App is Live:**
```
https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier
```

**Short URL:**
```
https://sitinurafifazkarima-smart-waste-classifier.hf.space
```

**Embed Code:**
```html
<iframe
  src="https://sitinurafifazkarima-smart-waste-classifier.hf.space"
  frameborder="0"
  width="850"
  height="450"
></iframe>
```

---

## 🔄 UPDATE DEPLOYMENT

Untuk update aplikasi setelah changes:

```powershell
cd "D:\Materi KIR SMPITIK\hf_space"

# Pull latest (if any changes from HF)
git pull origin main

# Copy updated files dari project
Copy-Item "D:\Materi KIR SMPITIK\app_pilahsampah_ver3\app_hf.py" -Force

# Commit and push
git add .
git commit -m "Update: [description]"
git push origin main

# HF auto-rebuild (5-10 min)
```

---

**Ikuti step-by-step ini dan aplikasi Anda akan live di Hugging Face!** 🚀
