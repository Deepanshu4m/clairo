from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.db.models import get_db, ChatHistory
from backend.auth.auth import get_current_user
from backend.agents.advisor import advisor_graph
from backend.agents.career_path import run_career_path_agent
from backend.agents.coach import run_coach_agent
from backend.agents.mock_interview import run_mock_interview_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db.add(ChatHistory(user_id=current_user.id, role="user", content=req.message))
    db.commit()

    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id)
        .order_by(ChatHistory.created_at.desc())
        .limit(20)
        .all()
    )
    messages = [{"role": h.role, "content": h.content} for h in reversed(history)]

    state = {
        "user_id": current_user.id,
        "messages": messages,
        "intent": "",
        "response": "",
    }

    result = advisor_graph.invoke(state)
    intent = result["intent"]
    response = result["response"]

    jobs = []
    if intent == "career_path":
        result_data = await run_career_path_agent(current_user.id, req.message, db)
        response = result_data["response"]
        jobs = result_data["jobs"]
    elif intent == "coach":
        response = await run_coach_agent(current_user.id, req.message, db)
    elif intent == "mock_interview":
        response = await run_mock_interview_agent(current_user.id, req.message, db)

    db.add(ChatHistory(user_id=current_user.id, role="assistant", content=response))
    db.commit()

    return {"response": response, "intent": intent, "jobs": jobs}

@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    history = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).order_by(ChatHistory.created_at).all()
    return [{"role": h.role, "content": h.content, "created_at": h.created_at} for h in history]

@router.delete("/history")
def clear_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Chat history cleared"}