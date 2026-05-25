from app.db.database import SessionLocal
from app.db.models import Meeting


def save_meeting(data):

    db = SessionLocal()

    meeting = Meeting(
        title=data["title"],
        source=data["source"],
        language=data["language"],
        transcript=data["transcript"],
        summary=data["summary"],
        action_items=data["action_items"],
        key_decisions=data["key_decisions"],
        open_questions=data["open_questions"]
    )

    db.add(meeting)

    db.commit()

    db.refresh(meeting)

    db.close()

    return meeting.id