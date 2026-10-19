import streamlit as st
from lead_analyzer import analyze_inquiry
from ml_model import predict_readiness
from database import save_analysis, list_analyses, init_db

st.set_page_config(page_title="LeadIQ | Cynbit AI Opportunity PoC", page_icon="🔎", layout="wide")
st.title("LeadIQ")
st.caption("AI-powered project inquiry intelligence • Assessment proof of concept")
st.info("Use synthetic/demo inquiries only. The readiness model is trained on small synthetic examples and is not a production lead-conversion model.")

with st.sidebar:
    st.header("Project overview")
    st.write("1. Extract inquiry details with an LLM or transparent offline fallback.")
    st.write("2. Predict readiness with a small ML baseline.")
    st.write("3. Explain missing information and suggest a next action.")
    st.write("4. Persist analysis records in SQLite by default, or MySQL when configured.")
    st.caption("LLM mode uses configured deployment secrets; without them, the clearly labelled rule-based fallback is used.")

message = st.text_area(
    "Customer project inquiry",
    height=150,
    placeholder="Example: We need an AI chatbot integrated with our website and CRM. Budget is ₹2 lakh and we'd like to launch within 4 weeks."
)
if st.button("Analyze inquiry", type="primary"):
    try:
        analysis, mode = analyze_inquiry(message)
        readiness = predict_readiness(analysis)
        st.session_state["last_result"] = (message, analysis, readiness, mode)
    except Exception as exc:
        st.error(str(exc))

if "last_result" in st.session_state:
    message, analysis, readiness, mode = st.session_state["last_result"]
    a, b, c = st.columns(3)
    a.metric("Service category", analysis.service_category)
    b.metric("Lead readiness", readiness["readiness"])
    c.metric("Urgency", analysis.urgency)
    st.caption(f"Extraction mode: {mode}")
    left, right = st.columns(2)
    with left:
        st.subheader("Extracted requirements")
        st.write(analysis.requirements or ["No explicit requirements extracted"])
        st.write("**Budget:**", analysis.budget or "Not provided")
        st.write("**Timeline:**", analysis.timeline or "Not provided")
        st.write("**Summary:**", analysis.summary)
    with right:
        st.subheader("Missing information")
        st.write(analysis.missing_information or ["No missing fields detected by current rules"])
        st.subheader("Recommended next step")
        st.write("Ask for clarification" if readiness["readiness"] != "Ready for discovery" else "Offer a discovery call for human review")
        st.subheader("Draft reply")
        st.text_area("Review and edit before sending", value=analysis.reply_draft, height=120, key="reply")
    st.caption(readiness["note"])
    if st.button("Save analysis to database"):
        try:
            record_id = save_analysis(message, analysis, readiness)
            st.success(f"Saved analysis record #{record_id}.")
        except Exception as exc:
            st.error(f"Database save failed: {type(exc).__name__}: {exc}")

st.divider()
st.subheader("Recent saved analyses")
try:
    records = list_analyses(20)
    if records:
        st.dataframe(records, use_container_width=True, hide_index=True)
    else:
        st.caption("No saved records yet.")
except Exception as exc:
    st.warning(f"Database is not ready yet: {type(exc).__name__}. Check DATABASE_URL and database permissions.")
