import logging
import os

from app.utils.audio_processor import (
    process_input
)

from app.core.transcriber import (
    transcribe_all
)

from app.core.summarize import (
    summarize,
    generate_title
)

from app.core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)

from app.rag.vector_store import (
    build_vector_store
)

from app.services.storage_service import (
    save_transcript,
    save_summary
)

from app.services.db_service import (
    create_meeting,
    update_meeting_files,
    mark_meeting_failed
)


logger = logging.getLogger(__name__)


# =========================
# Main AI Pipeline
# =========================
def run_pipeline(
    source: str,
    language: str = "en"
):

    meeting_id = None

    try:

        logger.info(
            "Starting AI pipeline"
        )

        # -------------------------
        # Process Audio
        # -------------------------
        chunks = process_input(source)

        logger.info(
            f"{len(chunks)} chunks created"
        )

        # -------------------------
        # Transcription
        # -------------------------
        transcription_result = (
            transcribe_all(
                chunks,
                language
            )
        )

        transcript = (
            transcription_result["text"]
        )

        segments = (
            transcription_result["segments"]
        )

        detected_language = (
            transcription_result["language"]
        )

        # -------------------------
        # Generate Title
        # -------------------------
        title = generate_title(
            transcript
        )

        # -------------------------
        # Create DB Record
        # -------------------------
        meeting_id = create_meeting(

            source=source,

            language=detected_language,

            title=title,

            file_type=os.path.splitext(
                source
            )[1]
            if os.path.isfile(source)
            else "youtube"
        )

        # -------------------------
        # Summarization
        # -------------------------
        summary = summarize(
            transcript
        )

        # -------------------------
        # Extract Structured Data
        # -------------------------
        action_items = (
            extract_action_items(
                transcript
            )
        )

        key_decisions = (
            extract_key_decisions(
                transcript
            )
        )

        open_questions = (
            extract_questions(
                transcript
            )
        )

        # -------------------------
        # Save Transcript
        # -------------------------
        transcript_path = (
            save_transcript(
                meeting_id,
                transcript
            )
        )

        # -------------------------
        # Save Summary JSON
        # -------------------------
        summary_data = {

            "segments": segments,

            "summary": summary,

            "action_items":
                action_items,

            "key_decisions":
                key_decisions,

            "open_questions":
                open_questions
        }

        summary_path = (
            save_summary(
                meeting_id,
                summary_data
            )
        )

        # -------------------------
        # Build Vector Store
        # -------------------------
        build_vector_store(
            meeting_id,
            transcript
        )

        # -------------------------
        # Update DB
        # -------------------------
        update_meeting_files(

            meeting_id,

            transcript_path,

            summary_path,

            vector_store_path=(
                f"vector_db/meeting_{meeting_id}"
            )
        )

        logger.info(
            "Pipeline completed successfully"
        )

        return {

            "meeting_id":
                meeting_id,

            "title":
                title,

            "language":
                detected_language,

            "summary":
                summary,

            "action_items":
                action_items,

            "key_decisions":
                key_decisions,

            "open_questions":
                open_questions
        }

    except Exception as e:

        logger.error(
            f"Pipeline failed: {e}"
        )

        if meeting_id:

            mark_meeting_failed(
                meeting_id,
                str(e)
            )

        raise Exception(
            f"Pipeline Error: {e}"
        )