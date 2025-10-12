from typing import Dict, Any, List, Optional
import os
import json
from datetime import datetime
from pathlib import Path
import logging

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, PieChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows

logger = logging.getLogger(__name__)

class PDFReportGenerator:
    """
    Generate professional PDF reports
    """
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.darkblue
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        ))
        
        # Caption style
        self.styles.add(ParagraphStyle(
            name='CustomCaption',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.grey
        ))
    
    def generate_research_report(
        self,
        report_data: Dict[str, Any],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a comprehensive research report
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pharmashe_research_report_{timestamp}.pdf"
        
        filepath = self.output_dir / filename
        
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Title page
        story.extend(self._create_title_page(report_data))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(report_data))
        story.append(PageBreak())
        
        # Market analysis
        if report_data.get("market_analysis"):
            story.extend(self._create_market_analysis(report_data["market_analysis"]))
            story.append(PageBreak())
        
        # Patent landscape
        if report_data.get("patent_landscape"):
            story.extend(self._create_patent_analysis(report_data["patent_landscape"]))
            story.append(PageBreak())
        
        # Clinical trials
        if report_data.get("clinical_trials"):
            story.extend(self._create_clinical_trials(report_data["clinical_trials"]))
            story.append(PageBreak())
        
        # Competitive analysis
        if report_data.get("competitive_analysis"):
            story.extend(self._create_competitive_analysis(report_data["competitive_analysis"]))
            story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations(report_data))
        
        # Build PDF
        doc.build(story)
        
        return str(filepath)
    
    def _create_title_page(self, report_data: Dict[str, Any]) -> List:
        """Create title page"""
        elements = []
        
        # Company logo placeholder
        elements.append(Spacer(1, 2*inch))
        
        # Title
        title = Paragraph("PharmaShe Research Report", self.styles['CustomTitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = Paragraph("Women's Oncology Market Analysis", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        elements.append(Spacer(1, 1*inch))
        
        # Report details
        details_data = [
            ["Report Generated:", datetime.now().strftime("%B %d, %Y")],
            ["Query:", report_data.get("query", "N/A")],
            ["Therapeutic Area:", report_data.get("therapeutic_area", "N/A")],
            ["Drug Name:", report_data.get("drug_name", "N/A")],
            ["Data Sources:", ", ".join(report_data.get("data_sources", []))],
        ]
        
        details_table = Table(details_data, colWidths=[2*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(details_table)
        
        return elements
    
    def _create_executive_summary(self, report_data: Dict[str, Any]) -> List:
        """Create executive summary section"""
        elements = []
        
        # Section title
        title = Paragraph("Executive Summary", self.styles['CustomSubtitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary content
        summary_text = report_data.get("executive_summary", 
            "This comprehensive analysis provides insights into the women's oncology market, "
            "including market trends, competitive landscape, patent analysis, and clinical trial activity. "
            "The findings support strategic decision-making for pharmaceutical development and market entry.")
        
        summary = Paragraph(summary_text, self.styles['CustomBody'])
        elements.append(summary)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Key findings
        if report_data.get("key_findings"):
            findings_title = Paragraph("Key Findings", self.styles['Heading3'])
            elements.append(findings_title)
            
            for finding in report_data["key_findings"]:
                finding_text = f"• {finding}"
                finding_para = Paragraph(finding_text, self.styles['CustomBody'])
                elements.append(finding_para)
        
        return elements
    
    def _create_market_analysis(self, market_data: Dict[str, Any]) -> List:
        """Create market analysis section"""
        elements = []
        
        # Section title
        title = Paragraph("Market Analysis", self.styles['CustomSubtitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Market overview
        if market_data.get("market_size"):
            overview_text = f"Market Size: ${market_data['market_size']:,.0f}M"
            overview = Paragraph(overview_text, self.styles['CustomBody'])
            elements.append(overview)
        
        if market_data.get("growth_rate"):
            growth_text = f"Growth Rate: {market_data['growth_rate']:.1f}% CAGR"
            growth = Paragraph(growth_text, self.styles['CustomBody'])
            elements.append(growth)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Market trends chart
        if market_data.get("trends_data"):
            chart = self._create_market_trends_chart(market_data["trends_data"])
            elements.append(chart)
            elements.append(Spacer(1, 0.2*inch))
        
        # Competitor analysis
        if market_data.get("competitors"):
            competitors_title = Paragraph("Top Competitors", self.styles['Heading3'])
            elements.append(competitors_title)
            
            competitor_data = [["Company", "Market Share", "Key Products"]]
            for comp in market_data["competitors"][:5]:
                competitor_data.append([
                    comp.get("name", "N/A"),
                    f"{comp.get('market_share', 0):.1f}%",
                    ", ".join(comp.get("key_products", []))
                ])
            
            comp_table = Table(competitor_data, colWidths=[2*inch, 1*inch, 2.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(comp_table)
        
        return elements
    
    def _create_patent_analysis(self, patent_data: Dict[str, Any]) -> List:
        """Create patent analysis section"""
        elements = []
        
        # Section title
        title = Paragraph("Patent Landscape Analysis", self.styles['CustomSubtitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Patent overview
        if patent_data.get("total_patents"):
            overview_text = f"Total Patents Analyzed: {patent_data['total_patents']:,}"
            overview = Paragraph(overview_text, self.styles['CustomBody'])
            elements.append(overview)
        
        if patent_data.get("active_patents"):
            active_text = f"Active Patents: {patent_data['active_patents']:,}"
            active = Paragraph(active_text, self.styles['CustomBody'])
            elements.append(active)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Freedom to operate analysis
        if patent_data.get("freedom_to_operate"):
            fto_title = Paragraph("Freedom to Operate Analysis", self.styles['Heading3'])
            elements.append(fto_title)
            
            fto = patent_data["freedom_to_operate"]
            risk_level = fto.get("overall_risk_level", "Unknown")
            blocking_patents = fto.get("blocking_patents", 0)
            
            risk_text = f"Overall Risk Level: {risk_level}"
            risk_para = Paragraph(risk_text, self.styles['CustomBody'])
            elements.append(risk_para)
            
            blocking_text = f"Blocking Patents: {blocking_patents}"
            blocking_para = Paragraph(blocking_text, self.styles['CustomBody'])
            elements.append(blocking_para)
        
        # Patent expiration opportunities
        if patent_data.get("upcoming_expirations"):
            exp_title = Paragraph("Patent Expiration Opportunities", self.styles['Heading3'])
            elements.append(exp_title)
            
            expirations = patent_data["upcoming_expirations"]
            total_expiring = expirations.get("total_expiring", 0)
            high_impact = expirations.get("high_impact_expirations", 0)
            
            exp_text = f"Patents Expiring (Next 5 Years): {total_expiring}"
            exp_para = Paragraph(exp_text, self.styles['CustomBody'])
            elements.append(exp_para)
            
            impact_text = f"High-Impact Expirations: {high_impact}"
            impact_para = Paragraph(impact_text, self.styles['CustomBody'])
            elements.append(impact_para)
        
        return elements
    
    def _create_clinical_trials(self, trials_data: Dict[str, Any]) -> List:
        """Create clinical trials section"""
        elements = []
        
        # Section title
        title = Paragraph("Clinical Trials Analysis", self.styles['CustomSubtitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Trial overview
        if trials_data.get("total_trials"):
            total_text = f"Total Trials: {trials_data['total_trials']:,}"
            total_para = Paragraph(total_text, self.styles['CustomBody'])
            elements.append(total_para)
        
        if trials_data.get("active_trials"):
            active_text = f"Active Trials: {trials_data['active_trials']:,}"
            active_para = Paragraph(active_text, self.styles['CustomBody'])
            elements.append(active_para)
        
        if trials_data.get("recruiting_trials"):
            recruiting_text = f"Currently Recruiting: {trials_data['recruiting_trials']:,}"
            recruiting_para = Paragraph(recruiting_text, self.styles['CustomBody'])
            elements.append(recruiting_para)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Phase distribution
        if trials_data.get("phase_distribution"):
            phase_title = Paragraph("Trial Phase Distribution", self.styles['Heading3'])
            elements.append(phase_title)
            
            phase_data = [["Phase", "Number of Trials"]]
            for phase, count in trials_data["phase_distribution"].items():
                phase_data.append([phase, str(count)])
            
            phase_table = Table(phase_data, colWidths=[2*inch, 1.5*inch])
            phase_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(phase_table)
        
        return elements
    
    def _create_competitive_analysis(self, competitive_data: Dict[str, Any]) -> List:
        """Create competitive analysis section"""
        elements = []
        
        # Section title
        title = Paragraph("Competitive Landscape", self.styles['CustomSubtitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Competitors
        if competitive_data.get("competitors"):
            comp_title = Paragraph("Top Competitors", self.styles['Heading3'])
            elements.append(comp_title)
            
            comp_data = [["Company", "Trial Count", "Market Position"]]
            for comp in competitive_data["competitors"][:10]:
                comp_data.append([
                    comp.get("company", "N/A"),
                    str(comp.get("trial_count", 0)),
                    "Leader" if comp.get("trial_count", 0) > 50 else "Active"
                ])
            
            comp_table = Table(comp_data, colWidths=[2*inch, 1*inch, 1.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(comp_table)
        
        return elements
    
    def _create_recommendations(self, report_data: Dict[str, Any]) -> List:
        """Create recommendations section"""
        elements = []
        
        # Section title
        title = Paragraph("Strategic Recommendations", self.styles['CustomSubtitle'])
        elements.append(title)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        recommendations = report_data.get("recommendations", [
            "Focus on underserved patient populations",
            "Develop combination therapies",
            "Leverage patent expiration opportunities",
            "Establish strategic partnerships",
            "Invest in biomarker-driven approaches"
        ])
        
        for i, rec in enumerate(recommendations, 1):
            rec_text = f"{i}. {rec}"
            rec_para = Paragraph(rec_text, self.styles['CustomBody'])
            elements.append(rec_para)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Next steps
        next_steps_title = Paragraph("Next Steps", self.styles['Heading3'])
        elements.append(next_steps_title)
        
        next_steps = [
            "Conduct detailed market research",
            "Develop business case",
            "Identify partnership opportunities",
            "Prepare regulatory strategy",
            "Establish project timeline"
        ]
        
        for step in next_steps:
            step_text = f"• {step}"
            step_para = Paragraph(step_text, self.styles['CustomBody'])
            elements.append(step_para)
        
        return elements
    
    def _create_market_trends_chart(self, trends_data: List[Dict]) -> Drawing:
        """Create market trends chart"""
        drawing = Drawing(400, 200)
        
        # Sample chart data
        data = [(10, 20, 30, 40, 50)]
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = data
        chart.lines[0].strokeColor = colors.darkblue
        
        drawing.add(chart)
        return drawing
