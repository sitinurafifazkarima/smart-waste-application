# 🏗️ ARSITEKTUR APLIKASI SMART WASTE CLASSIFIER

## 📋 Overview

Smart Waste Classifier adalah aplikasi pembelajaran machine learning berbasis web yang dirancang khusus untuk siswa SMP. Aplikasi ini mengintegrasikan konsep AI dengan edukasi lingkungan.

---

## 🎯 Tujuan Desain

1. **Edukatif**: Setiap fitur memiliki penjelasan yang mudah dipahami
2. **Interaktif**: Real-time visualization dan feedback
3. **User-friendly**: UI intuitif dengan tema eco-green
4. **Modular**: Kode terstruktur dan mudah di-maintain
5. **Scalable**: Mudah ditambah fitur baru

---

## 📁 Struktur Komponen

```
┌─────────────────────────────────────────────────────────┐
│                    APP.PY (Main)                        │
│  - Streamlit UI                                          │
│  - Page routing                                          │
│  - Session management                                    │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   MODULES    │    │    UTILS     │    │   CONFIG     │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ classifier   │    │ visualizer   │    │ Parameters   │
│ trainer      │    │ img_process  │    │ Colors       │
│ data_manager │    └──────────────┘    │ Messages     │
│ recommender  │                         │ Educational  │
└──────────────┘                         └──────────────┘
        │
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                    DATASET                              │
│  - Raw data (user uploads)                              │
│  - Processed data (train/test/validation)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🧩 Detail Modul

### 1. **app.py** - Aplikasi Utama
**Tanggung jawab:**
- Inisialisasi Streamlit
- Routing halaman (Home, Tambah Data, Training, Klasifikasi, Edukasi)
- Session state management
- Custom CSS loading
- UI rendering

**Fitur utama:**
- Multi-page navigation dengan sidebar
- Real-time progress tracking
- Interactive charts
- Responsive layout

**Dependencies:**
```python
streamlit, streamlit_option_menu, PIL
modules.*, utils.*, config
```

---

### 2. **modules/classifier.py** - Modul Klasifikasi
**Tanggung jawab:**
- Load model Keras
- Preprocessing gambar
- Prediksi kelas
- Confidence scoring

**Kelas utama:**
```python
class WasteClassifier:
    - __init__(model_path, labels_path)
    - preprocess_image(image_path) → np.ndarray
    - predict(image_path) → Dict[hasil]
    - predict_from_pil_image(pil_image) → Dict[hasil]
    - get_confidence_level(confidence) → str
    - reload_model()
```

**Flow:**
```
Image Input → Resize (224x224) → Normalize [-1,1] 
    → Model Predict → Argmax → Class + Confidence
```

---

### 3. **modules/trainer.py** - Modul Training
**Tanggung jawab:**
- Membuat arsitektur model CNN
- Data augmentation
- Training dengan callbacks
- Model evaluation
- Save model & logs

**Kelas utama:**
```python
class ModelTrainer:
    - __init__(processed_data_dir, model_save_path)
    - create_model(learning_rate) → keras.Model
    - prepare_data_generators(batch_size) → generators
    - train(epochs, lr, batch_size, callback) → Dict[results]

class TrainingProgressCallback(Callback):
    - on_epoch_end() → update progress
```

**Arsitektur Model:**
```
Input (224x224x3)
    ↓
Conv2D(32) → BatchNorm → Conv2D(32) → MaxPool → Dropout
    ↓
Conv2D(64) → BatchNorm → Conv2D(64) → MaxPool → Dropout
    ↓
Conv2D(128) → BatchNorm → Conv2D(128) → MaxPool → Dropout
    ↓
Flatten → Dense(256) → Dropout → Dense(128) → Dropout
    ↓
Output Dense(5) Softmax
```

**Data Augmentation:**
- Rotation: ±20°
- Width/Height shift: 20%
- Zoom: ±20%
- Horizontal flip
- Normalization: [-1, 1]

---

### 4. **modules/data_manager.py** - Manajemen Dataset
**Tanggung jawab:**
- Upload & organize gambar
- Split dataset (train/test/val)
- Statistik dataset
- Validasi dataset

**Kelas utama:**
```python
class DataManager:
    - __init__(raw_data_dir, processed_data_dir)
    - add_image(file, label) → Dict[result]
    - get_dataset_statistics() → Dict[stats]
    - split_dataset(ratios) → Dict[result]
    - check_dataset_ready() → Dict[status]
    - get_images_list(category) → List[images]
