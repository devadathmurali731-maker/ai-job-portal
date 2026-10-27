
import re
import string
from typing import Optional

NORMALIZATION_VERSION = "1.1"

FILLER_WORDS = {
    "um",
    "uh",
    "erm",
    "er",
    "ah",
    "hmm",
    "mm",
}


def normalize_transcript(
    text: Optional[str],
    *,
    remove_fillers: bool = True,
    capitalize: bool = True,
) -> str:
    """
    Normalize speech-to-text output without inventing missing answers.

    Features:
    - Handles None and empty input.
    - Removes common filler words.
    - Normalizes whitespace and punctuation.
    - Capitalizes sentence beginnings.
    - Adds final punctuation when needed.
    - Preserves partial answers.
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        raise TypeError("Transcript text must be a string or None.")

    text = text.strip()

    if not text:
        return ""

    # Remove filler words as standalone words.
    if remove_fillers:
        fillers = "|".join(
            re.escape(word)
            for word in sorted(FILLER_WORDS, key=len, reverse=True)
        )

        text = re.sub(
            rf"(?i)(?<!\w)(?:{fillers})(?!\w)",
            "",
            text,
        )

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    # Remove spaces before punctuation.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)

    # Add spaces after punctuation only when needed.
    # Do not split repeated exclamation or question marks.
    text = re.sub(
        r"([,;:!?])(?=[^\s!?])",
        r"\1 ",
        text,
    )

    # Normalize spaces around periods.
    text = re.sub(r"\s*\.\s*", ". ", text).strip()

    # Collapse repeated punctuation.
    text = re.sub(r"([!?])\1+", r"\1", text)
    text = re.sub(r"\.{2,}", ".", text)

    # Clean up whitespace again.
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    # Capitalize the beginning of the transcript and sentences.
    if capitalize:
        text = text[0].upper() + text[1:]

        text = re.sub(
            r"(?<=[.!?]\s)([a-z])",
            lambda match: match.group(1).upper(),
            text,
        )

    # Add terminal punctuation when none exists.
    if text and text[-1] not in string.punctuation:
        text += "."

    return text
