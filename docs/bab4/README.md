# Dokumentasi BAB IV - Implementasi dan Pengujian

## Struktur Folder

```
docs/bab4/
├── index.html          # File dokumentasi utama
├── README.md           # Panduan ini
└── images/             # Folder screenshot
    ├── 01_homepage.png
    ├── 02_searching.png
    ├── 03_preprocessing.png
    ├── 03_search_results.png
    ├── 04_tfidf_matrix.png
    ├── 05_tfidf_details.png
    ├── 06-cosine.png
    ├── 07-ranking.png
    ├── 08_cosine_table.png
    ├── 10_final_ranking.png
    ├── 11_detail_preprocessing_dark.png
    ├── 12_top_terms.png
    └── 13_cosine_detail_dark.png
```

## Mapping Gambar di Dokumentasi

| Gambar | File | Deskripsi |
|--------|------|-----------|
| Gambar 4.1 | `01_homepage.png` | Halaman Pencarian Utama |
| Gambar 4.2 | `03_search_results.png` | Tab Navigation CBF |
| Gambar 4.3 | `03_preprocessing.png` | Step 1: Preprocessing |
| Gambar 4.4 | `04_tfidf_matrix.png` | TF-IDF Matrix |
| Gambar 4.5 | `05_tfidf_details.png` | TF-IDF Calculation |
| Gambar 4.6 | `11_detail_preprocessing_dark.png` | Detail TF-IDF per Term |
| Gambar 4.7 | `12_top_terms.png` | Top TF-IDF Terms per Dokumen |
| Gambar 4.8 | `06-cosine.png` | Cosine Similarity |
| Gambar 4.9 | `08_cosine_table.png` | Detail Cosine Similarity |
| Gambar 4.10 | `07-ranking.png` | Final Ranking |
| Gambar 4.11 | `13_cosine_detail_dark.png` | Tab Detail Perhitungan |
| Gambar 4.12 | `10_final_ranking.png` | Statistik Hasil |

## Cara Membuka Dokumentasi

### Opsi 1: Double-click file
```
Buka: docs/bab4/index.html
```

### Opsi 2: Via Browser
```
Drag file index.html ke browser
atau
Klik kanan > Open with > Browser
```

## Struktur Dokumentasi BAB IV

```
BAB IV IMPLEMENTASI DAN PENGUJIAN
├── 4.1 Lingkungan Pengembangan
│   ├── 4.1.1 Perangkat Keras
│   ├── 4.1.2 Perangkat Lunak
│   └── 4.1.3 Library dan Framework
├── 4.2 Implementasi Sistem
│   ├── 4.2.1 Arsitektur Sistem
│   └── 4.2.2 Implementasi Content-Based Filtering
├── 4.3 Antarmuka Sistem
│   ├── 4.3.1 Halaman Pencarian Utama
│   ├── 4.3.2 Navigasi Proses CBF
│   ├── 4.3.3 Tahap 1: Text Preprocessing
│   ├── 4.3.4 Tahap 2: Perhitungan TF-IDF
│   ├── 4.3.5 Tahap 3: Perhitungan Cosine Similarity
│   ├── 4.3.6 Tahap 4: Hasil Ranking Akhir
│   └── 4.3.7 Tab Detail Perhitungan
├── 4.4 Pengujian Sistem
│   ├── 4.4.1 Pengujian Fungsional
│   └── 4.4.2 Pengujian Akurasi CBF
└── 4.5 Analisis Hasil
    ├── 4.5.1 Analisis Hasil Pencarian
    ├── 4.5.2 Analisis Relevansi Ranking
    └── 4.5.3 Analisis Perhitungan TF-IDF & Cosine
```

## Fitur Dokumentasi

1. **Sidebar Navigation** - Navigasi cepat ke setiap section
2. **12 Gambar** - Semua screenshot sudah terintegrasi
3. **Responsive Design** - Desktop dan mobile friendly
4. **Print-friendly** - Bisa di-print atau export PDF
5. **Interactive** - Smooth scrolling dan highlight aktif

## Export ke PDF/Word

### Via Browser:
1. Buka `index.html` di browser
2. Tekan `Ctrl + P`
3. Pilih "Save as PDF" atau printer
4. Simpan

### Catatan:
- Sidebar akan otomatis hidden saat print
- Layout akan menyesuaikan untuk print
