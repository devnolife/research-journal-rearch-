"""
Export Module
Untuk mengekspor hasil pencarian ke berbagai format
"""

import json
import csv
import io
from datetime import datetime


def export_to_csv(papers, filename=None):
    """
    Export papers ke format CSV
    
    Args:
        papers: List of paper dictionaries
        filename: Optional filename, if None returns string
    
    Returns:
        CSV string atau path file
    """
    if not papers:
        return ""
    
    # Define columns
    columns = ['No', 'Judul', 'Penulis', 'Tahun', 'Sumber', 'Sitasi', 'Skor Relevansi (%)', 'URL', 'Abstrak']
    
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    
    # Write header
    writer.writerow(columns)
    
    # Write data
    for i, paper in enumerate(papers, 1):
        row = [
            i,
            paper.get('title', ''),
            paper.get('authors', ''),
            paper.get('year', ''),
            paper.get('source', ''),
            paper.get('citations', '0'),
            paper.get('relevance_score', ''),
            paper.get('url', paper.get('scholar_url', '')),
            paper.get('abstract', '')[:500]  # Limit abstract length
        ]
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    if filename:
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(csv_content)
        return filename
    
    return csv_content


def export_to_json(papers, filename=None, include_metadata=True):
    """
    Export papers ke format JSON
    
    Args:
        papers: List of paper dictionaries
        filename: Optional filename
        include_metadata: Include export metadata
    
    Returns:
        JSON string atau path file
    """
    export_data = {
        'papers': papers,
        'total': len(papers)
    }
    
    if include_metadata:
        export_data['metadata'] = {
            'exported_at': datetime.now().isoformat(),
            'format_version': '1.0',
            'source': 'Sistem Pencarian Jurnal Ilmiah'
        }
    
    json_content = json.dumps(export_data, ensure_ascii=False, indent=2)
    
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json_content)
        return filename
    
    return json_content


def export_to_bibtex(papers, filename=None):
    """
    Export papers ke format BibTeX untuk referensi
    
    Args:
        papers: List of paper dictionaries
        filename: Optional filename
    
    Returns:
        BibTeX string atau path file
    """
    bibtex_entries = []
    
    for i, paper in enumerate(papers, 1):
        # Generate citation key
        first_author = paper.get('authors', 'unknown').split(',')[0].split()[-1] if paper.get('authors') else 'unknown'
        year = paper.get('year', 'n.d.')
        key = f"{first_author.lower()}{year}_{i}"
        
        # Clean title for BibTeX
        title = paper.get('title', 'Untitled').replace('{', '\\{').replace('}', '\\}')
        
        entry = f"""@article{{{key},
  title = {{{title}}},
  author = {{{paper.get('authors', 'Unknown')}}},
  year = {{{year}}},
  abstract = {{{paper.get('abstract', '')[:300]}}},
  url = {{{paper.get('url', '')}}},
  note = {{Source: {paper.get('source', 'Unknown')}, Citations: {paper.get('citations', '0')}}}
}}"""
        bibtex_entries.append(entry)
    
    bibtex_content = '\n\n'.join(bibtex_entries)
    
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(bibtex_content)
        return filename
    
    return bibtex_content


