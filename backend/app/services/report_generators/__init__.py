from typing import Dict, Any, List, Optional
import os
import json
from datetime import datetime
from pathlib import Path
import logging

from .pdf_generator import PDFReportGenerator
from .excel_generator import ExcelReportGenerator

logger = logging.getLogger(__name__)

class ReportService:
    """
    Main service for generating comprehensive reports
    """
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.pdf_generator = PDFReportGenerator(str(self.output_dir))
        self.excel_generator = ExcelReportGenerator(str(self.output_dir))
    
    async def generate_comprehensive_report(
        self,
        research_data: Dict[str, Any],
        report_type: str = "both",
        filename_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive research report
        """
        try:
            # Prepare report data
            report_data = self._prepare_report_data(research_data)
            
            results = {
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "files": [],
                "metadata": {
                    "query": report_data.get("query", ""),
                    "therapeutic_area": report_data.get("therapeutic_area", ""),
                    "drug_name": report_data.get("drug_name", ""),
                    "data_sources": report_data.get("data_sources", [])
                }
            }
            
            # Generate PDF report
            if report_type in ["pdf", "both"]:
                pdf_filename = self._generate_filename("pdf", filename_prefix)
                pdf_path = self.pdf_generator.generate_research_report(report_data, pdf_filename)
                results["files"].append({
                    "type": "pdf",
                    "filename": pdf_filename,
                    "path": pdf_path,
                    "size": os.path.getsize(pdf_path)
                })
            
            # Generate Excel report
            if report_type in ["excel", "both"]:
                excel_filename = self._generate_filename("xlsx", filename_prefix)
                excel_path = self.excel_generator.generate_research_report(report_data, excel_filename)
                results["files"].append({
                    "type": "excel",
                    "filename": excel_filename,
                    "path": excel_path,
                    "size": os.path.getsize(excel_path)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {str(e)}")
            return {"error": str(e), "report_type": report_type}
    
    def _prepare_report_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare and structure data for report generation
        """
        # Extract data from different sources
        clinical_trials = research_data.get("clinical_trials", {})
        patents = research_data.get("patents", {})
        literature = research_data.get("literature", {})
        fda_data = research_data.get("fda_data", {})
        
        # Calculate summary metrics
        total_trials = len(clinical_trials.get("trials", []))
        active_trials = len([t for t in clinical_trials.get("trials", []) 
                           if t.get("status") in ["Recruiting", "Active, not recruiting"]])
        
        total_patents = len(patents.get("patents", []))
        blocking_patents = patents.get("freedom_to_operate", {}).get("blocking_patents", 0)
        
        total_publications = len(literature.get("articles", []))
        
        # Market analysis data
        market_size = research_data.get("market_size", 15000)  # Default value
        growth_rate = research_data.get("growth_rate", 9.5)     # Default value
        
        # Prepare structured report data
        report_data = {
            "query": research_data.get("query", "Women's Oncology Research"),
            "therapeutic_area": research_data.get("therapeutic_area", "Women's Oncology"),
            "drug_name": research_data.get("drug_name"),
            "data_sources": ["ClinicalTrials.gov", "USPTO", "PubMed", "FDA"],
            
            # Executive summary
            "executive_summary": self._generate_executive_summary(research_data),
            "key_findings": self._extract_key_findings(research_data),
            
            # Market analysis
            "market_analysis": {
                "market_size": market_size,
                "growth_rate": growth_rate,
                "competitors": self._extract_competitors(clinical_trials),
                "trends_data": self._generate_trends_data(market_size, growth_rate)
            },
            
            # Patent analysis
            "patent_landscape": {
                "total_patents": total_patents,
                "active_patents": total_patents - blocking_patents,
                "blocking_patents": blocking_patents,
                "expiring_patents": patents.get("upcoming_expirations", {}).get("total_expiring", 0),
                "freedom_to_operate": patents.get("freedom_to_operate", {}),
                "upcoming_expirations": patents.get("upcoming_expirations", {})
            },
            
            # Clinical trials
            "clinical_trials": {
                "total_trials": total_trials,
                "active_trials": active_trials,
                "recruiting_trials": len([t for t in clinical_trials.get("trials", []) 
                                        if t.get("status") == "Recruiting"]),
                "completed_trials": len([t for t in clinical_trials.get("trials", []) 
                                       if t.get("status") == "Completed"]),
                "phase_distribution": self._calculate_phase_distribution(clinical_trials),
                "sponsor_analysis": self._extract_sponsors(clinical_trials)
            },
            
            # Competitive analysis
            "competitive_analysis": {
                "competitors": self._extract_competitors(clinical_trials),
                "market_gaps": self._identify_market_gaps(research_data),
                "opportunities": self._identify_opportunities(research_data)
            },
            
            # Literature analysis
            "literature": {
                "total_publications": total_publications,
                "recent_publications": literature.get("articles", [])[:10],
                "research_trends": self._extract_research_trends(literature)
            },
            
            # FDA data
            "fda_data": {
                "approved_drugs": fda_data.get("drugs", [])[:10],
                "safety_data": fda_data.get("events", []),
                "recalls": fda_data.get("recalls", [])
            },
            
            # Recommendations
            "recommendations": self._generate_recommendations(research_data),
            "next_steps": self._generate_next_steps(research_data)
        }
        
        return report_data
    
    def _generate_executive_summary(self, research_data: Dict[str, Any]) -> str:
        """Generate executive summary text"""
        therapeutic_area = research_data.get("therapeutic_area", "women's oncology")
        total_trials = len(research_data.get("clinical_trials", {}).get("trials", []))
        total_patents = len(research_data.get("patents", {}).get("patents", []))
        
        summary = f"""
        This comprehensive analysis of the {therapeutic_area} market reveals significant opportunities 
        for pharmaceutical development and market entry. The research identified {total_trials} active 
        clinical trials and {total_patents} relevant patents, indicating a dynamic and competitive 
        landscape with room for innovation and differentiation.
        
        Key market drivers include increasing incidence rates, advances in personalized medicine, 
        and growing demand for effective treatments with improved safety profiles. The analysis 
        suggests multiple pathways for strategic market entry, including combination therapies, 
        novel formulations, and targeted patient populations.
        """
        
        return summary.strip()
    
    def _extract_key_findings(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract key findings from research data"""
        findings = []
        
        # Clinical trials findings
        trials = research_data.get("clinical_trials", {}).get("trials", [])
        if trials:
            active_trials = len([t for t in trials if t.get("status") in ["Recruiting", "Active, not recruiting"]])
            findings.append(f"{active_trials} active clinical trials identified")
        
        # Patent findings
        patents = research_data.get("patents", {}).get("patents", [])
        if patents:
            findings.append(f"{len(patents)} patents analyzed in the landscape")
        
        # Literature findings
        articles = research_data.get("literature", {}).get("articles", [])
        if articles:
            findings.append(f"{len(articles)} recent scientific publications reviewed")
        
        # Market findings
        market_size = research_data.get("market_size", 0)
        if market_size > 0:
            findings.append(f"Market size estimated at ${market_size:,.0f}M")
        
        return findings
    
    def _extract_competitors(self, clinical_trials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract competitor information from clinical trials"""
        trials = clinical_trials.get("trials", [])
        sponsors = {}
        
        for trial in trials:
            sponsor = trial.get("sponsor", "Unknown")
            if sponsor not in sponsors:
                sponsors[sponsor] = {"trial_count": 0, "key_products": []}
            sponsors[sponsor]["trial_count"] += 1
        
        # Convert to list format
        competitors = []
        for sponsor, data in sponsors.items():
            competitors.append({
                "company": sponsor,
                "trial_count": data["trial_count"],
                "market_share": min(data["trial_count"] * 2, 20),  # Rough estimate
                "key_products": data["key_products"]
            })
        
        # Sort by trial count
        competitors.sort(key=lambda x: x["trial_count"], reverse=True)
        
        return competitors[:10]  # Top 10
    
    def _generate_trends_data(self, market_size: float, growth_rate: float) -> List[Dict[str, Any]]:
        """Generate market trends data"""
        trends = []
        current_size = market_size
        
        for year in range(2020, 2025):
            trends.append({
                "year": year,
                "market_size": current_size,
                "growth_rate": growth_rate,
                "key_events": f"Market expansion in {year}"
            })
            current_size *= (1 + growth_rate / 100)
        
        return trends
    
    def _calculate_phase_distribution(self, clinical_trials: Dict[str, Any]) -> Dict[str, int]:
        """Calculate phase distribution from clinical trials"""
        trials = clinical_trials.get("trials", [])
        phases = {}
        
        for trial in trials:
            phase = trial.get("phase", "Unknown")
            phases[phase] = phases.get(phase, 0) + 1
        
        return phases
    
    def _extract_sponsors(self, clinical_trials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract sponsor information"""
        trials = clinical_trials.get("trials", [])
        sponsors = {}
        
        for trial in trials:
            sponsor = trial.get("sponsor", "Unknown")
            if sponsor not in sponsors:
                sponsors[sponsor] = 0
            sponsors[sponsor] += 1
        
        # Convert to list format
        sponsor_list = []
        for sponsor, count in sponsors.items():
            sponsor_list.append({
                "name": sponsor,
                "trial_count": count,
                "focus_areas": ["Oncology", "Women's Health"]
            })
        
        # Sort by trial count
        sponsor_list.sort(key=lambda x: x["trial_count"], reverse=True)
        
        return sponsor_list[:10]  # Top 10
    
    def _identify_market_gaps(self, research_data: Dict[str, Any]) -> List[str]:
        """Identify market gaps and opportunities"""
        gaps = []
        
        trials = research_data.get("clinical_trials", {}).get("trials", [])
        if len(trials) < 50:
            gaps.append("Limited clinical trial activity - opportunity for new entrants")
        
        patents = research_data.get("patents", {}).get("patents", [])
        if len(patents) < 100:
            gaps.append("Sparse patent landscape - freedom to operate opportunities")
        
        gaps.append("Underserved patient populations")
        gaps.append("Need for combination therapies")
        gaps.append("Limited biomarker-driven approaches")
        
        return gaps
    
    def _identify_opportunities(self, research_data: Dict[str, Any]) -> List[str]:
        """Identify strategic opportunities"""
        opportunities = [
            "Focus on underserved populations",
            "Develop combination therapies",
            "Leverage patent expiration opportunities",
            "Establish strategic partnerships",
            "Invest in personalized medicine approaches"
        ]
        
        return opportunities
    
    def _extract_research_trends(self, literature: Dict[str, Any]) -> List[str]:
        """Extract research trends from literature"""
        trends = [
            "Immunotherapy combinations",
            "Biomarker-driven therapy",
            "Drug repurposing",
            "Novel drug delivery systems",
            "Precision medicine approaches"
        ]
        
        return trends
    
    def _generate_recommendations(self, research_data: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = [
            "Focus on underserved patient populations with high unmet medical needs",
            "Develop combination therapies leveraging existing approved drugs",
            "Leverage upcoming patent expiration opportunities for generic development",
            "Establish strategic partnerships with academic institutions and biotech companies",
            "Invest in biomarker research to enable personalized medicine approaches",
            "Consider novel drug delivery systems to improve patient compliance",
            "Develop comprehensive market access strategies for emerging markets"
        ]
        
        return recommendations
    
    def _generate_next_steps(self, research_data: Dict[str, Any]) -> List[str]:
        """Generate next steps for implementation"""
        next_steps = [
            "Conduct detailed market research and validation studies",
            "Develop comprehensive business case with financial projections",
            "Identify and evaluate potential partnership opportunities",
            "Prepare regulatory strategy and timeline",
            "Establish project management framework and timeline",
            "Conduct competitive intelligence monitoring",
            "Develop intellectual property strategy",
            "Create go-to-market strategy and launch plan"
        ]
        
        return next_steps
    
    def _generate_filename(self, extension: str, prefix: Optional[str] = None) -> str:
        """Generate filename for report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if prefix:
            return f"{prefix}_{timestamp}.{extension}"
        else:
            return f"pharmashe_report_{timestamp}.{extension}"
    
    def get_report_info(self, filepath: str) -> Dict[str, Any]:
        """Get information about a generated report"""
        try:
            path = Path(filepath)
            if not path.exists():
                return {"error": "File not found"}
            
            return {
                "filename": path.name,
                "filepath": str(path),
                "size": path.stat().st_size,
                "created": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                "extension": path.suffix
            }
        except Exception as e:
            return {"error": str(e)}
