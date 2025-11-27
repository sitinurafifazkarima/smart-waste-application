# 🚀 PANDUAN DEPLOYMENT - SMART WASTE CLASSIFIER

## ✅ Status Aplikasi
- **Framework**: Flask 3.0.0 + TensorFlow 2.15.0
- **Model**: keras_model.h5 (312 MB) - Sudah Tersedia ✅
- **Frontend**: HTML5/CSS3/JavaScript (Single Page Application)
- **Backend**: REST API dengan 8 endpoints
- **Git**: Repository sudah diinisialisasi ✅
- **Local Test**: BERHASIL - Server berjalan di http://localhost:5000 ✅

---

## 📋 PERSIAPAN DEPLOYMENT

### 1. Siapkan Platform Hosting

#### **Option A: Render.com (RECOMMENDED)**
1. Buat akun di https://render.com
2. Connect dengan GitHub repository
3. Buat **Web Service** baru
4. Pilih repository: `app_pilahsampah_ver3`
5. Konfigurasi otomatis dari `render.yaml`

**Settings:**
```yaml
Environment: Python 3.11
Build Command: pip install -r requirements_deploy.txt
Start Command: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
```

#### **Option B: Railway.app**
1. Buat akun di https://railway.app
2. New Project → Deploy from GitHub
3. Select Repository
4. Railway akan otomatis detect Python dan install dependencies
5. Environment variables akan diset otomatis

#### **Option C: Docker (VPS/Self-Hosted)**
```bash
# Build image
docker build -t smart-waste-classifier .

# Run container
docker run -d -p 8000:8000 smart-waste-classifier
```

---

## 🔧 KONFIGURASI GIT & GITHUB

### Push ke GitHub

```powershell
# 1. Buat repository baru di GitHub (tanpa README/gitignore)
# 2. Copy URL repository (contoh: https://github.com/username/smart-waste-classifier.git)

# 3. Add remote dan push
cd "D:\Materi KIR SMPITIK\app_pilahsampah_ver3"
git remote add origin https://github.com/username/smart-waste-classifier.git
git branch -M main
git push -u origin main
```

**CATATAN PENTING:**
- File `backend/model/keras_model.h5` (312MB) terlalu besar untuk GitHub
- Ada 2 opsi:
  1. **Git LFS** (Large File Storage): `git lfs track "*.h5"`
  2. **Upload manual** ke Render/Railway setelah deployment

---

## 🌍 LANGKAH DEPLOYMENT KE RENDER.COM

### Step 1: Push ke GitHub
```powershell
# Pastikan sudah push ke GitHub
git push origin main
```

