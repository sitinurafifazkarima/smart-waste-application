"""
🌍 SMART WASTE CLASSIFIER - FLASK API BACKEND
===============================================
Backend API untuk aplikasi klasifikasi sampah berbasis AI

Author: Smart Waste Classifier Team
Purpose: Deployment-ready Flask backend dengan keamanan dataset
Version: 3.0 (Flask Production Version)
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

# Import modul dari folder parent
sys.path.append(str(Path(__file__).parent.parent))
from modules.classifier import WasteClassifier
from modules.data_manager import DataManager
from modules.recommender import WasteRecommender

# Lazy import trainer to avoid loading TensorFlow at startup
_ModelTrainer = None
def _get_trainer():
    global _ModelTrainer
    if _ModelTrainer is None:
        from modules.trainer import ModelTrainer
        _ModelTrainer = ModelTrainer
    return _ModelTrainer

# 📁 KONFIGURASI PATH
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent

# Dataset private - TIDAK BOLEH diakses public!
DATASET_PRIVATE = BACKEND_DIR / "dataset_private"
RAW_DATA_DIR = DATASET_PRIVATE / "raw"
PROCESSED_DATA_DIR = DATASET_PRIVATE / "processed"

# Model storage
MODEL_DIR = BACKEND_DIR / "model"
MODEL_PATH = MODEL_DIR / "keras_model.h5"
LABELS_PATH = MODEL_DIR / "labels.txt"

# Upload temporary storage
UPLOAD_FOLDER = BACKEND_DIR / "uploads_temp"
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Frontend paths
FRONTEND_DIR = BASE_DIR / "frontend"
TEMPLATE_DIR = FRONTEND_DIR / "templates"
STATIC_DIR = FRONTEND_DIR / "static"

# Training logs
TRAINING_LOGS_DIR = BACKEND_DIR / "training_logs"
TRAINING_LOGS_DIR.mkdir(exist_ok=True)

# 🔧 KONFIGURASI FLASK
app = Flask(__name__, 
            template_folder=str(TEMPLATE_DIR),
            static_folder=str(STATIC_DIR))

# CORS untuk akses API dari frontend berbeda domain
CORS(app)

# Konfigurasi upload
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 🌍 GLOBAL VARIABLES
# Gunakan dictionary untuk thread-safe storage
app_state = {
    'classifier': None,
    'data_manager': None,
    'recommender': None,
    'training_status': {
        'in_progress': False,
        'current_epoch': 0,
        'total_epochs': 0,
        'progress': 0,
        'message': 'Idle',
        'accuracy': 0,
        'loss': 0
    },
    'model_accuracy': 0.0,
    'total_training_count': 0
}

# 🔐 KATEGORI SAMPAH & KONFIGURASI
WASTE_CATEGORIES = {
    "cardboard": "Cardboard",
    "glass": "Glass",
    "metal": "Metal",
    "paper": "Paper",
    "plastic": "Plastic"
}

CATEGORY_ICONS = {
    "cardboard": "📦",
    "glass": "🫙",
    "metal": "🔩",
    "paper": "📄",
    "plastic": "🥤"
}

# 🔧 HELPER FUNCTIONS
def allowed_file(filename):
    """
    ✅ Cek apakah file yang diupload valid
    Hanya menerima: jpg, jpeg, png
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_backend():
    """
    🚀 Inisialisasi backend saat startup
    Load model, data manager, recommender
    """
    print("\n" + "="*60)
    print("🌍 INITIALIZING SMART WASTE CLASSIFIER BACKEND")
    print("="*60)
    
    try:
        # Buat folder yang diperlukan
        MODEL_DIR.mkdir(exist_ok=True)
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Buat folder untuk setiap kategori sampah di RAW_DATA_DIR
        for category in WASTE_CATEGORIES.keys():
            (RAW_DATA_DIR / category).mkdir(exist_ok=True)
            print(f"  ✅ Created folder: {category}")
        
        # Copy model & labels jika ada di root
        old_model = BASE_DIR / "keras_model.h5"
        old_labels = BASE_DIR / "labels.txt"
        
        if old_model.exists() and not MODEL_PATH.exists():
            import shutil
            shutil.copy(old_model, MODEL_PATH)
            print(f"  📦 Copied model to: {MODEL_PATH}")
        
        if old_labels.exists() and not LABELS_PATH.exists():
            import shutil
            shutil.copy(old_labels, LABELS_PATH)
            print(f"  📋 Copied labels to: {LABELS_PATH}")
        
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
            print(f"  📊 Loaded training history: {app_state['total_training_count']} trainings")
        
        print("\n✅ Backend initialization completed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        traceback.print_exc()

# 🌐 ROUTES - PUBLIC PAGES

@app.route('/')
def index():
    """
    🏠 Landing page / Homepage
    Menampilkan UI utama aplikasi
    """
    return render_template('index.html')

@app.route('/health')
def health():
    """
    💚 Health check endpoint
    Untuk monitoring status server
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': app_state['classifier'] is not None,
        'training_in_progress': app_state['training_status']['in_progress']
    })

# 🔌 API ENDPOINTS

@app.route('/api/status', methods=['GET'])
def api_status():
    """
    📊 Get status sistem
    
    Returns:
        - Dataset statistics
        - Model status
        - Training history
        - AI level
    """
    try:
        # Get dataset stats
        stats = app_state['data_manager'].get_dataset_statistics()
        
        # Model status
        model_exists = MODEL_PATH.exists()
        
        # AI Level calculation
        accuracy = app_state['model_accuracy']
        if accuracy < 0.5:
            ai_level = "🥚 AI Telur"
        elif accuracy < 0.7:
            ai_level = "🐣 AI Anak Ayam"
        elif accuracy < 0.85:
            ai_level = "🐥 AI Ayam Muda"
        elif accuracy < 0.95:
            ai_level = "🦅 AI Elang"
        else:
            ai_level = "🚀 AI Roket"
        
        return jsonify({
            'success': True,
            'data': {
                'dataset': {
                    'total_images': stats['total_raw'],
                    'by_category': stats['raw'],
                    'ready_for_training': app_state['data_manager'].check_dataset_ready()['ready']
                },
                'model': {
                    'exists': model_exists,
                    'loaded': app_state['classifier'] is not None,
                    'accuracy': app_state['model_accuracy'],
                    'ai_level': ai_level
                },
                'training': {
                    'total_count': app_state['total_training_count'],
                    'status': app_state['training_status']
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    🔍 Klasifikasi gambar sampah
    
    Request:
        - file: image file (multipart/form-data)
    
    Returns:
        - Predicted class
        - Confidence score
        - All predictions
        - Recommendation
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
            result = app_state['classifier'].predict(filepath)
            
            # Get recommendation
            recommendation = app_state['recommender'].get_recommendation(result['class_name'])
            educational = app_state['recommender'].get_educational_content(result['class_name'])
            
            # Confidence level
            confidence = result['confidence']
            if confidence >= 0.9:
                confidence_level = "Sangat Yakin 🎯"
            elif confidence >= 0.75:
                confidence_level = "Yakin ✅"
            elif confidence >= 0.5:
                confidence_level = "Cukup Yakin 🤔"
            else:
                confidence_level = "Kurang Yakin ⚠️"
            
            return jsonify({
                'success': True,
                'data': {
                    'prediction': {
                        'class_name': result['class_name'],
                        'class_index': result['class_index'],
                        'confidence': result['confidence'],
                        'confidence_percent': result['confidence_percent'],
                        'confidence_level': confidence_level,
                        'icon': CATEGORY_ICONS.get(result['class_name'].lower(), '♻️'),
                        'all_predictions': result['all_predictions']
                    },
                    'recommendation': {
                        'icon': recommendation['icon'],
                        'main_action': recommendation['main_action'],
                        'description': recommendation['description'],
                        'tips': recommendation['tips'],
                        'environmental_impact': recommendation['environmental_impact'],
                        'economic_value': recommendation['economic_value']
                    },
                    'educational': {
                        'fun_fact': educational['fun_fact'],
                        'decompose_time': educational['decompose_time'],
                        'recycle_rate': educational['recycle_rate']
                    }
                }
            })
            
        finally:
            # Cleanup temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error saat prediksi: {str(e)}'
        }), 500

@app.route('/api/upload-training', methods=['POST'])
def api_upload_training():
    """
    📸 Upload gambar untuk data training
    
    Request:
        - file: image file
        - category: waste category (cardboard/glass/metal/paper/plastic)
    
    Returns:
        - Success status
        - Message
        - Updated statistics
    """
    try:
        # Cek file upload
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Tidak ada file yang diupload'
            }), 400
        
        file = request.files['file']
        category = request.form.get('category', '').lower()
        
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
        
        if category not in WASTE_CATEGORIES:
            return jsonify({
                'success': False,
                'error': f'Kategori tidak valid. Pilih: {", ".join(WASTE_CATEGORIES.keys())}'
            }), 400
        
        # Add to dataset
        result = app_state['data_manager'].add_image(file, category)
        
        if result['success']:
            # Get updated stats
            stats = app_state['data_manager'].get_dataset_statistics()
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'data': {
                    'category': category,
                    'category_count': stats['raw'].get(category, 0),
                    'total_images': stats['total_raw']
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error saat upload: {str(e)}'
        }), 500

@app.route('/api/train', methods=['POST'])
def api_train():
    """
    🧠 Mulai training model
    
    Request (JSON):
        - epochs: jumlah epoch (default: 20)
        - learning_rate: learning rate (default: 0.001)
        - batch_size: batch size (default: 32)
    
    Returns:
        - Success status
        - Training job ID (untuk tracking)
    """
    try:
        # Cek apakah sudah ada training yang berjalan
        if app_state['training_status']['in_progress']:
            return jsonify({
                'success': False,
                'error': 'Training sudah berjalan. Tunggu hingga selesai.'
            }), 400
        
        # Cek dataset ready
        ready_check = app_state['data_manager'].check_dataset_ready()
        if not ready_check['ready']:
            return jsonify({
                'success': False,
                'error': ready_check['recommendation']
            }), 400
        
        # Get parameters
        data = request.get_json() or {}
        epochs = data.get('epochs', 20)
        learning_rate = data.get('learning_rate', 0.001)
        batch_size = data.get('batch_size', 32)
        
        # Validasi parameters
        if not isinstance(epochs, int) or epochs < 5 or epochs > 100:
            return jsonify({
                'success': False,
                'error': 'Epochs harus antara 5-100'
            }), 400
        
        if not isinstance(learning_rate, (int, float)) or learning_rate <= 0:
            return jsonify({
                'success': False,
                'error': 'Learning rate harus > 0'
            }), 400
        
        if batch_size not in [8, 16, 32, 64]:
            return jsonify({
                'success': False,
                'error': 'Batch size harus 8, 16, 32, atau 64'
            }), 400
        
        # Generate training ID
        training_id = f"train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Update training status
        app_state['training_status'] = {
            'in_progress': True,
            'training_id': training_id,
            'current_epoch': 0,
            'total_epochs': epochs,
            'progress': 0,
            'message': 'Mempersiapkan dataset...',
            'accuracy': 0,
            'loss': 0,
            'start_time': datetime.now().isoformat()
        }
        
        # Run training di background thread
        def run_training():
            try:
                # Prepare dataset
                split_result = app_state['data_manager'].split_dataset()
                if not split_result['success']:
                    app_state['training_status']['in_progress'] = False
                    app_state['training_status']['message'] = f"Error: {split_result['message']}"
                    return
                
                # Progress callback
                def progress_callback(epoch_data):
                    app_state['training_status'].update({
                        'current_epoch': epoch_data['epoch'],
                        'progress': epoch_data['epoch'] / epochs * 100,
                        'message': f"Training epoch {epoch_data['epoch']}/{epochs}",
                        'accuracy': epoch_data['accuracy'],
                        'val_accuracy': epoch_data['val_accuracy'],
                        'loss': epoch_data['loss'],
                        'val_loss': epoch_data['val_loss']
                    })
                
                # Train model
                ModelTrainer = _get_trainer()
                trainer = ModelTrainer(str(PROCESSED_DATA_DIR), str(MODEL_PATH))
                result = trainer.train(
                    epochs=epochs,
                    learning_rate=learning_rate,
                    batch_size=batch_size,
                    progress_callback=progress_callback
                )
                
                if result['success']:
                    # Update app state
                    app_state['model_accuracy'] = result['test_accuracy']
                    app_state['total_training_count'] += 1
                    app_state['classifier'] = None  # Force reload
                    
                    # Reload classifier
                    app_state['classifier'] = WasteClassifier(str(MODEL_PATH), str(LABELS_PATH))
                    
                    # Save training log
                    log_file = TRAINING_LOGS_DIR / f"training_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(log_file, 'w') as f:
                        json.dump({
                            'training_id': training_id,
                            'timestamp': datetime.now().isoformat(),
                            'parameters': {
                                'epochs': epochs,
                                'learning_rate': learning_rate,
                                'batch_size': batch_size
                            },
                            'results': {
                                'test_accuracy': result['test_accuracy'],
                                'final_train_accuracy': result['final_train_accuracy'],
                                'final_val_accuracy': result['final_val_accuracy']
                            },
                            'history': result['history']
                        }, f, indent=2)
                    
                    app_state['training_status'].update({
                        'in_progress': False,
                        'progress': 100,
                        'message': f'Training selesai! Akurasi: {result["test_accuracy"]*100:.2f}%',
                        'completed': True,
                        'test_accuracy': result['test_accuracy'],
                        'end_time': datetime.now().isoformat()
                    })
                else:
                    app_state['training_status'].update({
                        'in_progress': False,
                        'message': f'Training gagal: {result.get("error", "Unknown error")}',
                        'completed': False,
                        'error': result.get('error')
                    })
            
            except Exception as e:
                app_state['training_status'].update({
                    'in_progress': False,
                    'message': f'Error: {str(e)}',
                    'completed': False,
                    'error': str(e)
                })
                traceback.print_exc()
        
        # Start training thread
        training_thread = threading.Thread(target=run_training)
        training_thread.daemon = True
        training_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Training dimulai!',
            'data': {
                'training_id': training_id,
                'epochs': epochs,
                'learning_rate': learning_rate,
                'batch_size': batch_size
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error saat memulai training: {str(e)}'
        }), 500

@app.route('/api/training-status', methods=['GET'])
def api_training_status():
    """
    📊 Get status training yang sedang berjalan
    
    Returns:
        - Training progress
        - Current metrics
        - Estimated time remaining
    """
    return jsonify({
        'success': True,
        'data': app_state['training_status']
    })

@app.route('/api/categories', methods=['GET'])
def api_categories():
    """
    📋 Get daftar kategori sampah
    
    Returns:
        - List kategori dengan icon dan deskripsi
    """
    categories = []
    for key, name in WASTE_CATEGORIES.items():
        categories.append({
            'id': key,
            'name': name,
            'icon': CATEGORY_ICONS.get(key, '♻️')
        })
    
    return jsonify({
        'success': True,
        'data': {
            'categories': categories
        }
    })

# 🚫 ERROR HANDLERS

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Endpoint tidak ditemukan'
        }), 404
    return render_template('index.html')  # SPA fallback

@app.errorhandler(413)
def too_large(error):
    """Handle file too large"""
    return jsonify({
        'success': False,
        'error': 'File terlalu besar. Maksimal 16MB'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Terjadi kesalahan server'
    }), 500

# 🚀 STARTUP
if __name__ == '__main__':
    # Initialize backend
    init_backend()
    
    # Get port from environment (untuk deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run Flask app
    print(f"\n🚀 Starting Flask server on port {port}...")
    print(f"🌍 Access at: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/api/status\n")
    
    # Development mode: debug=True
    # Production mode: debug=False
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
