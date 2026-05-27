# app/rag/rag_engine.py

import logging
import asyncio

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


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared LLM
# =========================
llm = ChatOpenAI(

    model=GPT_MODEL,

    openai_api_key=OPENAI_API_KEY,

    temperature=0.3
)


# =========================
# Shared Prompt
# =========================
qa_prompt = (
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


# =========================
# Shared QA Chain
# =========================
qa_chain = (

    qa_prompt

    | llm

    | StrOutputParser()
)


# =========================
# Ask Question
# =========================
async def ask_question(

    meeting_id: int,

    question: str
):

    try:

        logger.info(
            f"Question received: "
            f"{question}"
        )

        # -------------------------
        # Load Vector Store
        # CPU/IO Bound
        # -------------------------
        vector_store = (
            await asyncio.to_thread(

                load_vector_store,

                meeting_id
            )
        )

        # -------------------------
        # Create Retriever
        # -------------------------
        retriever = get_retriever(
            vector_store
        )

        # -------------------------
        # Rewrite Query
        # -------------------------
        rewritten_query = (
            await rewrite_query(
                question
            )
        )

        logger.info(
            f"Rewritten query: "
            f"{rewritten_query}"
        )

        # -------------------------
        # Retrieve Documents
        # -------------------------
        docs = await retriever.ainvoke(
            rewritten_query
        )

        # -------------------------
        # Metadata Filtering
        # IMPORTANT
        # -------------------------
        docs = [

            doc

            for doc in docs

            if doc.metadata.get(
                "meeting_id"
            ) == meeting_id
        ]

        logger.info(
            f"Retrieved {len(docs)} docs"
        )

        # -------------------------
        # No Context Found
        # -------------------------
        if not docs:

            return {

                "rewritten_query":
                    rewritten_query,

                "answer":
                    (
                        "I could not find "
                        "relevant information "
                        "in the meeting."
                    )
            }

        # -------------------------
        # Limit Context Size
        # Prevent token explosion
        # -------------------------
        MAX_CONTEXT_CHARS = 12000

        context_parts = []

        total_chars = 0

        for doc in docs:

            content = (
                doc.page_content.strip()
            )

            if not content:
                continue

            if (
                total_chars
                + len(content)
                > MAX_CONTEXT_CHARS
            ):
                break

            context_parts.append(
                content
            )

            total_chars += len(
                content
            )

        context = "\n\n".join(
            context_parts
        )

        logger.info(
            f"Context size: "
            f"{len(context)} chars"
        )

        # -------------------------
        # Generate Answer
        # -------------------------
        response = (
            await qa_chain.ainvoke({

                "context":
                    context,

                "question":
                    question
            })
        )

        logger.info(
            "Answer generated successfully"
        )

        return {

            "rewritten_query":
                rewritten_query,

            "answer":
                response.strip()
        }

    except Exception as e:

        logger.error(
            f"RAG QA failed: {e}"
        )

        return {

            "rewritten_query":
                question,

            "answer":
                (
                    "An error occurred while "
                    "processing your question."
                )
        }