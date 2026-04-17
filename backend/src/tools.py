import arxiv
from typing import List, Dict, Any

def fetch_arxiv_papers(query: str, max_results: int = 2) -> List[Dict[str, Any]]:
    """Real Arxiv wrapper utilizing the public API."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    docs = []
    try:
        client = arxiv.Client()
        for result in client.results(search):
            docs.append({
                "title": result.title,
                "summary": result.summary[:300] + "...", # truncate for mock
                "authors": [a.name for a in result.authors],
                "url": result.pdf_url
            })
    except Exception as e:
        print(f"Arxiv error: {e}")
    return docs
