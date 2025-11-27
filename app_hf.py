"""
🤗 SMART WASTE CLASSIFIER - HUGGING FACE SPACES VERSION
========================================================
Flask backend optimized for Hugging Face Spaces deployment

Author: Smart Waste Classifier Team
Deployment: Hugging Face Spaces
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path
import json
import uuid
from datetime import datetime
import threading
import traceback

# Import modul dari folder modules
sys.path.append(str(Path(__file__).parent))
from modules.classifier import WasteClassifier
from modules.data_manager import DataManager
from modules.recommender import WasteRecommender

# Lazy import ModelTrainer untuk mempercepat startup
_ModelTrainer = None

def _get_trainer():
    global _ModelTrainer
    if _ModelTrainer is None:
        from modules.trainer import ModelTrainer
        _ModelTrainer = ModelTrainer
    return _ModelTrainer

# 📁 KONFIGURASI PATH untuk Hugging Face
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"
TEMPLATES_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"

# Dataset private - TIDAK BOLEH diakses public!
DATASET_PRIVATE = BASE_DIR / "dataset_private"
RAW_DATA_DIR = DATASET_PRIVATE / "raw"
PROCESSED_DATA_DIR = DATASET_PRIVATE / "processed"

# Model dan logs
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "keras_model.h5"
LABELS_PATH = MODEL_DIR / "labels.txt"
TRAINING_LOGS_DIR = BASE_DIR / "training_logs"
UPLOAD_FOLDER = BASE_DIR / "uploads_temp"

# Create necessary folders
for folder in [MODEL_DIR, TRAINING_LOGS_DIR, UPLOAD_FOLDER, DATASET_PRIVATE, 
               RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# 🌐 FLASK APP CONFIGURATION
app = Flask(__name__, 
            template_folder=str(TEMPLATES_DIR),
            static_folder=str(STATIC_DIR))

# CORS untuk API access
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Upload configuration
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 🗄️ APPLICATION STATE
app_state = {
    'classifier': None,
    'data_manager': None,
    'recommender': None,
    'model_accuracy': 0.0,
    'total_images_classified': 0,
    'total_training_count': 0,
    'is_training': False,
    'training_progress': {},
    'model_path': None,
    'labels_path': None
}

# 🎯 WASTE CATEGORIES
WASTE_CATEGORIES = {
    'cardboard': {
        'name': 'Kardus/Karton',
        'color': '#8B4513',
        'icon': '📦',
        'recyclable': True
    },
    'glass': {
        'name': 'Kaca',
        'color': '#4169E1',
        'icon': '🍾',
        'recyclable': True
    },
    'metal': {
        'name': 'Logam',
        'color': '#708090',
        'icon': '🔩',
        'recyclable': True
    },
    'paper': {
        'name': 'Kertas',
        'color': '#F5F5DC',
        'icon': '📄',
        'recyclable': True
    },
    'plastic': {
        'name': 'Plastik',
        'color': '#FF6347',
        'icon': '🥤',
        'recyclable': True
    }
}

def init_backend():
    """
    🔧 Inisialisasi backend components
    Dipanggil saat aplikasi pertama kali dijalankan
    """
    print("\n" + "="*60)
    print("🤗 INITIALIZING HUGGING FACE SPACES BACKEND")
    print("="*60)
    
    try:
        # Create category folders
        for category in WASTE_CATEGORIES.keys():
            category_path = RAW_DATA_DIR / category
            category_path.mkdir(exist_ok=True)
            print(f"  ✅ Created folder: {category}")
        
        # Inisialisasi Data Manager
        app_state['data_manager'] = DataManager(
            str(RAW_DATA_DIR), 
            str(PROCESSED_DATA_DIR)
        )
        print("  ✅ Data Manager initialized")
        
        # Inisialisasi Recommender
        app_state['recommender'] = WasteRecommender()
        print("  ✅ Recommender initialized")
        
        # Load classifier jika model sudah ada
        # Lazy loading - akan di-load saat request pertama untuk mempercepat startup
        if MODEL_PATH.exists() and LABELS_PATH.exists():
            app_state['classifier'] = None  # Will be lazy loaded on first request
            app_state['model_path'] = str(MODEL_PATH)
            app_state['labels_path'] = str(LABELS_PATH)
            print("  ✅ Model found - will load on first prediction request")
        else:
            print("  ⚠️  Model not found - training required")
        
        # Load training history
        log_files = list(TRAINING_LOGS_DIR.glob("training_log_*.json"))
        if log_files:
            latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
            with open(latest_log, 'r') as f:
                log_data = json.load(f)
                app_state['model_accuracy'] = log_data.get('test_accuracy', 0.0)
                app_state['total_training_count'] = len(log_files)
        
        print("\n✅ Backend initialization completed!")
        print("="*60)
        print(f"\n🚀 Starting Flask server...")
        print(f"🌍 Running on Hugging Face Spaces")
        print(f"📚 API Docs: /api/status\n")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        traceback.print_exc()
        raise

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Homepage - Serve frontend SPA"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint untuk monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'Smart Waste Classifier',
        'platform': 'Hugging Face Spaces',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status')
def api_status():
    """
    📊 Get API status dan informasi sistem
    """
    model_loaded = app_state['classifier'] is not None
    model_ready = MODEL_PATH.exists() and LABELS_PATH.exists()
    
    return jsonify({
        'status': 'online',
        'model_loaded': model_loaded,
        'model_ready': model_ready,
        'model_accuracy': app_state['model_accuracy'],
        'total_images_classified': app_state['total_images_classified'],
        'total_training_count': app_state['total_training_count'],
        'is_training': app_state['is_training'],
        'categories': list(WASTE_CATEGORIES.keys()),
        'platform': 'Hugging Face Spaces',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    🔍 Klasifikasi gambar sampah
    """
    try:
        # Lazy load classifier jika belum di-load
        if app_state['classifier'] is None:
            if 'model_path' in app_state and 'labels_path' in app_state:
                print("  🔄 Loading model for first time...")
                app_state['classifier'] = WasteClassifier(
                    app_state['model_path'],
                    app_state['labels_path']
                )
                print("  ✅ Classifier loaded successfully")
            else:
                return jsonify({
                    'success': False,
                    'error': 'Model belum tersedia. Silakan lakukan training terlebih dahulu.'
                }), 400
        
        # Cek file upload
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Tidak ada file yang diupload'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nama file kosong'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Format file tidak didukung. Gunakan JPG, JPEG, atau PNG'
            }), 400
        
        # Save temporary file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Predict
            predicted_class, confidence, all_predictions = app_state['classifier'].predict(filepath)
            
            # Get recommendation
            recommendation = app_state['recommender'].get_recommendation(predicted_class)
            
            # Update stats
            app_state['total_images_classified'] += 1
            
            # Cleanup
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'predicted_class': predicted_class,
                'confidence': float(confidence),
                'all_predictions': [
                    {
                        'class': pred['class'],
                        'confidence': float(pred['confidence'])
                    }
                    for pred in all_predictions
                ],
                'recommendation': recommendation,
                'category_info': WASTE_CATEGORIES.get(predicted_class, {})
            })
            
        except Exception as e:
            # Cleanup on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error klasifikasi: {str(e)}'
        }), 500

@app.route('/api/categories')
def api_categories():
    """
    📋 Get daftar kategori sampah
    """
    return jsonify({
        'success': True,
        'categories': WASTE_CATEGORIES
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(
        STATIC_DIR,
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint tidak ditemukan'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({
        'success': False,
        'error': 'File terlalu besar. Maksimal 16MB'
    }), 413

# ==================== STARTUP ====================

if __name__ == '__main__':
    # Initialize backend
    init_backend()
    
    # Get port from environment (Hugging Face Spaces uses port 7860)
    port = int(os.environ.get('PORT', 7860))
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Set to False for production
    )
