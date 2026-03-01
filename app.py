import streamlit as st
import pdfplumber
import pandas as pd
import re

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="💼 Resume Ranking System",
    page_icon="💼",
    layout="wide"
)

# ------------------------------
# Professional Header
# ------------------------------
st.markdown("""
<div style='background-color:#4B79A1;padding:15px;border-radius:10px'>
    <h1 style='color:white;text-align:center;'>💼 Transparent Resume Ranking System</h1>
    <p style='color:white;text-align:center;font-size:16px;'>
        Upload your CV and get ranked instantly based on skills & experience!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------------------
# Optional: Instructions Box
# ------------------------------
with st.expander("📌 How it Works (Click to expand)"):
    st.markdown("""
1. Upload your resumes in PDF format.
2. System calculates **Skill Match (70%)** and **Experience (30%)**.
3. Missing skills are highlighted in **red**.
4. Download the ranked results as a **CSV file**.
5. Visual representation of skill match in a **bar chart**.
""")

# ------------------------------
# Dynamic Skills Input
# ------------------------------
skills_input = st.text_area(
    "Enter required skills (comma separated, optional, default skills shown):",
    value="python, sql, machine learning, data analysis, excel"
)
skills_list = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
required_skills = {skill: 10 for skill in skills_list}  # Equal weight

# ------------------------------
# File Upload Section (Stylish)
# ------------------------------
st.markdown("<h3 style='color:#4B79A1;'>📂 Upload Resumes</h3>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Drag & drop or browse your PDF resumes here 👇",
    type=["pdf"],
    accept_multiple_files=True
)

# ------------------------------
# Functions
# ------------------------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def calculate_skill_score(text):
    total_weight = sum(required_skills.values())
    matched_weight = 0
    matched_skills = []
    for skill, weight in required_skills.items():
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            matched_weight += weight
            matched_skills.append(skill)
    skill_percentage = (matched_weight / total_weight) * 100 if total_weight else 0
    return skill_percentage, matched_skills

def extract_experience(text):
    match = re.search(r'(\d+)\+?\s+years', text)
    return int(match.group(1)) if match else 0

def experience_score(years):
    return min(years, 5) / 5 * 100

def final_score(skill_pct, exp_score):
    return (0.7 * skill_pct) + (0.3 * exp_score)

def highlight_gap(val):
    if val:
        return 'color: red; font-weight:bold;'
    return ''

# ------------------------------
# Process Resumes
# ------------------------------
if uploaded_files:
    candidates = []
    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):
        text = extract_text(file)
        skill_pct, matched = calculate_skill_score(text)
        years = extract_experience(text)
        exp_score = experience_score(years)
        final = final_score(skill_pct, exp_score)
        gap = list(set(required_skills.keys()) - set(matched))

        candidates.append({
            "Name": file.name,
            "Skill Score (%)": round(skill_pct, 2),
            "Experience (Years)": years,
            "Final Score": round(final, 2),
            "Skill Gap": ", ".join(gap)
        })
        progress.progress((i+1)/len(uploaded_files))

    # Sort candidates
    candidates.sort(
        key=lambda x: (x["Final Score"], x["Skill Score (%)"], x["Experience (Years)"]),
        reverse=True
    )

    # DataFrame
    df = pd.DataFrame(candidates)

    # ------------------------------
    # Display Results in Two Columns
    # ------------------------------
    st.markdown("<h3 style='color:#4B79A1;'>🏆 Ranked Candidates</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        st.dataframe(df.style.applymap(highlight_gap, subset=['Skill Gap']), height=300)
    with col2:
        st.download_button(
            label="📥 Download Ranked CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='ranked_candidates.csv',
            mime='text/csv',
            use_container_width=True
        )

    # Skill Match Bar Chart
    st.markdown("<h3 style='color:#4B79A1;'>📊 Skill Match Chart</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Candidate": [c["Name"] for c in candidates],
        "Skill Match %": [c["Skill Score (%)"] for c in candidates]
    })
    st.bar_chart(chart_data.set_index("Candidate"))

else:
    st.info("Please upload at least one PDF resume to see results. 👆")