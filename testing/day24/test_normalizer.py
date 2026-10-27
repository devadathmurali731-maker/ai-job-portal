
import pytest

from src.transcription.normalizer import normalize_transcript


def test_removes_filler_words():
    assert normalize_transcript("um I work with Python uh") == "I work with Python."


def test_normalizes_whitespace_and_punctuation():
    assert normalize_transcript("  hello   ,world  !  ") == "Hello, world!"


def test_capitalizes_sentence_starts():
    assert normalize_transcript("hello. how are you? i am fine") == (
        "Hello. How are you? I am fine."
    )


def test_preserves_meaningful_words():
    assert normalize_transcript("I am a data analyst") == "I am a data analyst."


def test_handles_empty_and_silent_input():
    assert normalize_transcript("") == ""
    assert normalize_transcript("   ") == ""
    assert normalize_transcript(None) == ""


def test_preserves_partial_answer():
    assert normalize_transcript("because I used Python") == (
        "Because I used Python."
    )


def test_can_keep_fillers():
    assert normalize_transcript("um I think so", remove_fillers=False) == (
        "Um I think so."
    )


def test_rejects_non_string_input():
    with pytest.raises(TypeError):
        normalize_transcript(123)


def test_removes_repeated_punctuation():
    assert normalize_transcript("Great!!!") == "Great!"
