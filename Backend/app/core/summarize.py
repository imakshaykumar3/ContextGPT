# app/core/summarize.py
import logging

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    JsonOutputParser,
    StrOutputParser
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)

from app.config.settings import (
    GPT_MODEL,
    OPENAI_API_KEY,
    SUMMARY_CHUNK_SIZE,
    SUMMARY_CHUNK_OVERLAP
)


load_dotenv()


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared LLM
# =========================
llm_model = ChatOpenAI(
    model=GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    temperature=0.3
)


def get_llm():

    return llm_model


# =========================
# JSON Parser
# =========================
summary_parser = JsonOutputParser()


# =========================
# Split Transcript
# =========================
def split_transcript(transcript: str) -> list:

    logger.info("Splitting transcript")

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=SUMMARY_CHUNK_SIZE,
            chunk_overlap=SUMMARY_CHUNK_OVERLAP,
        )
    )

    chunks = splitter.split_text(transcript)

    logger.info(f"{len(chunks)} summary chunks created")

    return chunks


# =========================
# Generate Structured Summary
# =========================
def summarize(transcript: str):

    logger.info("Starting summarization")

    llm = get_llm()

    # -------------------------
    # MAP STEP
    # -------------------------
    map_prompt = (
        ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are an expert AI meeting summarizer.

                Summarize this transcript chunk.

                Focus on:
                - important discussions
                - decisions
                - action items
                - blockers
                - outcomes

                Keep summary concise.
                """
            ),
            (
                "human",
                "{text}"
            )
        ])
    )

    map_chain = (
        map_prompt
        | llm
        | StrOutputParser()
    )

    chunks = split_transcript(transcript)

    logger.info("Generating chunk summaries")

    chunk_summaries = [

        map_chain.invoke({
            "text": chunk
        })

        for chunk in chunks
    ]

    # -------------------------
    # COMBINE STEP
    # -------------------------
    combined = "\n\n".join(chunk_summaries)

    combine_prompt = (
        ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are an enterprise AI meeting assistant.

                Combine all partial summaries
                into ONE structured JSON response.

                Return ONLY valid JSON.

                JSON format:

                {
                  "overview": "...",

                  "discussion_points": [
                    "...",
                    "..."
                  ],

                  "decisions": [
                    "...",
                    "..."
                  ],

                  "risks": [
                    "...",
                    "..."
                  ],

                  "conclusion": "..."
                }

                Rules:
                - No markdown
                - No explanations
                - No extra text
                - Keep concise
                - discussion_points must be array
                - decisions must be array
                - risks must be array
                """
            ),
            (
                "human",
                "{text}"
            )
        ])
    )

    combine_chain = (

        RunnablePassthrough()

        | RunnableLambda(
            lambda x: {"text": x}
        )

        | combine_prompt

        | llm

        | summary_parser
    )

    final_summary = combine_chain.invoke(combined)

    logger.info("Structured summarization completed")

    return final_summary


# =========================
# Generate Meeting Title
# =========================
def generate_title(transcript: str) -> str:

    logger.info(
        "Generating meeting title"
    )

    llm = get_llm()

    title_prompt = (
        ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Generate a concise,
                professional meeting title.

                Rules:
                - Maximum 8 words
                - Clear and descriptive
                - No punctuation
                - Return title only
                """
            ),
            (
                "human",
                "{transcript}"
            )
        ])
    )

    title_chain = (

        RunnablePassthrough()

        | RunnableLambda(
            lambda x: {
                "transcript": x
            }
        )

        | title_prompt

        | llm

        | StrOutputParser()
    )

    title = title_chain.invoke(transcript).strip()

    logger.info(f"Generated title: {title}")

    return title