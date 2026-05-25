from app.utils.audio_processor import process_input
from app.core.transcriber import transcribe_all
from app.core.summarize import generate_title, summarize
from app.core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)

from app.services.db_service import save_meeting


def run_pipeline(source: str, language: str = "english") -> dict:

    # Process input audio/video
    chunks = process_input(source)

    # Transcribe
    transcript = transcribe_all(
        chunks,
        language=language
    )

    # Generate outputs
    title = generate_title(transcript)

    summary = summarize(transcript)

    action_items = extract_action_items(transcript)

    decisions = extract_key_decisions(transcript)

    questions = extract_questions(transcript)

    # Final result dictionary
    result = {
        "title": title,
        "source": source,
        "language": language,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
    }

    # Save to PostgreSQL
    meeting_id = save_meeting(result)

    # Add meeting ID to response
    result["meeting_id"] = meeting_id

    return result