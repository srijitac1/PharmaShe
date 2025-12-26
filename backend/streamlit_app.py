# Run with: streamlit run streamlit_app.py

import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

# Add current directory to sys.path to allow imports from 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.research_pipeline import build_pipeline
from app.models.schemas import ResearchState

st.set_page_config(
    page_title="PharmaShe",
    layout="wide"
)

st.title("PharmaShe — Agentic Scientific Workspace")

# Sidebar
with st.sidebar:
    st.header("Research Workspace")
    st.markdown("Active Agents")
    st.markdown("- Genomic Harvester")
    st.markdown("- IP & Regulatory Scout")
    st.markdown("- Literature Review Scout")
    st.markdown("- Trust Analyst (RRF)")
    st.markdown("---")
    st.markdown("Domain")
    st.markdown("Women's Oncology")

# Main input
focus = st.text_input(
    "Define biological focus",
    placeholder="e.g. Breast Cancer — BRCA1"
)

if st.button("Run Validation Pipeline"):
    if not focus:
        st.warning("Please define a biological focus.")
    else:
        pipeline = build_pipeline()

        initial_state = ResearchState(
            biological_focus=focus
        )

        with st.spinner("Agents are analyzing scientific evidence..."):
            # Invoke the pipeline
            result = pipeline.invoke(initial_state)

        st.subheader("Evidence Trace")
        for e in result.get("evidence", []):
            st.info(f"{e.source} — {e.finding}")

        st.subheader("Trust & Confidence")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("RR Fusion Score", result.get("rrf_score"))
            
        with col2:
            evidence_list = result.get("evidence", [])
            if evidence_list:
                k = 60
                chart_data = []
                for e in evidence_list:
                    contribution = 1 / (k + e.rank)
                    chart_data.append({
                        "Source": e.source,
                        "Contribution": contribution
                    })
                
                df = pd.DataFrame(chart_data)
                fig = px.bar(
                    df,
                    x="Contribution",
                    y="Source",
                    orientation='h',
                    title="Score Contribution by Source",
                    text_auto='.4f'
                )
                fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

        with st.expander("Agent Activity Log"):
            for log in result.get("logs", []):
                st.write(log)