# 📸 PANDUAN SCREENSHOT BAB IV - HASIL DAN PEMBAHASAN

## Langkah-langkah Screenshot Sistem

### Persiapan
1. Jalankan sistem: `python app.py`
2. Buka browser: `http://localhost:5000`
3. Siapkan tool screenshot (Windows: Snipping Tool / Win+Shift+S)

---

## Screenshot yang Perlu Diambil:

### 1️⃣ HALAMAN UTAMA (Homepage)
**File:** `screenshots/01_homepage.png`
- Tampilan awal sistem
- Judul sistem
- Form pencarian
- Button "Cari Jurnal"

**Yang Perlu Terlihat:**
- Header dengan judul sistem
- Search box kosong
- Tombol pencarian
- Link ke halaman metodologi

---

### 2️⃣ PROSES PENCARIAN
**File:** `screenshots/02_searching.png`
- Ketik query di search box: "machine learning"
- Pilih sumber: "Semantic Scholar" atau "Both"
- Klik tombol "Cari Jurnal"
- Screenshot saat loading/proses pencarian

**Query yang Disarankan:**
- "machine learning"
- "natural language processing"
- "deep learning"

---

### 3️⃣ HASIL PENCARIAN (Paper List)
**File:** `screenshots/03_search_results.png`
- Daftar jurnal yang ditemukan
- Skor relevansi (%) untuk setiap paper
- Judul, penulis, tahun publikasi
- Abstrak singkat
- Button aksi (View Details, Select, etc.)

**Yang Perlu Terlihat:**
- Minimal 5-10 paper hasil pencarian
- Skor relevansi yang berbeda-beda
- Ranking otomatis (tertinggi di atas)

---

### 4️⃣ DETAIL PAPER
**File:** `screenshots/04_paper_detail.png`
- Klik salah satu paper untuk lihat detail
- Informasi lengkap paper:
  - Judul lengkap
  - Penulis
  - Tahun publikasi
  - Abstrak lengkap
  - Skor relevansi
  - Sumber (Google Scholar/Semantic Scholar)
  - Link/URL paper

---

### 5️⃣ FITUR TF-IDF CALCULATION
**File:** `screenshots/05_tfidf_details.png`
- Pilih 1-3 paper (centang checkbox)
- Klik "Show TF-IDF Details" atau tombol analisis
- Screenshot hasil perhitungan:
  - Top keywords dengan bobot TF-IDF
  - Cosine similarity score
  - Tabel perhitungan

---

### 6️⃣ RESEARCH GAP ANALYSIS
**File:** `screenshots/06_research_gap.png`
- Pilih beberapa paper (5-10 paper)
- Klik "Analyze Research Gap"
- Screenshot hasil analisis:
  - Topik yang jarang diteliti
  - Keywords yang underrepresented
  - Saran penelitian

---

### 7️⃣ HALAMAN METODOLOGI
**File:** `screenshots/07_methodology_page.png`
- Klik link "Pelajari Metodologi"
- Screenshot halaman metodologi lengkap:
  - Penjelasan TF-IDF
  - Flow diagram 5 langkah
  - Contoh perhitungan

---

### 8️⃣ FLOW DIAGRAM TF-IDF
**File:** `screenshots/08_tfidf_flow.png`
- Di halaman metodologi
- Screenshot khusus untuk flow diagram:
  - 5 langkah: Pengumpulan → Preprocessing → TF-IDF → Similarity → Ranking
  - Dengan panah dan ikon

---

### 9️⃣ DETAIL LANGKAH PREPROCESSING
**File:** `screenshots/09_preprocessing_detail.png`
- Di halaman metodologi
- Klik pada step "Preprocessing"
- Screenshot panel detail yang muncul:
  - Penjelasan 4 tahap preprocessing
  - Contoh transformasi teks

---

### 🔟 EXPORT HASIL
**File:** `screenshots/10_export_options.png`
- Pilih beberapa paper
- Klik tombol "Export"
- Screenshot menu export dengan pilihan format:
  - CSV
  - JSON
  - BibTeX
  - RIS
  - HTML Report

---

### 1️⃣1️⃣ EVALUASI METRICS
**File:** `screenshots/11_evaluation_metrics.png`
- Setelah pencarian selesai
- Screenshot bagian evaluation metrics:
  - Precision
  - Recall
  - F-Measure
  - Accuracy
  - Total papers found

---

### 1️⃣2️⃣ RESPONSIVE DESIGN - MOBILE VIEW
**File:** `screenshots/12_mobile_view.png`
- Resize browser window menjadi mobile size (375px width)
- Atau gunakan DevTools (F12) → Toggle device toolbar
- Screenshot tampilan mobile:
  - Navigation yang collapsed
  - Layout yang menyesuaikan

---

### 1️⃣3️⃣ PERBANDINGAN DENGAN/TANPA CBF
**File:** `screenshots/13_with_without_cbf.png`
- Lakukan 2 pencarian dengan query sama
- Pencarian 1: Dengan CBF (Content-Based Filtering) ON
- Pencarian 2: Dengan CBF OFF
- Screenshot perbandingan hasil ranking

---

## Tips Screenshot:
1. **Resolusi:** Gunakan resolusi 1920x1080 atau minimal 1366x768
2. **Full Window:** Ambil screenshot full browser window
3. **Clean:** Tutup tab lain yang tidak perlu
4. **Zoom:** Pastikan zoom browser 100%
5. **Quality:** Save sebagai PNG untuk kualitas terbaik

## Setelah Semua Screenshot Diambil:
1. Simpan semua di folder `screenshots/`
2. Rename sesuai nomor di atas
3. Jalankan script untuk generate HTML dokumentasi
4. Update Word document BAB IV dengan referensi ke screenshot

---

## Nama File Screenshot (Checklist):
- [ ] `01_homepage.png`
- [ ] `02_searching.png`
- [ ] `03_search_results.png`
- [ ] `04_paper_detail.png`
- [ ] `05_tfidf_details.png`
- [ ] `06_research_gap.png`
- [ ] `07_methodology_page.png`
- [ ] `08_tfidf_flow.png`
- [ ] `09_preprocessing_detail.png`
- [ ] `10_export_options.png`
- [ ] `11_evaluation_metrics.png`
- [ ] `12_mobile_view.png`
- [ ] `13_with_without_cbf.png`
