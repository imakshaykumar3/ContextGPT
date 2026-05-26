# app/services/db_service.py
import logging

from app.db.database import (
    SessionLocal
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
def create_meeting(
    source,
    language,
    title,
    file_type=None
):

    db = SessionLocal()

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

        db.commit()

        db.refresh(meeting)

        logger.info(
            f"Meeting created: "
            f"{meeting.id}"
        )

        return meeting.id

    except Exception as e:

        db.rollback()

        logger.error(
            f"Meeting creation failed: {e}"
        )

        raise Exception(
            f"DB Error: {e}"
        )

    finally:

        db.close()


# =========================
# Update Meeting Files
# =========================
def update_meeting_files(

    meeting_id,

    transcript_path,

    summary_path,

    vector_store_path=None
):

    db = SessionLocal()

    try:

        logger.info(
            f"Updating meeting files "
            f"for {meeting_id}"
        )

        meeting = db.query(
            Meeting
        ).filter(
            Meeting.id == meeting_id
        ).first()

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

        db.commit()

        logger.info(
            "Meeting files updated"
        )

    except Exception as e:

        db.rollback()

        logger.error(
            f"Update failed: {e}"
        )

        raise Exception(
            f"DB Update Error: {e}"
        )

    finally:

        db.close()


# =========================
# Mark Meeting Failed
# =========================
def mark_meeting_failed(
    meeting_id,
    error_message
):

    db = SessionLocal()

    try:

        logger.info(
            f"Marking meeting "
            f"{meeting_id} failed"
        )

        meeting = db.query(
            Meeting
        ).filter(
            Meeting.id == meeting_id
        ).first()

        if not meeting:

            return

        meeting.status = "failed"

        meeting.error_message = (
            str(error_message)
        )

        db.commit()

        logger.info(
            "Meeting marked failed"
        )

    except Exception as e:

        db.rollback()

        logger.error(
            f"Failed status update failed: {e}"
        )

    finally:

        db.close()