import logging

from app.utils.audio_processor import process_input

from app.core.transcriber import transcribe_all

from app.core.summarize import (
    generate_title,
    summarize
)

from app.core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)

from app.services.db_service import (
    create_meeting,
    update_meeting_files
)

from app.services.storage_service import (
    save_transcript,
    save_summary
)


# Configure logger
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def run_pipeline(
    source: str,
    language: str = "english"
) -> dict:

    try:

        logger.info("Starting AI Meeting Pipeline")

        # Process input
        logger.info("Processing audio/video input")

        chunks = process_input(source)

        # Validate chunks
        if not chunks:

            raise Exception(
                "Audio processing failed"
            )

        logger.info(
            f"{len(chunks)} chunks created successfully"
        )

        # Transcription
        logger.info("Starting transcription")

        transcript = transcribe_all(
            chunks,
            language=language
        )

        if not transcript:

            raise Exception(
                "Transcription failed"
            )

        logger.info("Transcription completed")

        # Generate title
        logger.info("Generating meeting title")

        title = generate_title(transcript)

        # Generate summary
        logger.info("Generating summary")

        summary = summarize(transcript)

        # Extract action items
        logger.info("Extracting action items")

        action_items = extract_action_items(
            transcript
        )

        # Extract decisions
        logger.info("Extracting key decisions")

        decisions = extract_key_decisions(
            transcript
        )

        # Extract questions
        logger.info("Extracting open questions")

        questions = extract_questions(
            transcript
        )

        # Create DB record
        logger.info("Creating database record")

        meeting_id = create_meeting(
            source,
            language,
            title
        )

        logger.info(
            f"Meeting created with ID: {meeting_id}"
        )

        # Save transcript
        logger.info("Saving transcript file")

        transcript_path = save_transcript(
            meeting_id,
            transcript
        )

        # Prepare summary JSON
        summary_data = {
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions
        }

        # Save summary JSON
        logger.info("Saving summary JSON")

        summary_path = save_summary(
            meeting_id,
            summary_data
        )

        # Update DB with file paths
        logger.info("Updating database with file paths")

        update_meeting_files(
            meeting_id,
            transcript_path,
            summary_path
        )

        logger.info(
            "Pipeline completed successfully"
        )

        return {
            "meeting_id": meeting_id,

            "title": title,

            "transcript": transcript,

            "summary": summary,

            "action_items": action_items,

            "key_decisions": decisions,

            "open_questions": questions
        }

    except Exception as e:

        logger.error(
            f"Pipeline failed: {str(e)}"
        )

        raise Exception(
            f"Pipeline Error: {str(e)}"
        )