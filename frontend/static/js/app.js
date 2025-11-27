/**
 * 🌍 SMART WASTE CLASSIFIER - FRONTEND JAVASCRIPT
 * ================================================
 * Handles all frontend interactions dengan Flask API
 * 
 * Features:
 * - Page navigation
 * - API communication
 * - File uploads
 * - Training monitoring
 * - Real-time updates
 */

// 🌐 API Configuration
const API_BASE = window.location.origin;
const API = {
    STATUS: `${API_BASE}/api/status`,
    PREDICT: `${API_BASE}/api/predict`,
    UPLOAD_TRAINING: `${API_BASE}/api/upload-training`,
    TRAIN: `${API_BASE}/api/train`,
    TRAINING_STATUS: `${API_BASE}/api/training-status`,
    CATEGORIES: `${API_BASE}/api/categories`
};

// 🎨 Global State
let appState = {
    currentPage: 'home',
    systemStatus: null,
    trainingInterval: null,
    charts: {}
};

// ============================================
// 🚀 INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🌍 Smart Waste Classifier initialized');
    
    // Setup navigation
    setupNavigation();
    
    // Setup file uploads
    setupFileUploads();
    
    // Setup training controls
    setupTrainingControls();
    
    // Setup education tabs
    setupEducationTabs();
    
    // Load initial status
    loadSystemStatus();
    
    // Auto-refresh status setiap 30 detik
    setInterval(loadSystemStatus, 30000);
});

// ============================================
// 🧭 NAVIGATION
// ============================================

function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const pageName = this.dataset.page;
            navigateToPage(pageName);
        });
    });
}

function navigateToPage(pageName) {
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.page === pageName) {
            btn.classList.add('active');
        }
    });
    
    // Update pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(`page-${pageName}`).classList.add('active');
    
    appState.currentPage = pageName;
    
    // Load page-specific data
    switch(pageName) {
        case 'home':
            loadSystemStatus();
            break;
        case 'upload':
            loadDatasetStats();
            break;
        case 'train':
            checkTrainingStatus();
            break;
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================
// 📊 SYSTEM STATUS
// ============================================

async function loadSystemStatus() {
    try {
        const response = await fetch(API.STATUS);
        const result = await response.json();
        
        if (result.success) {
            appState.systemStatus = result.data;
            updateStatsBar(result.data);
            updateHomeChart(result.data.dataset.by_category);
        }
    } catch (error) {
        console.error('Error loading status:', error);
    }
}

function updateStatsBar(data) {
    // Update stats
    document.getElementById('stat-total-images').textContent = data.dataset.total_images;
    document.getElementById('stat-ai-level').textContent = data.model.ai_level;
    document.getElementById('stat-accuracy').textContent = 
        data.model.accuracy > 0 ? `${(data.model.accuracy * 100).toFixed(1)}%` : '0%';
    document.getElementById('stat-training-count').textContent = data.training.total_count;
}

function updateHomeChart(categoryData) {
    const canvas = document.getElementById('datasetCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart
    if (appState.charts.dataset) {
        appState.charts.dataset.destroy();
    }
    
    // Prepare data
    const labels = Object.keys(categoryData).map(k => k.charAt(0).toUpperCase() + k.slice(1));
    const values = Object.values(categoryData);
    
    // Create chart
    appState.charts.dataset = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Jumlah Gambar',
                data: values,
                backgroundColor: [
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(155, 89, 182, 0.8)',
                    'rgba(241, 196, 15, 0.8)',
                    'rgba(230, 126, 34, 0.8)'
                ],
                borderColor: [
                    'rgba(46, 204, 113, 1)',
                    'rgba(52, 152, 219, 1)',
                    'rgba(155, 89, 182, 1)',
                    'rgba(241, 196, 15, 1)',
                    'rgba(230, 126, 34, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// ============================================
// 📤 FILE UPLOADS
// ============================================

function setupFileUploads() {
    // Classify upload
    setupClassifyUpload();
    
    // Training data upload
    setupTrainingDataUpload();
}

function setupClassifyUpload() {
    const fileInput = document.getElementById('classify-file-input');
    const uploadBox = document.getElementById('classify-upload-box');
    const preview = document.getElementById('classify-preview');
    const previewImg = document.getElementById('classify-preview-img');
    const classifyBtn = document.getElementById('classify-btn');
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            previewClassifyImage(file);
        }
    });
    
    // Drag & Drop
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('drag-over');
    });
    
    uploadBox.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
    });
    
    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            previewClassifyImage(file);
        }
    });
    
    // Classify button
    classifyBtn.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (file) {
            classifyImage(file);
        }
    });
}

