# 📚 Research Journal Search System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Multi-Platform Journal Search System with Content-Based Filtering**

*Sistem Pencarian Jurnal Berbasis Multi Platform Menggunakan Content-Based Filtering*

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Reference](#api-reference)

</div>

---

## 📋 Overview

Research Journal Search System adalah aplikasi web untuk pencarian jurnal ilmiah dari berbagai platform akademik menggunakan pendekatan **Content-Based Filtering (CBF)**. Sistem ini mengimplementasikan algoritma **TF-IDF** (Term Frequency-Inverse Document Frequency) dan **Cosine Similarity** untuk memberikan ranking paper yang relevan dengan query pencarian.

### 🎯 Key Features

- **Multi-Platform Search**: Pencarian dari Semantic Scholar, Google Scholar, dan Mendeley
- **Content-Based Filtering**: Ranking paper menggunakan TF-IDF + Cosine Similarity
- **Smart Keyword Extraction**: Ekstraksi keyword otomatis dari cerita/deskripsi penelitian
- **Step-by-Step Visualization**: Visualisasi proses CBF (Preprocessing → TF-IDF → Cosine Similarity → Ranking)
- **Evaluation Metrics**: Precision, Recall, F-Measure
- **Multiple Export Formats**: CSV, JSON, BibTeX, RIS, HTML Report
- **PDF Abstract Extraction**: Upload PDF untuk ekstraksi abstrak otomatis
- **Research Topic Generation**: Generate topik penelitian dari paper terpilih

---

## 🏗️ Project Structure

```
research-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── src/                   # Source code packages
│   ├── __init__.py
│   ├── scrapers/          # Platform scrapers
│   │   ├── __init__.py
│   │   ├── scholar_scraper.py     # Google Scholar scraper
│   │   ├── mendeley_scraper.py    # Mendeley scraper
│   │   └── semantic_scholar.py    # Semantic Scholar API
│   ├── core/              # Core algorithms
│   │   ├── __init__.py
│   │   ├── content_based_filter.py  # TF-IDF + Cosine Similarity
│   │   └── evaluation_metrics.py    # Precision, Recall, F-Measure
│   └── utils/             # Utilities
│       ├── __init__.py
│       ├── export_module.py       # Export functions
│       ├── pdf_processor.py       # PDF processing
│       ├── topic_generator.py     # Topic generation
│       └── research_analyzer.py   # Research analysis
├── templates/             # HTML templates
│   └── index.html
├── static/                # Static files (JS, CSS)
│   └── cbf-calculation.js
├── docs/                  # Documentation
├── testing_results/       # Test outputs
└── uploads/               # Uploaded files
```

---

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome browser (for Google Scholar scraping)

### Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/research-system.git
   cd research-system
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data** (for text preprocessing)
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

5. **Run Application**
   ```bash
   python app.py
   ```

6. **Open Browser**
   ```
   http://localhost:5000
   ```

---

## 🚀 Usage

### Basic Search

1. Pilih sumber data (Semantic Scholar / Google Scholar / Mendeley)
2. Masukkan query pencarian atau deskripsi penelitian
3. Klik **"Cari Jurnal"**
4. Lihat hasil ranking dan detail perhitungan CBF

### Story Input Mode

1. Masukkan cerita/deskripsi penelitian di textarea
2. Sistem akan mengekstrak keyword secara otomatis
3. Keyword dapat diedit sebelum pencarian
4. Klik **"Cari Berdasarkan Cerita"**

### CBF Process Visualization

Setelah pencarian, klik **"Lihat Proses CBF"** untuk melihat:
- **Preprocessing**: Tokenisasi, stopword removal, lemmatization
- **TF-IDF**: Top terms dengan bobot TF-IDF
- **Cosine Similarity**: Matriks similarity antar dokumen
- **Ranking**: Paper diurutkan berdasarkan skor similarity

---

## 🔬 Algorithm Details

### Content-Based Filtering

```
1. Text Preprocessing
   - Case folding (lowercase)
   - Tokenization
   - Stopword removal (English & Indonesian)
   - Lemmatization

2. TF-IDF Vectorization
   - max_features: 5000
   - ngram_range: (1, 2)
   - sublinear_tf: True (1 + log(tf))

3. Cosine Similarity
   similarity(A, B) = (A · B) / (||A|| × ||B||)

4. Ranking
   Papers diurutkan berdasarkan skor cosine similarity
   terhadap query/reference paper
```

### Evaluation Metrics

- **Precision**: Relevan retrieved / Total retrieved
- **Recall**: Relevan retrieved / Total relevan
- **F-Measure**: 2 × (Precision × Recall) / (Precision + Recall)

---

## 📡 API Reference

### Search Papers
```http
POST /api/search
Content-Type: application/json

{
  "query": "machine learning",
  "max_results": 20,
  "source": "semantic",
  "use_cbf": true,
  "filters": {
    "year_start": 2020,
    "year_end": 2024
  }
}
```

### Get CBF Details
```http
POST /api/cbf-details
Content-Type: application/json

{
  "papers": [...],
  "query": "machine learning"
}
```

### Export Results
```http
POST /api/export
Content-Type: application/json

{
  "papers": [...],
  "format": "csv",
  "query": "search_results"
}
```

### Get Recommendations
```http
POST /api/recommendations
Content-Type: application/json

{
  "selected_papers": [...],
  "all_papers": [...],
  "top_n": 10
}
```

---

## 📦 Dependencies

| Package | Version | Description |
|---------|---------|-------------|
| Flask | 2.0+ | Web framework |
| scikit-learn | 1.0+ | TF-IDF, Cosine Similarity |
| nltk | 3.8+ | Text preprocessing |
| requests | 2.28+ | HTTP requests |
| beautifulsoup4 | 4.12+ | HTML parsing |
| selenium | 4.0+ | Browser automation |
| pdfplumber | 0.10+ | PDF processing |
| pandas | 2.0+ | Data manipulation |

---

## 🧪 Testing

```bash
# Run all tests
python run_testing.py

# Output files akan disimpan di testing_results/
```

---

## 📊 Sample Output

### Search Results
```json
{
  "success": true,
  "papers": [
    {
      "title": "Deep Learning for NLP",
      "authors": "John Doe, Jane Smith",
      "year": 2023,
      "abstract": "...",
      "similarity_score": 0.87,
      "rank": 1
    }
  ],
  "evaluation": {
    "precision": 0.85,
    "recall": 0.72,
    "f_measure": 0.78
  }
}
```

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👥 Authors

- **Developer** - *Initial work* - Research System Team

---

## 🙏 Acknowledgments

- [Semantic Scholar API](https://api.semanticscholar.org/)
- [Google Scholar](https://scholar.google.com/)
- [Mendeley](https://www.mendeley.com/)
- [scikit-learn](https://scikit-learn.org/)
- [NLTK](https://www.nltk.org/)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ for Academic Research

</div>
