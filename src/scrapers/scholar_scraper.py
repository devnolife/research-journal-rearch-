from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import re

def setup_driver():
    """Setup Chrome driver dengan options yang diperlukan"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Method 1: Try with webdriver-manager (recommended for Windows)
        from webdriver_manager.chrome import ChromeDriverManager
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
        
    except ImportError:
        print("webdriver-manager not found, trying system ChromeDriver...")
        try:
            # Method 2: Try system ChromeDriver
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
            
        except Exception as e:
            print(f"System ChromeDriver error: {e}")
            
            # Method 3: Try with explicit path (Windows common locations)
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
                r"C:\chromedriver\chromedriver.exe",
                "chromedriver.exe"
            ]
            
            for path in chrome_paths:
                try:
                    service = Service(path)
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    print(f"ChromeDriver found at: {path}")
                    return driver
                except:
                    continue
            
            # If all methods fail
            raise Exception("""
            ChromeDriver not found! Please:
            1. Run 'install_chromedriver.bat' to install automatically
            2. Or download ChromeDriver from https://chromedriver.chromium.org/
            3. Or install: pip install webdriver-manager
            """)
    
    except Exception as e:
        print(f"ChromeDriver setup error: {e}")
        raise Exception(f"Failed to setup ChromeDriver: {e}")

def scrape_papers_with_abstracts(query, max_results=20, filters=None):
    """Scrape papers dari Google Scholar dengan abstract dan filters"""
    driver = setup_driver()
    papers = []
    
    if filters is None:
        filters = {}
    
    try:
        # Build search query with filters
        search_query = build_search_query(query, filters)
        
        # Go to Google Scholar
        driver.get("https://scholar.google.com")
        
        # Find and fill search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.submit()
        
        time.sleep(3)
        
        # Apply additional filters if needed
        apply_scholar_filters(driver, filters)
        
        # Parse results
        page = 1
        while len(papers) < max_results and page <= 3:  # Max 3 pages
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract papers from current page
            page_papers = parse_scholar_page(soup)
            
            # Apply post-processing filters
            filtered_papers = apply_post_filters(page_papers, filters)
            papers.extend(filtered_papers)
            
            # Try to go to next page
            try:
                next_button = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
                if next_button.is_enabled():
                    next_button.click()
                    time.sleep(3)
                    page += 1
                else:
                    break
            except:
                break
        
        # Sort results if requested
        if filters.get('sortBy') == 'citations':
            papers.sort(key=lambda x: int(x.get('citations', '0').replace(',', '')), reverse=True)
        elif filters.get('sortBy') == 'date':
            papers.sort(key=lambda x: extract_year_from_authors(x.get('authors', '')), reverse=True)
        
        return papers[:max_results]
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return []
    
    finally:
        try:
            driver.quit()
        except:
            pass

def build_search_query(query, filters):
    """Build advanced search query dengan filters"""
    search_parts = [query]
    
    # Author filter
    if filters.get('author'):
        search_parts.append(f'author:"{filters["author"]}"')
    
    # Include required words
    if filters.get('includeWords'):
        search_parts.append(f'+{filters["includeWords"]}')
    
    # Exclude words
    if filters.get('excludeWords'):
        search_parts.append(f'-{filters["excludeWords"]}')
    
    # Journal/Conference filter
    if filters.get('journal'):
        search_parts.append(f'source:"{filters["journal"]}"')
    
    # Paper type filter
    if filters.get('paperType'):
        if filters['paperType'] == 'review':
            search_parts.append('intitle:review OR intitle:survey')
        elif filters['paperType'] == 'empirical':
            search_parts.append('intitle:experimental OR intitle:empirical')
    
    return ' '.join(search_parts)

def apply_scholar_filters(driver, filters):
    """Apply filters melalui Google Scholar interface"""
    try:
        # Year range filter
        if filters.get('yearFrom') or filters.get('yearTo'):
            # Click on "Any time" dropdown
            time_filter = driver.find_element(By.XPATH, "//div[@id='gs_hdr_tsi']")
            time_filter.click()
            time.sleep(1)
            
            # Custom range
            custom_range = driver.find_element(By.XPATH, "//a[contains(text(), 'Custom range')]")
            custom_range.click()
            time.sleep(1)
            
            # Fill year range
            if filters.get('yearFrom'):
                year_from = driver.find_element(By.NAME, "as_ylo")
                year_from.clear()
                year_from.send_keys(str(filters['yearFrom']))
            
            if filters.get('yearTo'):
                year_to = driver.find_element(By.NAME, "as_yhi")
                year_to.clear()
                year_to.send_keys(str(filters['yearTo']))
            
            # Submit
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            time.sleep(3)
    
    except Exception as e:
        print(f"Filter application error: {e}")

def apply_post_filters(papers, filters):
    """Apply filters setelah scraping"""
    filtered_papers = []
    
    for paper in papers:
        # Citation count filter
        if filters.get('minCitations'):
            citations = int(paper.get('citations', '0').replace(',', ''))
            if citations < int(filters['minCitations']):
                continue
        
        # Language filter (basic)
        if filters.get('language') and filters['language'] != 'any':
            # Simple language detection based on title/abstract content
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
            if filters['language'] == 'english':
                # Check for common English words
                english_indicators = ['the', 'and', 'of', 'to', 'in', 'for', 'with', 'by']
                if not any(word in text for word in english_indicators):
                    continue
        
        filtered_papers.append(paper)
    
    return filtered_papers

def extract_year_from_authors(authors_string):
    """Extract publication year dari authors string"""
    if not authors_string:
        return "0000"
    
    # Look for 4-digit year in authors string
    year_match = re.search(r'\b(19|20)\d{2}\b', authors_string)
    if year_match:
        return year_match.group()
    
    return "0000"

def parse_scholar_page(soup):
    """Parse hasil pencarian dari satu halaman"""
    papers = []
    
    for result in soup.select(".gs_ri"):
        try:
            # Extract title
            title_elem = result.select_one(".gs_rt a")
            title = title_elem.text.strip() if title_elem else "No title"
            
            # Extract URL
            url = title_elem.get('href', '') if title_elem else ''
            
            # Extract authors and year
            authors_elem = result.select_one(".gs_a")
            authors = authors_elem.text.strip() if authors_elem else "Unknown authors"
            
            # Extract abstract/snippet
            abstract_elem = result.select_one(".gs_rs")
            abstract = abstract_elem.text.strip() if abstract_elem else "No abstract available"
            
            # Extract citations
            citation_elem = result.select_one(".gs_fl a")
            citations = "0"
            if citation_elem and "Cited by" in citation_elem.text:
                citation_text = citation_elem.text
                citation_match = re.search(r'Cited by (\d+)', citation_text)
                if citation_match:
                    citations = citation_match.group(1)
            
            # Extract PDF link if available
            pdf_link = ""
            pdf_elem = result.select_one(".gs_or_ggsm a")
            if pdf_elem:
                pdf_link = pdf_elem.get('href', '')
            
            # Try to get enhanced abstract from PDF
            enhanced_abstract = get_enhanced_abstract(abstract, pdf_link)
            
            paper = {
                'title': clean_text(title),
                'authors': clean_text(authors),
                'abstract': clean_text(enhanced_abstract),
                'url': url,
                'pdf_url': pdf_link,
                'citations': citations,
                'year': extract_year_from_authors(authors)
            }
            
            papers.append(paper)
            
        except Exception as e:
            print(f"Error parsing paper: {e}")
            continue
    
    return papers

def get_enhanced_abstract(current_abstract, pdf_link):
    """Coba dapatkan abstract yang lebih lengkap dari PDF"""
    if len(current_abstract) > 300:  # Already good length
        return current_abstract
    
    if not pdf_link:
        return current_abstract
    
    try:
        # Try to fetch PDF content (limited attempt)
        response = requests.get(pdf_link, timeout=10, stream=True)
        if response.status_code == 200 and 'pdf' in response.headers.get('content-type', '').lower():
            # For now, return current abstract
            # Could implement PDF text extraction here if needed
            return current_abstract
    
    except Exception as e:
        pass
    
    return current_abstract

def clean_text(text):
    """Clean dan format text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,;:()[\]{}""''!?]', '', text)
    
    return text
