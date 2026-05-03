import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session
from backend.db.models import UserProfile
from backend.rag.retriever import get_career_context

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

COACH_PROMPT = """
You are Clairo, an expert AI skill coach for IT professionals.

User Profile:
- Name: {full_name}
- Current Skills: {skills}
- Experience: {experience}
- Summary: {summary}

Relevant Knowledge:
{context}

User's Question: {question}

Analyze the user's current skill set and provide:
1. Skill gaps based on their target role or question
2. Priority order of skills to learn (High / Medium / Low)
3. Best resources for each skill (free + paid)
4. Realistic weekly learning plan (hours per week)
5. Milestone checkpoints to measure progress

Be specific, practical, and motivating.
"""

async def run_coach_agent(user_id: int, question: str, db: Session) -> str:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        return "Please upload your resume first so I can analyze your skill gaps."

    query = f"{question} {' '.join(profile.skills or [])}"
    context = get_career_context(query)

    prompt = COACH_PROMPT.format(
        full_name=profile.full_name or "Professional",
        skills=", ".join(profile.skills or []),
        experience=str(profile.experience or []),
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