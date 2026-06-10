import streamlit as st
from extractor import extract_text_from_pdf
from analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("AI Resume Analyzer")
st.caption("Upload your resume and a job description to get an AI-powered analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume")
    input_method = st.radio("Input method", ["Upload PDF", "Paste text"], horizontal=True)
    
    resume_text = ""
    if input_method == "Upload PDF":
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file:
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                st.success("PDF extracted successfully!")
                with st.expander("Preview extracted text"):
                    st.text(resume_text[:1000] + "...")
            except Exception as e:
                st.error(f"Could not read PDF: {e}. Try pasting text instead.")
    else:
        resume_text = st.text_area(
            "Paste your resume text here",
            height=300,
            placeholder="Paste your full resume here..."
        )

with col2:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste the full job description you're applying for..."
    )

st.divider()

if st.button("Analyze Resume", type="primary", disabled=not (resume_text and job_description)):
    with st.spinner("Analyzing your resume with AI..."):
        try:
            result = analyze_resume(resume_text, job_description)

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Resume Score", f"{result['score']}/100")
                st.progress(result['score'] / 100)
            with c2:
                st.metric("JD Match", f"{result['jd_match_percent']}%")
                st.progress(result['jd_match_percent'] / 100)

            st.subheader("Overall Summary")
            st.info(result["summary"])

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Strengths")
                for s in result["strengths"]:
                    st.success(f"✓ {s}")
                st.subheader("Missing Skills / Keywords")
                for skill in result["missing_skills"]:
                    st.error(f"✗ {skill}")
            with col_b:
                st.subheader("Weaknesses")
                for w in result["weaknesses"]:
                    st.warning(f"⚠ {w}")
                st.subheader("Suggestions to Improve")
                for i, tip in enumerate(result["suggestions"], 1):
                    st.write(f"{i}. {tip}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")