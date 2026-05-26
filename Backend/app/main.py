# app/main.py
import logging

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
    level=logging.INFO
)

logger = logging.getLogger(
    __name__
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

    version="1.0.0"
)


# =========================
# Enable CORS
# =========================
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================
# Startup Event
# =========================
@app.on_event("startup")
def startup_event():

    logger.info(
        "Starting application"
    )

    # Initialize database
    init_db()

    logger.info(
        "Application startup complete"
    )


# =========================
# Root Route
# =========================
@app.get("/")
def root():

    return {

        "message": (
            "AI Meeting Assistant API"
        ),

        "status": "running"
    }


# =========================
# Include API Routes
# =========================
app.include_router(

    router,

    prefix="/api",

    tags=["AI Meeting Assistant"]
)