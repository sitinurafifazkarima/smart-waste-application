# 🚀 QUICKSTART GUIDE
# Smart Waste Classifier v3.0 - Flask Version

**Panduan cepat untuk menjalankan aplikasi di local development**

---

## ⚡ QUICK START (5 Menit)

### 1. Install Dependencies

```powershell
# Pastikan Python 3.11 terinstall
python --version

# Install dependencies
pip install -r requirements_deploy.txt
```

### 2. Copy Model (Jika Ada)

```powershell
# Copy model yang sudah dilatih
Copy-Item keras_model.h5 backend\model\
Copy-Item labels.txt backend\model\
```

Jika belum punya model, bisa training nanti via UI.

### 3. Run Flask App

```powershell
# Method 1: Direct Python
cd backend
python app.py

# Method 2: Via Gunicorn (production-like)
gunicorn --chdir backend app:app --bind 127.0.0.1:5000
```

### 4. Open Browser

```
http://localhost:5000
```

---

## 🎯 TESTING CHECKLIST

### ✅ Backend Health Check

Open: `http://localhost:5000/health`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-27T...",
  "model_loaded": true,
  "training_in_progress": false
}
```

### ✅ System Status

Open: `http://localhost:5000/api/status`

Should return dataset info, model status, etc.

### ✅ Frontend Pages

Navigate through all pages:
- 🏠 Home - Check statistics
- 📸 Upload - Add training data
- 🧠 Training - Test training UI
- 🔍 Classify - Test classification
- 📚 Education - Check educational content

---

## 📊 SAMPLE WORKFLOW

### 1. Add Training Data

1. Go to **Upload** page
2. Upload beberapa gambar sampah
3. Pilih kategori yang sesuai
4. Check dataset statistics

### 2. Train Model

1. Go to **Training** page
2. Set parameters:
   - Epochs: 10 (untuk testing cepat)
   - Learning Rate: 0.001
   - Batch Size: 32
3. Click **Mulai Training**
4. Watch progress bar
5. Wait until complete (~5-10 menit tergantung data)

### 3. Test Classification

1. Go to **Classify** page
2. Upload gambar sampah
3. Click **Klasifikasikan**
4. Check results:
   - Predicted class
   - Confidence score
   - Recommendations
   - Educational facts

---

## 🔧 DEVELOPMENT MODE

### Hot Reload (Auto-restart on code changes):

```powershell
# Set environment variable
$env:FLASK_ENV = "development"

# Run Flask
cd backend
python app.py
```

### Debug Mode:

In `backend/app.py`, change:
```python
app.run(
    host='0.0.0.0',
    port=5000,
    debug=True  # Enable debug mode
)
```

---

## 📁 FOLDER STRUCTURE CHECK

Pastikan folder-folder ini ada:

```
app_pilahsampah_ver3/
├── backend/
│   ├── app.py ✅
│   ├── model/
│   │   └── .gitkeep ✅
│   ├── dataset_private/
│   │   ├── raw/ ✅
│   │   └── processed/ ✅
│   ├── uploads_temp/ ✅
│   └── training_logs/ ✅
├── frontend/
│   ├── templates/
│   │   └── index.html ✅
│   └── static/
│       ├── css/style.css ✅
│       └── js/app.js ✅
└── modules/
    ├── classifier.py ✅
    ├── data_manager.py ✅
    ├── trainer.py ✅
    └── recommender.py ✅
```

---

## 🐛 TROUBLESHOOTING

### Issue: "ModuleNotFoundError"
```powershell
# Install missing module
pip install [module-name]

# Or reinstall all
pip install -r requirements_deploy.txt
```

### Issue: "Port already in use"
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Or use different port
python backend/app.py --port 5001
```

### Issue: "Model not found"
```
Solution: Upload keras_model.h5 dan labels.txt ke backend/model/
Atau lakukan training baru via UI
```

### Issue: "Dataset error"
```powershell
# Check folder permissions
# Pastikan folder dataset_private/raw/ bisa di-write
```

---

## 📊 API TESTING (curl / Postman)

### Health Check
```powershell
curl http://localhost:5000/health
```

### System Status
```powershell
curl http://localhost:5000/api/status
```

### Upload Training Data
```powershell
curl -X POST `
  -F "file=@path\to\image.jpg" `
  -F "category=plastic" `
  http://localhost:5000/api/upload-training
```

### Classify Image
```powershell
curl -X POST `
  -F "file=@path\to\sample.jpg" `
  http://localhost:5000/api/predict
```

### Start Training
```powershell
curl -X POST `
  -H "Content-Type: application/json" `
  -d '{\"epochs\":10,\"learning_rate\":0.001,\"batch_size\":32}' `
  http://localhost:5000/api/train
```

### Training Status
```powershell
curl http://localhost:5000/api/training-status
```

---

## 🎨 FRONTEND DEVELOPMENT

### Modify CSS:
Edit `frontend/static/css/style.css`

### Modify JavaScript:
Edit `frontend/static/js/app.js`

### Modify HTML:
Edit `frontend/templates/index.html`

**Note:** Refresh browser untuk melihat perubahan (Ctrl+F5 untuk hard refresh)

---

## 🧪 SAMPLE DATA

### Test Images:

Download sample images dari:
```
dataset/raw/cardboard/
dataset/raw/glass/
dataset/raw/metal/
dataset/raw/paper/
dataset/raw/plastic/
```

Atau ambil dari internet:
- Cardboard: foto kardus, karton
- Glass: foto botol kaca, gelas
- Metal: foto kaleng, aluminium
- Paper: foto kertas, koran
- Plastic: foto botol plastik, kantong

---

## 📝 DEVELOPMENT TIPS

### 1. Use Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements_deploy.txt
```

### 2. Keep Browser Console Open
Press F12 to see JavaScript errors/logs

### 3. Monitor Flask Logs
Check terminal untuk error messages

### 4. Test API First
Before testing UI, pastikan API endpoints berfungsi dengan curl/Postman

---

## 🚀 NEXT STEPS

Setelah testing lokal sukses:

1. ✅ Commit code ke Git
2. ✅ Push ke GitHub
3. ✅ Deploy ke platform pilihan (Render/Railway/VPS)
4. ✅ Lihat **README_DEPLOY.md** untuk panduan deployment

---

## 💡 USEFUL COMMANDS

### Check Python packages:
```powershell
pip list
```

### Update packages:
```powershell
pip install --upgrade -r requirements_deploy.txt
```

### Generate requirements:
```powershell
pip freeze > requirements_current.txt
```

### Clear Python cache:
```powershell
# Windows
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Force -Recurse
```

---

**Happy Coding! 🎉**

Jika ada masalah, check:
1. TROUBLESHOOTING.md
2. ARCHITECTURE.md
3. README_DEPLOY.md
