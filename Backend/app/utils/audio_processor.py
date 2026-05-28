# app/utils/audio_processor.py

import os
import uuid
import logging

import yt_dlp

from pydub import AudioSegment

from app.config.settings import (

    DOWNLOAD_DIR,

    CHUNK_DIR,

    CHUNK_MINUTES,

    AUDIO_SAMPLE_RATE,

    AUDIO_CHANNELS,

    YOUTUBE_AUDIO_QUALITY
)


# =========================
# Logger
# =========================
logger = logging.getLogger(__name__)


# =========================
# Create Directories
# =========================
os.makedirs(

    DOWNLOAD_DIR,

    exist_ok=True
)

os.makedirs(

    CHUNK_DIR,

    exist_ok=True
)


# =========================
# Download YouTube Audio
# =========================
def download_youtube_audio(
    url: str
) -> str:

    logger.info(
        "Downloading YouTube audio"
    )

    try:

        # Unique filename
        unique_id = str(
            uuid.uuid4()
        )

        output_path = os.path.join(

            DOWNLOAD_DIR,

            f"{unique_id}.%(ext)s"
        )

        ydl_opts = {

            "format":
                "bestaudio/best",

            "outtmpl":
                output_path,

            "postprocessors": [
                {
                    "key":
                        "FFmpegExtractAudio",

                    "preferredcodec":
                        "wav",

                    "preferredquality":
                        YOUTUBE_AUDIO_QUALITY,
                }
            ],

            "quiet":
                True,

            "no_warnings":
                True
        }

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = ydl.extract_info(

                url,

                download=True
            )

            filename = (

                os.path.splitext(

                    ydl.prepare_filename(
                        info
                    )
                )[0]

                + ".wav"
            )

        if not os.path.exists(
            filename
        ):

            raise Exception(
                "Downloaded audio file missing"
            )

        logger.info(
            "YouTube audio downloaded successfully"
        )

        return filename

    except Exception as e:

        logger.error(
            f"YouTube download failed: {e}"
        )

        raise Exception(
            "Failed to download YouTube audio"
        )


# =========================
# Convert To WAV
# =========================
def convert_to_wav(
    input_path: str
) -> str:

    logger.info(
        "Converting file to WAV"
    )

    try:

        if not os.path.exists(
            input_path
        ):

            raise FileNotFoundError(
                "Input file not found"
            )

        unique_id = str(
            uuid.uuid4()
        )

        output_path = os.path.join(

            DOWNLOAD_DIR,

            f"{unique_id}_converted.wav"
        )

        audio = AudioSegment.from_file(
            input_path
        )

        audio = (

            audio

            .set_channels(
                AUDIO_CHANNELS
            )

            .set_frame_rate(
                AUDIO_SAMPLE_RATE
            )
        )

        audio.export(

            output_path,

            format="wav"
        )

        logger.info(
            "Audio converted successfully"
        )

        return output_path

    except Exception as e:

        logger.error(
            f"Audio conversion failed: {e}"
        )

        raise Exception(
            "Failed to convert audio"
        )


# =========================
# Chunk Audio
# =========================
def chunk_audio(

    wav_path: str,

    chunk_minutes: int = CHUNK_MINUTES
) -> list[str]:

    logger.info(
        "Chunking audio"
    )

    try:

        if not os.path.exists(
            wav_path
        ):

            raise FileNotFoundError(
                "WAV file not found"
            )

        audio = AudioSegment.from_wav(
            wav_path
        )

        chunk_ms = (

            chunk_minutes

            * 60

            * 1000
        )

        chunks = []

        unique_id = str(
            uuid.uuid4()
        )

        for i, start in enumerate(

            range(
                0,
                len(audio),
                chunk_ms
            )
        ):

            chunk = audio[
                start:
                start + chunk_ms
            ]

            chunk_path = os.path.join(

                CHUNK_DIR,

                f"{unique_id}_chunk_{i}.wav"
            )

            chunk.export(

                chunk_path,

                format="wav"
            )

            chunks.append(
                chunk_path
            )

        logger.info(
            f"{len(chunks)} chunks created"
        )

        return chunks

    except Exception as e:

        logger.error(
            f"Audio chunking failed: {e}"
        )

        raise Exception(
            "Failed to chunk audio"
        )


# =========================
# Cleanup Temporary Files
# =========================
def cleanup_files(
    file_paths: list[str]
):

    for path in file_paths:

        try:

            if os.path.exists(path):

                os.remove(path)

        except Exception as e:

            logger.warning(
                f"Failed to remove "
                f"{path}: {e}"
            )


# =========================
# Process Input
# =========================
def process_input(
    source: str
) -> dict:

    wav_path = None

    downloaded_file = None

    try:

        # -------------------------
        # YouTube URL
        # -------------------------
        if source.startswith(
            ("https://", "http://")
        ):

            logger.info(
                "Detected YouTube URL"
            )

            wav_path = (
                download_youtube_audio(
                    source
                )
            )

            downloaded_file = wav_path

        # -------------------------
        # Local File
        # -------------------------
        else:

            logger.info(
                "Detected local file"
            )

            wav_path = convert_to_wav(
                source
            )

        # -------------------------
        # Chunk Audio
        # -------------------------
        chunks = chunk_audio(
            wav_path
        )

        logger.info(
            "Audio processing completed successfully"
        )

        return {

            "chunks":
                chunks,

            "wav_path":
                wav_path,

            "downloaded_file":
                downloaded_file
        }

    except Exception as e:

        logger.error(
            f"Audio processing failed: {e}"
        )

        # Cleanup on failure
        cleanup_targets = []

        if wav_path:
            cleanup_targets.append(
                wav_path
            )

        cleanup_files(
            cleanup_targets
        )

        raise Exception(
            f"Audio processing failed: {e}"
        )