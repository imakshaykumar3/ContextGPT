# app/api/routes.py

from fastapi import (

    APIRouter,

    HTTPException,

    UploadFile,

    File,

    Form,

    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from sqlalchemy import (
    select
)

from pydantic import BaseModel

import os
import uuid
import json
import logging
import asyncio
import aiofiles

from app.services.pipeline import (
    run_pipeline
)

from app.db.database import (
    get_db
)

from app.db.models import (
    Meeting
)

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
async def health():

    return {
        "status": "healthy"
    }


# =========================
# Home Route
# =========================
@router.get("/")
async def home():

    return {
        "message":
            "AI Meeting Assistant API Running"
    }


# =========================
# Process YouTube URL
# =========================
@router.post("/process-url")
async def process_url(
    request: ProcessRequest
):

    try:

        logger.info(
            "Processing YouTube URL"
        )

        # Run async pipeline
        result = await run_pipeline(

            request.source,

            request.language
        )

        logger.info(
            "YouTube processing completed"
        )

        return result

    except HTTPException:
        raise

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

        # Ensure upload directory exists
        os.makedirs(

            UPLOAD_DIR,

            exist_ok=True
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

        # Final save path
        file_path = os.path.join(

            UPLOAD_DIR,

            unique_filename
        )

        # =========================
        # Stream File Safely
        # =========================
        file_size = 0

        chunk_size = 1024 * 1024  # 1MB

        async with aiofiles.open(
            file_path,
            "wb"
        ) as buffer:

            while chunk := await file.read(
                chunk_size
            ):

                file_size += len(chunk)

                # Validate file size
                if file_size > MAX_FILE_SIZE:

                    await file.close()

                    raise HTTPException(

                        status_code=400,

                        detail=(
                            "File size exceeds "
                            "allowed limit"
                        )
                    )

                await buffer.write(chunk)

        logger.info(
            f"File saved: {file_path}"
        )

        # Close uploaded file
        await file.close()

        # =========================
        # Run AI Pipeline
        # =========================
        result = await run_pipeline(

            file_path,

            language
        )

        logger.info(
            "File processing completed"
        )

        return result

    except HTTPException:
        raise

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
async def get_meeting(

    meeting_id: int,

    db: AsyncSession = Depends(get_db)
):

    try:

        logger.info(
            f"Fetching meeting "
            f"{meeting_id}"
        )

        # =========================
        # Fetch Meeting
        # =========================
        result = await db.execute(

            select(Meeting).where(
                Meeting.id == meeting_id
            )
        )

        meeting = (
            result.scalar_one_or_none()
        )

        # Meeting not found
        if not meeting:

            raise HTTPException(

                status_code=404,

                detail="Meeting not found"
            )

        # =========================
        # Validate Files
        # =========================
        if not os.path.exists(
            meeting.transcript_path
        ):

            raise HTTPException(

                status_code=404,

                detail=(
                    "Transcript file missing"
                )
            )

        if not os.path.exists(
            meeting.summary_path
        ):

            raise HTTPException(

                status_code=404,

                detail=(
                    "Summary file missing"
                )
            )

        # =========================
        # Load Transcript
        # =========================
        async with aiofiles.open(

            meeting.transcript_path,

            "r",

            encoding="utf-8"
        ) as f:

            transcript_text = (
                await f.read()
            )

        # =========================
        # Load Summary JSON
        # =========================
        async with aiofiles.open(

            meeting.summary_path,

            "r",

            encoding="utf-8"
        ) as f:

            summary_content = (
                await f.read()
            )

            summary_data = json.loads(
                summary_content
            )

        logger.info(
            "Meeting fetched successfully"
        )

        return {

            "id":
                meeting.id,

            "title":
                meeting.title,

            "source":
                meeting.source,

            "language":
                meeting.language,

            "file_type":
                meeting.file_type,

            "status":
                meeting.status,

            "transcript":
                transcript_text,

            "segments":
                summary_data.get(
                    "segments",
                    []
                ),

            "summary":
                summary_data.get(
                    "summary",
                    {}
                ),

            "action_items":
                summary_data.get(
                    "action_items",
                    []
                ),

            "key_decisions":
                summary_data.get(
                    "key_decisions",
                    []
                ),

            "open_questions":
                summary_data.get(
                    "open_questions",
                    []
                ),

            "created_at":
                meeting.created_at,

            "updated_at":
                meeting.updated_at
        }

    except HTTPException:
        raise

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
async def chat_with_meeting(

    meeting_id: int,

    request: ChatRequest
):

    try:

        logger.info(
            f"Chat started for "
            f"meeting {meeting_id}"
        )

        # =========================
        # Ask RAG Question
        # =========================
        result = await ask_question(

            meeting_id,

            request.question
        )

        logger.info(
            "Chat response generated"
        )

        return {

            "meeting_id":
                meeting_id,

            "question":
                request.question,

            "rewritten_query":
                result.get(
                    "rewritten_query",
                    ""
                ),

            "answer":
                result.get(
                    "answer",
                    ""
                )
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.error(
            f"Chat failed: {e}"
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )