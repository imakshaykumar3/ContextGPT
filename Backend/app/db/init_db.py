# app/db/init_db.py

import logging

from app.db.database import (
    engine
)

from app.db.models import (
    Base
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Initialize Database
# =========================
async def init_db():

    try:

        logger.info(
            "Creating database tables"
        )

        async with engine.begin() as conn:

            await conn.run_sync(
                Base.metadata.create_all
            )

        logger.info(
            "Database initialized successfully"
        )

    except Exception as e:

        logger.error(
            f"Database initialization failed: {e}"
        )

        raise Exception(
            f"DB Init Error: {e}"
        )


# =========================
# Run Directly
# =========================
if __name__ == "__main__":

    import asyncio

    asyncio.run(
        init_db()
    )