```

**Dataset Flow:**
```
User Upload → Validate → Resize → Save to raw/
    ↓
Split Dataset → 70% train, 15% test, 15% validation
    ↓
Copy to processed/ (organized by split & category)
```

---

### 5. **modules/recommender.py** - Sistem Rekomendasi
**Tanggung jawab:**
- Memberikan rekomendasi pengelolaan sampah
- Tips praktis
- Educational content
- Nilai ekonomis & dampak lingkungan

**Kelas utama:**
```python
class WasteRecommender:
    - __init__()
    - get_recommendation(waste_type) → Dict[rec]
    - get_educational_content(waste_type) → Dict[edu]
    - get_quick_action(waste_type) → str
    - compare_waste_types(types) → Dict[comparison]
```

**Data Structure:**
```python
{
  "Plastic": {
    "icon": "🥤",
    "action": "Kurangi penggunaan",
    "description": "...",
    "tips": [...],
    "impact": "...",
    "value": "ekonomis_rendah"
  }
}
```

---

### 6. **utils/image_processor.py** - Image Utilities
**Fungsi:**
- `load_and_preprocess_image()` - Load & resize
- `normalize_image_array()` - Normalisasi [-1,1]
- `enhance_image()` - Brightness, contrast, sharpness
- `resize_image_for_display()` - Display optimization

---

### 7. **utils/visualizer.py** - Visualisasi
**Fungsi:**
- `plot_training_history()` - Matplotlib charts
- `plot_training_history_interactive()` - Plotly interactive
- `plot_prediction_confidence()` - Bar chart confidence
- `plot_dataset_distribution()` - Dataset stats
- `plot_ai_level_progress()` - Gauge chart gamifikasi

---

### 8. **config.py** - Konfigurasi
**Berisi:**
- Path configurations
- Waste categories & icons
- Recommendations database
- Educational content
- AI level system
- Color themes
- Default parameters
- Messages

---

## 🔄 Flow Diagram

### Flow 1: Tambah Data
```
User uploads image → Validate format → Select category
    ↓
Resize & optimize → Save to dataset/raw/{category}/
    ↓
Update statistics → Show success message
```

### Flow 2: Training Model
```
Check dataset ready → Configure parameters (epochs, LR)
    ↓
Split dataset (70/15/15) → Create data generators
    ↓
Build model architecture → Compile with optimizer
    ↓
Training loop:
  - Forward pass
  - Calculate loss
  - Backward pass
  - Update weights
  - Update UI (real-time)
    ↓
Evaluate on test set → Save model → Update AI level
```

### Flow 3: Klasifikasi
```
Upload image → Preprocess (resize + normalize)
    ↓
Model predict → Get class & confidence
    ↓
Show results:
  - Main prediction
  - Confidence chart
  - Recommendation
  - Educational facts
```

---

## 🎨 UI/UX Design Principles

### 1. **Color Scheme** (Eco-Green)
- Primary: `#2ECC71` (Green)
- Secondary: `#27AE60` (Dark Green)
- Accent: `#F39C12` (Orange)
- Background: `#E8F8F5` (Light Green)

### 2. **Layout**
- Sidebar: Navigation + Quick stats
- Main area: Content (responsive columns)
- Cards: Info boxes dengan border & shadow
- Charts: Interactive Plotly

### 3. **Interactive Elements**
- Progress bars untuk training
- Real-time updating charts
- Hover tooltips
- Button animations
- Success/warning/error messages dengan warna

### 4. **Educational UX**
- Expandable explanations (expanders)
- Analogi untuk konsep sulit
- Visual feedback (emojis, icons)
- Gamifikasi (levels, badges)

---

## 🔐 Session State Management

Streamlit session state variables:
```python
st.session_state.classifier         # WasteClassifier instance
st.session_state.data_manager       # DataManager instance
st.session_state.recommender        # WasteRecommender instance
st.session_state.training_in_progress  # bool
st.session_state.model_accuracy     # float
st.session_state.total_training_count  # int
```

