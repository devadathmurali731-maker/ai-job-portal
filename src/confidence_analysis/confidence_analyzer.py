
import re


HESITATION_PHRASES = [
    "um", "uh", "umm", "hmm", "i think", "i guess",
    "maybe", "perhaps", "not sure", "i am not sure",
    "i'm not sure", "i don't know", "i do not know",
    "sort of", "kind of"
]

UNCERTAINTY_PHRASES = [
    "not sure", "i am unsure", "i'm unsure",
    "i don't know", "i do not know", "maybe",
    "perhaps", "might be", "could be", "possibly",
    "i think", "i guess"
]


def count_phrases(text: str, phrases: list) -> list:
    """Find matching hesitation or uncertainty phrases."""

    text = text.lower()
    matches = []

    for phrase in phrases:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        count = len(re.findall(pattern, text))

        if count:
            matches.extend([phrase] * count)

    return matches


def analyze_response_length(
    answer: str,
    duration_seconds: float = None
) -> dict:
    """Measure response length and speaking pace when duration exists."""

    words = answer.strip().split() if answer.strip() else []

    word_count = len(words)
    character_count = len(answer.strip())

    if word_count == 0:
        category = "Empty"
    elif word_count < 5:
        category = "Very Short"
    elif word_count <= 30:
        category = "Moderate"
    else:
        category = "Long"

    words_per_minute = None
    pace_status = "Unavailable: audio duration not provided."

    if duration_seconds is not None:
        if duration_seconds <= 0:
            raise ValueError("Audio duration must be greater than zero.")

        words_per_minute = round(
            word_count / (duration_seconds / 60),
            2
        )

        pace_status = "Measured from transcript and audio duration."

    return {
        "word_count": word_count,
        "character_count": character_count,
        "length_category": category,
        "duration_seconds": duration_seconds,
        "words_per_minute": words_per_minute,
        "pace_status": pace_status
    }


def analyze_confidence(
    answer: str,
    understanding_result: dict,
    duration_seconds: float = None
) -> dict:
    """
    Estimate communication confidence from text-based indicators.

    This is a heuristic signal, not a psychological assessment.
    """

    if not isinstance(answer, str):
        answer = ""

    hesitation_matches = count_phrases(
        answer,
        HESITATION_PHRASES
    )

    uncertainty_matches = count_phrases(
        answer,
        UNCERTAINTY_PHRASES
    )

    length_result = analyze_response_length(
        answer,
        duration_seconds
    )

    intent = understanding_result.get("intent", {})

    intent_confidence = float(
        intent.get("confidence", 0)
    )

    intent_confidence = max(
        0,
        min(1, intent_confidence)
    )

    status = understanding_result.get("answer_status")

    confidence_score = 70

    confidence_score -= len(hesitation_matches) * 5
    confidence_score -= len(uncertainty_matches) * 7

    confidence_score += intent_confidence * 15

    if status == "missing":
        confidence_score -= 40
    elif status == "off_topic":
        confidence_score -= 20
    elif status == "vague":
        confidence_score -= 15

    if length_result["word_count"] < 3:
        confidence_score -= 10

    confidence_score = round(
        max(0, min(100, confidence_score)),
        2
    )

    if confidence_score >= 80:
        confidence_level = "High"
    elif confidence_score >= 60:
        confidence_level = "Moderate"
    elif confidence_score >= 40:
        confidence_level = "Low"
    else:
        confidence_level = "Very Low"

    return {
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "hesitation_count": len(hesitation_matches),
        "hesitation_phrases": hesitation_matches,
        "uncertainty_count": len(uncertainty_matches),
        "uncertainty_phrases": uncertainty_matches,
        "response_length": length_result,
        "intent_confidence": intent_confidence,
        "explanation": (
            "Estimated from text-based hesitation, uncertainty, "
            "response length, intent confidence, and answer status."
        )
    }
