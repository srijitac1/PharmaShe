import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class ClinicalTrialsAPI:
    """
    Integration with ClinicalTrials.gov API
    """
    
    def __init__(self, base_url: str = "https://clinicaltrials.gov/api/v2"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_trials(
        self, 
        condition: Optional[str] = None,
        intervention: Optional[str] = None,
        phase: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Search clinical trials with various filters
        """
        try:
            params = {
                "format": "json",
                "limit": limit,
                "offset": 0
            }
            
            if condition:
                params["condition"] = condition
            if intervention:
                params["intervention"] = intervention
            if phase:
                params["phase"] = phase
            if status:
                params["status"] = status
            
            response = await self.client.get(f"{self.base_url}/studies", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process and normalize the data
            processed_trials = []
            for study in data.get("studies", []):
                trial_data = self._process_trial_data(study)
                processed_trials.append(trial_data)
            
            return {
                "total_count": data.get("totalCount", 0),
                "trials": processed_trials,
                "search_params": params
            }
            
        except Exception as e:
            logger.error(f"Error searching clinical trials: {str(e)}")
            return {"error": str(e), "trials": []}
    
    def _process_trial_data(self, study: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw trial data into standardized format
        """
        protocol_section = study.get("protocolSection", {})
        identification_module = protocol_section.get("identificationModule", {})
        status_module = protocol_section.get("statusModule", {})
        design_module = protocol_section.get("designModule", {})
        conditions_module = protocol_section.get("conditionsModule", {})
        interventions_module = protocol_section.get("interventionsModule", {})
        sponsor_module = protocol_section.get("sponsorCollaboratorsModule", {})
        
        return {
            "nct_id": identification_module.get("nctId"),
            "title": identification_module.get("briefTitle"),
            "official_title": identification_module.get("officialTitle"),
            "status": status_module.get("overallStatus"),
            "phase": self._extract_phase(design_module),
            "study_type": design_module.get("studyType"),
            "conditions": conditions_module.get("conditions", []),
            "interventions": self._extract_interventions(interventions_module),
            "sponsor": sponsor_module.get("leadSponsor", {}).get("name"),
            "start_date": status_module.get("startDateStruct", {}).get("date"),
            "completion_date": status_module.get("completionDateStruct", {}).get("date"),
            "enrollment": design_module.get("enrollmentInfo", {}).get("count"),
            "locations": self._extract_locations(protocol_section),
            "url": f"https://clinicaltrials.gov/study/{identification_module.get('nctId')}"
        }
    
    def _extract_phase(self, design_module: Dict[str, Any]) -> Optional[str]:
        """Extract phase information from design module"""
        phases = design_module.get("phases", [])
        if phases:
            return phases[0] if isinstance(phases[0], str) else phases[0].get("label")
        return None
    
    def _extract_interventions(self, interventions_module: Dict[str, Any]) -> List[str]:
        """Extract intervention names"""
        interventions = interventions_module.get("interventions", [])
        return [intervention.get("name", "") for intervention in interventions]
    
    def _extract_locations(self, protocol_section: Dict[str, Any]) -> List[str]:
        """Extract study locations"""
        locations_module = protocol_section.get("contactsLocationsModule", {})
        locations = locations_module.get("locations", [])
        return [location.get("name", "") for location in locations]
    
    async def get_trial_details(self, nct_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific trial
        """
        try:
            response = await self.client.get(f"{self.base_url}/studies/{nct_id}")
            response.raise_for_status()
            
            data = response.json()
            return self._process_trial_data(data)
            
        except Exception as e:
            logger.error(f"Error getting trial details for {nct_id}: {str(e)}")
            return {"error": str(e)}
    
    async def get_trials_by_sponsor(self, sponsor_name: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get trials by sponsor name
        """
        return await self.search_trials(limit=limit)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
