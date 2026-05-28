# app/rag/vector_store.py

import os
import logging

from langchain_chroma import Chroma

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
# Get Meeting Paths
# =========================
def get_meeting_vector_path(
    meeting_id: int
) -> str:

    return os.path.join(

        CHROMA_DIR,

        f"meeting_{meeting_id}"
    )


def get_collection_name(
    meeting_id: int
) -> str:

    return f"meeting_{meeting_id}"


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
        # Create Documents
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

            for idx, chunk in enumerate(chunks)

            if chunk.strip()
        ]

        # -------------------------
        # Meeting-specific path
        # -------------------------
        persist_directory = (
            get_meeting_vector_path(
                meeting_id
            )
        )

        os.makedirs(

            persist_directory,

            exist_ok=True
        )

        # -------------------------
        # Create Vector Store
        # -------------------------
        vector_store = Chroma.from_documents(

            documents=docs,

            embedding=get_embeddings(),

            persist_directory=(
                persist_directory
            ),

            collection_name=(
                get_collection_name(
                    meeting_id
                )
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

        persist_directory = (
            get_meeting_vector_path(
                meeting_id
            )
        )

        if not os.path.exists(
            persist_directory
        ):

            raise Exception(
                "Meeting vector DB missing"
            )

        vector_store = Chroma(

            persist_directory=(
                persist_directory
            ),

            embedding_function=(
                get_embeddings()
            ),

            collection_name=(
                get_collection_name(
                    meeting_id
                )
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