import re
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def analyze_research_landscape(papers):
    """Comprehensive analysis of research papers untuk generate insights"""
    
    analysis = {
        'research_gaps': [],
        'future_directions': [],
        'interdisciplinary': [],
        'methodology_improvements': [],
        'trends': {
            'hot_topics': [],
            'key_authors': [],
            'publication_trend': '',
            'impact_summary': ''
        }
    }
    
    if not papers or len(papers) == 0:
        return analysis
    
    # Extract and analyze content
    all_texts = extract_texts_from_papers(papers)
    
    # 1. Identify Research Gaps
    analysis['research_gaps'] = identify_research_gaps(papers, all_texts)
    
    # 2. Generate Future Directions
    analysis['future_directions'] = generate_future_directions(papers, all_texts)
    
    # 3. Find Interdisciplinary Opportunities
    analysis['interdisciplinary'] = find_interdisciplinary_opportunities(papers, all_texts)
    
    # 4. Suggest Methodology Improvements
    analysis['methodology_improvements'] = suggest_methodology_improvements(papers, all_texts)
    
    # 5. Analyze Trends
    analysis['trends'] = analyze_trends(papers)
    
    return analysis

def extract_texts_from_papers(papers):
    """Extract dan combine semua teks dari papers"""
    all_texts = []
    
    for paper in papers:
        text_parts = []
        
        if paper.get('title'):
            text_parts.append(paper['title'])
        
        if paper.get('abstract'):
            text_parts.append(paper['abstract'])
        elif paper.get('snippet'):
            text_parts.append(paper['snippet'])
        
        combined_text = ' '.join(text_parts)
        all_texts.append(combined_text)
    
    return all_texts

def identify_research_gaps(papers, all_texts):
    """Identify potential research gaps"""
    gaps = []
    
    # Analyze common limitations mentioned in papers
    limitation_keywords = [
        'limitation', 'limited', 'constraint', 'challenge', 'problem',
        'difficulty', 'issue', 'lack of', 'absence of', 'insufficient',
        'future work', 'further research', 'more research needed'
    ]
    
    # Extract methodologies used
    methodologies = extract_methodologies(all_texts)
    methodology_gaps = analyze_methodology_gaps(methodologies)
    
    # Domain-specific gaps
    domains = extract_research_domains(all_texts)
    
    # Generate gap suggestions
    gaps.extend([
        "Integration of multiple methodological approaches for more robust results",
        "Long-term longitudinal studies to understand temporal effects",
        "Cross-cultural validation of findings across different populations",
        "Real-world implementation and scalability challenges",
        "Ethical implications and responsible research practices"
    ])
    
    # Add methodology-specific gaps
    gaps.extend(methodology_gaps)
    
    # Add domain-specific gaps
    for domain in domains[:3]:  # Top 3 domains
        gaps.append(f"Interdisciplinary research combining {domain} with other fields")
        gaps.append(f"Practical applications of {domain} in industry settings")
    
    return gaps[:8]  # Return top 8 gaps

def generate_future_directions(papers, all_texts):
    """Generate future research directions"""
    directions = []
    
    # Extract key concepts and technologies
    key_concepts = extract_key_concepts(all_texts)
    technologies = extract_technologies(all_texts)
    
    # Generate technology-driven directions
    for tech in technologies[:3]:
        directions.append(f"Advanced applications of {tech} in novel contexts")
        directions.append(f"Hybrid approaches combining {tech} with emerging technologies")
    
    # Generate concept-driven directions
    for concept in key_concepts[:3]:
        directions.append(f"Theoretical framework development for {concept}")
        directions.append(f"Empirical validation of {concept} across different domains")
    
    # General future directions
    directions.extend([
        "Development of standardized evaluation metrics and benchmarks",
        "Creation of large-scale datasets for comprehensive validation",
        "Integration of artificial intelligence and machine learning approaches",
        "Sustainability and environmental impact considerations",
        "Human-centered design and user experience optimization",
        "Policy implications and regulatory framework development"
    ])
    
    return directions[:10]  # Return top 10 directions

