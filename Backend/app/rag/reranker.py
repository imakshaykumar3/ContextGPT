# app/rag/reranker.py

import logging
import threading

from sentence_transformers import (
    CrossEncoder
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared Reranker Model
# =========================
_reranker = None

_reranker_lock = threading.Lock()


# =========================
# Load Reranker
# =========================
def get_reranker():

    global _reranker

    if _reranker is None:

        with _reranker_lock:

            if _reranker is None:

                logger.info(
                    "Loading BGE reranker model"
                )

                _reranker = CrossEncoder(

                    "BAAI/bge-reranker-base"
                )

                logger.info(
                    "BGE reranker loaded successfully"
                )

    return _reranker


# =========================
# Rerank Documents
# =========================
def rerank_documents(

    question: str,

    docs: list,

    top_k: int = 5
):

    try:

        logger.info(
            "Starting reranking"
        )

        if not docs:

            return []

        reranker = get_reranker()

        # -------------------------
        # Create Pairs
        # -------------------------
        pairs = [

            (
                question,

                doc.page_content
            )

            for doc in docs
        ]

        # -------------------------
        # Predict Scores
        # -------------------------
        scores = reranker.predict(
            pairs
        )

        # -------------------------
        # Combine Docs + Scores
        # -------------------------
        scored_docs = list(

            zip(docs, scores)
        )

        # -------------------------
        # Sort by Score Desc
        # -------------------------
        scored_docs.sort(

            key=lambda x: x[1],

            reverse=True
        )

        # -------------------------
        # Select Top Docs
        # -------------------------
        top_docs = [

            doc

            for doc, score in (
                scored_docs[:top_k]
            )
        ]

        logger.info(
            f"Reranked top "
            f"{len(top_docs)} docs"
        )

        return top_docs

    except Exception as e:

        logger.error(
            f"Reranking failed: {e}"
        )

        # Fallback
        return docs[:top_k]