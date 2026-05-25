from app.utils.audio_processor import process_input
from app.core.transcriber import transcribe_all
from app.core.summarize import generate_title, summarize
from app.core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)
from app.core.rag_engine import build_rag_chain


def run_pipeline(source: str) -> dict:

    chunks = process_input(source)
    language = "en"  # Default to English, can be made dynamic based on user input

    transcript = transcribe_all(
        chunks,
        language=language
    )

    title = generate_title(transcript)

    summary = summarize(transcript)

    action_items = extract_action_items(transcript)

    decisions = extract_key_decisions(transcript)

    questions = extract_questions(transcript)

    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
    }