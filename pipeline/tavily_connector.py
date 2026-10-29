import os
import logging
from tavily import TavilyClient

class TavilyLiteratureConnector:
    def __init__(self):
        # Automatically picks up TAVILY_API_KEY from environment variables
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            logging.warning("TAVILY_API_KEY not found in environment variables.")
        self.client = TavilyClient(api_key=api_key) if api_key else None

    def search_literature(self, query: str, max_results: int = 3):
        """
        Performs a scoped literature search targeting PubMed, ClinVar, and UniProt 
        to fetch evidence and URL source links for genomic variants.
        """
        if not self.client:
            return {"error": "Tavily client not initialized. Missing API key."}

        scoped_query = f"{query} (site:ncbi.nlm.nih.gov/pubmed OR site:ncbi.nlm.nih.gov/clinvar OR site:uniprot.org)"
        
        try:
            response = self.client.search(
                query=scoped_query,
                max_results=max_results,
                include_raw_content=False
            )
            
            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "snippet": item.get("content")
                })
            
            return {
                "query": query,
                "sources_found": len(results),
                "results": results
            }
        except Exception as e:
            logging.error(f"Tavily search failed: {e}")
            return {"error": str(e)}