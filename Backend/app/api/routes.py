from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.pipeline import run_pipeline

from app.db.database import SessionLocal
from app.db.models import Meeting

router = APIRouter()


class ProcessRequest(BaseModel):
    source: str
    language: str = "english"


@router.get("/")
def home():

    return {
        "message": "AI Meeting Assistant API Running"
    }


@router.post("/process")
def process_video(request: ProcessRequest):

    try:

        result = run_pipeline(
            request.source,
            request.language
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/meeting/{meeting_id}")
def get_meeting(meeting_id: int):

    db = SessionLocal()

    try:

        meeting = db.query(Meeting).filter(
            Meeting.id == meeting_id
        ).first()

        if not meeting:

            raise HTTPException(
                status_code=404,
                detail="Meeting not found"
            )

        return {
            "id": meeting.id,
            "title": meeting.title,
            "source": meeting.source,
            "language": meeting.language,
            "summary": meeting.summary,
            "action_items": meeting.action_items,
            "key_decisions": meeting.key_decisions,
            "open_questions": meeting.open_questions,
            "created_at": meeting.created_at
        }

    finally:

        db.close()