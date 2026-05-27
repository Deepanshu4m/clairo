from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.models import get_db, UserProfile
from backend.auth.auth import get_current_user
from backend.utils.pdf_parser import extract_text_from_pdf
from backend.agents.profile_agent import parse_resume

router = APIRouter()

@router.get("/")
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        return {"profile": None}
    return {
        "profile": {
            "full_name": profile.full_name,
            "summary": profile.summary,
            "skills": profile.skills,
            "experience": profile.experience,
            "education": profile.education,
        }
    }

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()

    raw_text = extract_text_from_pdf(file_bytes)
    if not raw_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    parsed = await parse_resume(raw_text)

    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.full_name = parsed.get("full_name")
        profile.skills = parsed.get("skills")
        profile.experience = parsed.get("experience")
        profile.education = parsed.get("education")
        profile.summary = parsed.get("summary")
        profile.raw_text = raw_text
    else:
        profile = UserProfile(
            user_id=current_user.id,
            full_name=parsed.get("full_name"),
            skills=parsed.get("skills"),
            experience=parsed.get("experience"),
            education=parsed.get("education"),
            summary=parsed.get("summary"),
            raw_text=raw_text,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)

    return {
        "message": "Resume uploaded and parsed successfully",
        "profile": {
            "full_name": profile.full_name,
            "summary": profile.summary,
            "skills": profile.skills,
            "experience": profile.experience,
            "education": profile.education,
        }
    }