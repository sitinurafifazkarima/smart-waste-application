"""
📁 MODUL DATA MANAGER - MANAJEMEN DATASET
Modul untuk upload dan organize dataset gambar sampah
"""

import os
import shutil
from pathlib import Path
from PIL import Image
from datetime import datetime
from typing import Dict, List
import json

class DataManager:
    """
    Kelas untuk manajemen dataset:
    - Upload gambar baru
    - Organize dataset ke folder sesuai label
    - Split dataset (train/test/validation)
    - Get statistik dataset
    """
    
    def __init__(self, raw_data_dir: str, processed_data_dir: str):
        """
        Inisialisasi Data Manager
        
        Args:
            raw_data_dir: Path ke folder dataset/raw
            processed_data_dir: Path ke folder dataset/processed
        """
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        
        # Pastikan folder exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """
        🔧 Pastikan semua folder yang dibutuhkan ada
        """
        # Raw data directories
        categories = ["cardboard", "glass", "metal", "paper", "plastic"]
        for category in categories:
            category_dir = self.raw_data_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
        
        # Processed data directories
        for split in ["train", "test", "validation"]:
            for category in categories:
                split_dir = self.processed_data_dir / split / category
                split_dir.mkdir(parents=True, exist_ok=True)
    
    def add_image(self, image_file, label: str, filename: str = None) -> Dict[str, any]:
        """
        📸 Tambahkan gambar baru ke dataset
        
        Args:
            image_file: File gambar (dari Streamlit uploader)
            label: Label kategori (cardboard/glass/metal/paper/plastic)
            filename: Nama file (optional, akan auto-generate jika None)
            
        Returns:
            Dict dengan info hasil upload
        """
        try:
            # Validasi label
            valid_labels = ["cardboard", "glass", "metal", "paper", "plastic"]
            if label.lower() not in valid_labels:
                return {
                    "success": False,
                    "message": f"Label tidak valid. Harus salah satu dari: {valid_labels}"
                }
            
            # Generate filename jika tidak ada
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{label}_{timestamp}.jpg"
            
            # Pastikan extension adalah .jpg
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filename = f"{filename}.jpg"
            
            # Path tujuan
            destination = self.raw_data_dir / label.lower() / filename
            
            # Buka dan save gambar
            image = Image.open(image_file)
            
            # Convert ke RGB jika perlu (untuk PNG dengan alpha channel)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize untuk efisiensi storage (optional)
            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save gambar
            image.save(destination, 'JPEG', quality=95)
            
            return {
                "success": True,
                "message": "✅ Gambar berhasil ditambahkan!",
                "path": str(destination),
                "label": label,
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def get_dataset_statistics(self) -> Dict[str, any]:
        """
        📊 Dapatkan statistik dataset
        
        Returns:
            Dict berisi statistik jumlah gambar per kategori
        """
        stats = {
            "raw": {},
            "processed": {"train": {}, "test": {}, "validation": {}},
            "total_raw": 0,
            "total_processed": 0
        }
        
        categories = ["cardboard", "glass", "metal", "paper", "plastic"]
        
        # Hitung raw data
        for category in categories:
            category_dir = self.raw_data_dir / category
            if category_dir.exists():
                count = len([f for f in category_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
                stats["raw"][category] = count
                stats["total_raw"] += count
            else:
                stats["raw"][category] = 0
        
        # Hitung processed data
        for split in ["train", "test", "validation"]:
            for category in categories:
                split_dir = self.processed_data_dir / split / category
                if split_dir.exists():
                    count = len([f for f in split_dir.iterdir() if f.is_file()])
                    stats["processed"][split][category] = count
                    stats["total_processed"] += count
                else:
                    stats["processed"][split][category] = 0
        
        return stats
    
    def split_dataset(self, train_ratio: float = 0.7, test_ratio: float = 0.15, validation_ratio: float = 0.15) -> Dict[str, any]:
        """
        📦 Split dataset dari raw ke train/test/validation
        
        Args:
            train_ratio: Proporsi data untuk training (default 70%)
            test_ratio: Proporsi data untuk testing (default 15%)
            validation_ratio: Proporsi data untuk validation (default 15%)
            
        Returns:
            Dict dengan info hasil split
        """
        try:
            import random
            
            # Validasi ratio
            if abs(train_ratio + test_ratio + validation_ratio - 1.0) > 0.01:
                return {
                    "success": False,
                    "message": "❌ Total ratio harus = 1.0"
                }
            
            categories = ["cardboard", "glass", "metal", "paper", "plastic"]
            split_info = {}
            
            for category in categories:
                # Get all images dari raw folder
                raw_dir = self.raw_data_dir / category
                if not raw_dir.exists():
                    continue
                
                images = [f for f in raw_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
                
                if len(images) == 0:
                    split_info[category] = "Tidak ada gambar"
                    continue
                
                # Shuffle images
                random.shuffle(images)
                
                # Calculate split indices
                total = len(images)
                train_end = int(total * train_ratio)
                test_end = train_end + int(total * test_ratio)
                
                # Split files
                train_files = images[:train_end]
                test_files = images[train_end:test_end]
                val_files = images[test_end:]
                
                # Copy ke processed folders
                for split_name, files in [("train", train_files), ("test", test_files), ("validation", val_files)]:
                    dest_dir = self.processed_data_dir / split_name / category
                    
                    # Clear existing files
                    if dest_dir.exists():
                        for f in dest_dir.iterdir():
                            if f.is_file():
                                f.unlink()
                    
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Copy files
                    for file in files:
                        shutil.copy2(file, dest_dir / file.name)
                
                split_info[category] = {
                    "train": len(train_files),
                    "test": len(test_files),
                    "validation": len(val_files)
                }
            
            return {
                "success": True,
                "message": "✅ Dataset berhasil di-split!",
                "split_info": split_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def delete_image(self, category: str, filename: str) -> Dict[str, any]:
        """
        🗑️ Hapus gambar dari dataset
        
        Args:
            category: Kategori sampah
            filename: Nama file
            
        Returns:
            Dict dengan info hasil delete
        """
        try:
            file_path = self.raw_data_dir / category / filename
            
            if file_path.exists():
                file_path.unlink()
                return {
                    "success": True,
                    "message": f"✅ {filename} berhasil dihapus"
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ File {filename} tidak ditemukan"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def get_images_list(self, category: str = None) -> List[Dict[str, str]]:
        """
        📋 Dapatkan list gambar di dataset
        
        Args:
            category: Kategori tertentu (None untuk semua)
            
        Returns:
            List of dict dengan info gambar
        """
        images_list = []
        
        if category:
            categories = [category]
        else:
            categories = ["cardboard", "glass", "metal", "paper", "plastic"]
        
        for cat in categories:
            cat_dir = self.raw_data_dir / cat
            if cat_dir.exists():
                for img_file in cat_dir.iterdir():
                    if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        images_list.append({
                            "category": cat,
                            "filename": img_file.name,
                            "path": str(img_file),
                            "size": img_file.stat().st_size,
                            "modified": datetime.fromtimestamp(img_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        })
        
        return images_list
    
    def check_dataset_ready(self) -> Dict[str, any]:
        """
        ✅ Cek apakah dataset siap untuk training
        
        Returns:
            Dict dengan status dan rekomendasi
        """
        stats = self.get_dataset_statistics()
        min_images_per_class = 10  # Minimal 10 gambar per kelas
        
        ready = True
        issues = []
        
        # Cek setiap kategori
        for category, count in stats["raw"].items():
            if count < min_images_per_class:
                ready = False
                issues.append(f"{category}: hanya {count} gambar (minimal {min_images_per_class})")
        
        return {
            "ready": ready,
            "total_images": stats["total_raw"],
            "min_required": min_images_per_class * 5,  # 5 kategori
            "issues": issues,
            "recommendation": "Tambahkan lebih banyak gambar untuk hasil training yang lebih baik!" if not ready else "Dataset siap untuk training! 🎯"
        }


# 🧪 TESTING
if __name__ == "__main__":
    from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
    
    dm = DataManager(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    
    # Test get statistics
    stats = dm.get_dataset_statistics()
    print("\n📊 Dataset Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Test check ready
    ready_check = dm.check_dataset_ready()
    print("\n✅ Dataset Ready Check:")
    print(json.dumps(ready_check, indent=2))
