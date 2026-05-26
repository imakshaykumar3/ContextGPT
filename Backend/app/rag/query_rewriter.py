#app/rag/query_rewriter.py
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


llm = ChatOpenAI(

    model=GPT_MODEL,

    openai_api_key=OPENAI_API_KEY,

    temperature=0.2
)


def rewrite_query(
    question: str
):

    prompt = (
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

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": question
    }).strip()