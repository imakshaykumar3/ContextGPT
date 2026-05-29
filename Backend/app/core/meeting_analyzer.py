# app/core/meeting_analyzer.py

import logging

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    JsonOutputParser
)

from app.config.settings import (
    GPT_MODEL,
    OPENAI_API_KEY
)

load_dotenv()

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
# Parser
# =========================
parser = JsonOutputParser()


# =========================
# Prompt
# =========================
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert enterprise meeting analyst.

Analyze the transcript and return ONLY valid JSON.

Required format:

{{
  "summary": {{
    "overview": "...",
    "key_points": [
      "..."
    ]
  }},

  "action_items": [
    {{
      "task": "...",
      "owner": "...",
      "due_date": "...",
      "priority": "High"
    }}
  ],

  "key_decisions": [
    {{
      "decision": "..."
    }}
  ],

  "open_questions": [
    {{
      "question": "..."
    }}
  ]
}}

Rules:

- Return valid JSON only
- No markdown
- No explanations
- No extra text
- Do not hallucinate

Action Items:
- owner = "Not specified" if unknown
- due_date = "Not specified" if unknown
- priority must be High / Medium / Low

Key Decisions:
- Only confirmed decisions

Open Questions:
- Only unresolved items

Summary:
- concise
- factual
- based only on transcript
"""
    ),
    (
        "human",
        "{transcript}"
    )
])


# =========================
# Chain
# =========================
chain = (
    prompt
    | llm
    | parser
)


# =========================
# Analyze Meeting
# =========================
async def analyze_meeting(
    transcript: str
):

    try:

        logger.info(
            "Running unified meeting analysis"
        )

        result = await chain.ainvoke({
            "transcript": transcript
        })

        return result

    except Exception as e:

        logger.error(
            f"Meeting analysis failed: {e}"
        )

        return {
            "summary": {},
            "action_items": [],
            "key_decisions": [],
            "open_questions": []
        }