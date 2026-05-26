#app/config/settings.py
import os

from dotenv import load_dotenv


load_dotenv()


# =========================
# OpenAI
# =========================
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

GPT_MODEL = "gpt-4o-mini"


# =========================
# Embedding Model
# =========================
EMBEDDING_MODEL = (
    "BAAI/bge-small-en-v1.5"
)


# =========================
# Vector Database
# =========================
CHROMA_DIR = "vector_db"


# =========================
# Storage Directories
# =========================
UPLOAD_DIR = "uploads"

TRANSCRIPT_DIR = "transcripts"

SUMMARY_DIR = "summaries"

DOWNLOAD_DIR = "downloads"

# =========================
# Storage Paths
# =========================
TRANSCRIPTS_DIR = "transcripts"

SUMMARIES_DIR = "summaries"

VECTOR_DB_DIR = "vector_db"


# =========================
# File Upload Limits
# =========================
MAX_FILE_SIZE = (
    60 * 1024 * 1024
)

# =========================
# Audio Processing
# =========================
CHUNK_DIR = "chunks"

CHUNK_MINUTES = 10

AUDIO_SAMPLE_RATE = 16000

AUDIO_CHANNELS = 1

YOUTUBE_AUDIO_QUALITY = "192"


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
# Chunking Settings
# =========================
CHUNK_SIZE = 2500

CHUNK_OVERLAP = 500


# =========================
# Retrieval Settings
# =========================
RETRIEVAL_K = 10

RETRIEVAL_FETCH_K = 40

# =========================
# Summarization
# =========================
SUMMARY_CHUNK_SIZE = 3000

SUMMARY_CHUNK_OVERLAP = 300

# =========================
# Whisper Settings
# =========================
WHISPER_MODEL = "small"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE_TYPE = "int8"

WHISPER_BEAM_SIZE = 1

WHISPER_VAD_FILTER = True

# =========================
# Database
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

DB_POOL_SIZE = 5

DB_MAX_OVERFLOW = 10

DB_POOL_RECYCLE = 300

DB_POOL_PRE_PING = True

DB_ECHO = False

# =========================
# Retrieval Settings
# =========================
RETRIEVAL_K = 10

RETRIEVAL_FETCH_K = 40

RETRIEVAL_SEARCH_TYPE = "mmr"