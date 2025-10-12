import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class FDADrugAPI:
    """
    Integration with FDA Drug API
    """
    
    def __init__(self, base_url: str = "https://api.fda.gov"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_drugs(
        self,
        search_term: str,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """
        Search FDA drug database
        """
        try:
            params = {
                "search": f"openfda.brand_name:{search_term} OR openfda.generic_name:{search_term}",
                "limit": limit,
                "skip": skip
            }
            
            response = await self.client.get(f"{self.base_url}/drug/label.json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process drug data
            processed_drugs = []
            for drug in data.get("results", []):
                drug_data = self._process_drug_data(drug)
                processed_drugs.append(drug_data)
            
            return {
                "total_count": data.get("meta", {}).get("results", {}).get("total", 0),
                "drugs": processed_drugs,
                "search_params": params
            }
            
        except Exception as e:
            logger.error(f"Error searching FDA drugs: {str(e)}")
            return {"error": str(e), "drugs": []}
    
    def _process_drug_data(self, drug: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw drug data into standardized format
        """
        openfda = drug.get("openfda", {})
        
        return {
            "brand_name": openfda.get("brand_name", [""])[0] if openfda.get("brand_name") else "",
            "generic_name": openfda.get("generic_name", [""])[0] if openfda.get("generic_name") else "",
            "manufacturer": openfda.get("manufacturer_name", [""])[0] if openfda.get("manufacturer_name") else "",
            "product_type": openfda.get("product_type", [""])[0] if openfda.get("product_type") else "",
            "route": openfda.get("route", [""])[0] if openfda.get("route") else "",
            "dosage_form": openfda.get("dosage_form", [""])[0] if openfda.get("dosage_form") else "",
            "active_ingredients": openfda.get("substance_name", []),
            "indications": drug.get("indications_and_usage", [""])[0] if drug.get("indications_and_usage") else "",
            "warnings": drug.get("warnings", [""])[0] if drug.get("warnings") else "",
            "adverse_reactions": drug.get("adverse_reactions", [""])[0] if drug.get("adverse_reactions") else "",
            "description": drug.get("description", [""])[0] if drug.get("description") else "",
            "clinical_pharmacology": drug.get("clinical_pharmacology", [""])[0] if drug.get("clinical_pharmacology") else "",
            "nonclinical_toxicology": drug.get("nonclinical_toxicology", [""])[0] if drug.get("nonclinical_toxicology") else "",
            "clinical_studies": drug.get("clinical_studies", [""])[0] if drug.get("clinical_studies") else "",
            "how_supplied": drug.get("how_supplied", [""])[0] if drug.get("how_supplied") else "",
            "storage_and_handling": drug.get("storage_and_handling", [""])[0] if drug.get("storage_and_handling") else "",
            "patient_counseling": drug.get("patient_counseling_information", [""])[0] if drug.get("patient_counseling_information") else ""
        }
    
    async def search_drugs_by_indication(self, indication: str, limit: int = 50) -> Dict[str, Any]:
        """
        Search drugs by indication
        """
        try:
            params = {
                "search": f"indications_and_usage:{indication}",
                "limit": limit
            }
            
            response = await self.client.get(f"{self.base_url}/drug/label.json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            processed_drugs = []
            for drug in data.get("results", []):
                drug_data = self._process_drug_data(drug)
                processed_drugs.append(drug_data)
            
            return {
                "total_count": data.get("meta", {}).get("results", {}).get("total", 0),
                "drugs": processed_drugs,
                "indication": indication
            }
            
        except Exception as e:
            logger.error(f"Error searching drugs by indication: {str(e)}")
            return {"error": str(e), "drugs": []}
    
    async def search_oncology_drugs(self, limit: int = 100) -> Dict[str, Any]:
        """
        Search for oncology-related drugs
        """
        oncology_terms = ["cancer", "oncology", "tumor", "neoplasm", "carcinoma", "sarcoma", "lymphoma", "leukemia"]
        search_query = " OR ".join([f"indications_and_usage:{term}" for term in oncology_terms])
        
        try:
            params = {
                "search": search_query,
                "limit": limit
            }
            
            response = await self.client.get(f"{self.base_url}/drug/label.json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            processed_drugs = []
            for drug in data.get("results", []):
                drug_data = self._process_drug_data(drug)
                processed_drugs.append(drug_data)
            
            return {
                "total_count": data.get("meta", {}).get("results", {}).get("total", 0),
                "drugs": processed_drugs,
                "search_type": "oncology"
            }
            
        except Exception as e:
            logger.error(f"Error searching oncology drugs: {str(e)}")
            return {"error": str(e), "drugs": []}
    
    async def get_drug_events(
        self,
        drug_name: str,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get adverse events for a specific drug
        """
        try:
            params = {
                "search": f"patient.drug.medicinalproduct:{drug_name}",
                "limit": limit
            }
            
            response = await self.client.get(f"{self.base_url}/drug/event.json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            events = []
            for event in data.get("results", []):
                event_data = {
                    "event_id": event.get("safetyreportid"),
                    "received_date": event.get("receivedate"),
                    "serious": event.get("serious"),
                    "outcome": event.get("patient", {}).get("reaction", []),
                    "drugs": event.get("patient", {}).get("drug", []),
                    "patient_age": event.get("patient", {}).get("patientonsetage"),
                    "patient_sex": event.get("patient", {}).get("patientsex")
                }
                events.append(event_data)
            
            return {
                "total_count": data.get("meta", {}).get("results", {}).get("total", 0),
                "events": events,
                "drug_name": drug_name
            }
            
        except Exception as e:
            logger.error(f"Error getting drug events: {str(e)}")
            return {"error": str(e), "events": []}
    
    async def get_drug_recalls(
        self,
        drug_name: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get drug recall information
        """
        try:
            params = {"limit": limit}
            
            if drug_name:
                params["search"] = f"product_description:{drug_name}"
            
            response = await self.client.get(f"{self.base_url}/drug/enforcement.json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            recalls = []
            for recall in data.get("results", []):
                recall_data = {
                    "recall_number": recall.get("recall_number"),
                    "product_description": recall.get("product_description"),
                    "reason_for_recall": recall.get("reason_for_recall"),
                    "recall_initiation_date": recall.get("recall_initiation_date"),
                    "recall_status": recall.get("status"),
                    "distribution_pattern": recall.get("distribution_pattern"),
                    "product_quantity": recall.get("product_quantity"),
                    "code_info": recall.get("code_info")
                }
                recalls.append(recall_data)
            
            return {
                "total_count": data.get("meta", {}).get("results", {}).get("total", 0),
                "recalls": recalls,
                "drug_name": drug_name
            }
            
        except Exception as e:
            logger.error(f"Error getting drug recalls: {str(e)}")
            return {"error": str(e), "recalls": []}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
