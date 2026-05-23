# #core/transcriber.py
# import whisper
# import os
# import requests
# import tempfile

# from dotenv import load_dotenv
# from pydub import AudioSegment

# load_dotenv()

# WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
# SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")
# SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
# SARVAM_PIECE_SECONDS = 25

# _model = None

# def load_whisper_model():
#     """Loads the Whisper model once and reuses it for all transcriptions."""
    
#     global _model

#     if _model is None:
#         print(f"Loading Model...{WHISPER_MODEL}")
#         _model = whisper.load_model(WHISPER_MODEL)
#         print("Whisper model loaded successfully")
    
#     return _model
    
# def transcribe_chunk_whisper(chunk_path:str, language:str = "en") -> str:

#     try:

#         print(f"Processing : {chunk_path}")

#         model = load_whisper_model()

#         result = model.transcribe(chunk_path, task = "transcribe", language=language, fp16=False)

#         print(f"Finished {chunk_path}")

#         return result['text'].strip()
    
#     except Exception as e:
#         print(
#             f"Errors transcribing "
#             f"{chunk_path}: {e}"
#         )

#         return ""

# # def _send_to_sarvam(piece_path: str):
# #     """Send one <=30s WAV file to Sarvam and return the English transcript"""
    
# #     headers = {"api-subscription-key": SARVAM_API_KEY}

# #     with open(piece_path, "rb") as f:
# #         files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
# #         data = {"model": SARVAM_MODEL, "with_diarization": "false"}

# #         response = requests.post(
# #             SARVAM_STT_TRANSLATE_URL,
# #             headers=headers,
# #             files=files,
# #             data=data,
# #             timeout=120
# #         )
    
# #     if not response.ok:
# #         raise RuntimeError(f"Sarvam API failed: {response.status_code} {response.text}")
    
# #     return response.json()["output"][0]["transcript"]
# def _send_to_sarvam(piece_path: str):

#     headers = {
#         "api-subscription-key": SARVAM_API_KEY
#     }

#     with open(piece_path, "rb") as f:

#         files = {
#             "file": (
#                 os.path.basename(piece_path),
#                 f,
#                 "audio/wav"
#             )
#         }

#         data = {
#             "model": SARVAM_MODEL,
#             "with_diarization": "false"
#         }

#         response = requests.post(
#             SARVAM_STT_TRANSLATE_URL,
#             headers=headers,
#             files=files,
#             data=data,
#             timeout=120
#         )

#     print("\n===== SARVAM RESPONSE =====")
#     print("Status Code:", response.status_code)
#     print("JSON:", response.json())
#     print("===========================\n")

#     if not response.ok:
#         raise RuntimeError(
#             f"Sarvam API failed: "
#             f"{response.status_code} {response.text}"
#         )

#     result = response.json()

#     return result["transcript"]
    
# def transcribe_chunk_sarvam(chunk_path: str) -> str:
#     """Sarvam sync API only accepts <=30s audio. We split this chunk into 25-seconds pieces, send each separately, and join the transcriptions"""
    
#     if not SARVAM_API_KEY:
#         raise RuntimeError("SARVAM_API_KEY is not set in the .env file")

#     audio = AudioSegment.from_wav(chunk_path)
#     piece_ms = int(SARVAM_PIECE_SECONDS * 1000)

#     pieces = []

#     total_pieces = (len(audio) + piece_ms - 1) // piece_ms

#     temp_dir = tempfile.mkdtemp()

#     for i in range(total_pieces):

#         start_ms = i * piece_ms
#         end_ms = start_ms + piece_ms

#         piece = audio[start_ms:end_ms]

#         piece_path = os.path.join(temp_dir, f"piece_{i}.wav")
#         piece.export(piece_path, format="wav")
#         pieces.append(piece_path)

#     transcriptions = []

#     for i, piece_path in enumerate(pieces):
#         print(f"Sending piece {i+1}/{len(pieces)} to Sarvam...")

#         try:
#             text = _send_to_sarvam(piece_path)
        
#             transcriptions.append(text)
     
#         finally:

#             if os.path.exists(piece_path):
#                 os.remove(piece_path)

#     return " ".join(transcriptions).strip()

# def transcribe_chunk(chunk_path: str, language: str = "en") -> str:
#     """
#     Route one chunk to Whisper or Sarvam depending on language choice.
#     - english  → Whisper (local model)
#     - hinglish → Sarvam (translates to English while transcribing)
#     """
#     if language.lower() == "hinglish":
#         return transcribe_chunk_sarvam(chunk_path)
#     return transcribe_chunk_whisper(chunk_path, language=language)

# def transcribe_all(chunks : list[str], language: str = "en") -> str:

#     transcripts = []

#     engine = "Sarvam AI" if language.lower() == "hinglish" else "whisper"
#     print(f"Using {engine} for transcription")

#     for i, chunk in enumerate(chunks):

#         print(
#             f"Transcribing chunk "
#             f"{i+1}/{len(chunks)}"
#         )

#         text = transcribe_chunk(chunk, language=language)
        
#         transcripts.append(text)

#     print("Transcription completed")

#     return " ".join(transcripts).strip()



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

        text = transcribe_chunk(chunk, language=language)

        transcripts.append(text)

    print("Transcription completed")

    return " ".join(transcripts).strip()