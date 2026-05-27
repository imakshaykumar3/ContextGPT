# app/rag/query_rewriter.py

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

from app.rag.prompts import (
    QUERY_REWRITE_PROMPT
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

    temperature=0.2
)


# =========================
# Shared Prompt
# =========================
rewrite_prompt = (
    ChatPromptTemplate.from_messages([

        (
            "system",

            QUERY_REWRITE_PROMPT
        ),

        (
            "human",

            "{question}"
        )
    ])
)


# =========================
# Shared Chain
# =========================
rewrite_chain = (

    rewrite_prompt

    | llm

    | StrOutputParser()
)


# =========================
# Rewrite Query
# =========================
async def rewrite_query(
    question: str
) -> str:

    try:

        logger.info(
            f"Rewriting query: "
            f"{question}"
        )

        rewritten_query = (
            await rewrite_chain.ainvoke({

                "question":
                    question
            })
        ).strip()

        logger.info(
            f"Rewritten query: "
            f"{rewritten_query}"
        )

        return rewritten_query

    except Exception as e:

        logger.error(
            f"Query rewrite failed: {e}"
        )

        # Fallback
        return question