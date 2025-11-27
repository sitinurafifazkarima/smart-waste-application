"""
📊 UTILITY - VISUALIZER
Utility functions untuk visualisasi data dan training metrics
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List
import plotly.graph_objects as go
import plotly.express as px

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

def plot_training_history(history: Dict, save_path: str = None):
    """
    📈 Plot training history (accuracy & loss)
    
    Args:
        history: Dict berisi history dari training
        save_path: Path untuk save plot (optional)
        
    Returns:
        matplotlib figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    epochs = range(1, len(history['accuracy']) + 1)
    
    # Plot Accuracy
    ax1.plot(epochs, history['accuracy'], 'b-', label='Training Accuracy', linewidth=2)
    ax1.plot(epochs, history['val_accuracy'], 'r-', label='Validation Accuracy', linewidth=2)
    ax1.set_title('📊 Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot Loss
    ax2.plot(epochs, history['loss'], 'b-', label='Training Loss', linewidth=2)
    ax2.plot(epochs, history['val_loss'], 'r-', label='Validation Loss', linewidth=2)
    ax2.set_title('📉 Model Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig

def plot_training_history_interactive(history: Dict):
    """
    📈 Plot training history dengan Plotly (interactive)
    
    Args:
        history: Dict berisi history dari training
        
    Returns:
        plotly figure
    """
    epochs = list(range(1, len(history['accuracy']) + 1))
    
    # Create subplots
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('📊 Model Accuracy', '📉 Model Loss')
    )
    
    # Accuracy plot
    fig.add_trace(
        go.Scatter(x=epochs, y=history['accuracy'], name='Training Accuracy',
                   mode='lines+markers', line=dict(color='blue', width=2)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=history['val_accuracy'], name='Validation Accuracy',
                   mode='lines+markers', line=dict(color='red', width=2)),
        row=1, col=1
    )
    
    # Loss plot
    fig.add_trace(
        go.Scatter(x=epochs, y=history['loss'], name='Training Loss',
                   mode='lines+markers', line=dict(color='blue', width=2)),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=history['val_loss'], name='Validation Loss',
                   mode='lines+markers', line=dict(color='red', width=2)),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Epoch", row=1, col=1)
    fig.update_xaxes(title_text="Epoch", row=1, col=2)
    fig.update_yaxes(title_text="Accuracy", row=1, col=1)
    fig.update_yaxes(title_text="Loss", row=1, col=2)
    
    fig.update_layout(height=500, showlegend=True)
    
    return fig

def plot_prediction_confidence(predictions: Dict, top_n: int = 5):
    """
    📊 Plot confidence score untuk prediksi
    
    Args:
        predictions: Dict {class_name: confidence_score}
        top_n: Tampilkan top N prediksi
        
    Returns:
        plotly figure
    """
    # Sort predictions by confidence
    sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    classes = [x[0] for x in sorted_preds]
    confidences = [x[1] * 100 for x in sorted_preds]
    
    # Color: hijau untuk tertinggi, gradient ke kuning untuk lainnya
    colors = ['#2ECC71' if i == 0 else '#F39C12' if i == 1 else '#95A5A6' 
              for i in range(len(classes))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=confidences,
            y=classes,
            orientation='h',
            marker=dict(color=colors),
            text=[f'{c:.1f}%' for c in confidences],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='🎯 Confidence Score per Kategori',
        xaxis_title='Confidence (%)',
        yaxis_title='Kategori Sampah',
        height=300,
        showlegend=False
    )
    
    return fig

def plot_dataset_distribution(stats: Dict):
    """
    📊 Plot distribusi dataset
    
    Args:
        stats: Dict statistik dataset dari DataManager
        
    Returns:
        plotly figure
    """
    categories = list(stats['raw'].keys())
    counts = list(stats['raw'].values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker=dict(
                color=counts,
                colorscale='Greens',
                showscale=False
            ),
            text=counts,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='📦 Distribusi Dataset per Kategori',
        xaxis_title='Kategori Sampah',
        yaxis_title='Jumlah Gambar',
        height=400
    )
    
    return fig

def plot_ai_level_progress(accuracy: float):
    """
    🎮 Plot progress level AI dengan gauge chart
    
    Args:
        accuracy: Accuracy model (0-1)
        
    Returns:
        plotly figure
    """
    # Determine level
    if accuracy < 0.5:
        level_name = "🥚 AI Telur"
        color = "#E74C3C"
    elif accuracy < 0.7:
        level_name = "🐣 AI Anak Ayam"
        color = "#F39C12"
    elif accuracy < 0.85:
        level_name = "🐥 AI Ayam Muda"
        color = "#F1C40F"
    elif accuracy < 0.95:
        level_name = "🦅 AI Elang"
        color = "#3498DB"
    else:
        level_name = "🚀 AI Roket"
        color = "#2ECC71"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=accuracy * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Level AI: {level_name}"},
        delta={'reference': 70},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "#E8F8F5"},
                {'range': [50, 70], 'color': "#D5F4E6"},
                {'range': [70, 85], 'color': "#A9DFBF"},
                {'range': [85, 95], 'color': "#7DCEA0"},
                {'range': [95, 100], 'color': "#52BE80"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig

def create_comparison_chart(data: Dict, title: str):
    """
    📊 Create comparison bar chart
    
    Args:
        data: Dict {label: value}
        title: Judul chart
        
    Returns:
        matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = list(data.keys())
    values = list(data.values())
    
    bars = ax.barh(labels, values, color='#2ECC71')
    ax.set_xlabel('Value')
    ax.set_title(title, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    return fig
