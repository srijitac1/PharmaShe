from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime, timedelta

from .clinical_trials_api import ClinicalTrialsAPI
from .uspto_api import USPTOAPI
from .pubmed_api import PubMedAPI
from .fda_api import FDADrugAPI

logger = logging.getLogger(__name__)

class ExternalAPIService:
    """
    Service to coordinate all external API integrations
    """
    
    def __init__(self):
        self.clinical_trials_api = ClinicalTrialsAPI()
        self.uspto_api = USPTOAPI()
        self.pubmed_api = PubMedAPI()
        self.fda_api = FDADrugAPI()
    
    async def search_comprehensive_research(
        self,
        query: str,
        therapeutic_area: Optional[str] = None,
        drug_name: Optional[str] = None,
        include_clinical_trials: bool = True,
        include_patents: bool = True,
        include_literature: bool = True,
        include_fda_data: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive research across all available APIs
        """
        try:
            tasks = []
            
            # Clinical Trials
            if include_clinical_trials:
                if therapeutic_area:
                    tasks.append(self.clinical_trials_api.search_trials(condition=therapeutic_area))
                elif drug_name:
                    tasks.append(self.clinical_trials_api.search_trials(intervention=drug_name))
                else:
                    tasks.append(self.clinical_trials_api.search_trials(condition="cancer"))
            
            # Patents
            if include_patents:
                if drug_name:
                    tasks.append(self.uspto_api.search_patents_by_drug(drug_name))
                elif therapeutic_area:
                    tasks.append(self.uspto_api.search_patents_by_therapeutic_area(therapeutic_area))
                else:
                    tasks.append(self.uspto_api.search_patents("cancer treatment"))
            
            # Literature
            if include_literature:
                if drug_name:
                    tasks.append(self.pubmed_api.search_by_drug(drug_name))
                elif therapeutic_area:
                    tasks.append(self.pubmed_api.search_by_therapeutic_area(therapeutic_area))
                else:
                    tasks.append(self.pubmed_api.search_articles("women cancer"))
            
            # FDA Data
            if include_fda_data:
                if drug_name:
                    tasks.append(self.fda_api.search_drugs(drug_name))
                else:
                    tasks.append(self.fda_api.search_oncology_drugs())
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            comprehensive_data = {
                "query": query,
                "therapeutic_area": therapeutic_area,
                "drug_name": drug_name,
                "timestamp": datetime.now().isoformat(),
                "clinical_trials": [],
                "patents": [],
                "literature": [],
                "fda_data": [],
                "errors": []
            }
            
            result_index = 0
            
            if include_clinical_trials:
                if result_index < len(results):
                    result = results[result_index]
                    if isinstance(result, Exception):
                        comprehensive_data["errors"].append(f"Clinical Trials API error: {str(result)}")
                    else:
                        comprehensive_data["clinical_trials"] = result.get("trials", [])
                    result_index += 1
            
            if include_patents:
                if result_index < len(results):
                    result = results[result_index]
                    if isinstance(result, Exception):
                        comprehensive_data["errors"].append(f"USPTO API error: {str(result)}")
                    else:
                        comprehensive_data["patents"] = result.get("patents", [])
                    result_index += 1
            
            if include_literature:
                if result_index < len(results):
                    result = results[result_index]
                    if isinstance(result, Exception):
                        comprehensive_data["errors"].append(f"PubMed API error: {str(result)}")
                    else:
                        comprehensive_data["literature"] = result.get("articles", [])
                    result_index += 1
            
            if include_fda_data:
                if result_index < len(results):
                    result = results[result_index]
                    if isinstance(result, Exception):
                        comprehensive_data["errors"].append(f"FDA API error: {str(result)}")
                    else:
                        comprehensive_data["fda_data"] = result.get("drugs", [])
                    result_index += 1
            
            return comprehensive_data
            
        except Exception as e:
            logger.error(f"Error in comprehensive research: {str(e)}")
            return {"error": str(e), "query": query}
    
    async def get_market_intelligence(
        self,
        therapeutic_area: str,
        drug_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get market intelligence data for a specific therapeutic area
        """
        try:
            tasks = []
            
            # Get clinical trials
            tasks.append(self.clinical_trials_api.search_trials(condition=therapeutic_area, limit=50))
            
            # Get patents
            tasks.append(self.uspto_api.search_patents_by_therapeutic_area(therapeutic_area, limit=50))
            
            # Get recent literature
            tasks.append(self.pubmed_api.search_recent_articles(f"{therapeutic_area} women", days=90, max_results=30))
            
            # Get FDA data
            if drug_name:
                tasks.append(self.fda_api.search_drugs(drug_name, limit=20))
            else:
                tasks.append(self.fda_api.search_oncology_drugs(limit=20))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            market_intelligence = {
                "therapeutic_area": therapeutic_area,
                "drug_name": drug_name,
                "timestamp": datetime.now().isoformat(),
                "clinical_trials": [],
                "patents": [],
                "recent_literature": [],
                "fda_drugs": [],
                "market_insights": {},
                "errors": []
            }
            
            # Process clinical trials
            if len(results) > 0 and not isinstance(results[0], Exception):
                trials_data = results[0]
                market_intelligence["clinical_trials"] = trials_data.get("trials", [])
                
                # Extract market insights from trials
                active_trials = [t for t in trials_data.get("trials", []) if t.get("status") == "Recruiting"]
                market_intelligence["market_insights"]["active_trials"] = len(active_trials)
                market_intelligence["market_insights"]["total_trials"] = len(trials_data.get("trials", []))
            
            # Process patents
            if len(results) > 1 and not isinstance(results[1], Exception):
                patents_data = results[1]
                market_intelligence["patents"] = patents_data.get("patents", [])
                
                # Extract patent insights
                market_intelligence["market_insights"]["total_patents"] = len(patents_data.get("patents", []))
            
            # Process literature
            if len(results) > 2 and not isinstance(results[2], Exception):
                literature_data = results[2]
                market_intelligence["recent_literature"] = literature_data.get("articles", [])
                
                # Extract research activity insights
                market_intelligence["market_insights"]["recent_publications"] = len(literature_data.get("articles", []))
            
            # Process FDA data
            if len(results) > 3 and not isinstance(results[3], Exception):
                fda_data = results[3]
                market_intelligence["fda_drugs"] = fda_data.get("drugs", [])
            
            return market_intelligence
            
        except Exception as e:
            logger.error(f"Error getting market intelligence: {str(e)}")
            return {"error": str(e), "therapeutic_area": therapeutic_area}
    
    async def get_competitive_landscape(
        self,
        therapeutic_area: str,
        drug_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get competitive landscape analysis
        """
        try:
            # Get comprehensive data
            comprehensive_data = await self.search_comprehensive_research(
                query=f"{therapeutic_area} competitive analysis",
                therapeutic_area=therapeutic_area,
                drug_name=drug_name
            )
            
            # Analyze competitive landscape
            competitive_analysis = {
                "therapeutic_area": therapeutic_area,
                "drug_name": drug_name,
                "timestamp": datetime.now().isoformat(),
                "competitors": [],
                "market_gaps": [],
                "opportunities": [],
                "threats": [],
                "data_sources": comprehensive_data
            }
            
            # Analyze clinical trials for competitors
            trials = comprehensive_data.get("clinical_trials", [])
            sponsors = {}
            for trial in trials:
                sponsor = trial.get("sponsor", "Unknown")
                if sponsor not in sponsors:
                    sponsors[sponsor] = 0
                sponsors[sponsor] += 1
            
            # Top competitors by trial activity
            top_sponsors = sorted(sponsors.items(), key=lambda x: x[1], reverse=True)[:10]
            competitive_analysis["competitors"] = [
                {"company": sponsor, "trial_count": count} 
                for sponsor, count in top_sponsors
            ]
            
            # Analyze patents for IP landscape
            patents = comprehensive_data.get("patents", [])
            assignees = {}
            for patent in patents:
                assignee = patent.get("assignee", "Unknown")
                if assignee not in assignees:
                    assignees[assignee] = 0
                assignees[assignee] += 1
            
            # Top patent holders
            top_assignees = sorted(assignees.items(), key=lambda x: x[1], reverse=True)[:10]
            competitive_analysis["ip_landscape"] = [
                {"company": assignee, "patent_count": count} 
                for assignee, count in top_assignees
            ]
            
            # Identify market gaps and opportunities
            if len(trials) < 20:
                competitive_analysis["opportunities"].append("Low clinical trial activity - potential for new entrants")
            
            if len(patents) < 50:
                competitive_analysis["opportunities"].append("Limited patent landscape - freedom to operate opportunities")
            
            # Recent literature analysis
            literature = comprehensive_data.get("literature", [])
            if len(literature) > 50:
                competitive_analysis["threats"].append("High research activity - competitive market")
            
            return competitive_analysis
            
        except Exception as e:
            logger.error(f"Error getting competitive landscape: {str(e)}")
            return {"error": str(e), "therapeutic_area": therapeutic_area}
    
    async def close(self):
        """Close all API clients"""
        await asyncio.gather(
            self.clinical_trials_api.close(),
            self.uspto_api.close(),
            self.pubmed_api.close(),
            self.fda_api.close(),
            return_exceptions=True
        )
