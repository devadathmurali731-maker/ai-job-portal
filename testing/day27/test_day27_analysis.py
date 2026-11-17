
from src.confidence_analysis.confidence_analyzer import (
    analyze_confidence,
    analyze_response_length
)

from src.confidence_analysis.contradiction_detector import (
    detect_contradictions
)

from src.sentiment_analysis.sentiment_scorer import (
    analyze_sentiment
)

from src.confidence_analysis.communication_analyzer import (
    analyze_communication
)


def create_answer(
    answer_id="A001",
    text="I have strong skills in Python.",
    status="complete",
    confidence=1.0
):
    return {
        "answer_id": answer_id,
        "question_id": "Q001",
        "original_text": text,
        "answer_status": status,
        "intent": {
            "intent": "skills",
            "confidence": confidence
        },
        "entities": {
            "skills": ["Python"],
            "experience": {"value": None, "unit": None},
            "availability": {"value": None, "unit": None},
            "salary_expectation": {
                "amount": None,
                "currency": None,
                "period": None
            }
        }
    }


def test_confidence_analysis():
    answer = create_answer()
    result = analyze_confidence(
        answer["original_text"],
        answer
    )

    assert result["confidence_score"] == 85
    assert result["confidence_level"] == "High"


def test_hesitation_detection():
    answer = create_answer(text="Um, I think I can do it.")

    result = analyze_confidence(
        answer["original_text"],
        answer
    )

    assert result["hesitation_count"] >= 1


def test_uncertainty_detection():
    answer = create_answer(text="I am not sure about this.")

    result = analyze_confidence(
        answer["original_text"],
        answer
    )

    assert result["uncertainty_count"] >= 1


def test_response_length():
    result = analyze_response_length(
        "I have strong skills in Python."
    )

    assert result["word_count"] == 6
    assert result["length_category"] == "Moderate"


def test_positive_sentiment():
    result = analyze_sentiment(
        "I am confident, skilled and motivated."
    )

    assert result["sentiment_label"] == "Positive"
    assert result["positive_word_count"] == 3


def test_negative_sentiment():
    result = analyze_sentiment(
        "I struggled with a difficult problem."
    )

    assert result["sentiment_label"] == "Negative"
    assert result["negative_word_count"] == 2


def test_neutral_sentiment():
    result = analyze_sentiment(
        "I have three years of experience."
    )

    assert result["sentiment_label"] == "Neutral"


def test_contradiction_detection():
    answers = [
        {
            "answer_id": "A001",
            "question_id": "Q001",
            "entities": {
                "experience": {"value": 3, "unit": "years"},
                "salary_expectation": {
                    "amount": None,
                    "currency": None,
                    "period": None
                },
                "availability": {"value": None, "unit": None}
            }
        },
        {
            "answer_id": "A002",
            "question_id": "Q002",
            "entities": {
                "experience": {"value": 5, "unit": "years"},
                "salary_expectation": {
                    "amount": None,
                    "currency": None,
                    "period": None
                },
                "availability": {"value": None, "unit": None}
            }
        }
    ]

    result = detect_contradictions(answers)

    assert result["has_contradictions"] is True
    assert result["contradiction_count"] == 1


def test_no_contradictions():
    answers = [create_answer()]

    result = detect_contradictions(answers)

    assert result["has_contradictions"] is False


def test_communication_analysis():
    answers = [
        create_answer(),
        create_answer(
            answer_id="A002",
            text="I don't know.",
            status="vague",
            confidence=0
        )
    ]

    result = analyze_communication(answers)

    assert result["total_answers"] == 2
    assert 0 <= result["average_confidence_score"] <= 100
    assert "communication_strength" in result
    assert "behavioral_indicators" in result
