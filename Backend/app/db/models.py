# app/db/models.py
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

    # =========================
    # Primary Key
    # =========================
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =========================
    # Meeting Metadata
    # =========================
    title = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        nullable=False
    )

    language = Column(
        String,
        nullable=False
    )

    file_type = Column(
        String
    )

    # =========================
    # File Storage
    # =========================
    transcript_path = Column(
        String
    )

    summary_path = Column(
        String
    )

    vector_store_path = Column(
        String
    )

    # =========================
    # Processing State
    # =========================
    status = Column(
        String,
        default="processing"
    )

    error_message = Column(
        String
    )

    # =========================
    # Timestamps
    # =========================
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )