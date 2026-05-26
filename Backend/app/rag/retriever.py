# app/rag/retriever.py
from app.config.settings import (

    RETRIEVAL_K,

    RETRIEVAL_FETCH_K,

    RETRIEVAL_SEARCH_TYPE
)


def get_retriever(
    vector_store
):

    return vector_store.as_retriever(

        search_type=RETRIEVAL_SEARCH_TYPE,

        search_kwargs={

            "k": RETRIEVAL_K,

            "fetch_k": RETRIEVAL_FETCH_K
        }
    )