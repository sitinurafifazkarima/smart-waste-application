"""
♻️ MODUL RECOMMENDER - SISTEM REKOMENDASI AKSI SAMPAH
Memberikan rekomendasi cara pengelolaan sampah berdasarkan hasil klasifikasi
"""

from typing import Dict
from config import WASTE_RECOMMENDATIONS, CATEGORY_ICONS

class WasteRecommender:
    """
    💡 Kelas untuk memberikan rekomendasi pengelolaan sampah
    
    Fitur:
    - Rekomendasi aksi berdasarkan jenis sampah
    - Tips pengelolaan
    - Info dampak lingkungan
    - Nilai ekonomis
    """
    
    def __init__(self):
        """
        Inisialisasi recommender dengan data dari config
        """
        self.recommendations = WASTE_RECOMMENDATIONS
        self.icons = CATEGORY_ICONS
    
    def get_recommendation(self, waste_type: str) -> Dict[str, any]:
        """
        📋 Dapatkan rekomendasi untuk jenis sampah tertentu
        
        Args:
            waste_type: Jenis sampah (Cardboard/Glass/Metal/Paper/Plastic)
            
        Returns:
            Dict berisi rekomendasi lengkap
        """
        # Capitalize first letter untuk matching
        waste_type = waste_type.capitalize()
        
        if waste_type not in self.recommendations:
            return {
                "error": f"Jenis sampah '{waste_type}' tidak dikenali",
                "available_types": list(self.recommendations.keys())
            }
        
        # Get recommendation data
        rec = self.recommendations[waste_type]
        
        # Format response
        response = {
            "waste_type": waste_type,
            "icon": rec["icon"],
            "main_action": rec["action"],
            "description": rec["description"],
            "tips": rec["tips"],
            "environmental_impact": rec["impact"],
            "economic_value": rec["value"],
            "formatted_message": self._format_message(waste_type, rec)
        }
        
        return response
    
    def _format_message(self, waste_type: str, rec: Dict) -> str:
        """
        📝 Format pesan rekomendasi yang mudah dibaca
        
        Args:
            waste_type: Jenis sampah
            rec: Data rekomendasi
            
        Returns:
            String pesan terformat
        """
        message = f"""
## {rec['icon']} Rekomendasi untuk {waste_type}

### 🎯 Aksi Utama:
**{rec['action']}**

### 📖 Penjelasan:
{rec['description']}

### 💡 Tips Praktis:
"""
        for i, tip in enumerate(rec['tips'], 1):
            message += f"{i}. {tip}\n"
        
        message += f"""
### 🌍 Dampak Lingkungan:
{rec['impact']}

### 💰 Nilai Ekonomis:
{self._get_economic_value_label(rec['value'])}
"""
        return message
    
    def _get_economic_value_label(self, value: str) -> str:
        """
        💵 Convert economic value code ke label yang readable
        
        Args:
            value: Code nilai ekonomis
            
        Returns:
            Label yang readable
        """
        labels = {
            "ekonomis_tinggi": "⭐⭐⭐ Nilai Ekonomi Tinggi - Bisa dijual dengan harga bagus!",
            "ekonomis_sedang": "⭐⭐ Nilai Ekonomi Sedang - Ada nilai jual",
            "ekonomis_rendah": "⭐ Nilai Ekonomi Rendah - Fokus pada dampak lingkungan"
        }
        return labels.get(value, "Tidak diketahui")
    
    def get_all_recommendations(self) -> Dict[str, Dict]:
        """
        📚 Dapatkan semua rekomendasi untuk semua jenis sampah
        
        Returns:
            Dict dengan semua rekomendasi
        """
        all_recs = {}
        for waste_type in self.recommendations.keys():
            all_recs[waste_type] = self.get_recommendation(waste_type)
        return all_recs
    
    def compare_waste_types(self, waste_types: list) -> Dict[str, any]:
        """
        📊 Bandingkan beberapa jenis sampah
        
        Args:
            waste_types: List jenis sampah untuk dibandingkan
            
        Returns:
            Dict perbandingan
        """
        comparison = {
            "waste_types": waste_types,
            "comparison": {}
        }
        
        for waste_type in waste_types:
            rec = self.get_recommendation(waste_type)
            if "error" not in rec:
                comparison["comparison"][waste_type] = {
                    "icon": rec["icon"],
                    "action": rec["main_action"],
                    "economic_value": rec["economic_value"],
                    "impact": rec["environmental_impact"]
                }
        
        return comparison
    
    def get_quick_action(self, waste_type: str) -> str:
        """
        ⚡ Dapatkan quick action (singkat) untuk UI
        
        Args:
            waste_type: Jenis sampah
            
        Returns:
            String aksi singkat
        """
        waste_type = waste_type.capitalize()
        
        if waste_type in self.recommendations:
            rec = self.recommendations[waste_type]
            return f"{rec['icon']} {rec['action']}"
        
        return "❓ Tidak diketahui"
    
    def get_educational_content(self, waste_type: str) -> Dict[str, str]:
        """
        🎓 Dapatkan konten edukatif untuk siswa
        
        Args:
            waste_type: Jenis sampah
            
        Returns:
            Dict konten edukatif
        """
        waste_type = waste_type.capitalize()
        
        educational_facts = {
            "Cardboard": {
                "fun_fact": "🌳 Mendaur ulang 1 ton karton dapat menyelamatkan 17 pohon!",
                "decompose_time": "⏰ Waktu terurai: 2 bulan",
                "recycle_rate": "📊 Tingkat daur ulang: 70-90% di negara maju"
            },
            "Glass": {
                "fun_fact": "♾️ Kaca bisa didaur ulang selamanya tanpa kehilangan kualitas!",
                "decompose_time": "⏰ Waktu terurai: 1 juta tahun (hampir tidak terurai)",
                "recycle_rate": "📊 Menghemat energi hingga 40% dibanding produksi baru"
            },
            "Metal": {
                "fun_fact": "⚡ Daur ulang aluminium menghemat 95% energi dibanding produksi baru!",
                "decompose_time": "⏰ Waktu terurai: 50-200 tahun",
                "recycle_rate": "📊 Tingkat daur ulang: 60-70% untuk kaleng aluminium"
            },
            "Paper": {
                "fun_fact": "📄 Kertas dapat didaur ulang 5-7 kali sebelum seratnya rusak!",
                "decompose_time": "⏰ Waktu terurai: 2-6 minggu",
                "recycle_rate": "📊 1 ton kertas daur ulang = 17 pohon + 26.000 liter air terhemat"
            },
            "Plastic": {
                "fun_fact": "🌊 Setiap menit, 1 truk sampah plastik masuk ke laut!",
                "decompose_time": "⏰ Waktu terurai: 20-500 tahun tergantung jenis",
                "recycle_rate": "📊 Hanya 9% plastik global yang benar-benar didaur ulang"
            }
        }
        
        if waste_type in educational_facts:
            return educational_facts[waste_type]
        
        return {
            "fun_fact": "Tidak ada data",
            "decompose_time": "Tidak diketahui",
            "recycle_rate": "Tidak diketahui"
        }
    
    def get_icon(self, waste_type: str) -> str:
        """
        🎨 Dapatkan ikon untuk jenis sampah
        
        Args:
            waste_type: Jenis sampah
            
        Returns:
            Emoji ikon
        """
        waste_type_lower = waste_type.lower()
        return self.icons.get(waste_type_lower, "♻️")


# 🧪 TESTING
if __name__ == "__main__":
    recommender = WasteRecommender()
    
    # Test get recommendation
    print("="*60)
    print("🧪 TESTING WASTE RECOMMENDER")
    print("="*60)
    
    waste_types = ["Cardboard", "Glass", "Metal", "Paper", "Plastic"]
    
    for waste_type in waste_types:
        rec = recommender.get_recommendation(waste_type)
        print(f"\n{rec['formatted_message']}")
        print("-"*60)
        
        # Test educational content
        edu = recommender.get_educational_content(waste_type)
        print("\n📚 KONTEN EDUKATIF:")
        for key, value in edu.items():
            print(f"   {value}")
        print("="*60)
    
    # Test comparison
    print("\n📊 PERBANDINGAN SAMPAH:")
    comparison = recommender.compare_waste_types(["Metal", "Plastic", "Paper"])
    print(comparison)
