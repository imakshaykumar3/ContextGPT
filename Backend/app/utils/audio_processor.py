#utils/audio_processor.py
import yt_dlp
from pydub import AudioSegment
import os

DOWNNLOAD_DIR = "downloads"
CHUNK_DIR = "chunks"

os.makedirs(DOWNNLOAD_DIR,exist_ok=True)
os.makedirs(CHUNK_DIR, exist_ok=True)


def download_youtube_audio(url:str) -> str:
    """Download YouTube audio as WAV"""
    output_path = os.path.join(DOWNNLOAD_DIR,"%(title)s.%(ext)s")

    ydl_opts = {
        "format":"bestaudio/best",
        "outtmpl":output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet":True,
        "no_warnings":True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url,download=True)
        filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".wav"

    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file into mono 16kHz WAV fromat using pydub"""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  #16kHz
    audio.export(output_path,format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int=10) -> list[str]:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    base_name = os.path.splitext(os.path.basename(wav_path))[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = os.path.join(CHUNK_DIR, f"{base_name}_chunk_{i}.wav")
        chunk.export(chunk_path, format = "wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:

    try:
        if source.startswith(("https://", "http://")):
            print("Detected YouTube URL. Downloading audio...")
            wav_path = download_youtube_audio(source)

        else:
            print("Detected local file. Converting to WAV...")
            wav_path = convert_to_wav(source)
        
        print("Chunking audio...")
        chunks = chunk_audio(wav_path)
        print(f"Audio ready - {len(chunks)} chunk(s) created.")
        return chunks
    
    except Exception as e:
        print(f"Error: {e}")

        return []