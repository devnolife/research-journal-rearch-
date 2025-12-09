"""
Semantic Scholar API Scraper
API gratis dan lebih reliable dibanding Google Scholar scraping
Tidak ada rate limiting yang ketat dan tidak memerlukan API key untuk basic usage
"""

import requests
import time

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_semantic_scholar(query, max_results=20, filters=None):
    """
    Search papers menggunakan Semantic Scholar API
    
    Args:
        query: Search query
        max_results: Maximum results to return
        filters: Optional filters (year, etc)
    
    Returns:
        List of paper dictionaries
    """
    if filters is None:
        filters = {}
    
    papers = []
    
    try:
        print(f"[DEBUG] Semantic Scholar search: {query}")
        
        # Build API request
        params = {
            'query': query,
            'limit': min(max_results, 100),  # API max is 100
            'fields': 'title,authors,abstract,year,citationCount,url,openAccessPdf,venue'
        }
        
        # Add year filter
        if filters.get('year'):
            year_value = filters['year']
            if '-' in str(year_value):
                years = year_value.split('-')
                params['year'] = f"{years[0]}-{years[1]}"
            else:
                params['year'] = year_value
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(
            SEMANTIC_SCHOLAR_API,
            params=params,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            papers = parse_semantic_scholar_response(data, max_results)
            print(f"[DEBUG] Found {len(papers)} papers from Semantic Scholar")
        else:
            print(f"[DEBUG] Semantic Scholar API returned status {response.status_code}")
            # Return empty list, fallback will be handled by caller
        
        # Apply post-filters
        if filters.get('minCitations'):
            min_cit = int(filters['minCitations'])
            papers = [p for p in papers if int(p.get('citations', '0')) >= min_cit]
        
        # Sort if requested
        if filters.get('sortBy') == 'citations':
            papers.sort(key=lambda x: int(x.get('citations', '0')), reverse=True)
        elif filters.get('sortBy') == 'date':
            papers.sort(key=lambda x: x.get('year', '0'), reverse=True)
        
        return papers[:max_results]
    
    except Exception as e:
        print(f"[ERROR] Semantic Scholar search error: {e}")
        return []


def parse_semantic_scholar_response(data, max_results):
    """Parse response dari Semantic Scholar API"""
    papers = []
    
    items = data.get('data', [])
    
    for item in items[:max_results]:
        try:
            # Extract authors
            authors_list = item.get('authors', [])
            authors = ', '.join([a.get('name', '') for a in authors_list[:5]])
            if len(authors_list) > 5:
                authors += ' et al.'
            
            # Get PDF URL if available
            pdf_url = ''
            open_access = item.get('openAccessPdf')
            if open_access and isinstance(open_access, dict):
                pdf_url = open_access.get('url', '')
            
            paper = {
                'title': item.get('title', 'No title'),
                'authors': authors or 'Unknown authors',
                'abstract': item.get('abstract', 'Tidak ada abstrak tersedia') or 'Tidak ada abstrak tersedia',
                'year': str(item.get('year', '')),
                'citations': str(item.get('citationCount', 0)),
                'url': item.get('url', ''),
                'scholar_url': item.get('url', ''),
                'pdf_link': pdf_url,
                'source': 'Semantic Scholar',
                'venue': item.get('venue', '')
            }
            
            papers.append(paper)
        
        except Exception as e:
            print(f"[DEBUG] Error parsing Semantic Scholar item: {e}")
            continue
    
    return papers


# Test
if __name__ == "__main__":
    print("Testing Semantic Scholar API...")
    papers = search_semantic_scholar("machine learning", max_results=5)
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title'][:60]}...")
        print(f"   Authors: {paper['authors'][:50]}...")
        print(f"   Year: {paper['year']}, Citations: {paper['citations']}")
        print(f"   Abstract: {paper['abstract'][:100]}...")
