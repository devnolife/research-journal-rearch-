"""
Script Testing untuk Sistem Pencarian Jurnal Berbasis Content-Based Filtering
Menghasilkan output sesuai proposal penelitian

Output folder: testing_results/
"""

import os
import json
import csv
from datetime import datetime
from semantic_scholar import search_semantic_scholar
from content_based_filter import ContentBasedFilter, rank_papers_with_cbf
from evaluation_metrics import evaluate_by_relevance_threshold, generate_evaluation_report

# Buat folder output
OUTPUT_DIR = 'testing_results'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def save_json(data, filename):
    """Simpan data ke file JSON"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Saved: {filepath}")

def save_csv(data, filename, headers):
    """Simpan data ke file CSV"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"  ✓ Saved: {filepath}")

def save_text(content, filename):
    """Simpan text ke file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved: {filepath}")


def run_test(query, max_results=10):
    """
    Jalankan testing lengkap untuk satu query
    """
    print(f"\n{'='*60}")
    print(f"TESTING: '{query}'")
    print(f"{'='*60}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    query_slug = query.replace(' ', '_')[:30]
    
    # =====================================================
    # TAHAP 1: PENGUMPULAN DATA (Searching)
    # =====================================================
    print("\n[1] PENGUMPULAN DATA dari Semantic Scholar...")
    
    papers = search_semantic_scholar(query, max_results)
    print(f"    Ditemukan: {len(papers)} jurnal")
    
    # Simpan hasil pencarian mentah
    save_json({
        'query': query,
        'timestamp': timestamp,
        'total_results': len(papers),
        'papers': papers
    }, f'1_hasil_pencarian_{query_slug}.json')
    
    # Simpan dalam format CSV
    csv_data = []
    for i, p in enumerate(papers, 1):
        csv_data.append([
            i,
            p.get('title', ''),
            p.get('authors', ''),
            p.get('year', ''),
            p.get('citations', ''),
            p.get('abstract', '')[:200] + '...' if len(p.get('abstract', '')) > 200 else p.get('abstract', '')
        ])
    save_csv(csv_data, f'1_hasil_pencarian_{query_slug}.csv', 
             ['No', 'Judul', 'Penulis', 'Tahun', 'Sitasi', 'Abstrak'])
    
    if not papers:
        print("    ⚠ Tidak ada hasil. Skip testing.")
        return None
    
    # =====================================================
    # TAHAP 2: PREPROCESSING
    # =====================================================
    print("\n[2] PREPROCESSING TEKS...")
    
    cbf = ContentBasedFilter()
    
    # Preprocess setiap dokumen
    preprocessing_results = []
    for i, paper in enumerate(papers):
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        preprocessed = cbf.preprocess_text(text)
        
        preprocessing_results.append({
            'dokumen': f'D{i+1}',
            'judul': paper.get('title', '')[:50] + '...',
            'teks_asli': text[:200] + '...',
            'setelah_preprocessing': preprocessed[:200] + '...',
            'jumlah_kata_asli': len(text.split()),
            'jumlah_kata_setelah': len(preprocessed.split())
        })
    
    save_json({
        'tahap': 'Preprocessing',
        'langkah': [
            '1. Case Folding (lowercase)',
            '2. Tokenisasi',
            '3. Penghapusan Stopwords',
            '4. Lemmatisasi'
        ],
        'hasil': preprocessing_results
    }, f'2_preprocessing_{query_slug}.json')
    
    # =====================================================
    # TAHAP 3: PEMBOBOTAN TF-IDF
    # =====================================================
    print("\n[3] PERHITUNGAN TF-IDF...")
    
    cbf.fit(papers)
    
    tfidf_results = []
    for i, paper in enumerate(papers):
        terms = cbf.get_tfidf_terms(i, 10)
        tfidf_results.append({
            'dokumen': f'D{i+1}',
            'judul': paper.get('title', '')[:60],
            'top_terms': [{'term': t, 'bobot_tfidf': round(w, 4)} for t, w in terms]
        })
    
    # Simpan hasil TF-IDF
    save_json({
        'tahap': 'Pembobotan TF-IDF',
        'formula': {
            'tfidf': 'TF-IDF(t,d) = TF(t,d) × IDF(t)',
            'tf': 'TF(t,d) = frekuensi term t dalam dokumen d',
            'idf': 'IDF(t) = log(N / df(t)) + 1'
        },
        'total_dokumen': len(papers),
        'total_terms_unik': len(cbf.vectorizer.get_feature_names_out()) if cbf.vectorizer else 0,
        'hasil_per_dokumen': tfidf_results
    }, f'3_tfidf_{query_slug}.json')
    
    # Buat tabel TF-IDF dalam format CSV
    tfidf_csv = []
    for doc in tfidf_results:
        for term_data in doc['top_terms']:
            tfidf_csv.append([
                doc['dokumen'],
                doc['judul'][:40],
                term_data['term'],
                term_data['bobot_tfidf']
            ])
    save_csv(tfidf_csv, f'3_tfidf_{query_slug}.csv',
             ['Dokumen', 'Judul', 'Term', 'Bobot TF-IDF'])
    
    # =====================================================
    # TAHAP 4: COSINE SIMILARITY
    # =====================================================
    print("\n[4] PERHITUNGAN COSINE SIMILARITY...")
    
    # Hitung similarity dengan query
    query_similarities = cbf.calculate_similarity_to_query(query)
    
    similarity_results = {
        'formula': 'Cosine Similarity = (A · B) / (||A|| × ||B||)',
        'deskripsi': 'Mengukur kemiripan sudut antara vektor query dan vektor dokumen',
        'query': query,
        'hasil_similarity': []
    }
    
    for idx, score in query_similarities:
        similarity_results['hasil_similarity'].append({
            'dokumen': f'D{idx+1}',
            'judul': papers[idx].get('title', '')[:60],
            'cosine_similarity': round(score, 4),
            'persentase': round(score * 100, 2)
        })
    
    save_json(similarity_results, f'4_cosine_similarity_{query_slug}.json')
    
    # Buat matriks similarity antar dokumen
    if cbf.tfidf_matrix is not None:
        from sklearn.metrics.pairwise import cosine_similarity
        sim_matrix = cosine_similarity(cbf.tfidf_matrix)
        
        # Simpan matriks dalam format readable
        matrix_text = "MATRIKS COSINE SIMILARITY ANTAR DOKUMEN\n"
        matrix_text += "=" * 60 + "\n\n"
        matrix_text += f"Query: {query}\n"
        matrix_text += f"Jumlah Dokumen: {len(papers)}\n\n"
        
        # Header
        matrix_text += "       "
        for i in range(min(len(papers), 10)):
            matrix_text += f"  D{i+1:02d}  "
        matrix_text += "\n"
        
        # Rows
        for i in range(min(len(papers), 10)):
            matrix_text += f"D{i+1:02d}   "
            for j in range(min(len(papers), 10)):
                matrix_text += f" {sim_matrix[i][j]:.3f} "
            matrix_text += "\n"
        
        save_text(matrix_text, f'4_matriks_similarity_{query_slug}.txt')
    
    # =====================================================
    # TAHAP 5: RANKING HASIL
    # =====================================================
    print("\n[5] RANKING BERDASARKAN RELEVANSI...")
    
    ranked_papers = rank_papers_with_cbf(papers, query)
    
    ranking_results = {
        'query': query,
        'metode': 'Content-Based Filtering dengan TF-IDF dan Cosine Similarity',
        'hasil_ranking': []
    }
    
    for rank, paper in enumerate(ranked_papers, 1):
        ranking_results['hasil_ranking'].append({
            'ranking': rank,
            'judul': paper.get('title', ''),
            'penulis': paper.get('authors', ''),
            'tahun': paper.get('year', ''),
            'skor_relevansi': paper.get('relevance_score', 0),
            'sitasi': paper.get('citations', 0)
        })
    
    save_json(ranking_results, f'5_ranking_{query_slug}.json')
    
    # Simpan ranking dalam CSV
    ranking_csv = []
    for r in ranking_results['hasil_ranking']:
        ranking_csv.append([
            r['ranking'],
            r['judul'],
            r['penulis'],
            r['tahun'],
            f"{r['skor_relevansi']}%",
            r['sitasi']
        ])
    save_csv(ranking_csv, f'5_ranking_{query_slug}.csv',
             ['Ranking', 'Judul', 'Penulis', 'Tahun', 'Skor Relevansi', 'Sitasi'])
    
    # =====================================================
    # TAHAP 6: EVALUASI
    # =====================================================
    print("\n[6] EVALUASI SISTEM...")
    
    evaluation = evaluate_by_relevance_threshold(ranked_papers)
    report = generate_evaluation_report(ranked_papers, query)
    
    eval_results = {
        'query': query,
        'total_hasil': len(ranked_papers),
        'distribusi_relevansi': {
            'tinggi_>=70%': evaluation.get('high_relevance', 0),
            'sedang_40-70%': evaluation.get('medium_relevance', 0),
            'rendah_<40%': evaluation.get('low_relevance', 0)
        },
        'statistik': {
            'rata_rata_skor': evaluation.get('average_score', 0),
            'skor_tertinggi': report.get('score_statistics', {}).get('max', 0),
            'skor_terendah': report.get('score_statistics', {}).get('min', 0),
            'median_skor': report.get('score_statistics', {}).get('median', 0)
        },
        'metrik': {
            'precision_tinggi': round(evaluation.get('high_relevance', 0) / len(ranked_papers) * 100, 2) if ranked_papers else 0
        }
    }
    
    save_json(eval_results, f'6_evaluasi_{query_slug}.json')
    
    # Buat laporan evaluasi teks
    eval_text = f"""
