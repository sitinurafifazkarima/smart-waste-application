# 📦 INSTRUKSI DEPLOYMENT MODEL FILE

## ⚠️ PENTING: Model File Tidak Ada di Git

File `keras_model.h5` (297.80 MB) terlalu besar untuk GitHub dan **TIDAK ter-upload** ke repository.

Anda perlu upload manual ke server production.

---

## 🎯 LOKASI MODEL FILE

**Local Computer:**
```
D:\Materi KIR SMPITIK\app_pilahsampah_ver3\backend\model\keras_model.h5
```

**Production Server Path:**
```
/opt/render/project/src/backend/model/keras_model.h5
```

---

## 🚀 CARA UPLOAD MODEL KE PRODUCTION

### **Option 1: Upload via Render Dashboard (RECOMMENDED)**

1. **Login ke Render Dashboard**
   - URL: https://dashboard.render.com
   - Pilih service: `smart-waste-application`

2. **Buka Shell Tab**
   - Klik service → **Shell** tab
   - Tunggu shell terbuka

3. **Upload via SCP/SFTP**
   ```bash
   # Di local computer PowerShell:
   scp "D:\Materi KIR SMPITIK\app_pilahsampah_ver3\backend\model\keras_model.h5" \
       [render-username]@[render-host]:/opt/render/project/src/backend/model/
   ```

4. **Atau Upload via Web Interface**
   - Render Dashboard → Service → Settings
   - Environment → **Persistent Disks**
   - Upload file ke persistent storage

### **Option 2: Download dari Cloud Storage**

Upload model ke Google Drive/Dropbox dulu, lalu download di server:

```bash
# 1. Upload keras_model.h5 ke Google Drive
# 2. Get shareable link (contoh: https://drive.google.com/file/d/FILE_ID/view)
# 3. Di Render Shell:

cd /opt/render/project/src/backend/model/
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=FILE_ID' -O keras_model.h5
```

### **Option 3: Git LFS (Alternative)**

Jika ingin model ter-version di git:

```powershell
# Di local computer:
cd "D:\Materi KIR SMPITIK\app_pilahsampah_ver3"

# Install Git LFS
git lfs install

# Track model files
git lfs track "*.h5"
git lfs track "backend/model/*.h5"

# Add lfs config
git add .gitattributes

# Add model back to git
git add backend/model/keras_model.h5

# Commit and push
git commit -m "Add model with Git LFS"
git push origin main
```

**Note:** Git LFS memiliki bandwidth limit di GitHub Free tier (1GB/month).

### **Option 4: Rebuild Model di Production**

Jika punya dataset training, rebuild model di server:

```bash
# Di Render Shell:
cd /opt/render/project/src

# Run training script
python -c "
from modules.trainer import ModelTrainer
trainer = ModelTrainer('./backend/dataset_private/processed', './backend/model/keras_model.h5')
trainer.train(epochs=20)
"
```

---

## ✅ VERIFY MODEL UPLOADED

Setelah upload, cek apakah file ada:

```bash
# Di Render Shell:
ls -lh /opt/render/project/src/backend/model/

# Output harus menunjukkan:
# keras_model.h5  (sekitar 298M)
# labels.txt      (sekitar 46 bytes)
```

Test API:

```bash
curl https://smart-waste-application.onrender.com/api/status
```

Output harus menunjukkan:
```json
{
  "status": "online",
  "model_loaded": true,
  "model_ready": true
}
```

---

## 🔧 TROUBLESHOOTING

### Model Not Found Error

```
FileNotFoundError: Model tidak ditemukan
```

**Solusi:**
1. Cek path: `ls -la /opt/render/project/src/backend/model/`
2. Pastikan file permission: `chmod 644 keras_model.h5`
3. Restart service di Render Dashboard

### Model Loading Timeout

```
Error: Model loading exceeded timeout
```

**Solusi:**
- Upgrade ke Render Starter plan (512 MB RAM)
- Model 298MB butuh minimum 512MB RAM untuk load

### Disk Space Full

```
Error: No space left on device
```

**Solusi:**
- Render Free tier: 512MB disk space
- Upgrade ke Starter plan: 20GB disk space
- Atau gunakan Persistent Disk (add-on)

---

## 📊 FILE SIZES

```
keras_model.h5:  297.80 MB  (312,262,400 bytes)
labels.txt:      46 bytes
Total:           ~298 MB
```

**Minimum Requirements:**
- RAM: 512 MB (untuk load model + TensorFlow)
- Disk: 500 MB (untuk model + dependencies)
- Bandwidth: 300 MB upload (one-time)

---

## 🎯 NEXT STEPS DEPLOYMENT

1. ✅ **Code di GitHub**: https://github.com/sitinurafifazkarima/smart-waste-application
2. ⏳ **Deploy ke Render**: Create Web Service dari GitHub repo
3. ⏳ **Upload Model**: Gunakan salah satu option di atas
4. ⏳ **Test Production**: Verify model loaded dan API works
5. ✅ **Go Live**: Share public URL!

---

## 📞 SUPPORT

Jika kesulitan upload model, alternatif:
1. Deploy tanpa model dulu (training mode)
2. Upload dataset via API `/api/upload-training`
3. Train model langsung di production via `/api/train`

Model akan ter-generate otomatis di server.

---

**Status: Model file siap di local, waiting untuk production upload** 📦
