import streamlit as st
from agents.master_agent import run_analysis

st.set_page_config(
    page_title="PharmaShe – Agentic Research Analyst",
    layout="wide"
)

st.title("🧠 PharmaShe")
st.subheader("DeepSomatic-inspired Agentic AI for Pharma Research")

query = st.text_input(
    "Enter supplement–drug interaction or research question:",
    placeholder="e.g. Curcumin interaction with Tamoxifen in breast cancer"
)

if st.button("Run Analysis"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("🧪 Analyst agent is reasoning..."):
            result = run_analysis(query)

        st.success("Analysis complete")

        st.markdown("### 🔍 Summary")
        st.write(result["summary"])

        st.markdown("### 📊 Evidence (RRF Scored)")
        st.json(result["evidence"])
