#app/api/routes.py
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form,
    Depends
)

from sqlalchemy.orm import Session

from pydantic import BaseModel

import os
import json
import uuid
import logging

from app.services.pipeline import run_pipeline


from app.db.database import get_db
from app.db.models import Meeting

from app.rag.rag_engine import (
    ask_question
)

from app.config.settings import (
    UPLOAD_DIR,
    MAX_FILE_SIZE,
    ALLOWED_EXTENSIONS
)


# =========================
# Router
# =========================
router = APIRouter()


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Request Schemas
# =========================
class ProcessRequest(BaseModel):

    source: str

    language: str = "en"


class ChatRequest(BaseModel):

    question: str


# =========================
# Health Check
# =========================
@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


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
def process_url(
    request: ProcessRequest
):

    try:

        logger.info(
            "Processing YouTube URL"
        )

        result = run_pipeline(
            request.source,
            request.language
        )

        logger.info(
            "YouTube processing completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"URL processing failed: {e}"
        )

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

        logger.info(
            "Processing uploaded file"
        )

        # Create upload directory
        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        # Read uploaded file
        contents = await file.read()

        # Validate file size
        if len(contents) > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=400,
                detail=(
                    "File size exceeds "
                    "allowed limit"
                )
            )

        # Validate extension
        ext = os.path.splitext(
            file.filename
        )[1].lower()

        if ext not in ALLOWED_EXTENSIONS:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file format"
                )
            )

        # Generate unique filename
        unique_filename = (
            f"{uuid.uuid4()}{ext}"
        )

        # Save uploaded file
        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(contents)

        logger.info(
            f"File saved: {file_path}"
        )

        # Run AI pipeline
        result = run_pipeline(
            file_path,
            language
        )

        logger.info(
            "File processing completed"
        )

        return result

    except Exception as e:

        logger.error(
            f"File upload failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Get Stored Meeting
# =========================
@router.get("/meeting/{meeting_id}")
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db)
):

    try:

        logger.info(
            f"Fetching meeting {meeting_id}"
        )

        meeting = db.query(
            Meeting
        ).filter(
            Meeting.id == meeting_id
        ).first()

        # Meeting not found
        if not meeting:

            raise HTTPException(
                status_code=404,
                detail="Meeting not found"
            )

        # Load transcript
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

        logger.info(
            "Meeting fetched successfully"
        )

        # Return response
        return {

            "id": meeting.id,

            "title": meeting.title,

            "source": meeting.source,

            "language": meeting.language,

            "transcript": transcript_text,

            "segments": summary_data.get(
                "segments",
                []
            ),

            "summary": summary_data.get(
                "summary",
                {}
            ),

            "action_items": summary_data.get(
                "action_items",
                []
            ),

            "key_decisions": summary_data.get(
                "key_decisions",
                []
            ),

            "open_questions": summary_data.get(
                "open_questions",
                []
            ),

            "created_at": meeting.created_at
        }

    except Exception as e:

        logger.error(
            f"Get meeting failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# Chat With Meeting
# =========================
@router.post("/chat/{meeting_id}")
def chat_with_meeting(
    meeting_id: int,
    request: ChatRequest
):

    try:

        logger.info(
            f"Chat started for "
            f"meeting {meeting_id}"
        )

        result = ask_question(
            meeting_id,
            request.question
        )

        logger.info(
            "Chat response generated"
        )

        return {

            "meeting_id": meeting_id,

            "question": request.question,

            "rewritten_query": result.get(
                "rewritten_query",
                ""
            ),

            "answer": result.get(
                "answer",
                ""
            )
        }

    except Exception as e:

        logger.error(
            f"Chat failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )