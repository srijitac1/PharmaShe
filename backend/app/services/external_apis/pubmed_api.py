import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class PubMedAPI:
    """
    Integration with PubMed API for scientific literature
    """
    
    def __init__(self, base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_articles(
        self,
        query: str,
        max_results: int = 100,
        sort: str = "relevance",
        mindate: Optional[str] = None,
        maxdate: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search PubMed articles
        """
        try:
            # First, search for article IDs
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "sort": sort,
                "retmode": "json"
            }
            
            if mindate:
                search_params["mindate"] = mindate
            if maxdate:
                search_params["maxdate"] = maxdate
            
            search_response = await self.client.get(
                f"{self.base_url}/esearch.fcgi",
                params=search_params
            )
            search_response.raise_for_status()
            
            search_data = search_response.json()
            pmids = search_data.get("esearchresult", {}).get("idlist", [])
            
            if not pmids:
                return {"articles": [], "total_count": 0}
            
            # Get detailed article information
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "json",
                "rettype": "abstract"
            }
            
            fetch_response = await self.client.get(
                f"{self.base_url}/efetch.fcgi",
                params=fetch_params
            )
            fetch_response.raise_for_status()
            
            fetch_data = fetch_response.json()
            
            # Process articles
            processed_articles = []
            articles = fetch_data.get("PubmedArticle", [])
            
            for article in articles:
                article_data = self._process_article_data(article)
                processed_articles.append(article_data)
            
            return {
                "total_count": search_data.get("esearchresult", {}).get("count", 0),
                "articles": processed_articles,
                "search_params": search_params
            }
            
        except Exception as e:
            logger.error(f"Error searching PubMed articles: {str(e)}")
            return {"error": str(e), "articles": []}
    
    def _process_article_data(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw article data into standardized format
        """
        medline_citation = article.get("MedlineCitation", {})
        article_data = medline_citation.get("Article", {})
        pmid = medline_citation.get("PMID", {}).get("#text", "")
        
        # Extract authors
        authors = []
        author_list = article_data.get("AuthorList", {}).get("Author", [])
        if isinstance(author_list, list):
            for author in author_list:
                last_name = author.get("LastName", "")
                first_name = author.get("ForeName", "")
                if last_name and first_name:
                    authors.append(f"{last_name}, {first_name}")
        
        # Extract journal information
        journal = article_data.get("Journal", {})
        journal_title = journal.get("Title", "")
        journal_issue = journal.get("JournalIssue", {})
        pub_date = journal_issue.get("PubDate", {})
        
        # Extract publication date
        year = pub_date.get("Year", "")
        month = pub_date.get("Month", "")
        day = pub_date.get("Day", "")
        
        publication_date = f"{year}-{month}-{day}" if year else ""
        
        # Extract keywords
        keywords = []
        keyword_list = medline_citation.get("KeywordList", {}).get("Keyword", [])
        if isinstance(keyword_list, list):
            keywords = [kw.get("#text", "") if isinstance(kw, dict) else kw for kw in keyword_list]
        
        return {
            "pmid": pmid,
            "title": article_data.get("ArticleTitle", ""),
            "abstract": article_data.get("Abstract", {}).get("AbstractText", ""),
            "authors": authors,
            "journal": journal_title,
            "publication_date": publication_date,
            "keywords": keywords,
            "doi": self._extract_doi(article_data),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        }
    
    def _extract_doi(self, article_data: Dict[str, Any]) -> Optional[str]:
        """Extract DOI from article data"""
        elocation_ids = article_data.get("ELocationID", [])
        if isinstance(elocation_ids, list):
            for eloc in elocation_ids:
                if eloc.get("@EIdType") == "doi":
                    return eloc.get("#text", "")
        return None
    
    async def search_by_drug(self, drug_name: str, max_results: int = 50) -> Dict[str, Any]:
        """
        Search articles related to a specific drug
        """
        query = f'"{drug_name}"[Title/Abstract] AND ("cancer"[Title/Abstract] OR "oncology"[Title/Abstract])'
        return await self.search_articles(query, max_results=max_results)
    
    async def search_by_therapeutic_area(self, therapeutic_area: str, max_results: int = 50) -> Dict[str, Any]:
        """
        Search articles by therapeutic area
        """
        query = f'"{therapeutic_area}"[Title/Abstract] AND ("women"[Title/Abstract] OR "female"[Title/Abstract])'
        return await self.search_articles(query, max_results=max_results)
    
    async def search_recent_articles(self, query: str, days: int = 30, max_results: int = 50) -> Dict[str, Any]:
        """
        Search for recent articles published in the last N days
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        mindate = start_date.strftime("%Y/%m/%d")
        maxdate = end_date.strftime("%Y/%m/%d")
        
        return await self.search_articles(
            query=query,
            max_results=max_results,
            mindate=mindate,
            maxdate=maxdate
        )
    
    async def get_article_details(self, pmid: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific article
        """
        try:
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "json",
                "rettype": "abstract"
            }
            
            response = await self.client.get(
                f"{self.base_url}/efetch.fcgi",
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("PubmedArticle", [])
            
            if articles:
                return self._process_article_data(articles[0])
            else:
                return {"error": "Article not found"}
                
        except Exception as e:
            logger.error(f"Error getting article details for PMID {pmid}: {str(e)}")
            return {"error": str(e)}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
