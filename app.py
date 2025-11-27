"""
🌍 SMART WASTE CLASSIFIER - APLIKASI UTAMA
Aplikasi Pembelajaran Machine Learning untuk Klasifikasi Sampah

Dibuat untuk: Siswa SMP
Tujuan: Belajar AI sambil peduli lingkungan
"""

import streamlit as st
from streamlit_option_menu import option_menu
import os
from pathlib import Path
from PIL import Image
import time

# Import modules
from modules.classifier import WasteClassifier
from modules.data_manager import DataManager
from modules.trainer import ModelTrainer
from modules.recommender import WasteRecommender
from utils.visualizer import (
    plot_training_history_interactive, 
    plot_prediction_confidence,
    plot_dataset_distribution,
    plot_ai_level_progress
)
from config import (
    MODEL_PATH, LABELS_PATH, RAW_DATA_DIR, PROCESSED_DATA_DIR,
    WASTE_CATEGORIES, CATEGORY_ICONS, EDUCATIONAL_CONTENT,
    AI_LEVELS, MESSAGES, DEFAULT_TRAINING_PARAMS
)

# 🎨 PAGE CONFIG
st.set_page_config(
    page_title="Smart Waste Classifier",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📱 CUSTOM CSS
def load_custom_css():
    """Load custom CSS untuk tema eco-green"""
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #2ECC71;
            --secondary-color: #27AE60;
            --accent-color: #F39C12;
            --background-color: #E8F8F5;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
        }
        
        .main-header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        /* Card styling */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #2ECC71;
        }
        
        .success-box {
            background: #D5F4E6;
            border-left: 4px solid #2ECC71;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background: #FEF5E7;
            border-left: 4px solid #F39C12;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .info-box {
            background: #EBF5FB;
            border-left: 4px solid #3498DB;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(46, 204, 113, 0.3);
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #2ECC71;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background-color: #2ECC71;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #E8F8F5 0%, #D5F4E6 100%);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 5px;
            background-color: #E8F8F5;
            color: #2C3E50;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
            color: white;
        }
        
        /* Educational boxes */
        .edu-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .edu-card h3 {
            margin-top: 0;
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)

# 🎯 INITIALIZE SESSION STATE
def init_session_state():
    """Inisialisasi session state variables"""
    if 'classifier' not in st.session_state:
        st.session_state.classifier = None
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    if 'recommender' not in st.session_state:
        st.session_state.recommender = WasteRecommender()
    if 'training_in_progress' not in st.session_state:
        st.session_state.training_in_progress = False
    if 'model_accuracy' not in st.session_state:
        st.session_state.model_accuracy = 0.0
    if 'total_training_count' not in st.session_state:
        st.session_state.total_training_count = 0

# 🏠 HALAMAN HOME
def page_home():
    """Halaman utama - Welcome & Info"""
    
    # Header
    st.markdown("""
        <div class="main-header animate-fade-in">
            <h1>♻️ Smart Waste Classifier</h1>
            <p>Mesin Belajar Memilah Sampah - Pembelajaran AI untuk Siswa</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="info-card animate-fade-in">
                <h2 style="color: #2ECC71; text-align: center;">🌍 Selamat Datang!</h2>
                <p style="text-align: center; font-size: 1.1rem;">
                    <b>Manfaatkan sampahmu untuk sumber belajar AI dalam memilah sampah</b>
                </p>
                <hr style="border-color: #2ECC71;">
                <p>
                    Aplikasi ini membantu kamu belajar tentang <b>Artificial Intelligence (AI)</b> 
                    sambil peduli lingkungan! 🤖🌱
                </p>
                <p>
                    Kamu akan:
                    <ul>
                        <li>📸 Menambah data training dari foto sampah</li>
                        <li>🧠 Melatih AI untuk mengenali jenis sampah</li>
                        <li>🔍 Mengklasifikasi sampah secara otomatis</li>
                        <li>♻️ Mendapat rekomendasi pengelolaan sampah</li>
                    </ul>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics
    st.subheader("📊 Status Sistem")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get statistics
    stats = st.session_state.data_manager.get_dataset_statistics()
    
    with col1:
        st.metric(
            label="📦 Total Data",
            value=stats['total_raw'],
            delta="gambar"
        )
    
    with col2:
        st.metric(
            label="🧠 AI Level",
            value=get_ai_level_name(st.session_state.model_accuracy),
            delta=f"{st.session_state.model_accuracy*100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="🎓 Training Count",
            value=st.session_state.total_training_count,
            delta="kali"
        )
    
    with col4:
        model_status = "✅ Ready" if os.path.exists(MODEL_PATH) else "⚠️ Perlu Training"
        st.metric(
            label="🤖 Model Status",
            value=model_status
        )
    
    # Dataset distribution
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📈 Distribusi Dataset")
    
    fig = plot_dataset_distribution(stats)
    st.plotly_chart(fig, use_container_width=True, key="home_dataset_distribution")
    
    # Info cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="success-box">
                <h3>✨ Fitur Utama</h3>
                <ul>
                    <li><b>📸 Tambah Data</b>: Upload foto sampah untuk training</li>
                    <li><b>🧠 Training Model</b>: Latih AI dengan parameter custom</li>
                    <li><b>🔍 Klasifikasi</b>: Identifikasi jenis sampah otomatis</li>
                    <li><b>♻️ Rekomendasi</b>: Tips pengelolaan sampah</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-box">
                <h3>🎓 Kategori Sampah</h3>
                <ul>
                    <li>📦 <b>Cardboard</b> - Kardus & karton</li>
                    <li>🫙 <b>Glass</b> - Kaca & botol kaca</li>
                    <li>🔩 <b>Metal</b> - Logam & kaleng</li>
                    <li>📄 <b>Paper</b> - Kertas</li>
                    <li>🥤 <b>Plastic</b> - Plastik</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# 📸 HALAMAN TAMBAH DATA
def page_add_data():
    """Halaman untuk menambah data training"""
    
    st.title("📸 Tambah Data Training")
    st.markdown("Upload foto sampah untuk memperkaya dataset AI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class="info-box">
                <h3>📋 Panduan Upload</h3>
                <ol>
                    <li>Pilih foto sampah yang jelas</li>
                    <li>Pilih kategori yang sesuai</li>
                    <li>Klik "Tambah ke Dataset"</li>
                </ol>
                <p><b>Tips:</b> Foto yang bagus = AI yang lebih pintar! 📸</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Upload form
        uploaded_file = st.file_uploader(
            "Pilih foto sampah",
            type=['jpg', 'jpeg', 'png'],
            help="Format: JPG, JPEG, atau PNG"
        )
        
        if uploaded_file is not None:
            # Preview image
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview Gambar", use_container_width=True)
            
            # Select category
            category = st.selectbox(
                "Pilih Kategori Sampah",
                options=list(WASTE_CATEGORIES.keys()),
                format_func=lambda x: f"{CATEGORY_ICONS.get(x, '♻️')} {WASTE_CATEGORIES[x]}"
            )
            
            # Add button
            if st.button("➕ Tambah ke Dataset", type="primary"):
                with st.spinner("Menambahkan gambar..."):
                    result = st.session_state.data_manager.add_image(
                        uploaded_file,
                        category
                    )
                    
                    if result['success']:
                        st.success(result['message'])
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result['message'])
    
    with col2:
        st.markdown("### 📊 Dataset Saat Ini")
        
        stats = st.session_state.data_manager.get_dataset_statistics()
        
        for category, count in stats['raw'].items():
            icon = CATEGORY_ICONS.get(category, '♻️')
            st.metric(
                label=f"{icon} {WASTE_CATEGORIES[category]}",
                value=f"{count} gambar"
            )
        
        st.markdown("---")
        
        # Dataset ready check
        ready_check = st.session_state.data_manager.check_dataset_ready()
        
        if ready_check['ready']:
            st.markdown("""
                <div class="success-box">
                    <b>✅ Dataset Siap!</b><br>
                    Kamu bisa mulai training model sekarang!
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="warning-box">
                    <b>⚠️ Dataset Belum Cukup</b><br>
                    {ready_check['recommendation']}
                </div>
            """, unsafe_allow_html=True)

# 🧠 HALAMAN TRAINING
def page_training():
    """Halaman untuk training model"""
    
    st.title("🧠 Training Model AI")
    st.markdown("Latih AI untuk mengenali jenis sampah dengan parameter yang bisa kamu atur!")
    
    # Check if dataset ready
    ready_check = st.session_state.data_manager.check_dataset_ready()
    
    if not ready_check['ready']:
        st.warning("⚠️ Dataset belum cukup untuk training! Tambahkan lebih banyak gambar dulu.")
        st.info(f"📊 Total gambar: {ready_check['total_images']} (minimal {ready_check['min_required']})")
        return
    
    # Educational content
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🎓 Apa itu Epoch?", expanded=False):
            edu = EDUCATIONAL_CONTENT['epoch']
            st.markdown(f"""
                **{edu['title']}**
                
                {edu['description']}
                
                **Analogi:** {edu['analogy']}
                
                💡 {edu['tips']}
            """)
    
    with col2:
        with st.expander("🎓 Apa itu Learning Rate?", expanded=False):
            edu = EDUCATIONAL_CONTENT['learning_rate']
            st.markdown(f"""
                **{edu['title']}**
                
                {edu['description']}
                
                **Analogi:** {edu['analogy']}
                
                💡 {edu['tips']}
            """)
    
    st.markdown("---")
    
    # Training parameters
    st.subheader("⚙️ Pengaturan Training")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        epochs = st.slider(
            "🔄 Jumlah Epoch",
            min_value=5,
            max_value=100,
            value=DEFAULT_TRAINING_PARAMS['epochs'],
            step=5,
            help="Semakin banyak epoch, semakin lama AI belajar"
        )
    
    with col2:
        learning_rate = st.select_slider(
            "⚡ Learning Rate",
            options=[0.0001, 0.0005, 0.001, 0.005, 0.01],
            value=DEFAULT_TRAINING_PARAMS['learning_rate'],
            help="Kecepatan belajar AI"
        )
    
    with col3:
        batch_size = st.selectbox(
            "📦 Batch Size",
            options=[8, 16, 32, 64],
            index=2,
            help="Jumlah gambar per batch"
        )
    
    # Estimate training time
    stats = st.session_state.data_manager.get_dataset_statistics()
    estimated_time = estimate_training_time(stats['total_raw'], epochs, batch_size)
    
    st.info(f"⏱️ Estimasi waktu training: **{estimated_time}**")
    
    # Training button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not st.session_state.training_in_progress:
        if st.button("🚀 Mulai Training!", type="primary", use_container_width=True):
            st.session_state.training_in_progress = True
            st.rerun()
    
    # Training process
    if st.session_state.training_in_progress:
        st.markdown("""
            <div class="info-box">
                <h3>🧠 AI Sedang Belajar...</h3>
                <p>Proses training sedang berlangsung. Silakan tunggu hingga selesai.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Prepare data first
        with st.spinner("📦 Mempersiapkan dataset..."):
            split_result = st.session_state.data_manager.split_dataset()
            if not split_result['success']:
                st.error(f"❌ Error: {split_result['message']}")
                st.session_state.training_in_progress = False
                return
            st.success("✅ Dataset berhasil dipersiapkan!")
        
        # Progress containers
        progress_bar = st.progress(0)
        status_text = st.empty()
        metrics_container = st.container()
        chart_container = st.container()
        
        # Training metrics storage
        training_metrics = {
            'accuracy': [],
            'val_accuracy': [],
            'loss': [],
            'val_loss': []
        }
        
        # Progress callback
        def update_progress(epoch_data):
            epoch = epoch_data['epoch']
            progress = epoch / epochs
            
            progress_bar.progress(progress)
            status_text.markdown(f"""
                **Epoch {epoch}/{epochs}** | 
                Loss: {epoch_data['loss']:.4f} | 
                Accuracy: {epoch_data['accuracy']*100:.2f}% | 
                ETA: {epoch_data['eta']:.1f}s
            """)
            
            # Update metrics
            training_metrics['accuracy'].append(epoch_data['accuracy'])
            training_metrics['val_accuracy'].append(epoch_data['val_accuracy'])
            training_metrics['loss'].append(epoch_data['loss'])
            training_metrics['val_loss'].append(epoch_data['val_loss'])
            
            # Update chart
            if len(training_metrics['accuracy']) > 0:
                with chart_container:
                    fig = plot_training_history_interactive(training_metrics)
                    st.plotly_chart(fig, use_container_width=True, key=f"training_progress_chart_epoch_{epoch}")
            
            # Update metrics display
            with metrics_container:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📊 Train Acc", f"{epoch_data['accuracy']*100:.2f}%")
                col2.metric("✅ Val Acc", f"{epoch_data['val_accuracy']*100:.2f}%")
                col3.metric("📉 Train Loss", f"{epoch_data['loss']:.4f}")
                col4.metric("📈 Val Loss", f"{epoch_data['val_loss']:.4f}")
        
        # Start training
        trainer = ModelTrainer(PROCESSED_DATA_DIR, MODEL_PATH)
        result = trainer.train(
            epochs=epochs,
            learning_rate=learning_rate,
            batch_size=batch_size,
            progress_callback=update_progress
        )
        
        # Training completed
        st.session_state.training_in_progress = False
        
        if result['success']:
            st.success("🎉 Training selesai!")
            st.balloons()
            
            # Update session state
            st.session_state.model_accuracy = result['test_accuracy']
            st.session_state.total_training_count += 1
            st.session_state.classifier = None  # Force reload
            
            # Show final results
            st.markdown("---")
            st.subheader("📊 Hasil Training")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🎯 Training Accuracy",
                    f"{result['final_train_accuracy']*100:.2f}%"
                )
            
            with col2:
                st.metric(
                    "✅ Validation Accuracy",
                    f"{result['final_val_accuracy']*100:.2f}%"
                )
            
            with col3:
                st.metric(
                    "🧪 Test Accuracy",
                    f"{result['test_accuracy']*100:.2f}%"
                )
            
            # AI Level
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🎮 Level AI")
            fig = plot_ai_level_progress(result['test_accuracy'])
            st.plotly_chart(fig, use_container_width=True, key="training_result_ai_level")
            
            # Final chart
            st.subheader("📈 Training History")
            fig = plot_training_history_interactive(result['history'])
            st.plotly_chart(fig, use_container_width=True, key="training_final_history")
            
        else:
            st.error(f"❌ Training gagal: {result.get('error', 'Unknown error')}")