def export_to_html_report(papers, query, evaluation=None):
    """
    Export ke laporan HTML yang bisa dicetak
    
    Args:
        papers: List of paper dictionaries
        query: Search query
        evaluation: Optional evaluation metrics
    
    Returns:
        HTML string
    """
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan Pencarian Jurnal - {query}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20mm;
        }}
        h1 {{ color: #1a365d; margin-bottom: 20px; font-size: 24px; }}
        h2 {{ color: #2d3748; margin: 20px 0 10px; font-size: 18px; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #3182ce; }}
        .meta {{ color: #718096; font-size: 14px; margin-top: 10px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
        .stat-box {{ 
            background: #f7fafc; 
            padding: 15px 20px; 
            border-radius: 8px; 
            border-left: 4px solid #3182ce;
            flex: 1;
            min-width: 150px;
        }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2d3748; }}
        .stat-label {{ color: #718096; font-size: 12px; }}
        .paper {{ 
            margin: 15px 0; 
            padding: 15px; 
            border: 1px solid #e2e8f0; 
            border-radius: 8px;
            page-break-inside: avoid;
        }}
        .paper-title {{ font-weight: bold; color: #2d3748; margin-bottom: 8px; }}
        .paper-meta {{ font-size: 13px; color: #718096; margin-bottom: 8px; }}
        .paper-abstract {{ font-size: 13px; color: #4a5568; }}
        .score {{ 
            display: inline-block;
            background: #48bb78; 
            color: white; 
            padding: 2px 8px; 
            border-radius: 4px; 
            font-size: 12px;
        }}
        .score.medium {{ background: #ed8936; }}
        .score.low {{ background: #e53e3e; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #718096; font-size: 12px; }}
        @media print {{
            body {{ padding: 10mm; }}
            .paper {{ break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Laporan Hasil Pencarian Jurnal Ilmiah</h1>
        <div class="meta">
            <strong>Kata Kunci:</strong> {query}<br>
            <strong>Tanggal:</strong> {datetime.now().strftime('%d %B %Y, %H:%M')}<br>
            <strong>Total Hasil:</strong> {len(papers)} jurnal
        </div>
    </div>
"""
    
    # Add evaluation stats if available
    if evaluation:
        html += f"""
    <h2>📊 Statistik Evaluasi</h2>
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{evaluation.get('average_score', 0)}%</div>
            <div class="stat-label">Rata-rata Skor Relevansi</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{evaluation.get('high_relevance', 0)}</div>
            <div class="stat-label">Relevansi Tinggi (≥70%)</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{evaluation.get('medium_relevance', 0)}</div>
            <div class="stat-label">Relevansi Sedang (40-70%)</div>
        </div>
    </div>
"""
    
    # Add papers
    html += "\n    <h2>📄 Daftar Jurnal</h2>\n"
    
    for i, paper in enumerate(papers, 1):
        score = paper.get('relevance_score', 0)
        score_class = 'low' if score < 40 else ('medium' if score < 70 else '')
        
        html += f"""
    <div class="paper">
        <div class="paper-title">{i}. {paper.get('title', 'Tanpa Judul')}</div>
        <div class="paper-meta">
            <strong>Penulis:</strong> {paper.get('authors', 'Tidak diketahui')} | 
            <strong>Tahun:</strong> {paper.get('year', '-')} | 
            <strong>Sumber:</strong> {paper.get('source', '-')} | 
            <strong>Sitasi:</strong> {paper.get('citations', '0')}
            <span class="score {score_class}">{score}% relevan</span>
        </div>
        <div class="paper-abstract">{paper.get('abstract', 'Tidak ada abstrak')[:400]}...</div>
    </div>
"""
    
    html += f"""
    <div class="footer">
        <p>Dihasilkan oleh Sistem Pencarian Jurnal Ilmiah Berbasis Content-Based Filtering</p>
        <p>TF-IDF + Cosine Similarity | {datetime.now().year}</p>
    </div>
</body>
</html>"""
    
    return html


def export_to_ris(papers, filename=None):
    """
    Export ke format RIS (Research Information Systems)
    Format standar untuk import ke reference managers
    """
    ris_entries = []
    
    for paper in papers:
        entry_lines = [
            "TY  - JOUR",  # Type: Journal Article
            f"TI  - {paper.get('title', '')}",
            f"AU  - {paper.get('authors', '').replace(', ', '\nAU  - ')}",
            f"PY  - {paper.get('year', '')}",
            f"AB  - {paper.get('abstract', '')}",
            f"UR  - {paper.get('url', '')}",
            f"N1  - Source: {paper.get('source', '')}, Relevance: {paper.get('relevance_score', '')}%",
            "ER  - "
        ]
        ris_entries.append('\n'.join(entry_lines))
    
    ris_content = '\n\n'.join(ris_entries)
    
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ris_content)
        return filename
    
    return ris_content


# Test
if __name__ == "__main__":
    print("Testing Export Module...")
    
    sample_papers = [
        {
            'title': 'Deep Learning for NLP',
            'authors': 'John Doe, Jane Smith',
            'year': '2024',
            'source': 'Semantic Scholar',
            'citations': '150',
            'relevance_score': 85.5,
            'url': 'https://example.com/paper1',
            'abstract': 'This paper explores deep learning techniques for natural language processing tasks.'
        },
        {
            'title': 'Machine Learning in Healthcare',
            'authors': 'Alice Brown',
            'year': '2023',
            'source': 'Google Scholar',
            'citations': '75',
            'relevance_score': 62.3,
            'url': 'https://example.com/paper2',
            'abstract': 'An investigation into machine learning applications in medical diagnosis.'
        }
    ]
    
    # Test CSV
    csv_output = export_to_csv(sample_papers)
    print(f"CSV Output (first 200 chars):\n{csv_output[:200]}...")
    
    # Test BibTeX
    bibtex_output = export_to_bibtex(sample_papers)
    print(f"\nBibTeX Output (first 300 chars):\n{bibtex_output[:300]}...")
    
    print("\nExport module ready!")
