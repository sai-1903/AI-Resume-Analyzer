import streamlit as st
import pdfplumber
import spacy
import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load Together.ai API key
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
st.write("🔐 API Key Loaded Successfully" if TOGETHER_API_KEY else "❌ API Key Not Found")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load job roles from CSV
@st.cache_data(show_spinner=False)
def load_job_data():
    df = pd.read_csv("data/job_roles_with_skills.csv")
    job_dict = {row['job_title']: row['required_skills'].split(', ') for _, row in df.iterrows()}
    return df, job_dict

job_df, job_roles = load_job_data()

# Sidebar to show all roles & skills
st.sidebar.title("📘 Explore Job Roles & Required Skills")
with st.sidebar.expander("💼 View All Job Roles"):
    for role, skills in job_roles.items():
        st.markdown(f"**{role}**")
        st.markdown(", ".join(skills))
        st.markdown("---")

# Combine all skills from all roles
skill_keywords = set(kw.strip().lower() for skills in job_roles.values() for kw in skills)

# PDF text extraction
def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            if not text.strip():
                st.warning("⚠️ No readable text found in this PDF. Try uploading another one.")
            return text
    except Exception as e:
        st.error(f"❌ Failed to read PDF: {e}")
        return ""

# Extract skills from resume text
def extract_skills(text):
    text = text.lower()
    return [skill for skill in skill_keywords if skill in text]

# Resume scoring
def calculate_resume_score(extracted_skills, required_skills):
    matched = set(extracted_skills) & set(required_skills)
    score = (len(matched) / len(required_skills)) * 100 if required_skills else 0
    return round(score, 2), list(matched)

# Get AI resume feedback
def get_resume_feedback(resume_text, api_key):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": f"You're a professional resume reviewer. The applicant is applying for a specific job role. Give feedback based on this resume:\n\n{resume_text[:3000]}"
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        st.write("📦 API Status:", response.status_code)
        st.write("📝 Response Preview:", response.text[:300])
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"❌ API error: {e}")
        return "No response."

# Set page
st.set_page_config(page_title="Resume Analyzer and Job Recommendation", layout="centered")
st.title("📄 Resume Analyzer")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file and TOGETHER_API_KEY:
    with st.spinner("📤 Extracting resume text..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        st.write("📄 Extracted text length:", len(resume_text))

    if resume_text.strip() == "":
        st.warning("⚠️ This resume doesn't contain readable text. Please try a different file.")
    else:
        # Preview resume
        st.subheader("📄 Resume Preview")
        st.text_area("Extracted Text", resume_text[:2000], height=200)

        # Extract skills
        skills = extract_skills(resume_text)
        st.subheader("🧠 Skills Found")
        st.write(skills if skills else "No known skills found.")
        # 🔍 Suggest Top 3 Job Roles Based on Skills
        top_matches = []
        for role, required in job_roles.items():
            match = len(set(skills) & set(required)) / len(required)
            top_matches.append((role, round(match * 100, 2)))
        top_matches = sorted(top_matches, key=lambda x: x[1], reverse=True)[:3]

        st.subheader("🔍 Top Job Roles Based on Your Skills")
        for role, score in top_matches:
            st.write(f"• {role} — {score}% match")

        st.subheader("🧪 DEBUG: Check Job Roles from CSV")
        st.write("Job roles loaded:", len(job_roles))
        st.write(sorted(job_roles.keys()))


        # 🔽 INSERT DROPDOWN HERE
        st.subheader("🎯 Select Your Target Job Role")
        target_job = st.selectbox(
            "Which role are you applying for?",
             options=sorted(job_roles.keys()),
             index=0,
             placeholder="Choose your job role..."
        )


        # Score resume for selected job
        required_skills = job_roles.get(target_job, [])
        score, matched_skills = calculate_resume_score(skills, required_skills)

        st.subheader("📊 Resume Match Score")
        st.metric(label=f"Match with '{target_job}'", value=f"{score} / 100")
        st.write("✅ Skills Matched:", matched_skills)

        # 🔽 Paste Missing Skills Block RIGHT HERE
        missing_skills = list(set(required_skills) - set(skills))
        st.subheader("❌ Missing Skills for This Role")
        st.write(missing_skills if missing_skills else "🎉 No missing skills!")

        # LLM feedback
        if st.button("💬 Get AI Feedback"):
            with st.spinner("🤖 Talking to Together.ai..."):
                feedback = get_resume_feedback(resume_text, TOGETHER_API_KEY)
                st.subheader("✅ Resume Suggestions")
                st.markdown(feedback)

else:
    st.info("📥 Please upload a PDF resume to begin.")
