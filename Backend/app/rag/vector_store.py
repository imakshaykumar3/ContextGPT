# app/rag/vector_store.py
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


logger = logging.getLogger(__name__)


# =========================
# Build Vector Store
# =========================
def build_vector_store(
    meeting_id: int,
    transcript: str
):

    logger.info(
        "Building vector store"
    )

    splitter = (
        RecursiveCharacterTextSplitter(

            chunk_size=CHUNK_SIZE,

            chunk_overlap=CHUNK_OVERLAP
        )
    )

    chunks = splitter.split_text(
        transcript
    )

    docs = [

        Document(
            page_content=chunk,
            metadata={
                "meeting_id": meeting_id,
                "chunk_index": idx
            }
        )

        for idx, chunk in enumerate(chunks)
    ]

    persist_dir = (
        f"{CHROMA_DIR}/meeting_{meeting_id}"
    )

    vector_store = Chroma.from_documents(

        documents=docs,

        embedding=get_embeddings(),

        persist_directory=persist_dir,

        collection_name=(
            f"meeting_{meeting_id}"
        )
    )

    logger.info(
        "Vector store created"
    )

    return vector_store


# =========================
# Load Vector Store
# =========================
def load_vector_store(
    meeting_id: int
):

    persist_dir = (
        f"{CHROMA_DIR}/meeting_{meeting_id}"
    )

    return Chroma(

        persist_directory=persist_dir,

        embedding_function=get_embeddings(),

        collection_name=(
            f"meeting_{meeting_id}"
        )
    )