**Why Session State?**
- Persist data across reruns
- Share data between pages
- Avoid reloading heavy models

---

## 🚀 Performance Optimizations

1. **Lazy Loading**
   - Model only loaded when needed
   - Cached in session state

2. **Image Optimization**
   - Resize uploads to max 800x800
   - JPEG compression (quality 95)

3. **Data Generators**
   - Streaming data loading (not all in memory)
   - Batch processing

4. **Progress Callbacks**
   - Incremental UI updates
   - Non-blocking operations

---

## 🧪 Testing Strategy

### Unit Tests
- `test_modules.py` - Test all modules independently
- Each module has `if __name__ == "__main__"` test block

### Integration Tests
- Full flow testing via UI
- Dataset → Training → Classification

### User Testing
- Siswa SMP as target users
- Feedback on clarity & usability

---

## 🔮 Future Enhancements

### Phase 2 (Potential):
1. **Multi-user support** - Database untuk tracking user progress
2. **Model comparison** - Compare different training runs
3. **Export reports** - PDF training reports
4. **Mobile app** - React Native version
5. **Real-time camera** - Direct classification dari webcam
6. **Collaborative learning** - Share datasets antar siswa
7. **Advanced metrics** - Confusion matrix, precision, recall
8. **Model versioning** - Keep history of models

### Technical Debt:
- Add comprehensive unit tests
- Implement logging system
- Add error monitoring
- Optimize for larger datasets (>10k images)

---

## 📊 Technical Specifications

**Requirements:**
- Python: 3.8+
- RAM: 4GB minimum (8GB recommended)
- Storage: 1GB for app + space for dataset
- CPU: Any modern CPU (GPU optional for faster training)

**Key Dependencies:**
- `streamlit >= 1.28.0` - UI framework
- `tensorflow >= 2.13.0` - ML framework
- `pillow >= 10.0.0` - Image processing
- `plotly >= 5.17.0` - Interactive charts

**Model Specs:**
- Input: 224x224x3 RGB images
- Output: 5 classes (softmax)
- Parameters: ~2-3M
- Training time: 5-60 min (depends on dataset size & epochs)

---

## 🎓 Educational Value

**Learning Outcomes:**
1. ✅ Understand basic ML concepts
2. ✅ Experience full ML pipeline
3. ✅ Data collection importance
4. ✅ Model evaluation & tuning
5. ✅ Environmental awareness
6. ✅ Critical thinking (when AI fails?)

**Teaching Tips:**
- Start with small dataset (5 images/class)
- Demonstrate overfitting with too many epochs
- Show impact of learning rate
- Discuss real-world AI limitations
- Connect to environmental science

---

## 📝 Code Style & Standards

**Conventions:**
- Type hints for function parameters
- Docstrings for all classes/functions
- Emoji in comments for visual clarity
- Modular design (single responsibility)
- Config-driven (avoid magic numbers)

**Documentation:**
- Every module has educational comments
- Complex algorithms explained
- Analogies for students

---

## 🤝 Contribution Guidelines

**For Educators:**
1. Customize `config.py` for your needs
2. Add more educational content
3. Adjust default parameters
4. Translate to your language

**For Developers:**
1. Follow existing code style
2. Add comments & docstrings
3. Test thoroughly
4. Update README

---

## 📞 Architecture Decisions

### Why Streamlit?
- ✅ Rapid development
- ✅ Python-native (no JS needed)
- ✅ Built-in widgets
- ✅ Easy deployment
- ❌ Limited customization (but OK for educational use)

### Why TensorFlow/Keras?
- ✅ Industry standard
- ✅ Excellent documentation
- ✅ Easy to learn
- ✅ Transfer learning support

### Why CNN Architecture?
- ✅ Proven for image classification
- ✅ Not too complex for students
- ✅ Fast training on CPU
- ✅ Good balance accuracy/speed

### Why Local Storage?
- ✅ Simple for classroom use
- ✅ No server needed
- ✅ Privacy (data stays local)
- ❌ No cloud backup (feature for later)

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-11-26  
**Author:** AI Assistant untuk Pendidikan
