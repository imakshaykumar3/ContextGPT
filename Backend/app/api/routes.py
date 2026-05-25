from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form
)

from pydantic import BaseModel

import os
import json

from app.services.pipeline import run_pipeline

from app.db.database import SessionLocal
from app.db.models import Meeting


router = APIRouter()


# =========================
# Request Schema
# =========================
class ProcessRequest(BaseModel):
    source: str
    language: str = "en"


# =========================
# Home Route
# =========================
@router.get("/")
def home():

    return {
        "message": "AI Meeting Assistant API Running"
    }


# =========================
# Process YouTube URL
# =========================
@router.post("/process-url")
def process_url(request: ProcessRequest):

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


# =========================
# Upload Local File
# =========================
@router.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    language: str = Form("en")
):

    try:

        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)

        # File size limit (60 MB)
        MAX_FILE_SIZE = 60 * 1024 * 1024

        # Read uploaded file
        contents = await file.read()

        # Validate file size
        if len(contents) > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=400,
                detail="File size exceeds 60 MB limit"
            )

        # Allowed file extensions
        allowed_extensions = [
            ".mp3",
            ".wav",
            ".mp4",
            ".m4a"
        ]

        # Validate extension
        ext = os.path.splitext(
            file.filename
        )[1].lower()

        if ext not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        # Save uploaded file
        file_path = f"uploads/{file.filename}"

        with open(file_path, "wb") as buffer:

            buffer.write(contents)

        # Run AI pipeline
        result = run_pipeline(
            file_path,
            language
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Get Stored Meeting
# =========================
@router.get("/meeting/{meeting_id}")
def get_meeting(meeting_id: int):

    db = SessionLocal()

    try:

        meeting = db.query(Meeting).filter(
            Meeting.id == meeting_id
        ).first()

        # Meeting not found
        if not meeting:

            raise HTTPException(
                status_code=404,
                detail="Meeting not found"
            )

        # Load transcript text
        with open(
            meeting.transcript_path,
            "r",
            encoding="utf-8"
        ) as f:

            transcript_text = f.read()

        # Load summary JSON
        with open(
            meeting.summary_path,
            "r",
            encoding="utf-8"
        ) as f:

            summary_data = json.load(f)

        # Return final response
        return {
            "id": meeting.id,

            "title": meeting.title,

            "source": meeting.source,

            "language": meeting.language,

            "transcript": transcript_text,

            "summary": summary_data["summary"],

            "action_items": summary_data["action_items"],

            "key_decisions": summary_data["key_decisions"],

            "open_questions": summary_data["open_questions"],

            "created_at": meeting.created_at
        }

    finally:

        db.close()