LAPORAN EVALUASI SISTEM PENCARIAN JURNAL
==========================================
Content-Based Filtering dengan TF-IDF + Cosine Similarity

Query: {query}
Tanggal: {datetime.now().strftime('%d %B %Y, %H:%M')}
Total Hasil: {len(ranked_papers)} jurnal

DISTRIBUSI RELEVANSI:
---------------------
• Relevansi Tinggi (≥70%)  : {evaluation.get('high_relevance', 0)} jurnal ({evaluation.get('high_percentage', 0)}%)
• Relevansi Sedang (40-70%): {evaluation.get('medium_relevance', 0)} jurnal ({evaluation.get('medium_percentage', 0)}%)
• Relevansi Rendah (<40%)  : {evaluation.get('low_relevance', 0)} jurnal ({evaluation.get('low_percentage', 0)}%)

STATISTIK SKOR:
---------------
• Rata-rata   : {evaluation.get('average_score', 0)}%
• Tertinggi   : {report.get('score_statistics', {}).get('max', 0)}%
• Terendah    : {report.get('score_statistics', {}).get('min', 0)}%
• Median      : {report.get('score_statistics', {}).get('median', 0)}%

TOP 5 HASIL PALING RELEVAN:
---------------------------
"""
    for i, paper in enumerate(ranked_papers[:5], 1):
        eval_text += f"{i}. [{paper.get('relevance_score', 0)}%] {paper.get('title', '')[:60]}...\n"
    
    save_text(eval_text, f'6_laporan_evaluasi_{query_slug}.txt')
    
    print(f"\n✅ Testing selesai! Hasil disimpan di folder: {OUTPUT_DIR}/")
    
    return {
        'query': query,
        'total_papers': len(papers),
        'evaluation': evaluation
    }


def run_all_tests():
    """
    Jalankan testing untuk beberapa query
    """
    print("\n" + "="*70)
    print("SISTEM PENCARIAN JURNAL ILMIAH BERBASIS CONTENT-BASED FILTERING")
    print("Testing Otomatis - Sesuai Proposal Penelitian")
    print("="*70)
    
    # Query untuk testing
    test_queries = [
        "machine learning classification",
        "deep learning neural network",
        "content based filtering recommendation"
    ]
    
    results = []
    for query in test_queries:
        result = run_test(query, max_results=10)
        if result:
            results.append(result)
    
    # Simpan ringkasan semua testing
    summary = {
        'tanggal_testing': datetime.now().isoformat(),
        'jumlah_query': len(test_queries),
        'ringkasan': results
    }
    save_json(summary, 'RINGKASAN_TESTING.json')
    
    print("\n" + "="*70)
    print("TESTING SELESAI!")
    print(f"Semua hasil tersimpan di folder: {OUTPUT_DIR}/")
    print("="*70)
    
    # List semua file yang dihasilkan
    print("\nFile yang dihasilkan:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f"  • {f} ({size:,} bytes)")


if __name__ == "__main__":
    run_all_tests()
