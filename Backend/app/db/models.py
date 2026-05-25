from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.db.database import Base


class Meeting(Base):

    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    source = Column(String)

    language = Column(String)

    transcript = Column(Text)

    summary = Column(Text)

    action_items = Column(Text)

    key_decisions = Column(Text)

    open_questions = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )