# app/db/database.py

import logging

from sqlalchemy.ext.asyncio import (

    create_async_engine,

    AsyncSession
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
# Async Database Engine
# =========================
logger.info(
    "Initializing async database engine"
)

engine = create_async_engine(

    DATABASE_URL,

    pool_size=DB_POOL_SIZE,

    max_overflow=DB_MAX_OVERFLOW,

    pool_pre_ping=DB_POOL_PRE_PING,

    pool_recycle=DB_POOL_RECYCLE,

    echo=DB_ECHO,

    future=True
)


# =========================
# Async Session Factory
# =========================
AsyncSessionLocal = sessionmaker(

    bind=engine,

    class_=AsyncSession,

    autoflush=False,

    autocommit=False,

    expire_on_commit=False
)


# =========================
# Base Model
# =========================
Base = declarative_base()


# =========================
# Dependency Injection
# =========================
async def get_db():

    async with AsyncSessionLocal() as db:

        try:

            yield db

        finally:

            await db.close()