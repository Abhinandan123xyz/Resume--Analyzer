from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an expert HR consultant and resume coach. Analyze the resume below against the job description and return a JSON object with EXACTLY this structure:

{{
  "score": <integer 0-100>,
  "jd_match_percent": <integer 0-100>,
  "strengths": [<list of 3-5 specific strengths as strings>],
  "weaknesses": [<list of 3-5 specific weaknesses as strings>],
  "missing_skills": [<list of skills/keywords present in JD but missing from resume>],
  "suggestions": [<list of 3-5 actionable improvement suggestions>],
  "summary": "<2-3 sentence overall assessment>"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY the JSON object. No explanation, no markdown, no extra text.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)