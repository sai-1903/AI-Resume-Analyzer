from utils.pdf_parser import extract_text_from_pdf
from utils.keyword_extractor import extract_skills
from utils.resume_scorer import calculate_resume_score  # ✅ New import
from utils.job_matcher import recommend_jobs
from utils.resume_feedback import get_resume_feedback

pdf_path = "data/sample_resumes/DS gen AI CV.pdf"
text = extract_text_from_pdf(pdf_path)

print("✅ Extracted Resume Text (First 500 characters):\n")
print(text[:500])

skills = extract_skills(text)
print("\n🔍 Extracted Skills from Resume:")
print(skills)

# Resume Scoring
score, matched_skills, found_keywords = calculate_resume_score(text, skills)

print(f"\n📊 Resume Score: {score} / 100")
print("✅ Matched Skills:", matched_skills)
print("🔍 Industry Keywords Found:", found_keywords)
# Job Role Recommendations
job_recommendations = recommend_jobs(skills)

print("\n🎯 Recommended Job Roles Based on Your Resume:")
for title, match in job_recommendations:
    print(f"• {title} — {match}% skill match")

from utils.resume_feedback import get_resume_feedback



from dotenv import load_dotenv
import os
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


get_resume_feedback(resume_text, TOGETHER_API_KEY)  


print("\n🧠 Resume Suggestions:\n", feedback)




