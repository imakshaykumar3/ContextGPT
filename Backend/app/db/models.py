from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime

from app.db.database import Base


class Meeting(Base):

    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    source = Column(String)

    language = Column(String)

    transcript_path = Column(String)

    summary_path = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )