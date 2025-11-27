# 🌍 Smart Waste Classifier - AI-Powered Waste Management System

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0.0](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow 2.15.0](https://img.shields.io/badge/tensorflow-2.15.0-orange.svg)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Aplikasi web berbasis AI untuk mengklasifikasikan sampah secara otomatis menggunakan Deep Learning**

Sistem ini membantu masyarakat memilah sampah dengan benar menggunakan teknologi computer vision dan memberikan rekomendasi pengelolaan sampah yang tepat.

---

## ✨ Fitur Utama

🔍 **Klasifikasi Otomatis**
- Upload foto sampah → AI mengidentifikasi jenis sampah
- 5 kategori: Cardboard, Glass, Metal, Paper, Plastic
- Confidence score untuk setiap prediksi
- Support JPG, JPEG, PNG (max 16MB)

🎓 **Halaman Edukasi**
- Panduan pemilahan sampah
- Tips reduce, reuse, recycle
- Informasi dampak lingkungan
- Gamifikasi untuk engagement

📊 **Training Dashboard**
- Upload dataset custom
- Training model dengan parameter adjustable
- Real-time training progress
- Visualisasi accuracy & loss

🔒 **Keamanan Dataset**
- Dataset private, tidak bisa diakses public
- API rate limiting
- File upload validation
- CORS protection

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- 512MB RAM minimum (1GB recommended)
- 500MB disk space

### Installation

```bash
# Clone repository
git clone https://github.com/sitinurafifazkarima/smart-waste-application.git
cd smart-waste-application

# Install dependencies
pip install -r requirements_deploy.txt

# Copy model files (REQUIRED - see MODEL_DEPLOYMENT_INSTRUCTIONS.md)
# Model tidak ada di git, download manual atau train baru

# Run development server
cd backend
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

---

## 📁 Project Structure

```
smart-waste-application/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── model/
│   │   ├── keras_model.h5     # Trained model (not in git)
│   │   └── labels.txt         # Class labels
│   ├── dataset_private/       # Training data (gitignored)
│   └── uploads_temp/          # Temporary uploads
├── frontend/
│   ├── templates/
│   │   └── index.html         # Single Page Application
│   └── static/
│       ├── css/style.css      # Responsive design
│       └── js/app.js          # API client
├── modules/
│   ├── classifier.py          # Image classification
│   ├── data_manager.py        # Dataset management
│   ├── trainer.py             # Model training
│   └── recommender.py         # Waste recommendations
├── requirements_deploy.txt    # Production dependencies
├── Procfile                   # Deployment config
├── render.yaml                # Render.com config
└── Dockerfile                 # Container config
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage with frontend SPA |
| GET | `/health` | Server health check |
| GET | `/api/status` | API status & model info |
| POST | `/api/predict` | Classify waste image |
| POST | `/api/upload-training` | Upload training data |
| POST | `/api/train` | Start model training |
| GET | `/api/training-status` | Get training progress |
| GET | `/api/categories` | Get waste categories |

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/predict \
  -F "file=@waste_image.jpg"
```

**Example Response:**

```json
{
  "success": true,
  "predicted_class": "plastic",
  "confidence": 0.94,
  "all_predictions": [
    {"class": "plastic", "confidence": 0.94},
    {"class": "paper", "confidence": 0.03},
    {"class": "metal", "confidence": 0.02}
  ],
  "recommendation": {
    "disposal": "Cuci dan keringkan sebelum dibuang ke tempat sampah plastik",
    "recyclable": true,
    "tips": "Pisahkan tutup botol dari badan botol"
  }
}
```

---

## 🎯 Deployment

### Deploy ke Render.com (FREE)

1. **Fork/Clone repository ini**

2. **Login ke Render Dashboard**
   - https://dashboard.render.com

3. **Create New Web Service**
   - Connect GitHub repository
   - Settings akan auto-detect dari `render.yaml`

4. **Environment Variables:**
   ```
   PYTHON_VERSION=3.11.0
   PORT=10000
   ```

5. **Deploy Settings:**
   ```
   Build Command: pip install -r requirements_deploy.txt
   Start Command: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
   ```

6. **Upload Model File** (REQUIRED)
   - Lihat instruksi lengkap: `MODEL_DEPLOYMENT_INSTRUCTIONS.md`
   - Model tidak ter-push ke git (terlalu besar)
   - Upload via Shell atau rebuild di production

7. **Wait for Build** (~5-10 minutes)

8. **Test Production URL**
   ```bash
   curl https://your-app.onrender.com/health
   ```

### Alternative Platforms
- **Railway**: Auto-deploy dari GitHub
- **Docker**: `docker build -t smart-waste . && docker run -p 8000:8000 smart-waste`
- **VPS**: Deploy dengan Gunicorn + Nginx

---

## 📊 Technology Stack

**Backend:**
- Flask 3.0.0 - Web framework
- TensorFlow 2.15.0 - Deep learning
- Keras 2.15.0 - Neural network API
- Gunicorn 21.2.0 - Production server
- Flask-CORS 4.0.0 - CORS handling

**ML/AI:**
- CNN Architecture - Image classification
- Pillow 10.1.0 - Image processing
- OpenCV 4.8.1 - Computer vision
- NumPy 1.24.3 - Numerical computing

**Frontend:**
- HTML5/CSS3 - Responsive UI
- Vanilla JavaScript - No framework dependencies
- Chart.js - Data visualization
- Fetch API - Async requests

---

## 📖 Documentation

- `DEPLOYMENT_GUIDE.md` - Panduan deployment lengkap
- `MODEL_DEPLOYMENT_INSTRUCTIONS.md` - Cara upload model ke production
- `ARCHITECTURE.md` - System architecture details
- `QUICKSTART_FLASK.md` - Quick start guide
- `TROUBLESHOOTING.md` - Common issues & solutions

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

**SMPITIK Smart Waste Team**
- Project Lead: Siti Nurafifa Zkarima
- GitHub: [@sitinurafifazkarima](https://github.com/sitinurafifazkarima)

---

## 🙏 Acknowledgments

- TensorFlow Team - Deep learning framework
- Flask Community - Web framework
- Teachable Machine - Initial model training
- Open source community - Various libraries

---

## 📞 Support

Jika ada pertanyaan atau masalah:
- 📧 Email: [your-email]
- 🐛 Issues: [GitHub Issues](https://github.com/sitinurafifazkarima/smart-waste-application/issues)
- 📚 Docs: Lihat folder documentation

---

## 🌟 Star this repo if you find it useful!

**Built with ❤️ for a cleaner environment** 🌱
