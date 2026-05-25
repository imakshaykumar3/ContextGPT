from app.db.database import SessionLocal
from app.db.models import Meeting


def create_meeting(source, language, title):

    db = SessionLocal()

    meeting = Meeting(
        source=source,
        language=language,
        title=title
    )

    db.add(meeting)

    db.commit()

    db.refresh(meeting)

    db.close()

    return meeting.id


def update_meeting_files(
    meeting_id,
    transcript_path,
    summary_path
):

    db = SessionLocal()

    meeting = db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()

    meeting.transcript_path = transcript_path
    meeting.summary_path = summary_path

    db.commit()

    db.close()