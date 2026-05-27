# app/services/db_service.py

import logging

from sqlalchemy import (
    select
)

from app.db.database import (
    AsyncSessionLocal
)

from app.db.models import (
    Meeting
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Create Meeting
# =========================
async def create_meeting(

    source: str,

    language: str,

    title: str,

    file_type: str = None
) -> int:

    async with AsyncSessionLocal() as db:

        try:

            logger.info(
                "Creating meeting record"
            )

            meeting = Meeting(

                source=source,

                language=language,

                title=title,

                file_type=file_type,

                status="processing"
            )

            db.add(meeting)

            await db.commit()

            await db.refresh(meeting)

            logger.info(
                f"Meeting created: "
                f"{meeting.id}"
            )

            return meeting.id

        except Exception as e:

            await db.rollback()

            logger.error(
                f"Meeting creation failed: {e}"
            )

            raise Exception(
                f"DB Error: {e}"
            )


# =========================
# Update Meeting Files
# =========================
async def update_meeting_files(

    meeting_id: int,

    transcript_path: str,

    summary_path: str,

    vector_store_path: str = None
):

    async with AsyncSessionLocal() as db:

        try:

            logger.info(
                f"Updating meeting "
                f"{meeting_id}"
            )

            result = await db.execute(

                select(Meeting).where(
                    Meeting.id == meeting_id
                )
            )

            meeting = (
                result.scalar_one_or_none()
            )

            if not meeting:

                raise Exception(
                    "Meeting not found"
                )

            meeting.transcript_path = (
                transcript_path
            )

            meeting.summary_path = (
                summary_path
            )

            meeting.vector_store_path = (
                vector_store_path
            )

            meeting.status = "completed"

            await db.commit()

            logger.info(
                "Meeting updated successfully"
            )

        except Exception as e:

            await db.rollback()

            logger.error(
                f"Meeting update failed: {e}"
            )

            raise Exception(
                f"DB Update Error: {e}"
            )


# =========================
# Mark Meeting Failed
# =========================
async def mark_meeting_failed(

    meeting_id: int,

    error_message: str
):

    async with AsyncSessionLocal() as db:

        try:

            logger.info(
                f"Marking meeting "
                f"{meeting_id} failed"
            )

            result = await db.execute(

                select(Meeting).where(
                    Meeting.id == meeting_id
                )
            )

            meeting = (
                result.scalar_one_or_none()
            )

            if not meeting:

                logger.warning(
                    "Meeting not found"
                )

                return

            meeting.status = "failed"

            meeting.error_message = (
                str(error_message)
            )

            await db.commit()

            logger.info(
                "Meeting marked failed"
            )

        except Exception as e:

            await db.rollback()

            logger.error(
                f"Failed status update error: {e}"
            )