# 🔍 HALAMAN KLASIFIKASI
def page_classification():
    """Halaman untuk klasifikasi sampah"""
    
    st.title("🔍 Klasifikasi Sampah")
    st.markdown("Upload foto sampah untuk diidentifikasi oleh AI")
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        st.warning("⚠️ Model belum tersedia! Silakan training model terlebih dahulu.")
        return
    
    # Load classifier
    if st.session_state.classifier is None:
        with st.spinner("🔄 Loading model..."):
            st.session_state.classifier = WasteClassifier(MODEL_PATH, LABELS_PATH)
            st.success("✅ Model berhasil dimuat!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload image
        uploaded_file = st.file_uploader(
            "Upload foto sampah untuk diklasifikasi",
            type=['jpg', 'jpeg', 'png'],
            key="classify_uploader"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar yang akan diklasifikasi", use_container_width=True)
            
            # Classify button
            if st.button("🎯 Klasifikasikan!", type="primary", use_container_width=True):
                with st.spinner("🧠 AI sedang menganalisis..."):
                    # Predict
                    result = st.session_state.classifier.predict_from_pil_image(image)
                    
                    # Show results
                    st.markdown("---")
                    st.markdown("## 🎯 Hasil Klasifikasi")
                    
                    # Main result
                    icon = st.session_state.recommender.get_icon(result['class_name'])
                    confidence_level = st.session_state.classifier.get_confidence_level(result['confidence'])
                    
                    st.markdown(f"""
                        <div class="success-box" style="text-align: center;">
                            <h1>{icon}</h1>
                            <h2>{result['class_name']}</h2>
                            <h3>Confidence: {result['confidence_percent']:.2f}%</h3>
                            <p>{confidence_level}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Confidence chart
                    st.subheader("📊 Confidence Score per Kategori")
                    fig = plot_prediction_confidence(result['all_predictions'])
                    st.plotly_chart(fig, use_container_width=True, key="classification_confidence_chart")
                    
                    # Recommendation
                    st.markdown("---")
                    st.markdown("## ♻️ Rekomendasi Pengelolaan")
                    
                    rec = st.session_state.recommender.get_recommendation(result['class_name'])
                    
                    st.markdown(f"""
                        <div class="info-card">
                            <h3>{rec['icon']} {rec['main_action']}</h3>
                            <p>{rec['description']}</p>
                            <br>
                            <h4>💡 Tips Praktis:</h4>
                            <ul>
                    """, unsafe_allow_html=True)
                    
                    for tip in rec['tips']:
                        st.markdown(f"<li>{tip}</li>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                            </ul>
                            <br>
                            <p><b>🌍 Dampak Lingkungan:</b> {rec['environmental_impact']}</p>
                            <p><b>💰 Nilai Ekonomis:</b> {rec['economic_value']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Educational content
                    edu = st.session_state.recommender.get_educational_content(result['class_name'])
                    
                    st.markdown("---")
                    st.markdown("## 🎓 Fakta Menarik")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.info(edu['fun_fact'])
                    
                    with col_b:
                        st.info(edu['decompose_time'])
                    
                    with col_c:
                        st.info(edu['recycle_rate'])
    
    with col2:
        st.markdown("### 🎯 Tips Klasifikasi")
        
        st.markdown("""
            <div class="info-box">
                <h4>📸 Foto yang Baik:</h4>
                <ul>
                    <li>Cahaya cukup terang</li>
                    <li>Objek terlihat jelas</li>
                    <li>Fokus pada sampah</li>
                    <li>Tidak blur/buram</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Statistik Model")
        
        if st.session_state.model_accuracy > 0:
            st.metric(
                "🎯 Model Accuracy",
                f"{st.session_state.model_accuracy*100:.2f}%"
            )
            
            ai_level = get_ai_level_name(st.session_state.model_accuracy)
            st.metric(
                "🎮 AI Level",
                ai_level
            )
        else:
            st.info("📊 Belum ada data training")

# 📚 HALAMAN EDUKASI
def page_education():
    """Halaman edukasi tentang AI dan sampah"""
    
    st.title("📚 Pusat Edukasi")
    st.markdown("Pelajari lebih lanjut tentang AI dan pengelolaan sampah")
    
    tab1, tab2, tab3 = st.tabs(["🤖 Tentang AI", "♻️ Tentang Sampah", "🎮 Level AI"])
    
    with tab1:
        st.header("🤖 Apa itu Artificial Intelligence?")
        
        st.markdown("""
            <div class="info-card">
                <h3>Definisi AI</h3>
                <p>
                    <b>Artificial Intelligence (AI)</b> atau Kecerdasan Buatan adalah 
                    kemampuan mesin untuk "belajar" dan "berpikir" seperti manusia.
                </p>
                <p>
                    Di aplikasi ini, AI belajar mengenali jenis sampah dari foto-foto 
                    yang kamu upload. Semakin banyak data, semakin pintar AI-nya!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔄 Bagaimana AI Belajar?")
            st.markdown("""
                1. **Input Data**: AI diberi banyak foto sampah dengan labelnya
                2. **Training**: AI mencari pola dari foto-foto tersebut
                3. **Testing**: AI diuji dengan foto baru
                4. **Prediksi**: AI bisa mengenali jenis sampah baru!
            """)
        
        with col2:
            st.markdown("### 📊 Istilah Penting")
            
            for key, value in EDUCATIONAL_CONTENT.items():
                with st.expander(f"{value['title']}"):
                    st.markdown(f"""
                        **Deskripsi:** {value['description']}
                        
                        **Analogi:** {value.get('analogy', 'N/A')}
                        
                        **Tips:** {value.get('tips', 'N/A')}
                    """)
    
    with tab2:
        st.header("♻️ Pengelolaan Sampah")
        
        st.markdown("""
            <div class="success-box">
                <h3>🌍 Mengapa Pemilahan Sampah Penting?</h3>
                <p>
                    Sampah yang dipilah dengan benar bisa:
                    <ul>
                        <li>♻️ Didaur ulang menjadi produk baru</li>
                        <li>🌳 Mengurangi penebangan pohon</li>
                        <li>💰 Bernilai ekonomis</li>
                        <li>🌊 Mengurangi pencemaran</li>
                    </ul>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Panduan Lengkap per Jenis Sampah")
        
        for waste_type in WASTE_CATEGORIES.values():
            with st.expander(f"{st.session_state.recommender.get_icon(waste_type)} {waste_type}"):
                rec = st.session_state.recommender.get_recommendation(waste_type)
                edu = st.session_state.recommender.get_educational_content(waste_type)
                
                st.markdown(f"**Aksi:** {rec['main_action']}")
                st.markdown(f"**Deskripsi:** {rec['description']}")
                st.markdown("**Tips:**")
                for tip in rec['tips']:
                    st.markdown(f"- {tip}")
                st.markdown(f"**Dampak:** {rec['environmental_impact']}")
                st.markdown(f"**Fakta Menarik:** {edu['fun_fact']}")
    
    with tab3:
        st.header("🎮 Sistem Level AI")
        
        st.markdown("""
            <div class="edu-card">
                <h3>🏆 Tingkatkan Level AI-mu!</h3>
                <p>
                    Semakin sering training dengan data yang bagus, 
                    semakin tinggi level AI-mu!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Level & Badge")
        
        for level_data in AI_LEVELS.values():
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                st.markdown(f"## {level_data['name']}")
            
            with col2:
                st.metric("Accuracy Required", f"{level_data['accuracy']}%+")
            
            with col3:
                st.metric("Badge", level_data['badge'])
        
        # Current level
        st.markdown("---")
        st.markdown("### 🎯 Level Saat Ini")
        
        if st.session_state.model_accuracy > 0:
            fig = plot_ai_level_progress(st.session_state.model_accuracy)
            st.plotly_chart(fig, use_container_width=True, key="education_current_ai_level")
        else:
            st.info("Belum ada model terlatih. Mulai training untuk mendapat level!")

# 🔧 HELPER FUNCTIONS
def get_ai_level_name(accuracy: float) -> str:
    """Get AI level name berdasarkan accuracy"""
    if accuracy < 0.5:
        return "🥚 AI Telur"
    elif accuracy < 0.7:
        return "🐣 AI Anak Ayam"
    elif accuracy < 0.85:
        return "🐥 AI Ayam Muda"
    elif accuracy < 0.95:
        return "🦅 AI Elang"
    else:
        return "🚀 AI Roket"

def estimate_training_time(total_images: int, epochs: int, batch_size: int) -> str:
    """Estimasi waktu training"""
    # Rough estimate: ~0.1s per batch per epoch
    batches_per_epoch = max(total_images // batch_size, 1)
    total_seconds = batches_per_epoch * epochs * 0.1
    
    if total_seconds < 60:
        return f"{total_seconds:.0f} detik"
    elif total_seconds < 3600:
        return f"{total_seconds/60:.1f} menit"
    else:
        return f"{total_seconds/3600:.1f} jam"

# 🎯 MAIN APP
def main():
    """Main application"""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌍 Smart Waste Classifier")
        st.markdown("---")
        
        page = option_menu(
            menu_title=None,
            options=["🏠 Home", "📸 Tambah Data", "🧠 Training", "🔍 Klasifikasi", "📚 Edukasi"],
            icons=["house", "camera", "brain", "search", "book"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#2ECC71", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "padding": "10px",
                    "border-radius": "5px"
                },
                "nav-link-selected": {"background-color": "#2ECC71", "color": "white"},
            }
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        stats = st.session_state.data_manager.get_dataset_statistics()
        st.metric("Total Data", stats['total_raw'])
        st.metric("Training Count", st.session_state.total_training_count)
        
        if st.session_state.model_accuracy > 0:
            st.metric("AI Accuracy", f"{st.session_state.model_accuracy*100:.1f}%")
        
        st.markdown("---")
        st.markdown("### ℹ️ Info")
        st.info("Aplikasi pembelajaran AI untuk siswa SMP. Dibuat dengan ❤️ untuk pendidikan.")
    
    # Route to pages
    if page == "🏠 Home":
        page_home()
    elif page == "📸 Tambah Data":
        page_add_data()
    elif page == "🧠 Training":
        page_training()
    elif page == "🔍 Klasifikasi":
        page_classification()
    elif page == "📚 Edukasi":
        page_education()

# 🚀 RUN APP
if __name__ == "__main__":
    main()
