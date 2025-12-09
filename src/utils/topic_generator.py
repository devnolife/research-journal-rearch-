from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def generate_research_topics(papers, n_topics=5):
    """Generate research topics dari papers yang dipilih"""
    
    if not papers or len(papers) == 0:
        return []
    
    # Combine title and abstract for analysis
    texts = []
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        texts.append(text)
    
    # Generate topics using different methods
    topics = []
    
    # Method 1: TF-IDF + Clustering
    tfidf_topics = generate_tfidf_topics(texts, n_topics)
    topics.extend(tfidf_topics)
    
    # Method 2: LDA Topic Modeling
    lda_topics = generate_lda_topics(texts, n_topics)
    topics.extend(lda_topics)
    
    # Method 3: Keyword-based suggestions
    keyword_topics = generate_keyword_based_topics(texts)
    topics.extend(keyword_topics)
    
    # Method 4: Gap analysis
    gap_topics = suggest_research_gaps(papers)
    topics.extend(gap_topics)
    
    # Remove duplicates and return unique topics
    unique_topics = list(set(topics))
    return unique_topics[:15]  # Return top 15 unique topics

def generate_tfidf_topics(texts, n_topics):
    """Generate topics menggunakan TF-IDF dan clustering"""
    try:
        # Preprocess texts
        clean_texts = [preprocess_text(text) for text in texts]
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.8
        )
        
        X = vectorizer.fit_transform(clean_texts)
        
        # Clustering
        kmeans = KMeans(n_clusters=min(n_topics, len(texts)), random_state=42)
        kmeans.fit(X)
        
        # Extract topics from clusters
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        
        for i in range(kmeans.n_clusters):
            # Get top terms for this cluster
            cluster_center = kmeans.cluster_centers_[i]
            top_indices = cluster_center.argsort()[-5:][::-1]
            top_terms = [feature_names[idx] for idx in top_indices]
            
            # Create readable topic
            topic = create_readable_topic(top_terms)
            topics.append(topic)
        
        return topics
    
    except Exception as e:
        print(f"Error in TF-IDF topic generation: {e}")
        return []

def generate_lda_topics(texts, n_topics):
    """Generate topics menggunakan LDA"""
    try:
        clean_texts = [preprocess_text(text) for text in texts]
        
        # Vectorization for LDA
        vectorizer = TfidfVectorizer(
            max_features=50,
            stop_words='english',
            min_df=1,
            max_df=0.8
        )
        
        X = vectorizer.fit_transform(clean_texts)
        
        # LDA Model
        lda = LatentDirichletAllocation(
            n_components=min(n_topics, len(texts)),
            random_state=42,
            max_iter=10
        )
        
        lda.fit(X)
        
        # Extract topics
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_indices = topic.argsort()[-5:][::-1]
            top_terms = [feature_names[i] for i in top_indices]
            
            topic_text = create_readable_topic(top_terms)
            topics.append(topic_text)
        
        return topics
    
    except Exception as e:
        print(f"Error in LDA topic generation: {e}")
        return []

def generate_keyword_based_topics(texts):
    """Generate topics berdasarkan keyword frequency"""
    try:
        # Extract all keywords
        all_keywords = []
        for text in texts:
            keywords = extract_keywords(text)
            all_keywords.extend(keywords)
        
        # Count frequency
        keyword_counts = Counter(all_keywords)
        top_keywords = keyword_counts.most_common(10)
        
        # Create topic suggestions
        topics = []
        for keyword, count in top_keywords:
            if count > 1:  # Only if appears in multiple papers
                topics.append(f"Advanced {keyword.title()} Applications")
                topics.append(f"{keyword.title()} in Modern Context")
                topics.append(f"Novel {keyword.title()} Approaches")
        
        return topics[:8]
    
    except Exception as e:
        print(f"Error in keyword-based topic generation: {e}")
        return []

def suggest_research_gaps(papers):
    """Suggest research gaps dan future work"""
    gap_topics = [
        "Integration of Multiple Approaches",
        "Real-world Implementation Challenges",
        "Scalability and Performance Optimization",
        "Cross-domain Applications",
        "Ethical Considerations and Guidelines",
        "Comparative Analysis Framework",
        "Long-term Impact Assessment",
        "Interdisciplinary Collaboration Methods"
    ]
    
    # Customize based on paper domains
    domains = extract_domains_from_papers(papers)
    customized_gaps = []
    
    for domain in domains:
        customized_gaps.append(f"{domain} Security and Privacy Issues")
        customized_gaps.append(f"Sustainable {domain} Solutions")
        customized_gaps.append(f"{domain} Accessibility Improvements")
    
    return gap_topics[:4] + customized_gaps[:4]

def extract_domains_from_papers(papers):
    """Extract research domains dari papers"""
    domain_keywords = {
        'AI': ['artificial intelligence', 'machine learning', 'deep learning', 'neural network'],
        'Healthcare': ['medical', 'health', 'clinical', 'patient', 'diagnosis'],
        'Education': ['learning', 'education', 'student', 'teaching', 'academic'],
        'Technology': ['system', 'algorithm', 'software', 'computing', 'technology'],
        'Data Science': ['data', 'analysis', 'analytics', 'mining', 'database']
    }
    
    domains = []
    all_text = ' '.join([f"{p.get('title', '')} {p.get('abstract', '')}" for p in papers]).lower()
    
    for domain, keywords in domain_keywords.items():
        if any(keyword in all_text for keyword in keywords):
            domains.append(domain)
    
    return domains[:3]  # Return top 3 domains

def preprocess_text(text):
    """Preprocess text untuk topic modeling"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    additional_stops = {'using', 'based', 'approach', 'method', 'study', 'research', 'paper', 'analysis', 'results', 'conclusion'}
    stop_words.update(additional_stops)
    
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    return ' '.join(filtered_words)

def extract_keywords(text):
    """Extract important keywords dari text"""
    # Preprocess
    clean_text = preprocess_text(text)
    words = word_tokenize(clean_text)
    
    # Filter by length and importance
    keywords = []
    important_words = [word for word in words if len(word) > 3]
    
    # Use simple frequency but filter common academic words
    common_academic = {'study', 'research', 'analysis', 'method', 'approach', 'result', 'conclusion', 'paper', 'work'}
    
    for word in important_words:
        if word not in common_academic:
            keywords.append(word)
    
    return keywords[:10]  # Return top 10 keywords

def create_readable_topic(terms):
    """Create readable topic dari terms"""
    if not terms:
        return "General Research Topic"
    
    # Clean and capitalize terms
    clean_terms = [term.replace('_', ' ').title() for term in terms if len(term) > 2]
    
    if len(clean_terms) >= 2:
        return f"{clean_terms[0]} and {clean_terms[1]} Integration"
    elif clean_terms:
        return f"Advanced {clean_terms[0]} Research"
    else:
        return "Interdisciplinary Research Approach"
