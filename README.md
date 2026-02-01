# 🚗 Dashboard Pasar BMW: Analisis Harga & Prediksi

Dashboard interaktif untuk menganalisis harga mobil BMW dengan fitur storytelling dan rekomendasi investasi.

## ✨ Fitur Utama

### 1. **Filter Interaktif**
- **Jenis Transmisi**: Pilih Automatic/Manual dengan jumlah data
- **Mata Uang**: Konversi otomatis ke Euro, Rupiah, atau US Dollar
- **Tahun**: Filter berdasarkan tahun atau pilih "All" untuk semua tahun
- **Model**: Multiselect untuk memilih beberapa model sekaligus

### 2. **KPI Metrics**
Dashboard menampilkan 4 metrik utama:
- 💰 **Harga Minimal**: Harga terendah dari data yang difilter
- 💎 **Harga Maksimal**: Harga tertinggi dari data yang difilter
- 📊 **Harga Rata-rata**: Rata-rata harga keseluruhan
- 📈 **Prediksi Harga**: Rata-rata harga forecast untuk masa depan

### 3. **Storytelling & Analisis Cerdas** 🎯
Dashboard memberikan insight otomatis berdasarkan data:

#### 📈 Model Terbaik
- Mengidentifikasi model dengan pertumbuhan harga tertinggi
- Menampilkan persentase kenaikan harga
- Memberikan rekomendasi investasi

#### 🔮 Prediksi Masa Depan
- Analisis forecasting untuk setiap model
- Rekomendasi **BELI**, **JUAL**, atau **HOLD**
- Estimasi potensi keuntungan/kerugian

#### 🛡️ Model Paling Stabil
- Identifikasi model dengan volatilitas terendah
- Cocok untuk investor yang menghindari risiko
- Jaminan harga tidak akan turun terlalu jauh saat dijual kembali

#### ⚖️ Perbandingan Performa
- Membandingkan model terbaik vs terlemah
- Menampilkan selisih performa
- Membantu pengambilan keputusan investasi

### 4. **Visualisasi Data**

#### 📉 Line Chart: Tren Harga per Tahun
- Menampilkan tren harga untuk semua model yang dipilih
- Interaktif dengan hover information
- Membantu melihat pola historis

#### 📊 Bar Chart: Rata-rata Harga per Model
- Perbandingan harga antar model
- Diurutkan dari terendah ke tertinggi
- Format horizontal untuk kemudahan membaca

#### 📋 Tabel Detail
- Menampilkan harga rata-rata per model
- Prediksi harga untuk setiap model
- Total keseluruhan di baris akhir

## 🎯 Cara Menggunakan

### Instalasi
```bash
pip install -r requirements.txt
```

### Menjalankan Dashboard
```bash
streamlit run app.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## 📊 Struktur Data

Dataset (`bmw_pricing_data.csv`) memiliki kolom:
- **Year**: Tahun (2010-2027)
- **Region**: Wilayah geografis
- **Fuel_Type**: Jenis bahan bakar (Diesel, Electric, Hybrid, Petrol)
- **Transmission**: Jenis transmisi (Automatic, Manual)
- **Model**: Model BMW (3 Series, 5 Series, 7 Series, M3, M5, X1, X3, X5, X6, i3, i8)
- **Price_USD**: Harga dalam USD
- **Type**: Actual (data historis) atau Forecast (prediksi)

## 💡 Contoh Insight yang Dihasilkan

### Skenario 1: Model dengan Tren Naik
```
📈 Model Terbaik: X5

Model X5 menunjukkan performa luar biasa dengan kenaikan harga 12.5% 
dalam beberapa tahun terakhir. Harga rata-rata saat ini mencapai $85,000.

✅ Rekomendasi: Model ini sangat bagus untuk investasi jangka panjang. 
Tren menunjukkan permintaan tinggi dan nilai yang terus meningkat.
```

### Skenario 2: Rekomendasi Beli
```
🔮 Prediksi Terbaik: i3

Berdasarkan analisis forecasting, model i3 diprediksi akan mengalami 
kenaikan harga sebesar 8.3% di masa depan.

💡 Strategi: Ini adalah waktu yang TEPAT UNTUK MEMBELI model ini. 
Jika Anda membeli sekarang dan menjual kembali dalam 2-3 tahun, 
potensi keuntungan sangat tinggi dengan risiko penurunan harga yang minimal.
```

### Skenario 3: Rekomendasi Jual
```
⚠️ Perhatian: M3

Model M3 diprediksi akan mengalami penurunan harga sekitar 5.2% di masa depan.

💡 Strategi: Jika Anda memiliki model ini, pertimbangkan untuk MENJUAL SEKARANG 
sebelum harga turun lebih jauh.
```

## 🔧 Teknologi yang Digunakan

- **Streamlit**: Framework untuk dashboard interaktif
- **Pandas**: Manipulasi dan analisis data
- **Plotly**: Visualisasi data interaktif
- **Python 3.8+**: Bahasa pemrograman

## 📝 Fitur Konversi Mata Uang

Dashboard mendukung 3 mata uang:
- **US Dollar** (USD): Rate 1.0
- **Euro** (EUR): Rate 0.92
- **Rupiah** (IDR): Rate 15,800

Semua nilai otomatis dikonversi sesuai pilihan pengguna.

## 🎓 Proyek

Dashboard ini dibuat sebagai bagian dari:
- **Mata Kuliah**: Sains Data
- **Program Studi**: Teknik Informatika Semester 7
- **Tujuan**: Analisis pasar dan prediksi harga mobil BMW

## 📈 Algoritma Analisis

### Perhitungan Tren
- Membandingkan rata-rata 3 tahun terakhir vs 3 tahun sebelumnya
- Menghitung persentase perubahan harga

### Prediksi Masa Depan
- Menggunakan data forecast dari dataset
- Membandingkan harga forecast dengan harga aktual terkini

### Volatilitas
- Menghitung standar deviasi harga
- Model dengan volatilitas rendah = lebih stabil

## 🚀 Tips Penggunaan

1. **Untuk Analisis Umum**: Pilih "All" pada filter Tahun dan Model
2. **Untuk Model Spesifik**: Pilih 1-3 model yang ingin dibandingkan
3. **Untuk Tahun Tertentu**: Pilih tahun spesifik untuk melihat snapshot harga
4. **Untuk Investasi**: Perhatikan bagian "Analisis Pasar & Rekomendasi Investasi"

## 📞 Support

Jika ada pertanyaan atau masalah, silakan hubungi tim pengembang.

---

**Dibuat dengan ❤️ menggunakan Streamlit & Plotly**
