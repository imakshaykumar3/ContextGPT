# app/rag/vector_store.py

import os
import logging

from langchain_chroma import (
    Chroma
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import (
    Document
)

from app.config.settings import (

    CHROMA_DIR,

    CHUNK_SIZE,

    CHUNK_OVERLAP
)

from app.rag.embeddings import (
    get_embeddings
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared Collection Name
# =========================
COLLECTION_NAME = "meetings"


# =========================
# Build Vector Store
# =========================
def build_vector_store(

    meeting_id: int,

    transcript: str
):

    try:

        logger.info(
            f"Building vector store "
            f"for meeting {meeting_id}"
        )

        # -------------------------
        # Split Transcript
        # -------------------------
        splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=CHUNK_SIZE,

                chunk_overlap=CHUNK_OVERLAP
            )
        )

        chunks = splitter.split_text(
            transcript
        )

        logger.info(
            f"{len(chunks)} chunks created"
        )

        # -------------------------
        # Build Documents
        # -------------------------
        docs = [

            Document(

                page_content=chunk.strip(),

                metadata={

                    "meeting_id":
                        meeting_id,

                    "chunk_index":
                        idx
                }
            )

            for idx, chunk in enumerate(
                chunks
            )

            if chunk.strip()
        ]

        # -------------------------
        # Ensure Chroma Directory
        # -------------------------
        os.makedirs(

            CHROMA_DIR,

            exist_ok=True
        )

        # -------------------------
        # Create Vector Store
        # -------------------------
        vector_store = Chroma.from_documents(

            documents=docs,

            embedding=get_embeddings(),

            persist_directory=CHROMA_DIR,

            collection_name=(
                COLLECTION_NAME
            )
        )

        logger.info(
            "Vector store created successfully"
        )

        return vector_store

    except Exception as e:

        logger.error(
            f"Vector store build failed: {e}"
        )

        raise Exception(
            f"Vector DB Error: {e}"
        )


# =========================
# Load Vector Store
# =========================
def load_vector_store(
    meeting_id: int
):

    try:

        logger.info(
            f"Loading vector store "
            f"for meeting {meeting_id}"
        )

        if not os.path.exists(
            CHROMA_DIR
        ):

            raise Exception(
                "Vector database missing"
            )

        vector_store = Chroma(

            persist_directory=CHROMA_DIR,

            embedding_function=(
                get_embeddings()
            ),

            collection_name=(
                COLLECTION_NAME
            )
        )

        logger.info(
            "Vector store loaded successfully"
        )

        return vector_store

    except Exception as e:

        logger.error(
            f"Failed to load vector store: {e}"
        )

        raise Exception(
            f"Load Vector DB Error: {e}"
        )