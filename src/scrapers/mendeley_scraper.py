"""
Mendeley Scraper - Menggunakan Mendeley Catalog API (Public)
API ini tidak memerlukan OAuth untuk pencarian catalog publik
"""
import requests
import re
import time

# Mendeley Public Catalog Search API
MENDELEY_CATALOG_SEARCH_URL = "https://api.mendeley.com/catalog"

def scrape_mendeley_papers(query, max_results=20, filters=None):
    """
    Scrape papers dari Mendeley Catalog API
    API ini publik dan tidak memerlukan autentikasi untuk pencarian dasar
    """
    papers = []
    
    if filters is None:
        filters = {}
    
    try:
        print(f"[DEBUG] Mendeley API search: {query}")
        
        # Build API request
        params = {
            'query': query,
            'limit': min(max_results, 100),  # API max limit
            'view': 'all'  # Get all available fields
        }
        
        # Add year filter if specified
        if filters.get('year'):
            year_value = filters['year']
            if '-' in str(year_value):
                years = year_value.split('-')
                params['min_year'] = years[0]
                params['max_year'] = years[1]
            else:
                params['min_year'] = year_value
                params['max_year'] = year_value
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/vnd.mendeley-document.1+json'
        }
        
        # Try the Catalog API first
        response = requests.get(
            MENDELEY_CATALOG_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            papers = parse_mendeley_api_response(data, max_results)
            print(f"[DEBUG] Found {len(papers)} papers from Mendeley API")
        else:
            print(f"[DEBUG] Mendeley API returned status {response.status_code}")
            # Fallback to web scraping approach
            papers = scrape_mendeley_web(query, max_results, filters)
        
        # Apply post-filters
        if filters.get('minCitations'):
            papers = [p for p in papers if int(p.get('readers', '0')) >= int(filters['minCitations'])]
        
        # Sort if requested
        if filters.get('sortBy') == 'citations':
            papers.sort(key=lambda x: int(x.get('readers', '0')), reverse=True)
        elif filters.get('sortBy') == 'date':
            papers.sort(key=lambda x: x.get('year', '0'), reverse=True)
        
        return papers[:max_results]
    
    except Exception as e:
        print(f"[ERROR] Mendeley search error: {e}")
        # Try web scraping as fallback
        return scrape_mendeley_web(query, max_results, filters)

def parse_mendeley_api_response(data, max_results):
    """Parse response dari Mendeley Catalog API"""
    papers = []
    
    items = data if isinstance(data, list) else data.get('documents', data.get('items', []))
    
    for item in items[:max_results]:
        try:
            # Extract authors
            authors_list = item.get('authors', [])
            authors = ', '.join([
                f"{a.get('first_name', '')} {a.get('last_name', '')}".strip()
                for a in authors_list[:5]
            ])
            if len(authors_list) > 5:
                authors += ' et al.'
            
            paper = {
                'title': item.get('title', 'No title'),
                'authors': authors or 'Unknown authors',
                'abstract': item.get('abstract', 'Tidak ada abstrak tersedia'),
                'year': str(item.get('year', '')),
                'readers': str(item.get('reader_count', item.get('reader_count_by_discipline', {}).get('total', 0))),
                'citations': str(item.get('reader_count', 0)),
                'url': f"https://www.mendeley.com/catalogue/{item.get('id', '')}",
                'pdf_url': '',
                'source': 'Mendeley',
                'doi': item.get('doi', ''),
                'journal': item.get('source', item.get('publisher', ''))
            }
            
            # Try to get PDF link
            if item.get('file_attached'):
                paper['pdf_url'] = paper['url']
            
            papers.append(paper)
        
        except Exception as e:
            print(f"[DEBUG] Error parsing Mendeley item: {e}")
            continue
    
    return papers

def scrape_mendeley_web(query, max_results=20, filters=None):
    """
    Fallback: Scrape dari Mendeley web menggunakan Selenium
    Digunakan jika API tidak tersedia
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from bs4 import BeautifulSoup
        
        print("[DEBUG] Falling back to Mendeley web scraping...")
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        papers = []
        
        try:
            # Navigate to Mendeley search
            search_url = f"https://www.mendeley.com/search/?query={query.replace(' ', '+')}"
            driver.get(search_url)
            time.sleep(5)  # Wait for JavaScript to load
            
            # Wait for content
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
            except:
                print("[DEBUG] Timeout waiting for Mendeley results")
            
            # Parse page
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Find result cards
            for article in soup.find_all('article')[:max_results]:
                try:
                    title_elem = article.find(['h2', 'h3', 'a'])
                    title = title_elem.get_text(strip=True) if title_elem else 'No title'
                    
                    link = title_elem.get('href', '') if title_elem and title_elem.name == 'a' else ''
                    if link and not link.startswith('http'):
                        link = 'https://www.mendeley.com' + link
                    
                    # Get year from text
                    text = article.get_text()
                    year_match = re.search(r'\b(19|20)\d{2}\b', text)
                    year = year_match.group() if year_match else ''
                    
                    paper = {
                        'title': title,
                        'authors': 'Unknown authors',
                        'abstract': 'Tidak ada abstrak tersedia',
                        'year': year,
                        'readers': '0',
                        'citations': '0',
                        'url': link,
                        'pdf_url': '',
                        'source': 'Mendeley'
                    }
                    papers.append(paper)
                
                except Exception as e:
                    continue
        
        finally:
            driver.quit()
        
        return papers
    
    except Exception as e:
        print(f"[ERROR] Mendeley web scraping error: {e}")
        return []

def clean_text(text):
    """Clean dan format text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Test function
if __name__ == "__main__":
    print("Testing Mendeley Scraper...")
    papers = scrape_mendeley_papers("machine learning", max_results=5)
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title'][:60]}...")
        print(f"   Authors: {paper['authors'][:50]}...")
        print(f"   Year: {paper['year']}, Readers: {paper['readers']}")
