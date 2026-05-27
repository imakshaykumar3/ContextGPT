# app/services/storage_service.py

import os
import json
import logging
import aiofiles

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
async def save_transcript(

    meeting_id: int,

    transcript: str
) -> str:

    try:

        logger.info(
            f"Saving transcript "
            f"for meeting {meeting_id}"
        )

        transcript_path = os.path.join(

            TRANSCRIPTS_DIR,

            f"meeting_{meeting_id}.txt"
        )

        async with aiofiles.open(

            transcript_path,

            "w",

            encoding="utf-8"
        ) as f:

            await f.write(
                transcript
            )

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
async def save_summary(

    meeting_id: int,

    data: dict
) -> str:

    try:

        logger.info(
            f"Saving summary "
            f"for meeting {meeting_id}"
        )

        summary_path = os.path.join(

            SUMMARIES_DIR,

            f"meeting_{meeting_id}.json"
        )

        async with aiofiles.open(

            summary_path,

            "w",

            encoding="utf-8"
        ) as f:

            await f.write(

                json.dumps(

                    data,

                    indent=4,

                    ensure_ascii=False
                )
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
async def load_transcript(
    transcript_path: str
) -> str:

    try:

        if not os.path.exists(
            transcript_path
        ):

            raise FileNotFoundError(
                "Transcript file not found"
            )

        async with aiofiles.open(

            transcript_path,

            "r",

            encoding="utf-8"
        ) as f:

            transcript = await f.read()

        return transcript

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
async def load_summary(
    summary_path: str
) -> dict:

    try:

        if not os.path.exists(
            summary_path
        ):

            raise FileNotFoundError(
                "Summary file not found"
            )

        async with aiofiles.open(

            summary_path,

            "r",

            encoding="utf-8"
        ) as f:

            content = await f.read()

        return json.loads(
            content
        )

    except Exception as e:

        logger.error(
            f"Failed to load summary: {e}"
        )

        raise Exception(
            f"Summary Load Error: {e}"
        )