function previewClassifyImage(file) {
    const uploadBox = document.getElementById('classify-upload-box');
    const preview = document.getElementById('classify-preview');
    const previewImg = document.getElementById('classify-preview-img');
    
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        uploadBox.style.display = 'none';
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function resetClassifyPage() {
    document.getElementById('classify-upload-box').style.display = 'block';
    document.getElementById('classify-preview').style.display = 'none';
    document.getElementById('classify-result').style.display = 'none';
    document.getElementById('classify-file-input').value = '';
}

async function classifyImage(file) {
    const classifyBtn = document.getElementById('classify-btn');
    const resultContainer = document.getElementById('classify-result');
    
    // Disable button
    classifyBtn.disabled = true;
    classifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Menganalisis...';
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        
        // Send request
        const response = await fetch(API.PREDICT, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayClassificationResult(result.data);
            resultContainer.style.display = 'block';
            
            // Scroll to result
            setTimeout(() => {
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        } else {
            showToast(result.error || 'Gagal mengklasifikasi gambar', 'error');
        }
    } catch (error) {
        console.error('Classification error:', error);
        showToast('Terjadi kesalahan saat mengklasifikasi', 'error');
    } finally {
        classifyBtn.disabled = false;
        classifyBtn.innerHTML = '<i class="fas fa-magic"></i> Klasifikasikan Sekarang!';
    }
}

function displayClassificationResult(data) {
    const pred = data.prediction;
    const rec = data.recommendation;
    const edu = data.educational;
    
    // Main result
    document.getElementById('result-icon').textContent = pred.icon;
    document.getElementById('result-class').textContent = pred.class_name;
    document.getElementById('result-confidence-text').textContent = `${pred.confidence_percent.toFixed(2)}%`;
    document.getElementById('result-confidence-level').textContent = pred.confidence_level;
    
    // Confidence chart
    displayConfidenceChart(pred.all_predictions);
    
    // Recommendation
    const recContent = document.getElementById('recommendation-content');
    recContent.innerHTML = `
        <h4>${rec.icon} ${rec.main_action}</h4>
        <p>${rec.description}</p>
        <h5>💡 Tips Praktis:</h5>
        <ul>
            ${rec.tips.map(tip => `<li>${tip}</li>`).join('')}
        </ul>
        <p><strong>🌍 Dampak Lingkungan:</strong> ${rec.environmental_impact}</p>
        <p><strong>💰 Nilai Ekonomis:</strong> ${rec.economic_value}</p>
    `;
    
    // Educational facts
    const eduFacts = document.getElementById('edu-facts');
    eduFacts.innerHTML = `
        <div class="edu-fact-card">
            <strong>🎓 Fakta Menarik</strong>
            <p>${edu.fun_fact}</p>
        </div>
        <div class="edu-fact-card">
            <strong>⏱️ Waktu Terurai</strong>
            <p>${edu.decompose_time}</p>
        </div>
        <div class="edu-fact-card">
            <strong>♻️ Tingkat Daur Ulang</strong>
            <p>${edu.recycle_rate}</p>
        </div>
    `;
}

function displayConfidenceChart(predictions) {
    const canvas = document.getElementById('confidenceChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart
    if (appState.charts.confidence) {
        appState.charts.confidence.destroy();
    }
    
    // Prepare data
    const labels = Object.keys(predictions);
    const values = Object.values(predictions).map(v => (v * 100).toFixed(2));
    
    // Create chart
    appState.charts.confidence = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Confidence (%)',
                data: values,
                backgroundColor: 'rgba(46, 204, 113, 0.8)',
                borderColor: 'rgba(46, 204, 113, 1)',
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// ============================================
// 📸 TRAINING DATA UPLOAD
// ============================================

function setupTrainingDataUpload() {
    const fileInput = document.getElementById('upload-training-file');
    const uploadBox = document.getElementById('upload-training-box');
    const preview = document.getElementById('upload-training-preview');
    const previewImg = document.getElementById('upload-training-preview-img');
    const uploadBtn = document.getElementById('upload-training-btn');
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            previewTrainingImage(file);
        }
    });
    
    // Upload button
    uploadBtn.addEventListener('click', function() {
        const file = fileInput.files[0];
        const category = document.getElementById('upload-category').value;
        
        if (!file) {
            showToast('Pilih gambar terlebih dahulu', 'error');
            return;
        }
        
        if (!category) {
            showToast('Pilih kategori sampah', 'error');
            return;
        }
        
        uploadTrainingData(file, category);
    });
}

function previewTrainingImage(file) {
    const uploadBox = document.getElementById('upload-training-box');
    const preview = document.getElementById('upload-training-preview');
    const previewImg = document.getElementById('upload-training-preview-img');
    
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        uploadBox.style.display = 'none';
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function resetUploadPage() {
    document.getElementById('upload-training-box').style.display = 'block';
    document.getElementById('upload-training-preview').style.display = 'none';
    document.getElementById('upload-training-file').value = '';
    document.getElementById('upload-category').value = '';
}

async function uploadTrainingData(file, category) {
    const uploadBtn = document.getElementById('upload-training-btn');
    
    // Disable button
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Mengupload...';
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', category);
        
        // Send request
        const response = await fetch(API.UPLOAD_TRAINING, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            resetUploadPage();
            loadDatasetStats();
            loadSystemStatus();
        } else {
            showToast(result.error || 'Gagal mengupload gambar', 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showToast('Terjadi kesalahan saat mengupload', 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-plus"></i> Tambah ke Dataset';
    }
}

async function loadDatasetStats() {
    try {
        const response = await fetch(API.STATUS);
        const result = await response.json();
        
        if (result.success) {
            const data = result.data.dataset;
            
            // Category stats
            const statsContainer = document.getElementById('dataset-category-stats');
            if (statsContainer) {
                let html = '';
                const icons = {
                    'cardboard': '📦',
                    'glass': '🫙',
                    'metal': '🔩',
                    'paper': '📄',
                    'plastic': '🥤'
                };
                
                for (const [category, count] of Object.entries(data.by_category)) {
                    const icon = icons[category] || '♻️';
                    const name = category.charAt(0).toUpperCase() + category.slice(1);
                    html += `
                        <div class="category-stat-item">
                            <span class="category-name">
                                <span class="cat-icon">${icon}</span>
                                ${name}
                            </span>
                            <span class="category-count">${count}</span>
                        </div>
                    `;
                }
                
                statsContainer.innerHTML = html;
            }
            
            // Ready check
            const readyCheck = document.getElementById('dataset-ready-check');
            if (readyCheck) {
                if (data.ready_for_training) {
                    readyCheck.className = 'ready-check ready';
                    readyCheck.innerHTML = `
                        <strong>✅ Dataset Siap!</strong>
                        <p>Kamu bisa mulai training model sekarang!</p>
                    `;
                } else {
                    readyCheck.className = 'ready-check not-ready';
                    readyCheck.innerHTML = `
                        <strong>⚠️ Dataset Belum Cukup</strong>
                        <p>Tambahkan lebih banyak gambar untuk setiap kategori</p>
                    `;
                }
            }
        }
    } catch (error) {
        console.error('Error loading dataset stats:', error);
    }
}

// ============================================
// 🧠 TRAINING
// ============================================

function setupTrainingControls() {
    // Epoch slider
    const epochSlider = document.getElementById('train-epochs');
    const epochValue = document.getElementById('train-epochs-value');
    
    if (epochSlider && epochValue) {
        epochSlider.addEventListener('input', function() {
            epochValue.textContent = this.value;
        });
    }
    
    // Start training button
    const startBtn = document.getElementById('start-training-btn');
    if (startBtn) {
        startBtn.addEventListener('click', startTraining);
    }
}

async function startTraining() {
    const epochs = parseInt(document.getElementById('train-epochs').value);
    const learningRate = parseFloat(document.getElementById('train-lr').value);
    const batchSize = parseInt(document.getElementById('train-batch').value);
    
    const startBtn = document.getElementById('start-training-btn');
    const progressSection = document.getElementById('training-progress');
    
    // Disable button
    startBtn.disabled = true;
    
    try {
        // Send training request
        const response = await fetch(API.TRAIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                epochs: epochs,
                learning_rate: learningRate,
                batch_size: batchSize
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('Training dimulai! 🚀', 'success');
            progressSection.style.display = 'block';
            
            // Start monitoring
            monitorTraining();
        } else {
            showToast(result.error || 'Gagal memulai training', 'error');
            startBtn.disabled = false;
        }
    } catch (error) {
        console.error('Training start error:', error);
        showToast('Terjadi kesalahan saat memulai training', 'error');
        startBtn.disabled = false;
    }
}

function monitorTraining() {
    // Clear existing interval
    if (appState.trainingInterval) {
        clearInterval(appState.trainingInterval);
    }
    
    // Poll training status every 2 seconds
    appState.trainingInterval = setInterval(async () => {
        try {
            const response = await fetch(API.TRAINING_STATUS);
            const result = await response.json();
            
            if (result.success) {
                updateTrainingProgress(result.data);
                
                // Check if completed
                if (!result.data.in_progress) {
                    clearInterval(appState.trainingInterval);
                    handleTrainingComplete(result.data);
                }
            }
        } catch (error) {
            console.error('Error monitoring training:', error);
        }
    }, 2000);
}

function updateTrainingProgress(status) {
    // Progress bar
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    
    if (progressBar) {
        progressBar.style.width = `${status.progress}%`;
    }
    
    if (progressText) {
        progressText.textContent = status.message;
    }
    
    // Metrics
    if (status.current_epoch && status.total_epochs) {
        document.getElementById('metric-epoch').textContent = 
            `${status.current_epoch}/${status.total_epochs}`;
    }
    
    if (status.accuracy !== undefined) {
        document.getElementById('metric-train-acc').textContent = 
            `${(status.accuracy * 100).toFixed(2)}%`;
    }
    
    if (status.val_accuracy !== undefined) {
        document.getElementById('metric-val-acc').textContent = 
            `${(status.val_accuracy * 100).toFixed(2)}%`;
    }
    
    if (status.loss !== undefined) {
        document.getElementById('metric-loss').textContent = 
            status.loss.toFixed(4);
    }
}

function handleTrainingComplete(status) {
    const progressSection = document.getElementById('training-progress');
    const resultSection = document.getElementById('training-result');
    const resultContent = document.getElementById('training-result-content');
    const startBtn = document.getElementById('start-training-btn');
    
    // Hide progress, show result
    progressSection.style.display = 'none';
    resultSection.style.display = 'block';
    
    // Re-enable start button
    startBtn.disabled = false;
    
    if (status.completed) {
        const accuracy = status.test_accuracy || 0;
        resultContent.innerHTML = `
            <div class="success-box">
                <h3>✅ Training Berhasil!</h3>
                <p>Model AI telah selesai dilatih dan siap digunakan!</p>
            </div>
            <div class="training-metrics">
                <div class="metric-card">
                    <div class="metric-label">Test Accuracy</div>
                    <div class="metric-value">${(accuracy * 100).toFixed(2)}%</div>
                </div>
            </div>
            <p>${status.message}</p>
        `;
        
        showToast('🎉 Training selesai!', 'success');
        
        // Reload system status
        loadSystemStatus();
    } else {
        resultContent.innerHTML = `
            <div class="warning-box">
                <h3>⚠️ Training Gagal</h3>
                <p>${status.message || status.error}</p>
            </div>
        `;
        
        showToast('Training gagal', 'error');
    }
}

async function checkTrainingStatus() {
    try {
        const response = await fetch(API.TRAINING_STATUS);
        const result = await response.json();
        
        if (result.success && result.data.in_progress) {
            document.getElementById('training-progress').style.display = 'block';
            monitorTraining();
        }
    } catch (error) {
        console.error('Error checking training status:', error);
    }
}

// ============================================
// 📚 EDUCATION TABS
// ============================================

function setupEducationTabs() {
    const tabs = document.querySelectorAll('.edu-tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            
            // Update tabs
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Update content
            document.querySelectorAll('.edu-tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`edu-${tabName}`).classList.add('active');
        });
    });
}

// ============================================
// 🔔 TOAST NOTIFICATIONS
// ============================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastIcon = document.getElementById('toast-icon');
    const toastMessage = document.getElementById('toast-message');
    
    // Set icon based on type
    const icons = {
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️'
    };
    
    toastIcon.textContent = icons[type] || icons.info;
    toastMessage.textContent = message;
    
    // Set class
    toast.className = `toast ${type}`;
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ============================================
// 🔧 UTILITIES
// ============================================

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDuration(seconds) {
    if (seconds < 60) return `${Math.round(seconds)}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
    return `${Math.round(seconds / 3600)}h`;
}

// Export for debugging
window.appDebug = {
    state: appState,
    api: API,
    showToast: showToast,
    loadSystemStatus: loadSystemStatus
};

console.log('✅ Smart Waste Classifier JS loaded successfully');
