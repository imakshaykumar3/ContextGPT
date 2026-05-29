import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.db.init_db import init_db


# =========================
# Logging Configuration
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

logger = logging.getLogger(__name__)


# =========================
# Application Lifespan
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        logger.info("Starting application")

        await init_db()

        logger.info("Database initialized")

        yield

    except Exception as e:

        logger.error(
            f"Application startup failed: {e}"
        )
        raise

    finally:

        logger.info(
            "Application shutdown"
        )


# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="AI Meeting Assistant",
    description="Enterprise AI Meeting Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,

    # Replace with frontend URL in production
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Root Endpoint
# =========================
@app.get("/", tags=["System"])
async def root():

    return {
        "message": "AI Meeting Assistant API",
        "status": "running"
    }


# =========================
# Routers
# =========================
app.include_router(
    auth_router,
    prefix="/api"
)

app.include_router(
    router,
    prefix="/api"
)