def find_interdisciplinary_opportunities(papers, all_texts):
    """Find interdisciplinary collaboration opportunities"""
    opportunities = []
    
    # Extract research domains
    domains = extract_research_domains(all_texts)
    
    # Common interdisciplinary combinations
    interdisciplinary_pairs = [
        ("Computer Science", "Healthcare"),
        ("Artificial Intelligence", "Education"),
        ("Data Science", "Social Sciences"),
        ("Engineering", "Environmental Studies"),
        ("Psychology", "Technology"),
        ("Business", "Sustainability"),
        ("Ethics", "Technology Development")
    ]
    
    # Generate opportunities based on detected domains
    primary_domains = domains[:2] if len(domains) >= 2 else domains
    
    for domain in primary_domains:
        opportunities.append(f"{domain} applications in healthcare and medical research")
        opportunities.append(f"Collaboration between {domain} and social sciences")
        opportunities.append(f"Integration of {domain} with environmental sustainability")
        opportunities.append(f"{domain} approaches to educational technology")
    
    # General interdisciplinary opportunities
    opportunities.extend([
        "Human-computer interaction and user experience research",
        "Digital humanities and cultural studies integration",
        "Bioengineering and medical technology development",
        "Economics and technology policy research",
        "Philosophy and ethics of emerging technologies"
    ])
    
    return opportunities[:8]  # Return top 8 opportunities

def suggest_methodology_improvements(papers, all_texts):
    """Suggest methodology improvements"""
    improvements = []
    
    # Analyze current methodologies
    methodologies = extract_methodologies(all_texts)
    
    # Sample size and statistical power improvements
    improvements.extend([
        "Increase sample sizes for better statistical power and generalizability",
        "Implement power analysis for appropriate study design",
        "Use mixed-methods approaches combining quantitative and qualitative data",
        "Apply advanced statistical techniques for more robust analysis"
    ])
    
    # Data collection improvements
    improvements.extend([
        "Utilize real-time data collection for more accurate measurements",
        "Implement multi-modal data collection strategies",
        "Develop automated data collection systems to reduce bias",
        "Use blockchain technology for data integrity and transparency"
    ])
    
    # Analysis improvements
    improvements.extend([
        "Apply machine learning techniques for pattern discovery",
        "Use advanced visualization techniques for better data interpretation",
        "Implement reproducible research practices and open science",
        "Conduct meta-analyses to synthesize findings across studies"
    ])
    
    return improvements[:8]  # Return top 8 improvements

def analyze_trends(papers):
    """Analyze current trends in the research area"""
    trends = {
        'hot_topics': [],
        'key_authors': [],
        'publication_trend': '',
        'impact_summary': ''
    }
    
    # Extract hot topics from titles and abstracts
    all_text = ' '.join([f"{p.get('title', '')} {p.get('abstract', p.get('snippet', ''))}" for p in papers])
    hot_topics = extract_trending_topics(all_text)
    trends['hot_topics'] = hot_topics[:5]
    
    # Extract key authors (most frequent)
    all_authors = []
    for paper in papers:
        authors_text = paper.get('authors', '')
        # Extract individual author names (simplified)
        authors = extract_author_names(authors_text)
        all_authors.extend(authors)
    
    author_counts = Counter(all_authors)
    trends['key_authors'] = [author for author, count in author_counts.most_common(5)]
    
    # Analyze publication trends
    years = extract_publication_years(papers)
    if years:
        year_counts = Counter(years)
        most_common_year = year_counts.most_common(1)[0]
        trends['publication_trend'] = f"Peak publication year: {most_common_year[0]} ({most_common_year[1]} papers)"
    
    # Calculate impact summary
    total_citations = sum(int(p.get('citations', '0').replace(',', '')) for p in papers)
    avg_citations = total_citations / len(papers) if papers else 0
    trends['impact_summary'] = f"Total citations: {total_citations:,} | Average: {avg_citations:.1f} per paper"
    
    return trends

def extract_methodologies(texts):
    """Extract research methodologies from texts"""
    methodology_keywords = [
        'machine learning', 'deep learning', 'neural network', 'algorithm',
        'survey', 'experiment', 'case study', 'analysis', 'simulation',
        'modeling', 'statistical', 'quantitative', 'qualitative', 'mixed methods',
        'regression', 'classification', 'clustering', 'optimization'
    ]
    
    found_methods = []
    combined_text = ' '.join(texts).lower()
    
    for method in methodology_keywords:
        if method in combined_text:
            found_methods.append(method)
    
    return found_methods

