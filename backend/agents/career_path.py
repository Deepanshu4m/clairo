import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session
from backend.db.models import UserProfile
from backend.rag.retriever import get_career_context

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

CAREER_PATH_PROMPT = """
You are Clairo, an expert AI career advisor for senior IT professionals.

User Profile:
- Name: {full_name}
- Skills: {skills}
- Experience: {experience}
- Education: {education}
- Summary: {summary}

Relevant Career Knowledge:
{context}

User's Question: {question}

Based on the user's profile and the career knowledge above, provide a detailed, personalized career path roadmap. Include:
1. Recommended next career role(s) based on their background
2. Key skills to develop (with priority order)
3. Estimated timeline (e.g. 3-6 months, 6-12 months)
4. Concrete action steps (courses, projects, certifications)
5. Potential challenges and how to overcome them

Be specific, actionable, and encouraging.
"""

async def run_career_path_agent(user_id: int, question: str, db: Session) -> str:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        return "Please upload your resume first so I can give you a personalized career roadmap."

    query = f"{question} {' '.join(profile.skills or [])} {' '.join([e.get('role','') for e in (profile.experience or [])])}"
    context = get_career_context(query)

    prompt = CAREER_PATH_PROMPT.format(
        full_name=profile.full_name or "Professional",
        skills=", ".join(profile.skills or []),
        experience=str(profile.experience or []),
        education=str(profile.education or []),
        summary=profile.summary or "Not provided",
        context=context,
        question=question,
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.4,
    )

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content