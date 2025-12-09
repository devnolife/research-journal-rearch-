"""
Evaluation Metrics Module
Untuk menghitung Precision, Recall, dan F-Measure sistem rekomendasi
"""

def calculate_precision(relevant_retrieved, total_retrieved):
    """
    Precision = Jumlah dokumen relevan yang diambil / Total dokumen yang diambil
    
    Args:
        relevant_retrieved: Jumlah dokumen relevan yang berhasil diambil
        total_retrieved: Total dokumen yang diambil sistem
    
    Returns:
        Precision score (0-1)
    """
    if total_retrieved == 0:
        return 0.0
    return relevant_retrieved / total_retrieved


def calculate_recall(relevant_retrieved, total_relevant):
    """
    Recall = Jumlah dokumen relevan yang diambil / Total dokumen relevan yang ada
    
    Args:
        relevant_retrieved: Jumlah dokumen relevan yang berhasil diambil
        total_relevant: Total dokumen relevan yang seharusnya ada
    
    Returns:
        Recall score (0-1)
    """
    if total_relevant == 0:
        return 0.0
    return relevant_retrieved / total_relevant


def calculate_f_measure(precision, recall, beta=1.0):
    """
    F-Measure = (1 + beta^2) * (precision * recall) / (beta^2 * precision + recall)
    
    Untuk beta=1 (F1-Score):
    F1 = 2 * (precision * recall) / (precision + recall)
    
    Args:
        precision: Precision score
        recall: Recall score
        beta: Weight parameter (default 1.0 for F1-score)
    
    Returns:
        F-Measure score (0-1)
    """
    if precision + recall == 0:
        return 0.0
    
    beta_squared = beta ** 2
    return (1 + beta_squared) * (precision * recall) / (beta_squared * precision + recall)


def evaluate_search_results(retrieved_papers, relevant_paper_ids, total_relevant_in_corpus=None):
    """
    Evaluasi hasil pencarian dengan Precision, Recall, F-Measure
    
    Args:
        retrieved_papers: List of papers yang diambil oleh sistem
        relevant_paper_ids: Set of paper IDs/titles yang dianggap relevan (ground truth)
        total_relevant_in_corpus: Total dokumen relevan di corpus (untuk recall)
    
    Returns:
        Dictionary dengan metrics
    """
    # Hitung relevant retrieved
    retrieved_titles = {p.get('title', '').lower().strip() for p in retrieved_papers}
    relevant_titles = {t.lower().strip() for t in relevant_paper_ids}
    
    relevant_retrieved = len(retrieved_titles & relevant_titles)
    total_retrieved = len(retrieved_papers)
    total_relevant = total_relevant_in_corpus if total_relevant_in_corpus else len(relevant_paper_ids)
    
    # Calculate metrics
    precision = calculate_precision(relevant_retrieved, total_retrieved)
    recall = calculate_recall(relevant_retrieved, total_relevant)
    f1 = calculate_f_measure(precision, recall, beta=1.0)
    f2 = calculate_f_measure(precision, recall, beta=2.0)  # F2 lebih menekankan recall
    
    return {
        'precision': round(precision * 100, 2),
        'recall': round(recall * 100, 2),
        'f1_score': round(f1 * 100, 2),
        'f2_score': round(f2 * 100, 2),
        'relevant_retrieved': relevant_retrieved,
        'total_retrieved': total_retrieved,
        'total_relevant': total_relevant
    }


def evaluate_by_relevance_threshold(papers, threshold=50.0):
    """
    Evaluasi berdasarkan threshold relevance_score
    Papers dengan score >= threshold dianggap "relevan"
    
    Args:
        papers: List of papers dengan relevance_score
        threshold: Threshold untuk dianggap relevan (default 50%)
    
    Returns:
        Evaluation metrics
    """
    total = len(papers)
    if total == 0:
        return {
            'high_relevance': 0,
            'medium_relevance': 0,
            'low_relevance': 0,
            'average_score': 0,
            'distribution': {}
        }
    
    high = sum(1 for p in papers if p.get('relevance_score', 0) >= 70)
    medium = sum(1 for p in papers if 40 <= p.get('relevance_score', 0) < 70)
    low = sum(1 for p in papers if p.get('relevance_score', 0) < 40)
    
    avg_score = sum(p.get('relevance_score', 0) for p in papers) / total
    
    return {
        'high_relevance': high,
        'medium_relevance': medium,
        'low_relevance': low,
        'high_percentage': round(high / total * 100, 2),
        'medium_percentage': round(medium / total * 100, 2),
        'low_percentage': round(low / total * 100, 2),
        'average_score': round(avg_score, 2),
        'total_papers': total
    }


def generate_evaluation_report(papers, query):
    """
    Generate laporan evaluasi lengkap
    
    Args:
        papers: List of papers dengan relevance_score
        query: Query yang digunakan
    
    Returns:
        Dictionary dengan laporan evaluasi
    """
    if not papers:
        return {'error': 'No papers to evaluate'}
    
    # Basic stats
    total = len(papers)
    scores = [p.get('relevance_score', 0) for p in papers]
    
    # Distribution analysis
    distribution = evaluate_by_relevance_threshold(papers)
    
    # Top and bottom papers
    sorted_papers = sorted(papers, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    report = {
        'query': query,
        'total_results': total,
        'score_statistics': {
            'average': round(sum(scores) / total, 2) if total > 0 else 0,
            'max': round(max(scores), 2) if scores else 0,
            'min': round(min(scores), 2) if scores else 0,
            'median': round(sorted(scores)[total // 2], 2) if scores else 0
        },
        'distribution': distribution,
        'top_5_papers': [
            {
                'title': p.get('title', '')[:80],
                'score': p.get('relevance_score', 0),
                'source': p.get('source', 'Unknown')
            }
            for p in sorted_papers[:5]
        ],
        'recommendations': []
    }
    
    # Add recommendations based on analysis
    if distribution['average_score'] < 30:
        report['recommendations'].append("Pertimbangkan untuk memperluas kata kunci pencarian")
    if distribution['high_percentage'] < 20:
        report['recommendations'].append("Hasil memiliki sedikit paper dengan relevansi tinggi")
    if total < 10:
        report['recommendations'].append("Jumlah hasil terbatas, coba kata kunci yang lebih umum")
    
    return report


# Test
if __name__ == "__main__":
    print("Testing Evaluation Metrics...")
    
    # Test basic metrics
    p = calculate_precision(8, 10)
    r = calculate_recall(8, 20)
    f1 = calculate_f_measure(p, r)
    
    print(f"Precision: {p:.2%}")
    print(f"Recall: {r:.2%}")
    print(f"F1-Score: {f1:.2%}")
    
    # Test with sample papers
    sample_papers = [
        {'title': 'Paper 1', 'relevance_score': 85.5},
        {'title': 'Paper 2', 'relevance_score': 72.3},
        {'title': 'Paper 3', 'relevance_score': 55.1},
        {'title': 'Paper 4', 'relevance_score': 45.0},
        {'title': 'Paper 5', 'relevance_score': 30.2},
    ]
    
    report = generate_evaluation_report(sample_papers, "machine learning")
    print(f"\nEvaluation Report:")
    print(f"  Average Score: {report['score_statistics']['average']}%")
    print(f"  High Relevance: {report['distribution']['high_percentage']}%")
