
import streamlit as st
import pandas as pd

from utils import clean_text, extract_text, get_all_scores
from skills import extract_skills

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# ---------------------- CUSTOM CSS ----------------------

st.markdown("""
<style>

/* -------- Background -------- */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
}

/* -------- Title -------- */
.title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #22c55e, #4ade80);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* -------- Section Headers -------- */
h2, h3 {
    color: #e2e8f0;
    margin-top: 20px;
}

/* -------- Card Style -------- */
.card {
    padding: 18px;
    border-radius: 16px;
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.1);
    margin-bottom: 15px;
    transition: 0.3s ease;
}

.card:hover {
    transform: scale(1.01);
    border: 1px solid rgba(74, 222, 128, 0.3);
}

/* -------- Buttons -------- */
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #16a34a, #15803d);
}

/* -------- Input Boxes -------- */
textarea, .stTextInput>div>div>input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}

/* -------- File Uploader -------- */
[data-testid="stFileUploader"] {
    background-color: #020617;
    border-radius: 12px;
    border: 1px solid #334155;
    padding: 10px;
}

/* -------- Table -------- */
[data-testid="stDataFrame"] {
    background-color: #020617;
    border-radius: 10px;
}

/* -------- Metrics -------- */
[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.6);
    padding: 10px;
    border-radius: 12px;
}

/* -------- Progress Bar -------- */
.stProgress > div > div {
    background-color: #22c55e;
}

/* -------- Scrollbar -------- */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------- HEADER ----------------------
st.markdown('<p class="title">AI Resume Screener</p>', unsafe_allow_html=True)
st.write("Match resumes with job descriptions using NLP + TF-IDF + BERT")

# ---------------------- INPUT SECTION ----------------------
col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("Job Description", height=250)

with col2:
    uploaded_files = st.file_uploader(
        "Upload Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

# ---------------------- BUTTON ----------------------
if st.button("Analyze Resumes"):

    if not job_desc or not uploaded_files:
        st.warning("Please provide Job Description and upload resumes")
        st.stop()

    # ---------------------- INITIALIZE ----------------------
    resumes, names = [], []
    skills_list = []
    matched_list = []
    missing_list = []

    job_desc_clean = clean_text(job_desc)
    job_skills = extract_skills(job_desc_clean)

    # ---------------------- PROCESS FILES ----------------------
    for file in uploaded_files:
        text = extract_text(file)
        text_clean = clean_text(text)

        resumes.append(text_clean)
        names.append(file.name)

        resume_skills = extract_skills(text_clean)

        matched = list(set(job_skills).intersection(set(resume_skills)))
        missing = list(set(job_skills) - set(resume_skills))

        skills_list.append(", ".join(resume_skills) if resume_skills else "None")
        matched_list.append(", ".join(matched) if matched else "None")
        missing_list.append(", ".join(missing) if missing else "None")

    # Safety check
    if len(resumes) == 0:
        st.error("No resumes processed")
        st.stop()

    # ---------------------- SCORING ----------------------
    tfidf_scores, bert_scores, final_scores = get_all_scores(job_desc_clean, resumes)

    scores = [round(s * 100, 2) for s in final_scores]

    # ---------------------- RESULTS DATAFRAME ----------------------
    results = pd.DataFrame({
        "Resume": names,
        "Match (%)": scores,
        "Skills Found": skills_list,
        "Matched Skills": matched_list,
        "Missing Skills": missing_list
    })

    # ---------------------- MODEL COMPARISON ----------------------
    st.subheader("Model Comparison")

    comparison_df = pd.DataFrame({
        "Resume": names,
        "TF-IDF": [round(s * 100, 2) for s in tfidf_scores],
        "BERT": [round(s * 100, 2) for s in bert_scores],
        "Final Score": scores
    })

    st.dataframe(comparison_df, use_container_width=True)

    # ---------------------- SORT RESULTS ----------------------
    results = results.sort_values(by="Match (%)", ascending=False)

    # ---------------------- TOP CANDIDATE ----------------------
    st.markdown("##Top Candidate")
    top = results.iloc[0]

    st.success(f"Best Match: **{top['Resume']}** ({top['Match (%)']}%)")

    # ---------------------- RESULTS DISPLAY ----------------------
    st.markdown("## Candidate Rankings")

    for _, row in results.iterrows():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(row["Resume"])
                st.write(f"**Skills:** {row['Skills Found']}")
                st.write(f"**Matched Skills:** {row['Matched Skills']}")
                st.write(f"**Missing Skills:** {row['Missing Skills']}")

            with col2:
                st.metric(label="Match %", value=f"{row['Match (%)']}%")
                st.progress(int(row["Match (%)"]))

            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------- EVALUATION ----------------------
    st.subheader("Evaluation")

    avg_score = sum(scores) / len(scores)
    top_score = max(scores)

    st.write(f"Average Match Score: **{round(avg_score, 2)}%**")
    st.write(f"Top Score: **{top_score}%**")

    # ---------------------- JD SKILLS ----------------------
    st.markdown("## Required Skills (from JD)")
    if job_skills:
        st.info(", ".join(job_skills))
    else:
        st.warning("No skills detected from Job Description")

    # ---------------------- DOWNLOAD ----------------------
    csv = results.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇ Download Results",
        csv,
        "final_results.csv",
        "text/csv"
    )

