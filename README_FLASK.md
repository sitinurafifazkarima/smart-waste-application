# 🌍 Smart Waste Classifier v3.0
### AI-Powered Waste Classification for Education

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-green)
![Flask](https://img.shields.io/badge/Flask-3.0-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![License](https://img.shields.io/badge/license-Educational-purple)

**Aplikasi pembelajaran AI untuk klasifikasi sampah - Siap deploy ke production!**

[🚀 Quick Start](#-quick-start) •
[📖 Documentation](#-documentation) •
[🌐 Deploy](#-deployment) •
[🎓 Features](#-features)

</div>

---

## 📋 Tentang Aplikasi

**Smart Waste Classifier** adalah aplikasi web berbasis AI yang mengajarkan konsep Machine Learning sambil peduli lingkungan. Aplikasi ini memungkinkan user untuk:

- 🔍 **Mengklasifikasi sampah** menggunakan AI
- 📸 **Menambah data training** sendiri
- 🧠 **Melatih model AI** dengan parameter custom
- ♻️ **Mendapat rekomendasi** pengelolaan sampah
- 🎓 **Belajar konsep AI** secara interaktif

### ✨ Keunggulan v3.0:

- ✅ **Production Ready** - Flask backend dengan Gunicorn
- ✅ **Modern UI** - Responsive design dengan tema eco-green
- ✅ **Dataset Aman** - Private server-side storage
- ✅ **Easy Deploy** - Support Render, Railway, Replit, VPS
- ✅ **Edukatif** - Konten pembelajaran lengkap

---

## 🎯 Features

### 1. 🔍 Image Classification
Upload foto sampah dan AI akan mengidentifikasi jenisnya:
- **5 Kategori:** Cardboard, Glass, Metal, Paper, Plastic
- **Confidence Score** untuk setiap kategori
- **Rekomendasi pengelolaan** sampah
- **Fakta edukatif** tentang dampak lingkungan

### 2. 📸 Dataset Management
Kelola data training dengan mudah:
- Upload foto sampah untuk training
- Pilih kategori yang sesuai
- Lihat statistik dataset real-time
- Validasi otomatis file upload

### 3. 🧠 AI Training
Latih model dengan kontrol penuh:
- Atur **epochs** (5-100)
- Pilih **learning rate** (0.0001-0.01)
- Set **batch size** (8-64)
- Monitor progress **real-time**
- Lihat training history & accuracy

### 4. 📚 Educational Content
Belajar sambil berkarya:
- Penjelasan konsep AI (Epoch, Learning Rate, etc.)
- Panduan pengelolaan sampah per jenis
- Sistem **gamifikasi level AI** (🥚→🚀)
- Tips recycling & dampak lingkungan

---

## 🚀 Quick Start

### Persyaratan:
- Python 3.11+
- 2GB RAM minimum (4GB untuk training)
- 500MB storage

### Instalasi Lokal:

```powershell
# 1. Clone repository
git clone https://github.com/USERNAME/smart-waste-classifier.git
cd smart-waste-classifier

# 2. Install dependencies
pip install -r requirements_deploy.txt

# 3. (Optional) Copy existing model
Copy-Item keras_model.h5 backend\model\
Copy-Item labels.txt backend\model\

# 4. Run Flask app
cd backend
python app.py

# 5. Open browser
# http://localhost:5000
```

**Lihat:** [QUICKSTART_FLASK.md](QUICKSTART_FLASK.md) untuk panduan lengkap

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[README_DEPLOY.md](README_DEPLOY.md)** | 🚀 Panduan deployment lengkap (Render/Railway/VPS) |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ Arsitektur teknis & API documentation |
| **[QUICKSTART_FLASK.md](QUICKSTART_FLASK.md)** | ⚡ Testing lokal & development guide |
| **[PROJECT_SUMMARY_FLASK.md](PROJECT_SUMMARY_FLASK.md)** | 📊 Overview project & tech stack |
| **[DIAGRAMS.md](DIAGRAMS.md)** | 🎨 Diagram visual arsitektur & data flow |

---

## 🌐 Deployment

### ☁️ Deploy ke Cloud Platform

**Recommended:** Render.com (Free tier, auto-deploy)

1. **Fork/Clone** repository ke GitHub
2. Sign up di [Render.com](https://render.com)
3. **Create Web Service** from GitHub repo
4. Configure:
   ```
   Build Command: pip install -r requirements_deploy.txt
   Start Command: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
   ```
5. **Deploy!** (~5-10 menit)

**Alternatif Platform:**
- **Railway** - Modern platform, good free tier
- **Replit** - Instant deploy, great for demo
- **VPS** - Full control, scalable

**Lihat:** [README_DEPLOY.md](README_DEPLOY.md) untuk panduan lengkap setiap platform

---

## 🏗️ Arsitektur

```
┌─────────────────────────────────────────┐
│           Users (Browser)                │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│      Cloud Platform (Render/Railway)     │
│  ┌─────────────────────────────────┐   │
│  │   Gunicorn WSGI Server          │   │
│  │   ├─ Flask App (Worker 1)       │   │
│  │   └─ Flask App (Worker 2)       │   │
│  └─────────────────────────────────┘   │
│                  ↓                       │
│  ┌─────────────────────────────────┐   │
│  │   Frontend (HTML/CSS/JS)        │   │
│  │   - Single Page App             │   │
│  │   - Responsive Design           │   │
│  └─────────────────────────────────┘   │
│                  ↓                       │
│  ┌─────────────────────────────────┐   │
│  │   Backend API                   │   │
│  │   - /api/predict                │   │
│  │   - /api/train                  │   │
│  │   - /api/upload-training        │   │
│  └─────────────────────────────────┘   │
│                  ↓                       │
│  ┌─────────────────────────────────┐   │
│  │   Private Storage (🔒)          │   │
│  │   - ML Model                    │   │
│  │   - Dataset (tidak public)      │   │
│  │   - Training Logs               │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Lihat:** [DIAGRAMS.md](DIAGRAMS.md) untuk diagram visual lengkap

---

## 📁 Struktur Project

```
app_pilahsampah_ver3/
│
├── backend/                      # Backend Flask
│   ├── app.py                   # Main application ⭐
│   ├── model/                   # ML model storage
│   ├── dataset_private/         # Private dataset
│   └── uploads_temp/            # Temporary uploads
│
├── frontend/                     # Frontend files
│   ├── templates/
│   │   └── index.html           # SPA ⭐
│   └── static/
│       ├── css/style.css        # Eco-green theme ⭐
│       └── js/app.js            # API communication ⭐
│
├── modules/                      # Python modules
│   ├── classifier.py            # Classification logic
│   ├── data_manager.py          # Dataset management
│   ├── trainer.py               # Model training
│   └── recommender.py           # Recommendations
│
├── utils/                        # Utilities
│   ├── image_processor.py
│   └── visualizer.py
│
├── requirements_deploy.txt       # Dependencies
├── Procfile                      # Deployment command
├── Dockerfile                    # Docker config
└── README.md                     # This file
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/health` | GET | Health check |
| `/api/status` | GET | System status |
| `/api/predict` | POST | Classify image |
| `/api/upload-training` | POST | Upload training data |
| `/api/train` | POST | Start training |
| `/api/training-status` | GET | Training progress |

**Lihat:** [ARCHITECTURE.md](ARCHITECTURE.md) untuk API documentation lengkap

---

## 🎨 Tech Stack

### Backend:
- **Flask 3.0** - Web framework
- **Gunicorn** - WSGI server
- **TensorFlow 2.15** - ML framework
- **Keras** - Deep learning
- **PIL/OpenCV** - Image processing

### Frontend:
- **HTML5/CSS3** - Structure & styling
- **Vanilla JavaScript** - No framework dependency
- **Chart.js** - Visualizations
- **Font Awesome** - Icons

### Deployment:
- **Docker** - Containerization
- **Render/Railway** - Cloud platforms
- **Nginx** - Reverse proxy (VPS)

---

## 🔐 Keamanan

### Dataset Protection:
✅ Dataset disimpan di folder private server
✅ Tidak ada route Flask yang expose dataset
✅ .gitignore exclude dataset dari repository
✅ File operations hanya via Python backend

### Upload Security:
✅ File type validation (jpg, jpeg, png only)
✅ File size limit (16MB)
✅ Secure filename handling
✅ Temp files auto-cleaned

---

## 🧪 Testing

### Local Testing:
```powershell
# Run app
cd backend
python app.py

# Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/status
```

### Production Testing:
```bash
# Health check
curl https://your-app.com/health

# Upload test
curl -X POST \
  -F "file=@test.jpg" \
  -F "category=plastic" \
  https://your-app.com/api/upload-training
```

**Lihat:** [QUICKSTART_FLASK.md](QUICKSTART_FLASK.md) untuk testing lengkap

---

## 📊 Spesifikasi

### Minimum Requirements:
- **RAM:** 1GB
- **CPU:** 1 core
- **Storage:** 500MB
- **Python:** 3.11+

### Recommended:
- **RAM:** 2GB (untuk training)
- **CPU:** 2 cores
- **Storage:** 1GB
- **HTTPS:** Required untuk production

### Scalability:
- Support multiple concurrent users
- Background training (non-blocking)
- Can scale horizontally with more workers

---

## 🎓 Untuk Pendidikan

Aplikasi ini cocok untuk:
- 🏫 **Pembelajaran AI di sekolah**
- 🌍 **Edukasi lingkungan**
- 💻 **Portfolio project**
- 🎯 **Demo ML application**
- 📚 **Teaching material**

### Learning Outcomes:
Students belajar tentang:
- Machine Learning concepts
- Training process & parameters
- Dataset management
- Web API integration
- Environmental awareness

---

## 🚧 Roadmap

### Version 3.1 (Q1 2026):
- [ ] User authentication
- [ ] Save classification history
- [ ] Multiple model support
- [ ] Batch classification

### Version 3.2:
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Social features
- [ ] Leaderboard

### Version 4.0:
- [ ] Microservices architecture
- [ ] Object detection (YOLO)
- [ ] Multi-language support
- [ ] Advanced analytics

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

## 📝 License

Educational use only. Created for learning purposes.

---

## 👥 Authors

**Smart Waste Classifier Team**
- AI/ML Development
- Backend Engineering
- Frontend Design
- Educational Content

---

## 📞 Support

Need help?
- 📖 Check [Documentation](#-documentation)
- 🐛 Report issues on GitHub
- 💬 Discussion forum (coming soon)

---

## 🌟 Showcase

### Screenshots:

**Home Page:**
- Dashboard dengan statistik
- Dataset distribution chart
- Quick links to features

**Classification:**
- Upload & preview
- Real-time classification
- Confidence visualization
- Recommendations

**Training:**
- Parameter controls
- Real-time progress
- Training metrics
- History chart

**Education:**
- AI concepts explained
- Waste management guide
- Level system

---

## 🎉 Acknowledgments

Terima kasih kepada:
- TensorFlow & Keras teams
- Flask community
- Open source contributors
- Students & educators using this app

---

## 📈 Stats

- **Lines of Code:** 5000+
- **Files:** 25+
- **API Endpoints:** 8
- **Supported Platforms:** 4
- **Documentation Pages:** 6

---

<div align="center">

**Smart Waste Classifier v3.0**

Dibuat dengan ❤️ untuk pendidikan lingkungan

[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![Deploy to Railway](https://img.shields.io/badge/Deploy%20to-Railway-0B0D0E?style=for-the-badge&logo=railway)](https://railway.app)

*Last Updated: November 27, 2025*

</div>
