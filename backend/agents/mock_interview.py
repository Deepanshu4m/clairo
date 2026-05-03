import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session
from backend.db.models import UserProfile

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

MOCK_INTERVIEW_PROMPT = """
You are Clairo, an expert AI interview coach for IT professionals.

User Profile:
- Name: {full_name}
- Skills: {skills}
- Experience: {experience}
- Education: {education}
- Summary: {summary}

User's Question: {question}

Generate a mock interview session with:
1. 5 technical questions relevant to their skills and experience level
2. 2 behavioral questions (STAR format expected)
3. 1 system design question appropriate for their seniority
4. For each question, provide a strong sample answer based on their profile
5. Tips on what interviewers are actually looking for in each answer

Make it feel like a real interview at a top tech company.
"""

async def run_mock_interview_agent(user_id: int, question: str, db: Session) -> str:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        return "Please upload your resume first so I can generate personalized interview questions."

    prompt = MOCK_INTERVIEW_PROMPT.format(
        full_name=profile.full_name or "Professional",
        skills=", ".join(profile.skills or []),
        experience=str(profile.experience or []),
        education=str(profile.education or []),
        summary=profile.summary or "Not provided",
        question=question,
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.5,
    )

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content