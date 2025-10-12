import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class USPTOAPI:
    """
    Integration with USPTO Patent API
    """
    
    def __init__(self, base_url: str = "https://developer.uspto.gov/ibd-api/v1"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_patents(
        self,
        query: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Search patents using USPTO API
        """
        try:
            params = {
                "searchText": query,
                "start": 0,
                "rows": limit
            }
            
            if start_date:
                params["fq"] = f"applicationDate:[{start_date} TO *]"
            if end_date:
                params["fq"] = f"applicationDate:[* TO {end_date}]"
            
            response = await self.client.get(f"{self.base_url}/patent/application", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process patent data
            processed_patents = []
            for patent in data.get("response", {}).get("docs", []):
                patent_data = self._process_patent_data(patent)
                processed_patents.append(patent_data)
            
            return {
                "total_count": data.get("response", {}).get("numFound", 0),
                "patents": processed_patents,
                "search_params": params
            }
            
        except Exception as e:
            logger.error(f"Error searching patents: {str(e)}")
            return {"error": str(e), "patents": []}
    
    def _process_patent_data(self, patent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw patent data into standardized format
        """
        return {
            "patent_number": patent.get("applicationNumberText", ""),
            "title": patent.get("inventionTitle", ""),
            "inventors": patent.get("inventorName", []),
            "assignee": patent.get("assigneeEntityName", ""),
            "filing_date": patent.get("applicationDate", ""),
            "issue_date": patent.get("patentIssueDate", ""),
            "abstract": patent.get("abstractText", ""),
            "claims": patent.get("claimText", ""),
            "classification": patent.get("primaryClassification", ""),
            "status": patent.get("applicationStatus", ""),
            "url": f"https://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1={patent.get('applicationNumberText', '')}"
        }
    
    async def search_patents_by_drug(self, drug_name: str, limit: int = 50) -> Dict[str, Any]:
        """
        Search patents related to a specific drug
        """
        query = f'"{drug_name}" OR "{drug_name.lower()}" OR "{drug_name.upper()}"'
        return await self.search_patents(query, limit=limit)
    
    async def search_patents_by_therapeutic_area(self, therapeutic_area: str, limit: int = 50) -> Dict[str, Any]:
        """
        Search patents by therapeutic area
        """
        query = f'"{therapeutic_area}" OR "cancer" OR "oncology"'
        return await self.search_patents(query, limit=limit)
    
    async def get_patent_details(self, patent_number: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific patent
        """
        try:
            response = await self.client.get(f"{self.base_url}/patent/application/{patent_number}")
            response.raise_for_status()
            
            data = response.json()
            return self._process_patent_data(data)
            
        except Exception as e:
            logger.error(f"Error getting patent details for {patent_number}: {str(e)}")
            return {"error": str(e)}
    
    async def get_expiring_patents(
        self, 
        years_ahead: int = 5,
        therapeutic_area: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get patents expiring in the next N years
        """
        try:
            current_date = datetime.now()
            future_date = current_date + timedelta(days=years_ahead * 365)
            
            query = "patent"
            if therapeutic_area:
                query += f' AND "{therapeutic_area}"'
            
            return await self.search_patents(
                query=query,
                start_date=current_date.strftime("%Y-%m-%d"),
                end_date=future_date.strftime("%Y-%m-%d"),
                limit=200
            )
            
        except Exception as e:
            logger.error(f"Error getting expiring patents: {str(e)}")
            return {"error": str(e), "patents": []}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
