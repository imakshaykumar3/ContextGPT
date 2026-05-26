#app/core/transcriber.py
import logging

from faster_whisper import (
    WhisperModel
)

from dotenv import load_dotenv

from app.config.settings import (
    WHISPER_MODEL,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_BEAM_SIZE,
    WHISPER_VAD_FILTER
)


load_dotenv()


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Shared Whisper Model
# =========================
_model = None


def load_whisper_model():

    """
    Load Whisper model once
    and reuse globally.
    """

    global _model

    if _model is None:

        logger.info(
            f"Loading Whisper model: "
            f"{WHISPER_MODEL}"
        )

        _model = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE
        )

        logger.info("Whisper model loaded successfully")

    return _model


# =========================
# Transcribe Single Chunk
# =========================
def transcribe_chunk(chunk_path: str,language: str = "en"):

    try:

        logger.info(
            f"Transcribing chunk: "
            f"{chunk_path}"
        )

        model = load_whisper_model()

        segments, info = model.transcribe(
            chunk_path,

            beam_size=WHISPER_BEAM_SIZE,

            vad_filter=WHISPER_VAD_FILTER,

            language=language
        )

        transcript_segments = []

        for segment in segments:

            transcript_segments.append({

                "start": round(segment.start,2),

                "end": round(segment.end,2),

                "text": segment.text.strip()
            })

        full_text = " ".join([
            segment["text"]
            for segment in transcript_segments
        ])

        logger.info(
            f"Finished transcribing: "
            f"{chunk_path}"
        )

        return {

            "text": full_text,

            "segments": transcript_segments,

            "language": info.language,

            "language_probability":
                round(
                    info.language_probability,
                    2
                )
        }

    except Exception as e:

        logger.error(
            f"Transcription failed for "
            f"{chunk_path}: {e}"
        )

        return {

            "text": "",

            "segments": [],

            "language": language,

            "language_probability": 0.0
        }


# =========================
# Transcribe All Chunks
# =========================
def transcribe_all(chunks: list[str],language: str = "en"):

    logger.info("Starting full transcription")

    transcripts = []

    all_segments = []

    detected_language = language

    for i, chunk in enumerate(chunks):

        logger.info(
            f"Transcribing chunk "
            f"{i+1}/{len(chunks)}"
        )

        result = transcribe_chunk(chunk, language)

        transcripts.append(result["text"])

        all_segments.extend(result["segments"])

        detected_language = (result["language"])

    full_transcript = " ".join(transcripts).strip()

    logger.info("Full transcription completed")

    return {

        "text": full_transcript,

        "segments": all_segments,

        "language": detected_language
    }