def analyze_methodology_gaps(methodologies):
    """Analyze gaps in current methodologies"""
    gaps = []
    
    # Check for missing common methodologies
    common_methods = ['machine learning', 'statistical analysis', 'experimental design', 'simulation']
    
    for method in common_methods:
        if method not in methodologies:
            gaps.append(f"Limited use of {method} approaches in current research")
    
    # Suggest advanced methods
    if 'machine learning' in methodologies:
        gaps.append("Exploration of advanced deep learning architectures")
        gaps.append("Integration of explainable AI techniques")
    
    return gaps

def extract_research_domains(texts):
    """Extract research domains from texts"""
    domain_keywords = {
        'Artificial Intelligence': ['ai', 'artificial intelligence', 'machine learning', 'neural', 'deep learning'],
        'Computer Science': ['computer', 'software', 'algorithm', 'programming', 'computing'],
        'Data Science': ['data', 'analytics', 'big data', 'statistics', 'mining'],
        'Healthcare': ['health', 'medical', 'clinical', 'patient', 'treatment'],
        'Education': ['education', 'learning', 'teaching', 'student', 'academic'],
        'Engineering': ['engineering', 'system', 'design', 'development', 'technical'],
        'Social Sciences': ['social', 'behavior', 'human', 'society', 'psychology'],
        'Business': ['business', 'management', 'organization', 'strategy', 'economic']
    }
    
    domain_scores = {}
    combined_text = ' '.join(texts).lower()
    
    for domain, keywords in domain_keywords.items():
        score = sum(combined_text.count(keyword) for keyword in keywords)
        if score > 0:
            domain_scores[domain] = score
    
    # Return domains sorted by frequency
    return sorted(domain_scores.keys(), key=lambda x: domain_scores[x], reverse=True)

def extract_key_concepts(texts):
    """Extract key research concepts"""
    # Use TF-IDF to find important terms
    try:
        vectorizer = TfidfVectorizer(
            max_features=20,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get average TF-IDF scores
        mean_scores = tfidf_matrix.mean(axis=0).A1
        concepts = [(feature_names[i], mean_scores[i]) for i in range(len(feature_names))]
        concepts.sort(key=lambda x: x[1], reverse=True)
        
        return [concept[0] for concept in concepts[:10]]
    except:
        return ['research', 'analysis', 'method', 'approach', 'system']

def extract_technologies(texts):
    """Extract mentioned technologies"""
    tech_keywords = [
        'blockchain', 'IoT', 'cloud computing', 'big data', 'artificial intelligence',
        'machine learning', 'deep learning', 'neural networks', 'NLP', 'computer vision',
        'robotics', 'VR', 'AR', 'quantum computing', 'edge computing'
    ]
    
    found_techs = []
    combined_text = ' '.join(texts).lower()
    
    for tech in tech_keywords:
        if tech.lower() in combined_text:
            found_techs.append(tech)
    
    return found_techs[:5]

def extract_trending_topics(text):
    """Extract trending topics using simple keyword frequency"""
    # Clean and tokenize
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.update(['research', 'study', 'analysis', 'method', 'approach', 'paper', 'work'])
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Get most frequent words
    word_freq = Counter(filtered_words)
    top_words = word_freq.most_common(10)
    
    return [word for word, freq in top_words]

def extract_author_names(authors_text):
    """Extract individual author names from authors string"""
    if not authors_text:
        return []
    
    # Simple extraction - split by common delimiters
    authors = re.split(r'[,;]', authors_text)
    
    # Clean and filter
    clean_authors = []
    for author in authors:
        author = author.strip()
        # Remove years and other non-name content
        author = re.sub(r'\b\d{4}\b', '', author)
        author = re.sub(r'[^\w\s]', ' ', author)
        author = ' '.join(author.split())
        
        if len(author) > 3 and not author.isdigit():
            clean_authors.append(author)
    
    return clean_authors[:3]  # Max 3 authors per paper

def extract_publication_years(papers):
    """Extract publication years from papers"""
    years = []
    
    for paper in papers:
        authors_text = paper.get('authors', '')
        # Look for 4-digit years
        year_matches = re.findall(r'\b(19|20)\d{2}\b', authors_text)
        if year_matches:
            years.append(year_matches[0])
    
    return years