### Step 2: Deploy di Render
1. Login ke https://render.com
2. Klik **New** → **Web Service**
3. Connect GitHub dan pilih repository
4. **Settings:**
   - Name: `smart-waste-classifier`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements_deploy.txt`
   - Start Command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
   - Instance Type: `Free` (atau `Starter` untuk performa lebih baik)

5. **Environment Variables:**
   ```
   PYTHON_VERSION=3.11.0
   PORT=10000
   ```

6. Klik **Create Web Service**

### Step 3: Upload Model (Jika Tidak Pakai Git LFS)
Jika model tidak ter-push karena file size:
1. Buka Render Dashboard
2. Pilih service yang baru dibuat
3. Buka **Shell** tab
4. Upload file `backend/model/keras_model.h5` manual via:
   ```bash
   # Download dari link alternatif atau upload via SFTP
   # Atau build model di server
   ```

### Step 4: Test Deployment
1. Tunggu build selesai (~5-10 menit)
2. Akses URL yang diberikan Render (contoh: https://smart-waste-classifier.onrender.com)
3. Test endpoints:
   - `GET /health` → Check server health
   - `GET /api/status` → Check API status
   - `POST /api/predict` → Test klasifikasi

---

## 📊 MONITORING & TROUBLESHOOTING

### Cek Logs
**Render:**
- Dashboard → Service → **Logs** tab
- Monitor real-time logs

**Railway:**
- Project → Service → **Deployments** → View Logs

### Common Issues

#### 1. **Build Timeout**
```
Error: Build exceeded time limit
```
**Solusi:** 
- Upgrade ke Render Starter plan ($7/month)
- Atau deploy ke Railway (lebih generous dengan resource)

#### 2. **Model Not Found**
```
Error: FileNotFoundError: keras_model.h5
```
**Solusi:**
```bash
# Pastikan model ada di path yang benar
ls backend/model/
# Output harus ada: keras_model.h5, labels.txt
```

#### 3. **Out of Memory**
```
Error: MemoryError during model loading
```
**Solusi:**
- Upgrade instance ke Render Starter (512MB RAM)
- Atau gunakan Railway Pro plan

#### 4. **TensorFlow Import Slow**
Ini normal! Lazy loading yang kita implement akan:
- Server start cepat (~5 detik)
- TensorFlow load saat request pertama (~20-30 detik)
- Request selanjutnya instant

---

## 🔒 KEAMANAN DATASET

Dataset di `backend/dataset_private/` **TIDAK akan ter-publish** karena sudah ada di `.gitignore`:

```gitignore
# Dataset private - jangan di-commit!
backend/dataset_private/*
!backend/dataset_private/.gitkeep
```

Hanya admin yang bisa upload data training via API endpoint `/api/upload-training`.

---

## 🎯 TESTING LOCAL SEBELUM DEPLOY

```powershell
# 1. Install dependencies
pip install -r requirements_deploy.txt

# 2. Run Flask
cd backend
python app.py

# 3. Test di browser
# Buka: http://localhost:5000

# 4. Test API dengan curl
curl http://localhost:5000/health
curl http://localhost:5000/api/status
```

---

## 📱 AKSES APLIKASI

Setelah deployment sukses:

### **Public URL** (contoh):
- Render: `https://smart-waste-classifier.onrender.com`
- Railway: `https://smart-waste-classifier.up.railway.app`

### **Fitur yang Tersedia:**
1. ✅ Homepage dengan info aplikasi
2. ✅ Upload & Klasifikasi gambar sampah
3. ✅ Upload dataset untuk training
4. ✅ Training model dengan parameter custom
5. ✅ Halaman edukasi pengelolaan sampah

---

## 🔄 UPDATE APLIKASI

Setiap kali ada perubahan:

```powershell
# 1. Commit changes
git add .
git commit -m "Update: deskripsi perubahan"

# 2. Push ke GitHub
git push origin main

# 3. Auto-deploy
# Render/Railway akan otomatis rebuild dan deploy
```

---

## 💰 ESTIMASI BIAYA

### Free Tier:
- **Render Free**: 750 jam/bulan (cukup untuk 1 service 24/7)
  - ⚠️ Server sleep setelah 15 menit tidak ada traffic
  - Cold start: 30-60 detik
  
- **Railway Free**: $5 credit/bulan (~100-500 jam tergantung usage)
  - No sleep
  - Cold start: 0 detik

### Paid Plans:
- **Render Starter**: $7/month
  - 512 MB RAM
  - No sleep
  - Lebih cocok untuk TensorFlow

- **Railway Pro**: $20/month credit
  - Pay per usage
  - Flexible scaling

---

## 📚 NEXT STEPS

1. ✅ **Local sudah berjalan** - Flask running di http://localhost:5000
2. ⏳ **Pending**: Push ke GitHub
3. ⏳ **Pending**: Deploy ke Render/Railway
4. ⏳ **Pending**: Test production URL
5. ⏳ **Pending**: Share public link

---

## 🆘 BUTUH BANTUAN?

Cek dokumentasi lengkap:
- `README_DEPLOY.md` - Deployment details
- `ARCHITECTURE.md` - Sistem architecture
- `QUICKSTART_FLASK.md` - Quick start guide
- `TROUBLESHOOTING.md` - Common problems & solutions

---

## ✅ CHECKLIST DEPLOYMENT

- [x] Git initialized
- [x] Dependencies installed
- [x] Model files copied to `backend/model/`
- [x] Local server tested (http://localhost:5000)
- [x] Git commit sukses
- [ ] GitHub repository created
- [ ] Pushed to GitHub
- [ ] Deployment platform selected
- [ ] Application deployed
- [ ] Production URL tested
- [ ] Public access confirmed

---

**🎉 Selamat! Aplikasi Anda siap di-deploy ke production!**
