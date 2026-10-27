
from pathlib import Path
from typing import Any
from math import gcd

import numpy as np
import soundfile as sf
import torch
from scipy.signal import resample_poly
from transformers import pipeline


DEFAULT_MODEL = "openai/whisper-base"
WHISPER_SAMPLE_RATE = 16000


class SpeechToText:
    """CPU-compatible Whisper speech-to-text integration."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name
        self._recognizer: Any = None

    def _load_model(self) -> None:
        """Load Whisper only when speech transcription is requested."""
        if self._recognizer is None:
            self._recognizer = pipeline(
                task="automatic-speech-recognition",
                model=self.model_name,
                device=-1,
            )

    def _empty_result(self, sample_rate: int) -> dict[str, Any]:
        return {
            "text": "",
            "status": "silence",
            "model": self.model_name,
            "sample_rate": sample_rate,
            "segments": [],
        }

    def transcribe(self, audio_path: str | Path) -> dict[str, Any]:
        """Transcribe an audio file and return structured results."""
        path = Path(audio_path)

        if not path.is_file():
            raise FileNotFoundError(f"Audio file not found: {path}")

        audio, sample_rate = sf.read(
            path,
            dtype="float32",
            always_2d=True,
        )

        if audio.size == 0 or audio.shape[0] == 0:
            return self._empty_result(sample_rate)

        # Convert stereo or multichannel audio to mono.
        audio = audio.mean(axis=1)

        # Detect silence before loading the model.
        if float(np.max(np.abs(audio))) < 1e-4:
            return self._empty_result(sample_rate)

        # Resample to Whisper's expected 16 kHz without torchaudio.
        if sample_rate != WHISPER_SAMPLE_RATE:
            common = gcd(int(sample_rate), WHISPER_SAMPLE_RATE)
            up = WHISPER_SAMPLE_RATE // common
            down = int(sample_rate) // common
            audio = resample_poly(audio, up, down).astype(np.float32)

        self._load_model()

        feature_extractor = self._recognizer.feature_extractor
        model = self._recognizer.model
        tokenizer = self._recognizer.tokenizer

        inputs = feature_extractor(
            audio,
            sampling_rate=WHISPER_SAMPLE_RATE,
            return_tensors="pt",
        )

        input_features = inputs.input_features.to(model.device)

        with torch.inference_mode():
            generated = model.generate(input_features=input_features)

        text = tokenizer.batch_decode(
            generated,
            skip_special_tokens=True,
        )[0].strip()

        return {
            "text": text,
            "status": "complete" if text else "silence",
            "model": self.model_name,
            "sample_rate": WHISPER_SAMPLE_RATE,
            "segments": [],
        }
