# app/db/models.py

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from sqlalchemy.sql import func

from app.db.database import Base


# =========================
# User Model
# =========================
class User(Base):

    __tablename__ = "users"

    # -------------------------
    # Primary Key
    # -------------------------
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -------------------------
    # User Info
    # -------------------------
    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    # -------------------------
    # Timestamp
    # -------------------------
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # -------------------------
    # Relationship
    # -------------------------
    meetings = relationship(
        "Meeting",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================
# Meeting Model
# =========================
class Meeting(Base):

    __tablename__ = "meetings"

    # -------------------------
    # Primary Key
    # -------------------------
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -------------------------
    # User Ownership
    # -------------------------
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    # -------------------------
    # Meeting Metadata
    # -------------------------
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

    # -------------------------
    # File Storage
    # -------------------------
    transcript_path = Column(
        String
    )

    summary_path = Column(
        String
    )

    vector_store_path = Column(
        String
    )

    # -------------------------
    # Processing State
    # -------------------------
    status = Column(
        String,
        default="processing",
        index=True
    )

    error_message = Column(
        Text
    )

    # -------------------------
    # Timestamps
    # -------------------------
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # -------------------------
    # Relationship
    # -------------------------
    user = relationship(
        "User",
        back_populates="meetings"
    )