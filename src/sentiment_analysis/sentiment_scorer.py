
import re


POSITIVE_WORDS = [
    "confident",
    "strong",
    "excellent",
    "good",
    "success",
    "successful",
    "achieved",
    "improved",
    "effective",
    "skilled",
    "experienced",
    "motivated",
    "passionate",
    "enjoy",
    "love",
    "capable",
    "proficient",
    "positive",
    "completed",
    "contributed"
]


NEGATIVE_WORDS = [
    "difficult",
    "weak",
    "failed",
    "failure",
    "problem",
    "challenge",
    "unable",
    "struggle",
    "poor",
    "negative",
    "worried",
    "afraid",
    "disappointed",
    "mistake",
    "lack",
    "confused",
    "uncertain",
    "nervous",
    "unfortunately",
    "regret"
]


def count_sentiment_words(text: str, word_list: list) -> list:
    """Count positive or negative words in the response."""

    text = text.lower()
    matches = []

    for word in word_list:
        pattern = r"\b" + re.escape(word) + r"\b"
        count = len(re.findall(pattern, text))

        if count:
            matches.extend([word] * count)

    return matches


def analyze_sentiment(answer: str) -> dict:
    """
    Estimate sentiment using a simple positive and negative
    vocabulary-based scoring approach.
    """

    if not isinstance(answer, str):
        answer = ""

    positive_matches = count_sentiment_words(
        answer,
        POSITIVE_WORDS
    )

    negative_matches = count_sentiment_words(
        answer,
        NEGATIVE_WORDS
    )

    positive_count = len(positive_matches)
    negative_count = len(negative_matches)

    sentiment_score = 50 + (
        positive_count - negative_count
    ) * 10

    sentiment_score = round(
        max(0, min(100, sentiment_score)),
        2
    )

    if sentiment_score >= 60:
        sentiment_label = "Positive"
    elif sentiment_score <= 40:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return {
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment_label,
        "positive_word_count": positive_count,
        "negative_word_count": negative_count,
        "positive_words": positive_matches,
        "negative_words": negative_matches,
        "explanation": (
            "Sentiment is estimated using a predefined "
            "positive and negative vocabulary."
        )
    }
