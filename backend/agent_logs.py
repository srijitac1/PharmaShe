import streamlit as st
import pandas as pd
import sys
import os
from sqlalchemy import desc

# Add parent directory to sys.path to allow imports from 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.core.database import SessionLocal
from app.models.models import AgentResult, ResearchSession

st.set_page_config(
    page_title="Agent Logs | PharmaShe",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📜 Agent Execution History")
st.markdown("Detailed audit log of all worker agent activities and their results.")

def get_logs():
    db = SessionLocal()
    try:
        # Join with ResearchSession to get context
        results = db.query(
            AgentResult,
            ResearchSession.title.label("session_title")
        ).join(
            ResearchSession, AgentResult.session_id == ResearchSession.id
        ).order_by(
            desc(AgentResult.created_at)
        ).limit(100).all()
        return results
    finally:
        db.close()

if st.button("🔄 Refresh Logs"):
    st.rerun()

# Fetch logs
logs_data = get_logs()

if logs_data:
    # Prepare data for dataframe
    table_data = []
    for log, session_title in logs_data:
        table_data.append({
            "ID": log.id,
            "Timestamp": log.created_at,
            "Agent": log.agent_type.replace("_", " ").title(),
            "Status": log.status,
            "Session": session_title,
            "Query": log.query
        })
    
    df = pd.DataFrame(table_data)
    
    # Main Table
    st.dataframe(
        df,
        column_config={
            "Timestamp": st.column_config.DatetimeColumn(
                "Time",
                format="D MMM YYYY, h:mm a"
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                help="Execution status",
                width="small"
            ),
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # Detail View
    st.subheader("🔍 Log Inspector")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_id = st.selectbox(
            "Select Log ID",
            options=df["ID"].tolist(),
            index=0
        )
    
    if selected_id:
        # Find the specific log entry
        selected_entry = next((item for item in logs_data if item[0].id == selected_id), None)
        
        if selected_entry:
            log, session_title = selected_entry
            
            # Status Banner
            if log.status == "completed":
                st.success(f"Execution Completed Successfully at {log.created_at}")
            elif log.status == "failed":
                st.error(f"Execution Failed at {log.created_at}")
            else:
                st.warning(f"Execution Status: {log.status}")
            
            # Metadata Grid
            m1, m2, m3 = st.columns(3)
            m1.info(f"**Agent:**\n{log.agent_type}")
            m2.info(f"**Session:**\n{session_title}")
            m3.info(f"**ID:**\n{log.id}")
            
            # Content
            st.markdown("### Query")
            st.code(log.query, language="text")
            
            st.markdown("### Result Data")
            st.json(log.result_data)
            
            if log.error_message:
                st.markdown("### Error Details")
                st.error(log.error_message)

else:
    st.info("No agent logs found in the database. Run queries in the main application to generate history.")