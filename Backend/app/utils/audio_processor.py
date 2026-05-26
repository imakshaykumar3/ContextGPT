#app/utils/audio_processor.py
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
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

os.makedirs(CHUNK_DIR, exist_ok=True)


# =========================
# Download YouTube Audio
# =========================
def download_youtube_audio(url: str) -> str:

    logger.info("Downloading YouTube audio")

    try:

        # Generate unique filename
        unique_id = str(uuid.uuid4())

        output_path = os.path.join(
            DOWNLOAD_DIR,
            f"{unique_id}.%(ext)s"
        )

        ydl_opts = {

            "format": "bestaudio/best",

            "outtmpl": output_path,

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",

                    "preferredcodec": "wav",

                    "preferredquality":
                        YOUTUBE_AUDIO_QUALITY,
                }
            ],

            "quiet": True,

            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

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

        logger.info("YouTube audio downloaded successfully")

        return filename

    except Exception as e:

        logger.error(f"YouTube download failed: {e}")

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

        output_path = (
            os.path.splitext(
                input_path
            )[0]
            + "_converted.wav"
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

        audio = AudioSegment.from_wav(
            wav_path
        )

        chunk_ms = (
            chunk_minutes
            * 60
            * 1000
        )

        chunks = []

        base_name = os.path.splitext(
            os.path.basename(
                wav_path
            )
        )[0]

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
                f"{base_name}_chunk_{i}.wav"
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
# Process Input
# =========================
def process_input(
    source: str
) -> list[str]:

    try:

        # YouTube URL
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

        # Local File
        else:

            logger.info(
                "Detected local file"
            )

            wav_path = convert_to_wav(
                source
            )

        # Chunk audio
        chunks = chunk_audio(
            wav_path
        )

        logger.info(
            "Audio processing completed successfully"
        )

        return chunks

    except Exception as e:

        logger.error(
            f"Audio processing failed: {e}"
        )

        raise Exception(
            f"Audio processing failed: {e}"
        )