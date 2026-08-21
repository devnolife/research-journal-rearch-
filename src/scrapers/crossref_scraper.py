"""
CrossRef API Scraper
API publik yang stabil untuk mencari paper akademik
Tidak memerlukan API key dan memiliki rate limit yang lebih longgar
"""

import requests
import time

CROSSREF_API = "https://api.crossref.org/works"


def search_crossref(query, max_results=20, filters=None):
    """
    Search papers menggunakan CrossRef API

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
        print(f"[DEBUG] CrossRef search: {query}")

        # Build API request
        params = {
            "query": query,
            "rows": min(max_results, 100),
            "select": "title,author,abstract,published-print,published-online,is-referenced-by-count,URL,link,container-title",
        }

        # Add year filter
        if filters.get("year"):
            year_value = filters["year"]
            if "-" in str(year_value):
                years = year_value.split("-")
                params["filter"] = f"from-pub-date:{years[0]},until-pub-date:{years[1]}"
            else:
                params["filter"] = (
                    f"from-pub-date:{year_value},until-pub-date:{year_value}"
                )

        headers = {"User-Agent": "ResearchSystem/1.0 (mailto:research@example.com)"}

        response = requests.get(
            CROSSREF_API, params=params, headers=headers, timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            papers = parse_crossref_response(data, max_results)
            print(f"[DEBUG] Found {len(papers)} papers from CrossRef")
        else:
            print(f"[DEBUG] CrossRef API returned status {response.status_code}")

        # Apply post-filters
        if filters.get("minCitations"):
            min_cit = int(filters["minCitations"])
            papers = [p for p in papers if int(p.get("citations", "0")) >= min_cit]

        # Sort if requested
        if filters.get("sortBy") == "citations":
            papers.sort(key=lambda x: int(x.get("citations", "0")), reverse=True)
        elif filters.get("sortBy") == "date":
            papers.sort(key=lambda x: x.get("year", "0"), reverse=True)

        return papers[:max_results]

    except Exception as e:
        print(f"[ERROR] CrossRef search error: {e}")
        return []


def parse_crossref_response(data, max_results):
    """Parse response dari CrossRef API"""
    papers = []

    items = data.get("message", {}).get("items", [])

    for item in items[:max_results]:
        try:
            # Extract title
            title_list = item.get("title", [])
            title = title_list[0] if title_list else "No title"

            # Extract authors
            authors_list = item.get("author", [])
            authors = ", ".join(
                [
                    f"{a.get('given', '')} {a.get('family', '')}".strip()
                    for a in authors_list[:5]
                ]
            )
            if len(authors_list) > 5:
                authors += " et al."

            # Extract year
            year = ""
            pub_date = item.get("published-print") or item.get("published-online")
            if pub_date and "date-parts" in pub_date:
                date_parts = pub_date["date-parts"]
                if date_parts and date_parts[0]:
                    year = str(date_parts[0][0])

            # Extract abstract
            abstract = item.get("abstract", "")
            if abstract:
                # Clean HTML tags from abstract
                import re

                abstract = re.sub(r"<[^>]+>", "", abstract)
            else:
                abstract = "Tidak ada abstrak tersedia"

            # Get PDF link if available
            pdf_link = ""
            links = item.get("link", [])
            for link in links:
                if link.get("content-type") == "application/pdf":
                    pdf_link = link.get("URL", "")
                    break

            paper = {
                "title": title,
                "authors": authors or "Unknown authors",
                "abstract": abstract[:1000]
                if abstract
                else "Tidak ada abstrak tersedia",
                "year": year,
                "citations": str(item.get("is-referenced-by-count", 0)),
                "url": item.get("URL", ""),
                "scholar_url": item.get("URL", ""),
                "pdf_link": pdf_link,
                "source": "CrossRef",
                "venue": ", ".join(item.get("container-title", []))
                if item.get("container-title")
                else "",
            }

            papers.append(paper)

        except Exception as e:
            print(f"[DEBUG] Error parsing CrossRef item: {e}")
            continue

    return papers


# Test
if __name__ == "__main__":
    print("Testing CrossRef API...")
    papers = search_crossref("machine learning", max_results=5)
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title'][:60]}...")
        print(f"   Authors: {paper['authors'][:50]}...")
        print(f"   Year: {paper['year']}, Citations: {paper['citations']}")
        print(f"   Abstract: {paper['abstract'][:100]}...")
