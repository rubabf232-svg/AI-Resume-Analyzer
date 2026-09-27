import os
import re
from dotenv import load_dotenv

load_dotenv()

SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql",
    "mysql", "postgresql", "mongodb", "pandas", "numpy", "scipy",
    "scikit-learn", "tensorflow", "pytorch", "machine learning",
    "deep learning", "artificial intelligence", "generative ai",
    "prompt engineering", "nlp", "llm", "streamlit", "fastapi",
    "flask", "django", "rest api", "git", "github", "docker",
    "linux", "cybersecurity", "networking", "wireshark", "splunk",
    "siem", "soc", "penetration testing", "ethical hacking",
    "cloud computing", "aws", "azure", "gcp", "html", "css",
    "react", "node.js", "excel", "power bi", "tableau"
]

def normalize(text):
    return re.sub(r"\s+", " ", text.lower())

def detect_skills(text):
    text = normalize(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)
    return sorted(set(found))

def calculate_keyword_match(resume_text, job_description):
    resume_skills = set(detect_skills(resume_text))
    job_skills = set(detect_skills(job_description))

    if not job_skills:
        return 0, [], []

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    score = round((len(matched) / len(job_skills)) * 100)
    return score, matched, missing

def rule_based_analysis(resume_text, job_description):
    score, matched, missing = calculate_keyword_match(resume_text, job_description)

    suggestions = []
    if missing:
        suggestions.append("Consider adding relevant missing skills only if you genuinely have them.")
    if score < 50:
        suggestions.append("Tailor the resume summary and project descriptions to the job requirements.")
    if "github" not in normalize(resume_text):
        suggestions.append("If you have relevant public projects, consider adding your GitHub profile.")
    if "project" not in normalize(resume_text):
        suggestions.append("Add 2–4 relevant projects with technologies and measurable outcomes.")
    suggestions.append("Keep claims truthful and avoid adding skills you cannot demonstrate.")

    summary = (
        f"The resume contains {len(matched)} skills that match the detected job requirements. "
        f"The keyword-based match is {score}%. This score is an aid, not a hiring prediction."
    )

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "summary": summary
    }

def ai_analysis(resume_text, job_description):
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return rule_based_analysis(resume_text, job_description)

    client = Groq(api_key=api_key)
    prompt = f"""
You are a resume analysis assistant.

Analyze the resume against the job description.
Do NOT invent experience or skills.

Return ONLY valid JSON with:
{{
  "match_score": integer from 0 to 100,
  "matched_skills": ["..."],
  "missing_skills": ["..."],
  "suggestions": ["..."],
  "summary": "..."
}}

Resume:
{resume_text[:14000]}

Job Description:
{job_description[:10000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a careful resume analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)

def analyze_resume(resume_text, job_description, use_ai=True):
    if use_ai:
        try:
            return ai_analysis(resume_text, job_description)
        except Exception:
            return rule_based_analysis(resume_text, job_description)
    return rule_based_analysis(resume_text, job_description)
