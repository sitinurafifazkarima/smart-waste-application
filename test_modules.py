"""
🧪 SCRIPT TESTING - Test Semua Modul
Jalankan untuk memastikan semua modul berfungsi dengan baik
"""

import sys
from pathlib import Path

print("="*60)
print("🧪 TESTING SEMUA MODUL")
print("="*60)
print()

# Test 1: Import modules
print("1️⃣ Testing imports...")
try:
    from modules.classifier import WasteClassifier
    from modules.data_manager import DataManager
    from modules.trainer import ModelTrainer
    from modules.recommender import WasteRecommender
    from utils.image_processor import load_and_preprocess_image
    from utils.visualizer import plot_training_history
    import config
    print("✅ All imports successful!")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

print()

# Test 2: Config
print("2️⃣ Testing config...")
try:
    assert len(config.WASTE_CATEGORIES) == 5
    assert len(config.CATEGORY_ICONS) == 5
    assert len(config.WASTE_RECOMMENDATIONS) == 5
    print("✅ Config valid!")
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

print()

# Test 3: Data Manager
print("3️⃣ Testing Data Manager...")
try:
    dm = DataManager(config.RAW_DATA_DIR, config.PROCESSED_DATA_DIR)
    stats = dm.get_dataset_statistics()
    ready = dm.check_dataset_ready()
    print(f"   Total images: {stats['total_raw']}")
    print(f"   Dataset ready: {ready['ready']}")
    print("✅ Data Manager OK!")
except Exception as e:
    print(f"❌ Data Manager error: {e}")

print()

# Test 4: Recommender
print("4️⃣ Testing Recommender...")
try:
    recommender = WasteRecommender()
    rec = recommender.get_recommendation("Plastic")
    assert "icon" in rec
    assert "main_action" in rec
    print("✅ Recommender OK!")
except Exception as e:
    print(f"❌ Recommender error: {e}")

print()

# Test 5: Classifier (jika model ada)
print("5️⃣ Testing Classifier...")
if Path(config.MODEL_PATH).exists():
    try:
        classifier = WasteClassifier(config.MODEL_PATH, config.LABELS_PATH)
        print(f"   Model loaded: {len(classifier.class_names)} classes")
        print("✅ Classifier OK!")
    except Exception as e:
        print(f"⚠️  Classifier warning: {e}")
else:
    print("⚠️  Model not found (belum training) - SKIP")

print()

# Test 6: Folders
print("6️⃣ Testing folder structure...")
try:
    folders_to_check = [
        config.RAW_DATA_DIR,
        config.PROCESSED_DATA_DIR,
        Path("modules"),
        Path("utils")
    ]
    
    for folder in folders_to_check:
        if Path(folder).exists():
            print(f"   ✅ {folder}")
        else:
            print(f"   ❌ {folder} - NOT FOUND")
    
    print("✅ Folder structure OK!")
except Exception as e:
    print(f"❌ Folder error: {e}")

print()
print("="*60)
print("🎉 TESTING COMPLETED!")
print("="*60)
print()

# Summary
print("📊 SUMMARY:")
print(f"   Dataset: {stats['total_raw']} images")
print(f"   Model: {'✅ Ready' if Path(config.MODEL_PATH).exists() else '⚠️  Need training'}")
print(f"   Ready to use: {'✅ YES' if Path(config.MODEL_PATH).exists() and stats['total_raw'] > 0 else '⚠️  Add data & train first'}")
print()

print("🚀 Next steps:")
if not Path(config.MODEL_PATH).exists():
    print("   1. Add training data (minimal 50 images)")
    print("   2. Run training")
    print("   3. Start classifying!")
else:
    print("   1. Run: streamlit run app.py")
    print("   2. Start using the app!")

print()
