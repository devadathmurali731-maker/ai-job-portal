
import copy

import pytest

from src.transcription.transcript_processor import process_transcript


@pytest.fixture
def sample_transcript():
    return {
        "transcript_id": "TR-024",
        "candidate_id": "CAN-001",
        "job_id": "JOB-001",
        "question_id": "Q-001",
        "timestamp": "2026-10-26T06:30:00Z",
        "language": "en",
        "transcript_text": "um i have three years of experience",
        "confidence": 0.96,
        "normalization_version": "1.0",
        "source": "speech_to_text",
        "segments": [
            {
                "text": "um i have three years",
                "start_seconds": 0.0,
                "end_seconds": 2.1,
                "confidence": 0.97,
            }
        ],
    }


def test_normalizes_transcript_text(sample_transcript):
    result = process_transcript(sample_transcript)

    assert result["transcript"]["transcript_text"] == (
        "I have three years of experience."
    )


def test_preserves_transcript_metadata(sample_transcript):
    result = process_transcript(sample_transcript)
    transcript = result["transcript"]

    assert transcript["transcript_id"] == "TR-024"
    assert transcript["candidate_id"] == "CAN-001"
    assert transcript["job_id"] == "JOB-001"
    assert transcript["question_id"] == "Q-001"
    assert transcript["timestamp"] == "2026-10-26T06:30:00Z"
    assert transcript["confidence"] == 0.96
    assert transcript["source"] == "speech_to_text"


def test_normalizes_segments_and_preserves_timing(sample_transcript):
    result = process_transcript(sample_transcript)
    segment = result["transcript"]["segments"][0]

    assert segment["text"] == "I have three years."
    assert segment["start_seconds"] == 0.0
    assert segment["end_seconds"] == 2.1
    assert segment["confidence"] == 0.97


def test_sets_normalization_version(sample_transcript):
    result = process_transcript(sample_transcript)

    assert result["transcript"]["normalization_version"] == "1.1"


def test_does_not_modify_original_transcript(sample_transcript):
    original = copy.deepcopy(sample_transcript)

    process_transcript(sample_transcript)

    assert sample_transcript == original


def test_detects_silence(sample_transcript):
    sample_transcript["transcript_text"] = "   "
    result = process_transcript(sample_transcript)

    assert result["status"] == "silence"
    assert result["transcript"]["transcript_text"] == ""


def test_detects_partial_answer(sample_transcript):
    sample_transcript["transcript_text"] = "because I used Python"
    result = process_transcript(sample_transcript)

    assert result["status"] == "partial"


def test_rejects_missing_required_fields(sample_transcript):
    del sample_transcript["candidate_id"]

    with pytest.raises(ValueError, match="Missing required"):
        process_transcript(sample_transcript)


def test_rejects_non_dictionary_input():
    with pytest.raises(TypeError):
        process_transcript("not a transcript")


def test_handles_transcript_without_segments(sample_transcript):
    sample_transcript.pop("segments")

    result = process_transcript(sample_transcript)

    assert "segments" not in result["transcript"]
    assert result["transcript"]["transcript_text"] == (
        "I have three years of experience."
    )
