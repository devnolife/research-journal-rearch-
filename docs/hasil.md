# 📋 HASIL PERUBAHAN SISTEM

## 🎯 Judul Skripsi
**PERANCANGAN SISTEM PENCARIAN JURNAL BERBASIS MULTI PLATFORM MENGGUNAKAN CONTENT-BASED FILTERING**

---

## 🔄 Perubahan yang Telah Dibuat

### ✅ Fitur Baru

| No | Fitur | Deskripsi | File |
|----|-------|-----------|------|
| 1 | **Input Cerita Penelitian** | User bisa menjelaskan penelitian dalam bentuk narasi, sistem otomatis ekstrak keywords | `templates/index.html` |
| 2 | **Auto Extract Keywords** | Sistem mendeteksi kata kunci penting dari cerita user | `templates/index.html` |
| 3 | **Visualisasi Step-by-Step** | Proses CBF ditampilkan dalam 4 langkah interaktif | `templates/index.html` |
| 4 | **Step 1: Preprocessing** | Menampilkan teks original vs preprocessed | `templates/index.html` |
| 5 | **Step 2: TF-IDF Table** | Menampilkan top terms dengan skor TF-IDF | `templates/index.html` |
| 6 | **Step 3: Cosine Similarity** | Menampilkan matriks similarity query-dokumen | `templates/index.html` |
| 7 | **Step 4: Ranking** | Hasil ranking dengan badge peringkat dan skor | `templates/index.html` |
| 8 | **Formula Display** | Menampilkan rumus-rumus yang digunakan | `templates/index.html` |

---

## 📁 File yang Dimodifikasi

### 1. `templates/index.html`

**Perubahan:**
- Tambah textarea untuk input cerita penelitian
- Tambah section ekstraksi keywords otomatis
- Tambah CSS styling untuk story input dan process steps
- Tambah section CBF Process dengan 4 step interaktif
- Tambah JavaScript untuk:
  - `extractKeywords()` - ekstrak kata kunci dari cerita
  - `handleStoryInput()` - handle input cerita
  - `showStep()` - navigasi antar step
  - `displayCBFProcess()` - tampilkan proses CBF
  - `populatePreprocessing()` - isi data preprocessing
  - `populateTFIDF()` - isi data TF-IDF
  - `populateSimilarity()` - isi data similarity
  - `populateRanking()` - isi data ranking

### 2. `content_based_filter.py`

**Perubahan pada function `get_cbf_calculation_details()`:**
- Tambah return data `preprocessing` dengan teks original dan preprocessed
- Tambah return data `tfidf` dengan top terms dan skor
- Tambah return data `papers` dengan nilai similarity per paper
- Tambah return data `ranking` yang sudah diurutkan
- Tambah return data `similarity_matrix` antar dokumen

### 3. `app.py`

**Perubahan:**
- Hapus endpoint screenshot automation
- Hapus import asyncio dan threading
- Kode lebih clean dan fokus pada fitur utama

---

## 🧮 Alur Proses CBF (Update untuk BAB 3)

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT USER                                   │
│   ┌─────────────────────┐    ┌─────────────────────┐           │
│   │   Cerita Narasi     │ OR │   Kata Kunci        │           │
│   │   (Textarea)        │    │   (Input Text)      │           │
│   └─────────────────────┘    └─────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 EKSTRAKSI KEYWORDS (Jika Cerita)                │
│   • Tokenisasi teks                                             │
│   • Hapus stopwords (Indonesia + English)                       │
│   • Hitung frekuensi kata                                       │
│   • Ambil top 8 keywords                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                PENCARIAN MULTI-PLATFORM                         │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│   │  Semantic   │  │   Google    │  │  Mendeley   │           │
│   │  Scholar    │  │  Scholar    │  │             │           │
│   │   (API)     │  │ (Selenium)  │  │ (Scraping)  │           │
│   └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         CONTENT-BASED FILTERING (Visualisasi Step-by-Step)      │
│                                                                 │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  STEP 1: PREPROCESSING                                  ║   │
│  ║  • Case Folding (lowercase)                             ║   │
│  ║  • Tokenization (pecah kata)                            ║   │
│  ║  • Stopword Removal (hapus kata umum)                   ║   │
│  ║  • Lemmatization (bentuk dasar)                         ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│                              │                                  │
│                              ▼                                  │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  STEP 2: TF-IDF CALCULATION                             ║   │
│  ║  • TF(t,d) = freq(t) in d / total terms in d            ║   │
│  ║  • IDF(t) = log(N / df(t)) + 1                          ║   │
│  ║  • TF-IDF = TF × IDF                                    ║   │
│  ║  • Tampilkan tabel top terms dengan skor                ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│                              │                                  │
│                              ▼                                  │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  STEP 3: COSINE SIMILARITY                              ║   │
│  ║  • cos(θ) = (A·B) / (||A|| × ||B||)                     ║   │
│  ║  • Hitung similarity query dengan setiap dokumen        ║   │
│  ║  • Tampilkan matriks similarity                         ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│                              │                                  │
│                              ▼                                  │
│  ╔═════════════════════════════════════════════════════════╗   │
│  ║  STEP 4: RANKING                                        ║   │
│  ║  • Urutkan dokumen berdasarkan skor similarity          ║   │
│  ║  • Tampilkan ranking dengan badge #1, #2, #3...         ║   │
│  ║  • Skor relevansi dalam persen                          ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUT                                   │
│   • Daftar jurnal terurut berdasarkan relevansi                │
│   • Detail perhitungan tiap step                               │
│   • Export ke CSV, JSON, BibTeX, HTML, RIS                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📐 Rumus yang Ditampilkan di Sistem

