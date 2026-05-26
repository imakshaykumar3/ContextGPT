# app/rag/rag_engine.py
import logging

from langchain_openai import (
    ChatOpenAI
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from app.config.settings import (

    GPT_MODEL,

    OPENAI_API_KEY
)

from app.rag.vector_store import (
    build_vector_store,
    load_vector_store
)

from app.rag.retriever import (
    get_retriever
)

from app.rag.query_rewriter import (
    rewrite_query
)

from app.rag.prompts import (
    RAG_QA_PROMPT
)


logger = logging.getLogger(__name__)


llm = ChatOpenAI(

    model=GPT_MODEL,

    openai_api_key=OPENAI_API_KEY,

    temperature=0.3
)


# =========================
# Ask Question
# =========================
def ask_question(
    meeting_id: int,
    question: str
):

    logger.info(
        f"Question received: {question}"
    )

    # Load vector DB
    vector_store = load_vector_store(
        meeting_id
    )

    # Create retriever
    retriever = get_retriever(
        vector_store
    )

    # Rewrite query
    rewritten_query = rewrite_query(
        question
    )

    logger.info(
        f"Rewritten query: "
        f"{rewritten_query}"
    )

    # Retrieve documents
    docs = retriever.invoke(
        rewritten_query
    )

    logger.info(
        f"Retrieved {len(docs)} docs"
    )

    if not docs:

        return {

            "rewritten_query":
                rewritten_query,

            "answer":
                "I could not find "
                "relevant information "
                "in the meeting."
        }

    # Build context
    context = "\n\n".join([

        doc.page_content

        for doc in docs
    ])

    # Prompt
    prompt = (
        ChatPromptTemplate.from_messages([
            (
                "system",
                RAG_QA_PROMPT
            ),
            (
                "human",
                "{question}"
            )
        ])
    )

    # QA chain
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({

        "context": context,

        "question": question
    })

    logger.info(
        "Answer generated"
    )

    return {

        "rewritten_query":
            rewritten_query,

        "answer":
            response
    }