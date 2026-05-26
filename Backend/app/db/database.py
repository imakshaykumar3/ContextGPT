# app/db/database.py
import logging

from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

from app.config.settings import (
    DATABASE_URL,
    DB_POOL_SIZE,
    DB_MAX_OVERFLOW,
    DB_POOL_RECYCLE,
    DB_POOL_PRE_PING,
    DB_ECHO
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Database Engine
# =========================
logger.info("Initializing database engine")

engine = create_engine(

    DATABASE_URL,

    pool_size=DB_POOL_SIZE,

    max_overflow=DB_MAX_OVERFLOW,

    pool_pre_ping=DB_POOL_PRE_PING,

    pool_recycle=DB_POOL_RECYCLE,

    echo=DB_ECHO,

    future=True
)


# =========================
# Session Factory
# =========================
SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)


# =========================
# Base Model
# =========================
Base = declarative_base()


# =========================
# Dependency Injection
# =========================
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()