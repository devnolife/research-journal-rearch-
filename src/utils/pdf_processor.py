import fitz  # PyMuPDF
import re
import os

def extract_abstract_from_pdf(file_path):
    """Extract abstract dari PDF file"""
    
    if not os.path.exists(file_path):
        return "File not found"
    
    try:
        doc = fitz.open(file_path)
        text = ""
        
        # Usually abstract is on first 2-3 pages
        max_pages = min(3, len(doc))
        
        for page_num in range(max_pages):
            page = doc[page_num]
            page_text = page.get_text()
            text += page_text + "\n"
        
        doc.close()
        
        # Extract abstract from text
        abstract = find_abstract_in_text(text)
        
        if abstract:
            return clean_abstract(abstract)
        else:
            # If no abstract found, return first few sentences
            return extract_opening_sentences(text)
    
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return "Could not extract abstract from PDF"

def find_abstract_in_text(text):
    """Find abstract section dalam text"""
    
    if not text:
        return ""
    
    text_lower = text.lower()
    
    # Patterns untuk mencari abstract section
    abstract_patterns = [
        # Standard abstract patterns
        r'abstract\s*[:.]?\s*(.*?)(?=\n\s*\n|\n\s*(?:keywords|introduction|1\.|i\.|background|index terms))',
        r'abstract\s*[:.]?\s*(.*?)(?=\n\s*(?:keywords|introduction|1\.))',
        
        # Indonesian patterns
        r'abstrak\s*[:.]?\s*(.*?)(?=\n\s*(?:kata kunci|pendahuluan|1\.|i\.|latar belakang))',
        
        # Alternative patterns
        r'summary\s*[:.]?\s*(.*?)(?=\n\s*(?:keywords|introduction|1\.))',
        r'overview\s*[:.]?\s*(.*?)(?=\n\s*(?:keywords|introduction|1\.))',
        
        # More flexible patterns
        r'abstract\s*[:.]?\s*(.*?)(?=\n\s*[A-Z][a-z]+ [a-z]+:)',
        r'abstract\s*[:.]?\s*(.*?)(?=\n\s*\d+\.)',
    ]
    
    for pattern in abstract_patterns:
        match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = match.group(1).strip()
            
            # Check if abstract is reasonable length
            if 50 <= len(abstract) <= 2000:  # Reasonable abstract length
                return abstract
    
    return ""

def extract_opening_sentences(text, max_sentences=5):
    """Extract opening sentences jika abstract tidak ditemukan"""
    
    if not text:
        return ""
    
    # Clean text first
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', clean_text)
    
    # Filter out very short sentences and headers
    valid_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if (len(sentence) > 20 and 
            not sentence.isupper() and  # Skip headers
            not re.match(r'^\d+', sentence) and  # Skip numbered items
            'abstract' not in sentence.lower()[:20]):  # Skip abstract headers
            valid_sentences.append(sentence)
            
            if len(valid_sentences) >= max_sentences:
                break
    
    return '. '.join(valid_sentences) + '.' if valid_sentences else "Could not extract meaningful content"

def clean_abstract(abstract):
    """Clean dan format abstract text"""
    
    if not abstract:
        return ""
    
    # Remove extra whitespace
    abstract = re.sub(r'\s+', ' ', abstract)
    
    # Remove line breaks within sentences
    abstract = re.sub(r'\s*\n\s*', ' ', abstract)
    
    # Remove special characters at the beginning
    abstract = re.sub(r'^[^\w]+', '', abstract)
    
    # Ensure it ends with proper punctuation
    if abstract and not abstract.rstrip()[-1] in '.!?':
        abstract = abstract.rstrip() + '.'
    
    # Remove very short fragments at the end
    sentences = abstract.split('.')
    if len(sentences) > 1 and len(sentences[-2]) < 10:
        abstract = '.'.join(sentences[:-2]) + '.'
    
    # Capitalize first letter
    if abstract:
        abstract = abstract[0].upper() + abstract[1:]
    
    return abstract.strip()

def extract_keywords_from_pdf(file_path):
    """Extract keywords dari PDF jika tersedia"""
    
    try:
        doc = fitz.open(file_path)
        text = ""
        
        # Check first 2 pages for keywords
        for page_num in range(min(2, len(doc))):
            page = doc[page_num]
            page_text = page.get_text()
            text += page_text
        
        doc.close()
        
        # Look for keywords section
        keywords = find_keywords_in_text(text)
        return keywords
    
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def find_keywords_in_text(text):
    """Find keywords section dalam text"""
    
    if not text:
        return []
    
    text_lower = text.lower()
    
    # Patterns untuk keywords
    keyword_patterns = [
        r'keywords\s*[:.]?\s*(.*?)(?=\n\s*\n|\n\s*(?:introduction|1\.|i\.))',
        r'key words\s*[:.]?\s*(.*?)(?=\n\s*\n|\n\s*(?:introduction|1\.))',
        r'kata kunci\s*[:.]?\s*(.*?)(?=\n\s*\n|\n\s*(?:pendahuluan|1\.))',
        r'index terms\s*[:.]?\s*(.*?)(?=\n\s*\n|\n\s*(?:introduction|1\.))',
    ]
    
    for pattern in keyword_patterns:
        match = re.search(pattern, text_lower, re.DOTALL)
        if match:
            keywords_text = match.group(1).strip()
            
            # Parse keywords (usually separated by commas, semicolons, or dashes)
            keywords = re.split(r'[,;•·\-\n]+', keywords_text)
            keywords = [kw.strip() for kw in keywords if kw.strip() and len(kw.strip()) > 2]
            
            return keywords[:10]  # Return max 10 keywords
    
    return []

def extract_metadata_from_pdf(file_path):
    """Extract metadata dari PDF"""
    
    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata
        
        # Get text from first page for title extraction
        first_page_text = doc[0].get_text() if len(doc) > 0 else ""
        
        doc.close()
        
        # Extract title from metadata or first page
        title = metadata.get('title', '') or extract_title_from_text(first_page_text)
        
        result = {
            'title': title,
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': metadata.get('creationDate', ''),
            'modification_date': metadata.get('modDate', '')
        }
        
        return result
    
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {}

def extract_title_from_text(text):
    """Extract title dari first page text"""
    
    if not text:
        return ""
    
    # Split into lines
    lines = text.split('\n')
    
    # Look for title (usually first few non-empty lines)
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        line = line.strip()
        if (len(line) > 10 and 
            not line.isupper() and  # Not all caps header
            not re.match(r'^\d+', line) and  # Not starting with number
            line.count(' ') >= 2):  # Has multiple words
            return line
    
    return ""
