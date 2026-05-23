# core/transcriber.py

from faster_whisper import WhisperModel
import os

from dotenv import load_dotenv

load_dotenv()

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_whisper_model():
    """
    Loads the Whisper model once
    and reuses it for all transcriptions.
    """

    global _model

    if _model is None:
        print(f"Loading Model... {WHISPER_MODEL}")

        _model = WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )

        print("Whisper model loaded successfully")

    return _model


def transcribe_chunk(chunk_path: str, language: str = "en") -> str:

    try:

        print(f"Processing: {chunk_path}")

        model = load_whisper_model()

        segments, info = model.transcribe(
            chunk_path,
            beam_size=1,
            vad_filter=True,
            language=language
        )

        text = " ".join(
            [segment.text for segment in segments]
        )

        print(f"Finished: {chunk_path}")

        return text.strip()

    except Exception as e:

        print(
            f"Error transcribing "
            f"{chunk_path}: {e}"
        )

        return ""


def transcribe_all(chunks: list[str], language: str = "en") -> str:

    transcripts = []

    print("Using Faster-Whisper for transcription")

    for i, chunk in enumerate(chunks):

        print(
            f"Transcribing chunk "
            f"{i+1}/{len(chunks)}"
        )

        text = transcribe_chunk(chunk, language)

        transcripts.append(text)

    print("Transcription completed")

    return " ".join(transcripts).strip()