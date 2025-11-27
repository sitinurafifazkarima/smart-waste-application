# 🚀 PANDUAN DEPLOYMENT
# Smart Waste Classifier - AI Pemilah Sampah

<div align="center">

![Smart Waste Classifier](https://img.shields.io/badge/Smart%20Waste%20Classifier-v3.0-green)
![Flask](https://img.shields.io/badge/Flask-3.0-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Python](https://img.shields.io/badge/Python-3.11-yellow)

**Aplikasi AI untuk Klasifikasi Sampah - Siap Deploy ke Production**

</div>

---

## 📋 DAFTAR ISI

1. [Arsitektur Deployment](#-arsitektur-deployment)
2. [Persiapan](#-persiapan)
3. [Deploy ke Render.com](#-deploy-ke-rendercom)
4. [Deploy ke Railway](#-deploy-ke-railway)
5. [Deploy ke Replit](#-deploy-ke-replit)
6. [Deploy ke VPS](#-deploy-ke-vps)
7. [Testing & Troubleshooting](#-testing--troubleshooting)
8. [Keamanan Dataset](#-keamanan-dataset)

---

## 🏗️ ARSITEKTUR DEPLOYMENT

```
┌─────────────────────────────────────────────────────────┐
│                  PUBLIC INTERNET                         │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         Users (Browser / Mobile)                │    │
│  └────────────────────────────────────────────────┘    │
│                         ↕                                │
│  ┌────────────────────────────────────────────────┐    │
│  │         Cloud Platform (Render/Railway)         │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │   Frontend (HTML/CSS/JS)                  │  │    │
│  │  │   - Static files served by Flask          │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                     ↕                            │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │   Flask API Backend                       │  │    │
│  │  │   - Gunicorn WSGI server                 │  │    │
│  │  │   - /api/* endpoints                     │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                     ↕                            │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │   Private Server-Side Components         │  │    │
│  │  │   - ML Model (keras_model.h5)           │  │    │
│  │  │   - Dataset (PRIVATE, tidak public)      │  │    │
│  │  │   - Training logs                         │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### ✅ Keunggulan Arsitektur:
- **Frontend & Backend terintegrasi** dalam satu aplikasi Flask
- **Dataset aman** di server, tidak bisa diakses public
- **API endpoints** terstruktur dengan baik
- **Scalable** - bisa ditambah worker sesuai kebutuhan
- **Responsive** - UI modern dan mobile-friendly

---

## 📦 PERSIAPAN

### 1. Struktur Folder Final

Pastikan struktur folder seperti ini:

```
app_pilahsampah_ver3/
├── backend/
│   ├── app.py                 # Flask application
│   ├── api/                   # (optional) API modules
│   ├── model/                 # Model storage
│   │   ├── .gitkeep
│   │   └── keras_model.h5     # Upload setelah training
│   ├── dataset_private/       # PRIVATE - tidak di git
│   │   ├── raw/
│   │   └── processed/
│   ├── uploads_temp/          # Temporary uploads
│   │   └── .gitkeep
│   └── training_logs/         # Training history
│       └── .gitkeep
├── frontend/
│   ├── templates/
│   │   └── index.html         # Main HTML
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── app.js
│       └── images/
├── modules/                   # Python modules
│   ├── __init__.py
│   ├── classifier.py
│   ├── data_manager.py
│   ├── trainer.py
│   └── recommender.py
├── utils/
│   ├── __init__.py
│   ├── image_processor.py
│   └── visualizer.py
├── requirements_deploy.txt    # Production dependencies
├── Procfile                   # Deployment commands
├── render.yaml               # Render.com config
├── Dockerfile                # Docker config
├── .gitignore
└── README_DEPLOY.md          # This file
```

### 2. Copy Model & Labels

Jika sudah ada model terlatih:

```powershell
# Copy dari root ke backend/model/
Copy-Item keras_model.h5 backend/model/
Copy-Item labels.txt backend/model/
```

### 3. Setup Git Repository

```powershell
# Initialize git (jika belum)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Smart Waste Classifier v3.0"

# Create GitHub repository (via GitHub website)
# Then push
git remote add origin https://github.com/USERNAME/smart-waste-classifier.git
git branch -M main
git push -u origin main
```

---

## 🌐 DEPLOY KE RENDER.COM

**Render.com** adalah platform deploy gratis yang mudah dan reliable.

### Langkah-langkah:

#### 1. Buat Akun Render
- Kunjungi [render.com](https://render.com)
- Sign up dengan GitHub account

#### 2. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Pilih repository: `smart-waste-classifier`

#### 3. Konfigurasi

```yaml
Name: smart-waste-classifier
Region: Singapore (atau terdekat)
Branch: main
Root Directory: (leave blank)
Runtime: Python 3
Build Command: pip install -r requirements_deploy.txt
Start Command: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
Instance Type: Free
```

#### 4. Environment Variables (Optional)

```
PYTHON_VERSION = 3.11.0
FLASK_ENV = production
```

#### 5. Deploy!

- Click **"Create Web Service"**
- Tunggu proses build (~5-10 menit)
- Setelah selesai, app accessible di: `https://smart-waste-classifier-xxxx.onrender.com`

#### 6. Upload Model (via Render Shell)

Setelah deploy sukses:

1. Go to **Shell** tab di Render dashboard
2. Upload `keras_model.h5` dan `labels.txt`:

```bash
# Via Render Shell atau SFTP
# Model akan otomatis dimuat saat restart
```

**Atau** bisa include model di git (jika ukuran < 100MB)

### ✅ Testing

Akses URL: `https://your-app.onrender.com`

- Home page harus muncul
- Check `/health` endpoint: `https://your-app.onrender.com/health`
- Check `/api/status`: `https://your-app.onrender.com/api/status`

---

## 🚂 DEPLOY KE RAILWAY

**Railway** adalah platform modern dengan free tier yang bagus.

### Langkah-langkah:

#### 1. Buat Akun Railway
- Kunjungi [railway.app](https://railway.app)
- Sign up dengan GitHub

#### 2. Deploy from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Pilih repository: `smart-waste-classifier`
4. Railway akan auto-detect Python

#### 3. Konfigurasi

Railway auto-detect `Procfile`, tapi bisa manual set:

**Settings → Start Command:**
```bash
gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

**Variables:**
```
PYTHON_VERSION = 3.11
FLASK_ENV = production
PORT = 5000
```

#### 4. Deploy

- Railway auto-deploy on git push
- URL: `https://smart-waste-classifier-production.up.railway.app`

#### 5. Upload Model

Via Railway CLI atau include in repo.

### ✅ Testing

Sama seperti Render - test all endpoints.

---

## 🔧 DEPLOY KE REPLIT

**Replit** cocok untuk prototyping dan demo cepat.

### Langkah-langkah:

#### 1. Create Repl

1. Buat account di [replit.com](https://replit.com)
2. Click **"+ Create Repl"**
3. Import from GitHub: `https://github.com/USERNAME/smart-waste-classifier`

#### 2. Setup

Replit akan detect Python. Pastikan:

**`.replit` file:**
```toml
run = "gunicorn --chdir backend app:app --bind 0.0.0.0:5000"
language = "python3"

[nix]
channel = "stable-23_05"

[deployment]
run = ["sh", "-c", "gunicorn --chdir backend app:app --bind 0.0.0.0:5000"]
```

#### 3. Install Dependencies

```bash
pip install -r requirements_deploy.txt
```

#### 4. Run

Click **"Run"** button. App akan jalan di Replit webview.

#### 5. Deploy (Optional)

Replit punya deployment berbayar untuk production.

### ✅ Testing

Test via Replit webview atau URL public.

---

## 🖥️ DEPLOY KE VPS

Deploy ke VPS memberikan kontrol penuh. Cocok untuk production serius.

### Prerequisites:

- VPS (DigitalOcean, AWS EC2, Linode, Vultr, etc.)
- Ubuntu 22.04 LTS
- Minimal 2GB RAM
- Domain name (optional)

### Langkah-langkah:

#### 1. Setup VPS

```bash
# SSH ke VPS
ssh root@your-vps-ip

# Update system
apt update && apt upgrade -y

# Install Python & tools
apt install python3.11 python3.11-venv python3-pip nginx git -y
```

#### 2. Clone Repository

```bash
# Create user (recommended)
adduser wasteapp
usermod -aG sudo wasteapp
su - wasteapp

# Clone repo
cd /home/wasteapp
git clone https://github.com/USERNAME/smart-waste-classifier.git
cd smart-waste-classifier
```

#### 3. Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_deploy.txt
```

#### 4. Upload Model

```bash
# Via SCP from local machine
scp keras_model.h5 wasteapp@your-vps-ip:/home/wasteapp/smart-waste-classifier/backend/model/
scp labels.txt wasteapp@your-vps-ip:/home/wasteapp/smart-waste-classifier/backend/model/
```

#### 5. Setup Gunicorn Service

Create `/etc/systemd/system/wasteapp.service`:

```ini
[Unit]
Description=Smart Waste Classifier
After=network.target

[Service]
User=wasteapp
Group=wasteapp
WorkingDirectory=/home/wasteapp/smart-waste-classifier
Environment="PATH=/home/wasteapp/smart-waste-classifier/venv/bin"
ExecStart=/home/wasteapp/smart-waste-classifier/venv/bin/gunicorn --chdir backend app:app --bind 127.0.0.1:5000 --timeout 120 --workers 2

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
sudo systemctl start wasteapp
sudo systemctl enable wasteapp
sudo systemctl status wasteapp
```

#### 6. Setup Nginx

Create `/etc/nginx/sites-available/wasteapp`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Atau IP address

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Upload size limit
        client_max_body_size 16M;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/wasteapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. Setup SSL (Optional tapi Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### ✅ Testing

Access: `http://your-domain.com` atau `http://your-vps-ip`

---

## 🧪 TESTING & TROUBLESHOOTING

### Testing Checklist:

#### ✅ Backend Health Check

```bash
# Test health endpoint
curl https://your-app.com/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-11-27T...",
  "model_loaded": true,
  "training_in_progress": false
}
```

#### ✅ System Status

```bash
curl https://your-app.com/api/status

# Should return dataset info, model status, etc.
```

#### ✅ Upload Test

```bash
# Test file upload
curl -X POST \
  -F "file=@test_image.jpg" \
  -F "category=plastic" \
  https://your-app.com/api/upload-training
```

#### ✅ Classification Test

```bash
curl -X POST \
  -F "file=@sample.jpg" \
  https://your-app.com/api/predict
```

### Common Issues:

#### ❌ Issue: "Model not found"
**Solution:**
- Upload `keras_model.h5` dan `labels.txt` ke `backend/model/`
- Restart application

#### ❌ Issue: "Memory error saat training"
**Solution:**
- Upgrade ke paid plan (minimal 2GB RAM)
- Reduce batch size
- Reduce image size

#### ❌ Issue: "Slow response"
**Solution:**
- Increase gunicorn workers
- Add Redis cache
- Optimize model size

#### ❌ Issue: "File upload gagal"
**Solution:**
- Check `MAX_CONTENT_LENGTH` di Flask config
- Check Nginx `client_max_body_size`
- Validate file format

### Logs:

#### Render/Railway:
Check **Logs** tab di dashboard

#### VPS:
```bash
# Application logs
sudo journalctl -u wasteapp -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

---

## 🔐 KEAMANAN DATASET

### ✅ Dataset Protection:

1. **Folder `backend/dataset_private/` TIDAK di-commit ke git**
   ```
   # .gitignore contains:
   backend/dataset_private/raw/*
   backend/dataset_private/processed/*
   ```

2. **Tidak ada routing Flask ke folder dataset**
   ```python
   # Flask app.py TIDAK punya route seperti:
   # @app.route('/dataset/<path:filename>')  # ❌ JANGAN!
   ```

3. **Dataset hanya diakses dari backend Python**
   ```python
   # Backend internal access only
   data_manager = DataManager(str(RAW_DATA_DIR), ...)
   ```

4. **Upload validation ketat**
   ```python
   # File type check
   allowed_file(filename)  # Only jpg, jpeg, png
   ```

### 🚨 Security Best Practices:

1. **Environment Variables** untuk sensitive data
2. **HTTPS** wajib untuk production
3. **Rate limiting** untuk prevent abuse
4. **Input validation** untuk semua uploads
5. **CORS** hanya dari trusted domains

---

## 📊 MONITORING

### Recommended Tools:

- **Uptime**: UptimeRobot, Pingdom
- **Logs**: Papertrail, Loggly
- **Performance**: New Relic, Datadog
- **Errors**: Sentry

### Basic Monitoring Script:

```python
# monitor.py
import requests
import time

def check_health():
    try:
        r = requests.get('https://your-app.com/health', timeout=10)
        if r.status_code == 200:
            print(f"✅ App healthy: {r.json()}")
        else:
            print(f"⚠️ App unhealthy: {r.status_code}")
    except Exception as e:
        print(f"❌ App down: {e}")

# Run every 5 minutes
while True:
    check_health()
    time.sleep(300)
```

---

## 🎓 POST-DEPLOYMENT

### Setelah Deploy Sukses:

1. **Upload model awal** (jika belum ada)
2. **Upload sample dataset** untuk testing
3. **Test semua fitur**:
   - Upload gambar training
   - Jalankan training
   - Test klasifikasi
4. **Share URL** dengan user
5. **Monitor logs** untuk error

### Maintenance:

```bash
# Update code (di VPS)
cd /home/wasteapp/smart-waste-classifier
git pull origin main
sudo systemctl restart wasteapp

# Backup model
cp backend/model/keras_model.h5 backups/model_$(date +%Y%m%d).h5
```

---

## 📚 RESOURCES

- **Flask Docs**: https://flask.palletsprojects.com/
- **Gunicorn**: https://gunicorn.org/
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app/
- **TensorFlow**: https://www.tensorflow.org/

---

## 🎉 SELESAI!

Aplikasi Smart Waste Classifier kamu sekarang sudah LIVE dan bisa diakses public! 🌍♻️

### Next Steps:

1. ✅ Share URL dengan siswa/user
2. ✅ Collect feedback
3. ✅ Train model dengan data lebih banyak
4. ✅ Improve accuracy
5. ✅ Add more features!

---

**Dibuat dengan ❤️ untuk pendidikan lingkungan**

*Smart Waste Classifier v3.0 - Production Ready*
