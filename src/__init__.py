# Research System Package
from .scrapers import (
    scrape_papers_with_abstracts,
    scrape_mendeley_papers,
    search_semantic_scholar
)
from .core import (
    ContentBasedFilter,
    rank_papers_with_cbf,
    get_paper_recommendations,
    find_similar_papers,
    get_cbf_calculation_details,
    generate_evaluation_report,
    evaluate_by_relevance_threshold
)
from .utils import (
    export_to_csv,
    export_to_json,
    export_to_bibtex,
    export_to_html_report,
    export_to_ris,
    extract_abstract_from_pdf,
    generate_research_topics
)

__version__ = '1.0.0'
__author__ = 'Research System Team'

__all__ = [
    # Scrapers
    'scrape_papers_with_abstracts',
    'scrape_mendeley_papers', 
    'search_semantic_scholar',
    
    # Core
    'ContentBasedFilter',
    'rank_papers_with_cbf',
    'get_paper_recommendations',
    'find_similar_papers',
    'get_cbf_calculation_details',
    'generate_evaluation_report',
    'evaluate_by_relevance_threshold',
    
    # Utils
    'export_to_csv',
    'export_to_json',
    'export_to_bibtex',
    'export_to_html_report',
    'export_to_ris',
    'extract_abstract_from_pdf',
    'generate_research_topics'
]
