# app/config/settings.py

import os
import torch

from dotenv import load_dotenv


# =========================
# Load Environment Variables
# =========================
load_dotenv()


# =========================
# Environment
# =========================
ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)

DEBUG = (
    ENVIRONMENT == "development"
)


# =========================
# OpenAI
# =========================
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

if not OPENAI_API_KEY:

    raise ValueError(
        "OPENAI_API_KEY is missing"
    )


GPT_MODEL = os.getenv(
    "GPT_MODEL",
    "gpt-4o-mini"
)


# =========================
# Embedding Model
# =========================
EMBEDDING_MODEL = os.getenv(

    "EMBEDDING_MODEL",

    "BAAI/bge-small-en-v1.5"
)


# =========================
# Vector Database
# =========================
CHROMA_DIR = os.getenv(
    "CHROMA_DIR",
    "vector_db"
)


# =========================
# Storage Directories
# =========================
UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR",
    "uploads"
)

TRANSCRIPTS_DIR = os.getenv(
    "TRANSCRIPTS_DIR",
    "transcripts"
)

SUMMARIES_DIR = os.getenv(
    "SUMMARIES_DIR",
    "summaries"
)

DOWNLOAD_DIR = os.getenv(
    "DOWNLOAD_DIR",
    "downloads"
)

CHUNK_DIR = os.getenv(
    "CHUNK_DIR",
    "chunks"
)


# =========================
# File Upload Limits
# =========================
MAX_FILE_SIZE = int(
    os.getenv(
        "MAX_FILE_SIZE",
        60 * 1024 * 1024
    )
)


# =========================
# Supported Upload Formats
# =========================
ALLOWED_EXTENSIONS = [

    ".mp3",

    ".wav",

    ".mp4",

    ".m4a"
]


# =========================
# Audio Processing
# =========================
CHUNK_MINUTES = int(
    os.getenv(
        "CHUNK_MINUTES",
        10
    )
)

AUDIO_SAMPLE_RATE = int(
    os.getenv(
        "AUDIO_SAMPLE_RATE",
        16000
    )
)

AUDIO_CHANNELS = int(
    os.getenv(
        "AUDIO_CHANNELS",
        1
    )
)

YOUTUBE_AUDIO_QUALITY = os.getenv(
    "YOUTUBE_AUDIO_QUALITY",
    "192"
)


# =========================
# Whisper Settings
# =========================
WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "small"
)

WHISPER_DEVICE = (

    "cuda"

    if torch.cuda.is_available()

    else "cpu"
)

WHISPER_COMPUTE_TYPE = os.getenv(

    "WHISPER_COMPUTE_TYPE",

    "float16"
    if WHISPER_DEVICE == "cuda"
    else "int8"
)

WHISPER_BEAM_SIZE = int(
    os.getenv(
        "WHISPER_BEAM_SIZE",
        1
    )
)

WHISPER_VAD_FILTER = (
    os.getenv(
        "WHISPER_VAD_FILTER",
        "true"
    ).lower() == "true"
)


# =========================
# Text Chunking
# =========================
CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        2500
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        500
    )
)


# =========================
# Summarization
# =========================
SUMMARY_CHUNK_SIZE = int(
    os.getenv(
        "SUMMARY_CHUNK_SIZE",
        3000
    )
)

SUMMARY_CHUNK_OVERLAP = int(
    os.getenv(
        "SUMMARY_CHUNK_OVERLAP",
        300
    )
)


# =========================
# Retrieval Settings
# =========================
RETRIEVAL_K = int(
    os.getenv(
        "RETRIEVAL_K",
        10
    )
)

RETRIEVAL_FETCH_K = int(
    os.getenv(
        "RETRIEVAL_FETCH_K",
        40
    )
)

RETRIEVAL_SEARCH_TYPE = os.getenv(
    "RETRIEVAL_SEARCH_TYPE",
    "mmr"
)


# =========================
# Database
# =========================
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not DATABASE_URL:

    raise ValueError(
        "DATABASE_URL is missing"
    )


# =========================
# Async DB Pool
# =========================
DB_POOL_SIZE = int(
    os.getenv(
        "DB_POOL_SIZE",
        5
    )
)

DB_MAX_OVERFLOW = int(
    os.getenv(
        "DB_MAX_OVERFLOW",
        10
    )
)

DB_POOL_RECYCLE = int(
    os.getenv(
        "DB_POOL_RECYCLE",
        300
    )
)

DB_POOL_PRE_PING = (
    os.getenv(
        "DB_POOL_PRE_PING",
        "true"
    ).lower() == "true"
)

DB_ECHO = (
    os.getenv(
        "DB_ECHO",
        "false"
    ).lower() == "true"
)


# =========================
# OpenAI Timeouts
# =========================
OPENAI_REQUEST_TIMEOUT = int(
    os.getenv(
        "OPENAI_REQUEST_TIMEOUT",
        120
    )
)


# =========================
# Ensure Directories Exist
# =========================
for directory in [

    UPLOAD_DIR,

    TRANSCRIPTS_DIR,

    SUMMARIES_DIR,

    DOWNLOAD_DIR,

    CHUNK_DIR,

    CHROMA_DIR
]:

    os.makedirs(
        directory,
        exist_ok=True
    )