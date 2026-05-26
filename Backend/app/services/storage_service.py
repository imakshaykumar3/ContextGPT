# app/services/storage_service.py
import os
import json
import logging

from app.config.settings import (
    TRANSCRIPTS_DIR,
    SUMMARIES_DIR
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Ensure Directories Exist
# =========================
os.makedirs(
    TRANSCRIPTS_DIR,
    exist_ok=True
)

os.makedirs(
    SUMMARIES_DIR,
    exist_ok=True
)


# =========================
# Save Transcript
# =========================
def save_transcript(
    meeting_id,
    transcript
):

    try:

        logger.info(
            f"Saving transcript "
            f"for meeting {meeting_id}"
        )

        transcript_path = os.path.join(

            TRANSCRIPTS_DIR,

            f"meeting_{meeting_id}.txt"
        )

        with open(
            transcript_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(transcript)

        logger.info(
            "Transcript saved successfully"
        )

        return transcript_path

    except Exception as e:

        logger.error(
            f"Failed to save transcript: {e}"
        )

        raise Exception(
            f"Transcript Save Error: {e}"
        )


# =========================
# Save Summary JSON
# =========================
def save_summary(
    meeting_id,
    data
):

    try:

        logger.info(
            f"Saving summary "
            f"for meeting {meeting_id}"
        )

        summary_path = os.path.join(

            SUMMARIES_DIR,

            f"meeting_{meeting_id}.json"
        )

        with open(
            summary_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False
            )

        logger.info(
            "Summary JSON saved successfully"
        )

        return summary_path

    except Exception as e:

        logger.error(
            f"Failed to save summary: {e}"
        )

        raise Exception(
            f"Summary Save Error: {e}"
        )


# =========================
# Load Transcript
# =========================
def load_transcript(
    transcript_path
):

    try:

        with open(
            transcript_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except Exception as e:

        logger.error(
            f"Failed to load transcript: {e}"
        )

        raise Exception(
            f"Transcript Load Error: {e}"
        )


# =========================
# Load Summary
# =========================
def load_summary(
    summary_path
):

    try:

        with open(
            summary_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        logger.error(
            f"Failed to load summary: {e}"
        )

        raise Exception(
            f"Summary Load Error: {e}"
        )