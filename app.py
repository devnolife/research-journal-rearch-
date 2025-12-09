from flask import Flask, render_template, request, jsonify, Response
import json
import os

# Import from restructured packages
from src.scrapers import scrape_papers_with_abstracts, scrape_mendeley_papers, search_semantic_scholar
from src.core import (
    rank_papers_with_cbf, 
    get_paper_recommendations, 
    find_similar_papers, 
    get_cbf_calculation_details,
    generate_evaluation_report, 
    evaluate_by_relevance_threshold
)
from src.utils import (
    generate_research_topics, 
    extract_abstract_from_pdf,
    export_to_csv, 
    export_to_json, 
    export_to_bibtex, 
    export_to_html_report, 
    export_to_ris
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if not exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_papers():
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 20)
        filters = data.get('filters', {})
        source = data.get('source', 'semantic')  # scholar, mendeley, semantic, or both
        use_cbf = data.get('use_cbf', True)  # Use Content-Based Filtering
        
        print(f"[DEBUG] Search request: query='{query}', max_results={max_results}, source={source}")
        print(f"[DEBUG] Filters: {filters}, CBF: {use_cbf}")
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        papers = []
        
        # Search based on source selection
        if source == 'scholar':
            print(f"[DEBUG] Searching Google Scholar...")
            scholar_papers = scrape_papers_with_abstracts(query, max_results, filters)
            for paper in scholar_papers:
                paper['source'] = 'Google Scholar'
            papers.extend(scholar_papers)
            print(f"[DEBUG] Found {len(scholar_papers)} papers from Google Scholar")
            
            # Fallback to Semantic Scholar if Google fails
            if len(papers) == 0:
                print(f"[DEBUG] Google Scholar failed, falling back to Semantic Scholar...")
                semantic_papers = search_semantic_scholar(query, max_results, filters)
                papers.extend(semantic_papers)
        
        elif source == 'semantic':
            print(f"[DEBUG] Searching Semantic Scholar...")
            semantic_papers = search_semantic_scholar(query, max_results, filters)
            papers.extend(semantic_papers)
            print(f"[DEBUG] Found {len(semantic_papers)} papers from Semantic Scholar")
        
        elif source == 'mendeley':
            print(f"[DEBUG] Searching Mendeley...")
            mendeley_papers = scrape_mendeley_papers(query, max_results, filters)
            for paper in mendeley_papers:
                paper['source'] = 'Mendeley'
            papers.extend(mendeley_papers)
            print(f"[DEBUG] Found {len(mendeley_papers)} papers from Mendeley")
        
        elif source == 'both':
            # Use Semantic Scholar (more reliable) + Mendeley
            print(f"[DEBUG] Searching multiple sources...")
            
            # Semantic Scholar
            semantic_papers = search_semantic_scholar(query, max_results // 2, filters)
            papers.extend(semantic_papers)
            print(f"[DEBUG] Found {len(semantic_papers)} papers from Semantic Scholar")
            
            # Mendeley
            mendeley_papers = scrape_mendeley_papers(query, max_results // 2, filters)
            for paper in mendeley_papers:
                paper['source'] = 'Mendeley'
            papers.extend(mendeley_papers)
            print(f"[DEBUG] Found {len(mendeley_papers)} papers from Mendeley")
        
        # Apply Content-Based Filtering (TF-IDF + Cosine Similarity ranking)
        if use_cbf and papers:
            print(f"[DEBUG] Applying Content-Based Filtering...")
            try:
                papers = rank_papers_with_cbf(papers, query)
                print(f"[DEBUG] Papers ranked by relevance")
            except Exception as e:
                print(f"[WARNING] CBF failed: {e}, returning unranked results")
        
        # Limit total results
        papers = papers[:max_results]
        
        # Generate evaluation metrics
        evaluation = evaluate_by_relevance_threshold(papers) if papers else {}
        
        print(f"[DEBUG] Total papers: {len(papers)}")
        
        if papers:
            print(f"[DEBUG] Top paper: {papers[0].get('title', 'No title')[:50]}...")
        
        return jsonify({
            'success': True,
            'papers': papers,
            'total': len(papers),
            'evaluation': evaluation
        })
    
    except Exception as e:
        print(f"[ERROR] Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-papers', methods=['POST'])
def analyze_papers():
    try:
        data = request.get_json()
        selected_papers = data.get('papers', [])
        
        if not selected_papers:
            return jsonify({'error': 'No papers provided for analysis'}), 400
        
        # Perform comprehensive analysis
        from src.utils.research_analyzer import analyze_research_landscape
        analysis = analyze_research_landscape(selected_papers)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-topics', methods=['POST'])
def generate_topics():
    try:
        data = request.get_json()
        selected_papers = data.get('papers', [])
        
        if not selected_papers:
            return jsonify({'error': 'No papers selected'}), 400
        
        # Generate research topics
        topics = generate_research_topics(selected_papers)
        
        return jsonify({
            'success': True,
            'topics': topics
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.lower().endswith('.pdf'):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract abstract from PDF
            abstract = extract_abstract_from_pdf(filepath)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'abstract': abstract,
                'filename': filename
            })
        
        return jsonify({'error': 'Invalid file format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Content-Based Filtering: Rekomendasi paper berdasarkan yang dipilih user
    """
    try:
        data = request.get_json()
        selected_papers = data.get('selected_papers', [])
        all_papers = data.get('all_papers', [])
        top_n = data.get('top_n', 10)
        
        if not selected_papers:
            return jsonify({'error': 'No papers selected'}), 400
        
        print(f"[DEBUG] Getting recommendations based on {len(selected_papers)} selected papers")
        
        recommendations = get_paper_recommendations(selected_papers, all_papers, top_n)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    
    except Exception as e:
        print(f"[ERROR] Recommendations error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/similar-papers', methods=['POST'])
def get_similar_papers_api():
    """
    Cari paper yang mirip dengan paper tertentu
    """
    try:
        data = request.get_json()
        reference_paper = data.get('reference_paper', {})
        all_papers = data.get('all_papers', [])
        top_n = data.get('top_n', 5)
        
        if not reference_paper:
            return jsonify({'error': 'No reference paper provided'}), 400
        
        print(f"[DEBUG] Finding similar papers to: {reference_paper.get('title', 'Unknown')[:50]}")
        
        similar = find_similar_papers(reference_paper, all_papers, top_n)
        
        return jsonify({
            'success': True,
            'similar_papers': similar,
            'total': len(similar)
        })
    
    except Exception as e:
        print(f"[ERROR] Similar papers error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate_results():
    """
    Generate evaluation report dengan Precision, Recall, F-Measure
    """
    try:
        data = request.get_json()
        papers = data.get('papers', [])
        query = data.get('query', '')
        
        if not papers:
            return jsonify({'error': 'No papers to evaluate'}), 400
        
        report = generate_evaluation_report(papers, query)
        
        return jsonify({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        print(f"[ERROR] Evaluation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_results():
    """
    Export hasil pencarian ke berbagai format
    """
    try:
        data = request.get_json()
        papers = data.get('papers', [])
        format_type = data.get('format', 'csv')  # csv, json, bibtex, html, ris
        query = data.get('query', 'search_results')
        evaluation = data.get('evaluation', None)
        
        if not papers:
            return jsonify({'error': 'No papers to export'}), 400
        
        print(f"[DEBUG] Exporting {len(papers)} papers to {format_type}")
        
        if format_type == 'csv':
            content = export_to_csv(papers)
            mimetype = 'text/csv'
            filename = f'jurnal_{query.replace(" ", "_")}.csv'
        
        elif format_type == 'json':
            content = export_to_json(papers)
            mimetype = 'application/json'
            filename = f'jurnal_{query.replace(" ", "_")}.json'
        
        elif format_type == 'bibtex':
            content = export_to_bibtex(papers)
            mimetype = 'application/x-bibtex'
            filename = f'jurnal_{query.replace(" ", "_")}.bib'
        
        elif format_type == 'html':
            content = export_to_html_report(papers, query, evaluation)
            mimetype = 'text/html'
            filename = f'laporan_{query.replace(" ", "_")}.html'
        
        elif format_type == 'ris':
            content = export_to_ris(papers)
            mimetype = 'application/x-research-info-systems'
            filename = f'jurnal_{query.replace(" ", "_")}.ris'
        
        else:
            return jsonify({'error': f'Unsupported format: {format_type}'}), 400
        
        return Response(
            content,
            mimetype=mimetype,
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    
    except Exception as e:
        print(f"[ERROR] Export error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cbf-details', methods=['POST'])
def get_cbf_details():
    """
    Dapatkan detail perhitungan TF-IDF dan Cosine Similarity
    untuk papers yang dipilih
    """
    try:
        data = request.get_json()
        selected_papers = data.get('papers', [])
        query = data.get('query', '')
        
        if not selected_papers:
            return jsonify({'error': 'No papers selected'}), 400
        
        print(f"[DEBUG] Getting CBF calculation details for {len(selected_papers)} papers")
        
        details = get_cbf_calculation_details(selected_papers, query)
        
        return jsonify({
            'success': True,
            'details': details
        })
    
    except Exception as e:
        print(f"[ERROR] CBF details error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
