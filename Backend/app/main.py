# app/main.py

import logging

from contextlib import (
    asynccontextmanager
)

from fastapi import (
    FastAPI
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.api.routes import (
    router
)

from app.db.init_db import (
    init_db
)


# =========================
# Configure Logging
# =========================
logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(
    __name__
)


# =========================
# Lifespan Handler
# =========================
@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    try:

        logger.info(
            "Starting application"
        )

        # Initialize database
        await init_db()

        logger.info(
            "Database initialized"
        )

        logger.info(
            "Application startup complete"
        )

        yield

    except Exception as e:

        logger.error(
            f"Startup failed: {e}"
        )

        raise

    finally:

        logger.info(
            "Application shutdown"
        )


# =========================
# Create FastAPI App
# =========================
app = FastAPI(

    title="AI Meeting Assistant",

    description=(
        "Enterprise AI Meeting "
        "Intelligence Platform"
    ),

    version="1.0.0",

    lifespan=lifespan
)


# =========================
# Enable CORS
# =========================
app.add_middleware(

    CORSMiddleware,

    # WARNING:
    # Replace "*" in production
    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================
# Root Route
# =========================
@app.get("/")
async def root():

    return {

        "message":
            "AI Meeting Assistant API",

        "status":
            "running"
    }


# =========================
# Include API Routes
# =========================
app.include_router(

    router,

    prefix="/api",

    tags=[
        "AI Meeting Assistant"
    ]
)