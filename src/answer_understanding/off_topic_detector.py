
import re

from src.answer_understanding.intent_classifier import (
    classify_intent,
    INTENT_KEYWORDS
)


QUESTION_INTENTS = {
    "skills": ["skills"],
    "experience": ["experience"],
    "availability": ["availability"],
    "salary": ["salary_expectation"],
    "salary_expectation": ["salary_expectation"]
}


def detect_off_topic(question_type: str, answer: str) -> dict:
    """Check whether an answer contains information relevant to its question."""

    if not isinstance(answer, str) or not answer.strip():
        return {
            "is_off_topic": False,
            "reason": "Answer is missing",
            "detected_intent": "missing"
        }

    expected_intents = QUESTION_INTENTS.get(
        question_type.lower(),
        []
    )

    detected = classify_intent(answer)

    if not expected_intents:
        return {
            "is_off_topic": False,
            "reason": "Unknown question type; relevance cannot be determined",
            "detected_intent": detected["intent"]
        }

    text = answer.lower()

    # Check for any expected intent, even when the answer contains
    # several different types of information.
    for intent in expected_intents:
        for keyword in INTENT_KEYWORDS[intent]:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                return {
                    "is_off_topic": False,
                    "reason": "Answer contains relevant information",
                    "detected_intent": detected["intent"]
                }

    return {
        "is_off_topic": True,
        "reason": "Answer does not contain recognizable information for the expected category",
        "detected_intent": detected["intent"]
    }
