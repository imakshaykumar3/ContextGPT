# app/core/extractor.py
import logging

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    JsonOutputParser
)

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)

from app.config.settings import (
    GPT_MODEL,
    OPENAI_API_KEY
)


load_dotenv()


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared LLM Instance
# =========================
llm_model = ChatOpenAI(
    model=GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    temperature=0.2
)


def get_llm():

    return llm_model


# =========================
# JSON Parsers
# =========================
action_parser = JsonOutputParser()

decision_parser = JsonOutputParser()

question_parser = JsonOutputParser()


# =========================
# Build Extraction Chain
# =========================
def build_chain(system_prompt: str, parser):

    logger.info("Building extraction chain")

    llm = get_llm()

    chat_prompt = (
        ChatPromptTemplate.from_messages([
            (
                "system",
                system_prompt
            ),
            (
                "human",
                "{text}"
            ),
        ])
    )

    chain = (
        RunnablePassthrough()

        | RunnableLambda(
            lambda x: {"text": x}
        )

        | chat_prompt

        | llm

        | parser
    )

    return chain


# =========================
# Extract Action Items
# =========================
def extract_action_items(transcript: str):

    logger.info("Extracting action items")

    chain = build_chain(
        """
        You are an expert meeting analyst.

        Extract ALL explicit action items
        from the meeting transcript.

        Return ONLY valid JSON.

        JSON format:

        [
          {
            "task": "...",
            "owner": "...",
            "due_date": "...",
            "priority": "High"
          }
        ]

        Rules:
        - No markdown
        - No explanations
        - No extra text
        - If owner missing:
          "Not specified"
        - If due date missing:
          "Not specified"
        - Infer priority carefully
        - Priority must be:
          High / Medium / Low
        - Return empty list [] if none found
        """,
        action_parser
    )

    result = chain.invoke(transcript)

    logger.info("Action items extracted")

    return result


# =========================
# Extract Key Decisions
# =========================
def extract_key_decisions(transcript: str):

    logger.info("Extracting key decisions")

    chain = build_chain(
        """
        You are an expert meeting analyst.

        Extract all IMPORTANT confirmed
        decisions from the meeting transcript.

        Return ONLY valid JSON.

        JSON format:

        [
          {
            "decision": "..."
          }
        ]

        Rules:
        - No markdown
        - No explanations
        - No extra text
        - Do NOT hallucinate
        - Only include confirmed decisions
        - Return empty list [] if none found
        """,
        decision_parser
    )

    result = chain.invoke(transcript)

    logger.info("Key decisions extracted")

    return result


# =========================
# Extract Open Questions
# =========================
def extract_questions(transcript: str):

    logger.info("Extracting open questions")

    chain = build_chain(
        """
        You are an expert meeting analyst.

        Extract unresolved questions,
        blockers, follow-ups,
        or pending discussions.

        Return ONLY valid JSON.

        JSON format:

        [
          {
            "question": "..."
          }
        ]

        Rules:
        - No markdown
        - No explanations
        - No extra text
        - Be literal
        - Do NOT infer
        - Only unresolved items
        - Return empty list [] if none found
        """,
        question_parser
    )

    result = chain.invoke(transcript)

    logger.info("Open questions extracted")

    return result