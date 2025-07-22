# utils/resume_scorer.py

def calculate_resume_score(text, extracted_skills, required_skills=None):
    score = 0
    total_weight = 100

    # Default required skills
    if required_skills is None:
        required_skills = [
    # Core Data & AI
    "python", "sql", "excel", "power bi", "tableau", "data analysis", "data visualization",
    "machine learning", "deep learning", "nlp", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",

    # Generative AI & Prompting
    "chatgpt", "prompt engineering", "langchain", "llm", "huggingface",

    # Web & App Dev
    "html", "css", "javascript", "react", "node.js", "firebase", "express", "mongodb",

    # DevOps & Cloud
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "ci/cd", "linux",

    # Databases & ETL
    "mysql", "postgresql", "mongodb", "nosql", "etl", "airflow", "spark", "hadoop",

    # UI/UX & Product
    "figma", "adobe xd", "prototyping", "wireframes", "user testing", "ui design", "product management",

    # Mobile & Game Dev
    "flutter", "android", "ios", "unity", "c#", "game development",

    # Cybersecurity
    "network security", "kali linux", "vulnerability assessment", "penetration testing",

    # Soft Skills & Practices
    "agile", "jira", "scrum", "problem solving", "communication", "stakeholder management"
]


    # Skill Match Score (60%)
    matched = [skill for skill in extracted_skills if skill in required_skills]
    skill_score = (len(matched) / len(required_skills)) * 60

    # Formatting Score (20%)
    formatting_score = 0
    if "education" in text.lower(): formatting_score += 5
    if "experience" in text.lower(): formatting_score += 5
    if "skills" in text.lower(): formatting_score += 5
    if "projects" in text.lower(): formatting_score += 5

    # Keyword Score (20%)
    keywords = ["data", "analysis", "insight", "model", "visualization"]
    found_keywords = [kw for kw in keywords if kw in text.lower()]
    keyword_score = (len(found_keywords) / len(keywords)) * 20

    # Final score
    score = skill_score + formatting_score + keyword_score
    return round(score, 2), matched, found_keywords
