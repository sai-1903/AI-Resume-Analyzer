# utils/job_matcher.py

import pandas as pd

def recommend_jobs(skills, job_data_path="data/job_roles_with_skills.csv"):
    skills = [s.lower() for s in skills]
    
    df = pd.read_csv(job_data_path)
    recommendations = []

    for index, row in df.iterrows():
        job_skills = row['required_skills'].lower().split(',')
        match_count = len(set(skills) & set(job_skills))
        match_score = match_count / len(job_skills)

        if match_score >= 0.4:  # at least 40% skill match
            recommendations.append((row['job_title'], round(match_score * 100, 2)))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:3]  # top 3 job matches
