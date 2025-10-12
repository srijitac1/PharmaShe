from typing import Dict, Any, List
from sqlalchemy.orm import Session
import json
import random
from datetime import datetime, timedelta

from .base_agent import BaseAgent

class ClinicalTrialsAgent(BaseAgent):
    """
    Clinical Trials Agent for monitoring clinical development pipeline
    """
    
    def __init__(self):
        super().__init__("clinical_trials")
        self.description = "Monitors clinical development pipeline and trial activity"
    
    async def process_query(self, query: str, db: Session) -> Dict[str, Any]:
        """
        Analyze clinical trials data and pipeline
        """
        try:
            keywords = self._extract_keywords(query)
            
            # Analyze clinical trials
            trial_analysis = await self._analyze_trial_pipeline(keywords, db)
            sponsor_analysis = await self._analyze_sponsors(keywords, db)
            phase_distribution = await self._analyze_phases(keywords, db)
            geographic_distribution = await self._analyze_geography(keywords, db)
            
            # Create summary
            summary = self._create_trial_summary(trial_analysis, sponsor_analysis, phase_distribution)
            
            response_data = {
                "trial_pipeline": trial_analysis,
                "sponsor_analysis": sponsor_analysis,
                "phase_distribution": phase_distribution,
                "geographic_distribution": geographic_distribution,
                "key_insights": self._extract_trial_insights(trial_analysis, sponsor_analysis)
            }
            
            return self._format_response(response_data, summary)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    async def _analyze_trial_pipeline(self, keywords: List[str], db: Session) -> Dict[str, Any]:
        """
        Analyze the clinical trial pipeline
        """
        # Simulate clinical trial analysis
        pipeline = {
            "total_trials": random.randint(200, 2000),
            "active_trials": random.randint(100, 1000),
            "completed_trials": random.randint(50, 500),
            "recruiting_trials": random.randint(30, 300),
            "trial_status_distribution": {
                "recruiting": random.randint(20, 200),
                "active_not_recruiting": random.randint(15, 150),
                "completed": random.randint(30, 300),
                "terminated": random.randint(5, 50),
                "suspended": random.randint(2, 20),
                "withdrawn": random.randint(3, 30)
            },
            "therapeutic_areas": {
                "breast_cancer": random.randint(50, 500),
                "ovarian_cancer": random.randint(30, 300),
                "cervical_cancer": random.randint(20, 200),
                "endometrial_cancer": random.randint(15, 150),
                "other_gynecological": random.randint(25, 250)
            },
            "intervention_types": {
                "drug": random.randint(100, 1000),
                "biological": random.randint(50, 500),
                "device": random.randint(20, 200),
                "procedure": random.randint(30, 300),
                "behavioral": random.randint(10, 100)
            }
        }
        
        return pipeline
    
    async def _analyze_sponsors(self, keywords: List[str], db: Session) -> Dict[str, Any]:
        """
        Analyze trial sponsors and their activity
        """
        # Simulate sponsor analysis
        sponsors = {
            "top_sponsors": [
                {
                    "name": "Roche",
                    "trial_count": random.randint(20, 100),
                    "focus_areas": ["Breast cancer", "Ovarian cancer"],
                    "phase_distribution": {"Phase I": 5, "Phase II": 15, "Phase III": 8}
                },
                {
                    "name": "Pfizer",
                    "trial_count": random.randint(15, 80),
                    "focus_areas": ["Breast cancer", "Cervical cancer"],
                    "phase_distribution": {"Phase I": 3, "Phase II": 12, "Phase III": 6}
                },
                {
                    "name": "Merck",
                    "trial_count": random.randint(12, 70),
                    "focus_areas": ["Cervical cancer", "Endometrial cancer"],
                    "phase_distribution": {"Phase I": 4, "Phase II": 10, "Phase III": 5}
                },
                {
                    "name": "Novartis",
                    "trial_count": random.randint(10, 60),
                    "focus_areas": ["Breast cancer", "Ovarian cancer"],
                    "phase_distribution": {"Phase I": 2, "Phase II": 8, "Phase III": 4}
                }
            ],
            "academic_institutions": [
                {"name": "MD Anderson Cancer Center", "trial_count": random.randint(5, 30)},
                {"name": "Memorial Sloan Kettering", "trial_count": random.randint(4, 25)},
                {"name": "Dana-Farber Cancer Institute", "trial_count": random.randint(3, 20)}
            ],
            "emerging_sponsors": [
                {"name": "BioNTech", "trial_count": random.randint(2, 15)},
                {"name": "Moderna", "trial_count": random.randint(1, 10)},
                {"name": "CureVac", "trial_count": random.randint(1, 8)}
            ]
        }
        
        return sponsors
    
    async def _analyze_phases(self, keywords: List[str], db: Session) -> Dict[str, Any]:
        """
        Analyze trial phase distribution
        """
        # Simulate phase analysis
        phases = {
            "phase_distribution": {
                "Phase I": random.randint(30, 300),
                "Phase II": random.randint(50, 500),
                "Phase III": random.randint(20, 200),
                "Phase IV": random.randint(10, 100),
                "Not Applicable": random.randint(20, 200)
            },
            "phase_success_rates": {
                "Phase I to II": round(random.uniform(60, 80), 1),
                "Phase II to III": round(random.uniform(30, 50), 1),
                "Phase III to Approval": round(random.uniform(60, 80), 1)
            },
            "average_duration": {
                "Phase I": f"{random.randint(12, 24)} months",
                "Phase II": f"{random.randint(18, 36)} months",
                "Phase III": f"{random.randint(24, 48)} months"
            },
            "key_phase_insights": [
                "High Phase II activity indicates strong pipeline",
                "Phase III trials focus on combination therapies",
                "Early phase trials exploring novel mechanisms"
            ]
        }
        
        return phases
    
    async def _analyze_geography(self, keywords: List[str], db: Session) -> Dict[str, Any]:
        """
        Analyze geographic distribution of trials
        """
        # Simulate geographic analysis
        geography = {
            "regional_distribution": {
                "North America": random.randint(80, 800),
                "Europe": random.randint(60, 600),
                "Asia": random.randint(40, 400),
                "Latin America": random.randint(20, 200),
                "Africa": random.randint(5, 50),
                "Oceania": random.randint(10, 100)
            },
            "top_countries": [
                {"country": "United States", "trial_count": random.randint(50, 500)},
                {"country": "China", "trial_count": random.randint(30, 300)},
                {"country": "Germany", "trial_count": random.randint(20, 200)},
                {"country": "United Kingdom", "trial_count": random.randint(15, 150)},
                {"country": "Japan", "trial_count": random.randint(12, 120)}
            ],
            "regulatory_environment": {
                "FDA_approved_trials": random.randint(100, 1000),
                "EMA_approved_trials": random.randint(80, 800),
                "NMPA_approved_trials": random.randint(60, 600)
            }
        }
        
        return geography
    
    def _extract_trial_insights(self, trial_analysis: Dict, sponsor_analysis: Dict) -> List[str]:
        """
        Extract key insights from trial analysis
        """
        insights = []
        
        # Pipeline insights
        total_trials = trial_analysis["total_trials"]
        active_trials = trial_analysis["active_trials"]
        insights.append(f"Strong pipeline with {total_trials:,} total trials, {active_trials:,} currently active")
        
        # Therapeutic area insights
        if trial_analysis["therapeutic_areas"]:
            top_area = max(trial_analysis["therapeutic_areas"].items(), key=lambda x: x[1])
            insights.append(f"{top_area[0].replace('_', ' ').title()} dominates with {top_area[1]} trials")
        
        # Sponsor insights
        if sponsor_analysis["top_sponsors"]:
            top_sponsor = max(sponsor_analysis["top_sponsors"], key=lambda x: x["trial_count"])
            insights.append(f"{top_sponsor['name']} leads with {top_sponsor['trial_count']} trials")
        
        # Phase insights
        phase_dist = trial_analysis.get("phase_distribution", {})
        if phase_dist:
            max_phase = max(phase_dist.items(), key=lambda x: x[1])
            insights.append(f"Highest activity in {max_phase[0]} with {max_phase[1]} trials")
        
        return insights
    
    def _create_trial_summary(self, trial_analysis: Dict, sponsors: Dict, phases: Dict) -> str:
        """
        Create comprehensive clinical trial summary
        """
        summary_parts = []
        
        # Overall pipeline
        total_trials = trial_analysis["total_trials"]
        active_trials = trial_analysis["active_trials"]
        recruiting_trials = trial_analysis["recruiting_trials"]
        
        summary_parts.append(f"**Clinical Pipeline:** {total_trials:,} total trials identified, with {active_trials:,} active and {recruiting_trials:,} currently recruiting.")
        
        # Therapeutic areas
        if trial_analysis["therapeutic_areas"]:
            top_areas = sorted(trial_analysis["therapeutic_areas"].items(), key=lambda x: x[1], reverse=True)[:3]
            area_summary = ", ".join([f"{area.replace('_', ' ').title()} ({count})" for area, count in top_areas])
            summary_parts.append(f"**Leading Therapeutic Areas:** {area_summary}")
        
        # Sponsor activity
        if sponsors["top_sponsors"]:
            top_sponsor = max(sponsors["top_sponsors"], key=lambda x: x["trial_count"])
            summary_parts.append(f"**Top Sponsor:** {top_sponsor['name']} with {top_sponsor['trial_count']} trials")
        
        # Phase distribution
        if phases["phase_distribution"]:
            max_phase = max(phases["phase_distribution"].items(), key=lambda x: x[1])
            summary_parts.append(f"**Phase Activity:** Highest activity in {max_phase[0]} with {max_phase[1]} trials")
        
        return "\n\n".join(summary_parts)
