#$ app/rag/embeddings.py
from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from app.config.settings import (
    EMBEDDING_MODEL
)


# =========================
# Shared Embedding Model
# =========================
embeddings_model = HuggingFaceEmbeddings(

    model_name=EMBEDDING_MODEL,

    model_kwargs={
        "device": "cpu"
    }
)


def get_embeddings():

    return embeddings_model