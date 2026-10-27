
from copy import deepcopy
from typing import Any

from src.transcription.normalizer import (
    NORMALIZATION_VERSION,
    normalize_transcript,
)


def process_transcript(transcript: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize a Day 23 transcript while preserving its metadata.

    Empty transcripts are marked as silence.
    Non-empty transcripts are marked as complete or partial.
    """
    if not isinstance(transcript, dict):
        raise TypeError("Transcript must be a dictionary.")

    required_fields = {
        "transcript_id",
        "candidate_id",
        "job_id",
        "question_id",
        "timestamp",
        "language",
        "transcript_text",
        "confidence",
    }

    missing_fields = required_fields - transcript.keys()
    if missing_fields:
        raise ValueError(
            f"Missing required transcript fields: {sorted(missing_fields)}"
        )

    result = deepcopy(transcript)

    original_text = result["transcript_text"]
    if not isinstance(original_text, str):
        raise TypeError("transcript_text must be a string.")

    cleaned_text = normalize_transcript(original_text)
    result["transcript_text"] = cleaned_text
    result["normalization_version"] = NORMALIZATION_VERSION

    # Normalize segment text without altering timings or confidence.
    if "segments" in result:
        if not isinstance(result["segments"], list):
            raise ValueError("segments must be a list.")

        for segment in result["segments"]:
            if not isinstance(segment, dict):
                raise ValueError("Each segment must be a dictionary.")

            if "text" not in segment or not isinstance(segment["text"], str):
                raise ValueError("Each segment must contain string text.")

            segment["text"] = normalize_transcript(segment["text"])

    # Status is returned separately so the Day 23 schema stays unchanged.
    if not cleaned_text:
        status = "silence"
    elif original_text.strip() and not original_text.rstrip().endswith(
        (".", "!", "?", ",", ";", ":")
    ):
        status = "partial"
    else:
        status = "complete"

    return {
        "transcript": result,
        "status": status,
    }
