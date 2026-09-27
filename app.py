import os
import re
import json
import streamlit as st
from pathlib import Path

from resume_parser import extract_text
from analyzer import analyze_resume, calculate_keyword_match

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.caption("Analyze a resume against a job description using AI-assisted skills and keyword analysis.")

with st.sidebar:
    st.header("⚙️ Settings")
    api_provider = st.selectbox("AI Provider", ["Groq", "Local/Rule-based"])
    st.info("For Groq, add GROQ_API_KEY to your .env file. The rule-based mode works without an API key.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    resume_file = st.file_uploader("PDF or DOCX", type=["pdf", "docx"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=250,
        placeholder="Example: We are looking for a Python developer with Pandas, SQL, Git, APIs..."
    )

if resume_file:
    try:
        resume_text = extract_text(resume_file)
        st.success(f"Resume loaded: {resume_file.name}")
        with st.expander("View extracted resume text"):
            st.text(resume_text[:12000])
    except Exception as e:
        st.error(f"Could not read the resume: {e}")
        resume_text = ""
else:
    resume_text = ""

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if not resume_text:
        st.warning("Please upload a PDF or DOCX resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste a job description.")
        st.stop()

    with st.spinner("Analyzing resume..."):
        result = analyze_resume(
            resume_text,
            job_description,
            use_ai=(api_provider == "Groq")
        )

    st.divider()
    st.subheader("📊 Analysis")

    c1, c2, c3 = st.columns(3)
    c1.metric("Keyword Match", f"{result['match_score']}%")
    c2.metric("Matched Skills", len(result["matched_skills"]))
    c3.metric("Missing Skills", len(result["missing_skills"]))

    tab1, tab2, tab3, tab4 = st.tabs(
        ["✅ Matched Skills", "⚠️ Missing Skills", "🧠 AI Suggestions", "📋 Summary"]
    )

    with tab1:
        if result["matched_skills"]:
            st.write(", ".join(result["matched_skills"]))
        else:
            st.info("No strong matching skills detected.")

    with tab2:
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.success("No major missing skills detected from the extracted skill list.")

    with tab3:
        for item in result["suggestions"]:
            st.write(f"• {item}")

    with tab4:
        st.write(result["summary"])

    report = json.dumps(result, indent=2, ensure_ascii=False)
    st.download_button(
        "⬇️ Download Analysis JSON",
        data=report,
        file_name="resume_analysis.json",
        mime="application/json"
    )
