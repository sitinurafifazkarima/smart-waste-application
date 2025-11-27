# 🤗 DEPLOYMENT GUIDE - HUGGING FACE SPACES

## 🎯 Keuntungan Hugging Face Spaces

✅ **FREE Unlimited Hosting**
- Tidak ada batasan waktu
- Tidak ada cold start
- Persistent storage gratis
- Community support

✅ **Easy Deployment**
- Push ke GitHub → Auto deploy
- Docker support
- Git LFS untuk file besar
- Built-in monitoring

✅ **Performance**
- CPU: 2 cores, 16GB RAM (Free tier)
- Optional GPU upgrade ($0.60/hour)
- Fast CDN worldwide
- No bandwidth limits

---

## 📋 LANGKAH DEPLOYMENT

### Step 1: Persiapan Repository

```powershell
cd "D:\Materi KIR SMPITIK\app_pilahsampah_ver3"

# Copy file untuk Hugging Face
Copy-Item Dockerfile_HF Dockerfile -Force
Copy-Item requirements_hf.txt requirements.txt -Force
Copy-Item README_HF.md README.md -Force

# Commit changes
git add .
git commit -m "Prepare for Hugging Face Spaces deployment"
git push origin main
```

### Step 2: Setup Git LFS untuk Model File

Model keras_model.h5 (297MB) perlu Git LFS:

```powershell
# Install Git LFS (if not installed)
# Download dari: https://git-lfs.github.com/

# Initialize Git LFS
git lfs install

# Track model files
git lfs track "*.h5"
git lfs track "model/*.h5"

# Add .gitattributes
git add .gitattributes

# Add model file
git add model/keras_model.h5

# Commit
git commit -m "Add model with Git LFS"
git push origin main
```

### Step 3: Create Hugging Face Space

1. **Login ke Hugging Face**
   - URL: https://huggingface.co/
   - Create account (gratis)

2. **Create New Space**
   - Klik profile → **Spaces**
   - Click **Create new Space**

3. **Configure Space**
   ```
   Space name: smart-waste-classifier
   License: MIT
   Space SDK: Docker
   Space hardware: CPU basic (FREE)
   Visibility: Public
   ```

4. **Connect GitHub Repository**
   - Settings → Repository
   - Select: "Import from GitHub"
   - Choose: sitinurafifazkarima/smart-waste-application
   - Branch: main

### Step 4: Configure Space Settings

Di Hugging Face Space Settings, tambahkan:

**Files and versions:**
- Pastikan semua file ter-upload
- Cek `model/keras_model.h5` ada (via Git LFS)

**Space metadata (README.md header):**
```yaml
---
title: Smart Waste Classifier
emoji: 🌍
colorFrom: green
colorTo: blue
sdk: docker
app_file: app_hf.py
pinned: false
license: mit
---
```

### Step 5: Deploy!

Hugging Face akan otomatis:
1. Clone repository
2. Download LFS files
3. Build Docker image
4. Start container
5. Expose di URL public

**Build time:** ~10-15 menit
**Public URL:** `https://huggingface.co/spaces/[username]/smart-waste-classifier`

---

## 🔧 ALTERNATIVE: Deploy Tanpa Docker

Jika ingin lebih cepat, gunakan **Streamlit SDK**:

### Option: Streamlit Interface

```powershell
# Install gradio
pip install gradio

# Create app_gradio.py
```

Buat file `app_gradio.py`:

```python
import gradio as gr
from modules.classifier import WasteClassifier
from modules.recommender import WasteRecommender

# Load model
classifier = WasteClassifier("model/keras_model.h5", "model/labels.txt")
recommender = WasteRecommender()

def classify_image(image):
    # Predict
    predicted_class, confidence, all_preds = classifier.predict_from_array(image)
    
    # Get recommendation
    recommendation = recommender.get_recommendation(predicted_class)
    
    return {
        "class": predicted_class,
        "confidence": f"{confidence:.2%}",
        "recommendation": recommendation['disposal']
    }

# Gradio Interface
demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="numpy"),
    outputs=gr.JSON(),
    title="🌍 Smart Waste Classifier",
    description="Upload gambar sampah untuk klasifikasi otomatis"
)

if __name__ == "__main__":
    demo.launch(server_port=7860)
```

