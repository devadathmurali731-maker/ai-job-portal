
import re


INTENT_KEYWORDS = {
    "skills": [
        "skills", "python", "java", "sql", "excel", "machine learning",
        "communication", "leadership", "programming", "data analysis"
    ],
    "experience": [
        "experience", "years", "months", "worked", "working",
        "company", "project", "professional", "internship"
    ],
    "availability": [
        "available", "availability", "joining", "notice period",
        "immediately", "join", "days", "weeks"
    ],
    "salary_expectation": [
        "salary", "expected", "expectation", "lpa", "lakhs",
        "compensation", "per annum", "package"
    ]
}


def classify_intent(answer: str) -> dict:
    """
    Classify a candidate's answer using keyword-based intent detection.
    Returns the detected intent and a confidence score.
    """

    if not isinstance(answer, str) or not answer.strip():
        return {
            "intent": "missing",
            "confidence": 1.0,
            "matched_keywords": []
        }

    text = answer.lower()
    scores = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        matched = [
            keyword for keyword in keywords
            if re.search(r"\b" + re.escape(keyword) + r"\b", text)
        ]
        scores[intent] = matched

    best_intent = max(scores, key=lambda key: len(scores[key]))
    matched_keywords = scores[best_intent]

    if not matched_keywords:
        return {
            "intent": "general",
            "confidence": 0.0,
            "matched_keywords": []
        }

    total_matches = sum(len(items) for items in scores.values())
    confidence = len(matched_keywords) / total_matches

    return {
        "intent": best_intent,
        "confidence": round(confidence, 2),
        "matched_keywords": matched_keywords
    }
