"""
🖼️ UTILITY - IMAGE PROCESSOR
Utility functions untuk pemrosesan gambar
"""

import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import io

def load_and_preprocess_image(image_source, target_size=(224, 224)):
    """
    📸 Load dan preprocess gambar
    
    Args:
        image_source: Path ke file atau PIL Image
        target_size: Ukuran target (width, height)
        
    Returns:
        PIL Image yang sudah dipreprocess
    """
    # Load image
    if isinstance(image_source, str):
        image = Image.open(image_source)
    else:
        image = image_source
    
    # Convert ke RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = ImageOps.fit(image, target_size, Image.Resampling.LANCZOS)
    
    return image

def normalize_image_array(image_array):
    """
    🔢 Normalisasi array gambar ke range [-1, 1]
    
    Args:
        image_array: numpy array dari gambar
        
    Returns:
        Normalized array
    """
    return (image_array.astype(np.float32) / 127.5) - 1

def image_to_array(image, normalize=True):
    """
    🔄 Convert PIL Image ke numpy array
    
    Args:
        image: PIL Image
        normalize: Apakah perlu dinormalisasi
        
    Returns:
        numpy array
    """
    array = np.asarray(image)
    
    if normalize:
        array = normalize_image_array(array)
    
    return array

def enhance_image(image, brightness=1.0, contrast=1.0, sharpness=1.0):
    """
    ✨ Enhance gambar (brightness, contrast, sharpness)
    
    Args:
        image: PIL Image
        brightness: Faktor brightness (1.0 = normal)
        contrast: Faktor contrast (1.0 = normal)
        sharpness: Faktor sharpness (1.0 = normal)
        
    Returns:
        Enhanced PIL Image
    """
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)
    
    return image

def resize_image_for_display(image, max_size=(800, 800)):
    """
    📏 Resize gambar untuk display (tetap jaga aspect ratio)
    
    Args:
        image: PIL Image
        max_size: Ukuran maksimal (width, height)
        
    Returns:
        Resized PIL Image
    """
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

def get_image_info(image):
    """
    ℹ️ Dapatkan informasi gambar
    
    Args:
        image: PIL Image atau path ke file
        
    Returns:
        Dict dengan info gambar
    """
    if isinstance(image, str):
        image = Image.open(image)
    
    return {
        "size": image.size,
        "mode": image.mode,
        "format": image.format,
        "width": image.width,
        "height": image.height
    }

def save_image_bytes(image, format='JPEG', quality=95):
    """
    💾 Convert PIL Image ke bytes (untuk upload/download)
    
    Args:
        image: PIL Image
        format: Format file (JPEG/PNG)
        quality: Quality (1-100)
        
    Returns:
        Bytes object
    """
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format, quality=quality)
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()
