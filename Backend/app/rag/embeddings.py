# app/rag/embeddings.py

import logging
import threading

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from app.config.settings import (
    EMBEDDING_MODEL
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared Embedding Model
# =========================
_embeddings_model = None

_embeddings_lock = threading.Lock()


# =========================
# Get Embeddings Model
# =========================
def get_embeddings():

    global _embeddings_model

    if _embeddings_model is None:

        with _embeddings_lock:

            if _embeddings_model is None:

                logger.info(
                    f"Loading embedding model: "
                    f"{EMBEDDING_MODEL}"
                )

                _embeddings_model = (
                    HuggingFaceEmbeddings(

                        model_name=EMBEDDING_MODEL,

                        model_kwargs={
                            "device": "cpu"
                        },

                        encode_kwargs={
                            "normalize_embeddings": True
                        }
                    )
                )

                logger.info(
                    "Embedding model loaded successfully"
                )

    return _embeddings_model