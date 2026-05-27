# app/rag/retriever.py

import logging

from app.config.settings import (

    RETRIEVAL_K,

    RETRIEVAL_FETCH_K,

    RETRIEVAL_SEARCH_TYPE
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Get Retriever
# =========================
def get_retriever(
    vector_store
):

    logger.info(
        "Creating retriever"
    )

    retriever = vector_store.as_retriever(

        search_type=(
            RETRIEVAL_SEARCH_TYPE
        ),

        search_kwargs={

            "k":
                RETRIEVAL_K,

            "fetch_k":
                RETRIEVAL_FETCH_K,
        }
    )

    logger.info(
        "Retriever created successfully"
    )

    return retriever