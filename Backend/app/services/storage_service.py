import os
import json


def save_transcript(meeting_id, transcript):

    os.makedirs("transcripts", exist_ok=True)

    transcript_path = (
        f"transcripts/meeting_{meeting_id}.txt"
    )

    with open(
        transcript_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(transcript)

    return transcript_path


def save_summary(meeting_id, data):

    os.makedirs("summaries", exist_ok=True)

    summary_path = (
        f"summaries/meeting_{meeting_id}.json"
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

    return summary_path