# utils/keyword_extractor.py

import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Define skill keywords (you can expand this list)
SKILL_KEYWORDS = [
    "python", "sql", "excel", "power bi", "tableau", "pandas",
    "numpy", "matplotlib", "seaborn", "scikit-learn",
    "nlp", "machine learning", "deep learning",
    "chatgpt", "prompt engineering", "data analysis", "data visualization"
]

def extract_skills(text):
    text = text.lower()
    doc = nlp(text)
    
    found_skills = set()
    for token in doc:
        for skill in SKILL_KEYWORDS:
            if skill in token.text:
                found_skills.add(skill)

    return list(found_skills)