Update README.md header:
```yaml
sdk: gradio
sdk_version: "4.0.0"
app_file: app_gradio.py
```

---

## 📊 MONITORING & MAINTENANCE

### Check Space Status

**Dashboard:** https://huggingface.co/spaces/[username]/smart-waste-classifier/settings

**Metrics:**
- Build status
- Runtime logs
- API usage
- Visitor stats

### Update Deployment

```powershell
# Update code
git add .
git commit -m "Update: [description]"
git push origin main

# Hugging Face auto-rebuild (5-10 min)
```

### View Logs

```bash
# Di Hugging Face Space page
Klik "Community" tab → "Logs"
```

---

## 🎯 TESTING DEPLOYMENT

### Test Endpoints

```bash
# Health check
curl https://huggingface.co/spaces/[username]/smart-waste-classifier/health

# API status
curl https://huggingface.co/spaces/[username]/smart-waste-classifier/api/status

# Predict (with image)
curl -X POST https://huggingface.co/spaces/[username]/smart-waste-classifier/api/predict \
  -F "file=@test_image.jpg"
```

### Load Testing

```python
import requests
import time

url = "https://huggingface.co/spaces/[username]/smart-waste-classifier/api/predict"

# Test 10 requests
for i in range(10):
    start = time.time()
    response = requests.post(url, files={'file': open('test.jpg', 'rb')})
    elapsed = time.time() - start
    print(f"Request {i+1}: {elapsed:.2f}s - Status: {response.status_code}")
```

---

## 💰 COST COMPARISON

| Platform | Free Tier | Paid Plans | Cold Start | Model Support |
|----------|-----------|------------|------------|---------------|
| **Hugging Face** | ✅ Unlimited | GPU $0.60/h | ❌ None | ✅ Git LFS |
| Render | 750h/month | $7/month | ✅ 30-60s | ⚠️ Manual |
| Railway | $5 credit | $20/month | ❌ None | ⚠️ Manual |
| Vercel | Function only | $20/month | ✅ 10s | ❌ No support |

**Winner: Hugging Face Spaces** 🏆
- Unlimited free hosting
- Perfect untuk ML models
- Community visibility

---

## 🆘 TROUBLESHOOTING

### Build Failed

**Error:** "Out of memory during build"
```yaml
# Solution: Reduce dependencies
# Gunakan tensorflow-cpu bukan tensorflow
```

**Error:** "Git LFS file not found"
```bash
# Solution: Re-track dengan LFS
git lfs migrate import --include="*.h5"
git push origin main --force
```

### Runtime Errors

**Error:** "Port 7860 already in use"
```python
# app_hf.py - pastikan port benar
port = int(os.environ.get('PORT', 7860))
```

**Error:** "Model not loading"
```bash
# Check file exists
ls -la model/keras_model.h5

# Check LFS pointer
cat model/keras_model.h5 | head -n 5
# Jika muncul "version https://git-lfs...", file belum di-pull
```

### Performance Issues

**Slow predictions:**
- Upgrade ke GPU Space ($0.60/hour)
- Settings → Hardware → GPU T4

**Memory issues:**
- Optimize model loading (lazy load)
- Use `tensorflow-cpu` bukan full tensorflow
- Clear uploads_temp regularly

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Git LFS installed dan configured
- [ ] Model file tracked dengan LFS
- [ ] Dockerfile_HF renamed to Dockerfile
- [ ] requirements_hf.txt renamed to requirements.txt
- [ ] README_HF.md dengan correct metadata
- [ ] Pushed to GitHub
- [ ] Hugging Face Space created
- [ ] Repository connected
- [ ] Build successful
- [ ] Public URL accessible
- [ ] API endpoints tested
- [ ] Frontend UI working
- [ ] Model predictions accurate

---

## 🚀 GO LIVE!

**Public URL Format:**
```
https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier
```

**Embed in Website:**
```html
<iframe
  src="https://huggingface.co/spaces/sitinurafifazkarima/smart-waste-classifier"
  frameborder="0"
  width="850"
  height="450"
></iframe>
```

**Share Direct Link:**
```
https://sitinurafifazkarima-smart-waste-classifier.hf.space
```

---

**Status: Ready untuk deployment ke Hugging Face Spaces!** 🤗