### TF-IDF
```
TF-IDF(t,d) = TF(t,d) × IDF(t)

TF(t,d) = Frequency of term t in document d / Total terms in d
IDF(t) = log(Total documents / Documents containing t)
```

### Cosine Similarity
```
cos(θ) = (A · B) / (||A|| × ||B||)

Dimana:
• A · B = Dot product dari vektor A dan B
• ||A|| = Magnitude (panjang) vektor A
• ||B|| = Magnitude (panjang) vektor B

Hasil: 0 (tidak mirip) hingga 1 (sangat mirip)
```

---

## 📸 Yang Perlu Di-Screenshot

| No | Screenshot | Keterangan |
|----|------------|------------|
| 1 | Halaman Utama | Form input cerita + search |
| 2 | Keywords Terdeteksi | Hasil ekstraksi dari cerita |
| 3 | Step 1 - Preprocessing | Teks original vs preprocessed |
| 4 | Step 2 - TF-IDF | Tabel top terms dengan skor |
| 5 | Step 3 - Cosine Similarity | Matriks similarity |
| 6 | Step 4 - Ranking | Hasil ranking dengan skor |
| 7 | Hasil Pencarian | Daftar jurnal lengkap |
| 8 | Export | Proses export data |

---

## 🗂️ Mapping ke BAB Skripsi

### BAB 3 - Metodologi Penelitian (UPDATE)

**3.1 Perancangan Sistem**
- Diagram alur sistem (flowchart di atas)
- Use case diagram

**3.2 Implementasi Content-Based Filtering**
- 3.2.1 Preprocessing Text
  - File: `content_based_filter.py` → function `preprocess_text()`
  - Screenshot: Step 1 di UI
  
- 3.2.2 Perhitungan TF-IDF
  - File: `content_based_filter.py` → class `ContentBasedFilter`
  - Library: `sklearn.feature_extraction.text.TfidfVectorizer`
  - Screenshot: Step 2 di UI
  
- 3.2.3 Perhitungan Cosine Similarity
  - File: `content_based_filter.py`
  - Library: `sklearn.metrics.pairwise.cosine_similarity`
  - Screenshot: Step 3 di UI
  
- 3.2.4 Ranking Hasil
  - Pengurutan berdasarkan skor similarity
  - Screenshot: Step 4 di UI

**3.3 Integrasi Multi-Platform**
- Semantic Scholar API
- Google Scholar Scraping
- Mendeley Scraping

**3.4 Antarmuka Pengguna**
- Input cerita/keyword
- Visualisasi step-by-step
- Export hasil

---

## ✅ Status Project

| Komponen | Status |
|----------|--------|
| Input Cerita | ✅ Selesai |
| Ekstraksi Keywords | ✅ Selesai |
| Multi-Platform Search | ✅ Selesai |
| TF-IDF Calculation | ✅ Selesai |
| Cosine Similarity | ✅ Selesai |
| Ranking | ✅ Selesai |
| Visualisasi Step-by-Step | ✅ Selesai |
| Export Data | ✅ Selesai |
| Evaluasi (Precision, Recall) | ✅ Selesai |

---

*Dokumen ini dibuat: 9 Desember 2025*
