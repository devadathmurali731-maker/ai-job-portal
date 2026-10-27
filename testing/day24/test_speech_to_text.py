import numpy as np
import pytest
import soundfile as sf

from src.transcription.speech_to_text import SpeechToText


def test_missing_audio_file_raises_error(tmp_path):
    recognizer = SpeechToText()
    with pytest.raises(FileNotFoundError):
        recognizer.transcribe(tmp_path / "missing.wav")


def test_silent_audio_returns_silence(tmp_path):
    audio_path = tmp_path / "silence.wav"
    sf.write(audio_path, np.zeros(16000, dtype=np.float32), 16000)

    result = SpeechToText().transcribe(audio_path)

    assert result["text"] == ""
    assert result["status"] == "silence"
    assert result["sample_rate"] == 16000


def test_near_silent_audio_returns_silence(tmp_path):
    audio_path = tmp_path / "quiet.wav"
    sf.write(
        audio_path,
        np.full(16000, 1e-6, dtype=np.float32),
        16000,
    )

    result = SpeechToText().transcribe(audio_path)

    assert result["status"] == "silence"


def test_stereo_silence_returns_silence(tmp_path):
    audio_path = tmp_path / "stereo.wav"
    sf.write(
        audio_path,
        np.zeros((16000, 2), dtype=np.float32),
        16000,
    )

    result = SpeechToText().transcribe(audio_path)

    assert result["status"] == "silence"


def test_model_load_is_lazy():
    recognizer = SpeechToText()
    assert recognizer._recognizer is None
