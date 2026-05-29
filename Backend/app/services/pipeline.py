# app/services/pipeline.py

import os
import logging
import asyncio

from app.utils.audio_processor import (
    process_input,
    cleanup_files
)

from app.core.transcriber import (
    transcribe_all
)

from app.core.summarize import (
    generate_title
)

from app.core.meeting_analyzer import (
    analyze_meeting
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


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Main AI Pipeline
# =========================
async def run_pipeline(
    source: str,
    language: str = "en",
    user_id: int = None
):

    meeting_id = None

    chunks = []

    wav_path = None

    try:

        logger.info(
            "Starting AI pipeline"
        )

        # -------------------------
        # Process Audio
        # CPU-bound
        # -------------------------
        processing_result = (
            await asyncio.to_thread(
                process_input,
                source
            )
        )

        chunks = (
            processing_result["chunks"]
        )

        wav_path = (
            processing_result["wav_path"]
        )

        logger.info(
            f"{len(chunks)} chunks created"
        )

        # -------------------------
        # Transcription
        # CPU-bound Whisper
        # -------------------------
        transcription_result = (
            await asyncio.to_thread(
                transcribe_all,
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
        title = await generate_title(
            transcript
        )

        # -------------------------
        # Create DB Record
        # -------------------------
        if user_id is None:

            raise Exception(
                "user_id is required"
            )

        meeting_id = await create_meeting(

            user_id=user_id,

            source=source,

            language=detected_language,

            title=title,

            file_type=(
                os.path.splitext(source)[1]
                if os.path.isfile(source)
                else "youtube"
            )
        )

        # -------------------------
        # Unified Meeting Analysis
        # Single GPT Call
        # -------------------------
        analysis = await analyze_meeting(
            transcript
        )

        summary = analysis.get(
            "summary",
            {}
        )

        action_items = analysis.get(
            "action_items",
            []
        )

        key_decisions = analysis.get(
            "key_decisions",
            []
        )

        open_questions = analysis.get(
            "open_questions",
            []
        )

        logger.info(
            "Meeting analysis completed"
        )

        # -------------------------
        # Save Transcript
        # -------------------------
        transcript_path = (
            await save_transcript(
                meeting_id,
                transcript
            )
        )

        # -------------------------
        # Save Summary JSON
        # -------------------------
        summary_data = {

            "segments":
                segments,

            "summary":
                summary,

            "action_items":
                action_items,

            "key_decisions":
                key_decisions,

            "open_questions":
                open_questions
        }

        summary_path = (
            await save_summary(
                meeting_id,
                summary_data
            )
        )

        # -------------------------
        # Build Vector Store
        # -------------------------
        await asyncio.to_thread(
            build_vector_store,
            meeting_id,
            transcript
        )

        # -------------------------
        # Update DB
        # -------------------------
        await update_meeting_files(
            meeting_id,
            transcript_path,
            summary_path,
            vector_store_path=(
                os.path.join(
                    "vector_db",
                    f"meeting_{meeting_id}"
                )
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

            await mark_meeting_failed(
                meeting_id,
                str(e)
            )

        raise Exception(
            f"Pipeline Error: {e}"
        )

    finally:

        try:

            cleanup_targets = []

            # -------------------------
            # Cleanup chunks
            # -------------------------
            if chunks:

                cleanup_targets.extend(
                    chunks
                )

            # -------------------------
            # Cleanup temp WAV
            # -------------------------
            if (
                wav_path
                and os.path.exists(
                    wav_path
                )
            ):

                cleanup_targets.append(
                    wav_path
                )

            # -------------------------
            # Remove temp files
            # -------------------------
            cleanup_files(
                cleanup_targets
            )

            logger.info(
                "Temporary files cleaned successfully"
            )

        except Exception as cleanup_error:

            logger.warning(
                f"Cleanup failed: "
                f"{cleanup_error}"
            )