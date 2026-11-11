
import pytest

from src.screening_scoring.question_scorer import (
    score_question,
    normalize_score
)

from src.screening_scoring.screening_scoring_engine import (
    calculate_screening_score
)


def create_sample_result(status="complete", off_topic=False):
    return {
        "question_id": "Q001",
        "answer_id": "A001",
        "answer_status": status,
        "is_off_topic": off_topic,
        "missing_fields": [],
        "entities": {
            "skills": ["Python"],
            "experience": {"value": 3, "unit": "years"},
            "availability": {
                "type": None,
                "value": None,
                "unit": None
            },
            "salary_expectation": {
                "amount": None,
                "currency": None,
                "period": None
            }
        }
    }


def test_complete_answer_scoring():
    answer = "I have 3 years of experience in Python and SQL."
    result = score_question(answer, create_sample_result())

    assert result["normalized_score"] == 100


def test_missing_answer_scoring():
    result = create_sample_result("missing")
    score = score_question("", result)

    assert score["normalized_score"] == 0


def test_off_topic_answer_relevance():
    result = create_sample_result("off_topic", True)
    score = score_question("I like music.", result)

    assert score["scores"]["relevance"] == 0


def test_off_topic_answer_completeness():
    result = create_sample_result("off_topic", True)
    score = score_question("I like music.", result)

    assert score["scores"]["completeness"] == 0


def test_vague_answer_completeness():
    result = create_sample_result("vague")
    score = score_question("I am good.", result)

    assert score["scores"]["completeness"] == 40


def test_score_normalization():
    assert normalize_score(120) == 100
    assert normalize_score(-10) == 0
    assert normalize_score(75) == 75


def test_overall_screening_score():
    results = [
        {
            "normalized_score": 80,
            "scores": {
                "clarity": 80,
                "relevance": 90,
                "completeness": 70,
                "consistency": 80
            }
        },
        {
            "normalized_score": 100,
            "scores": {
                "clarity": 100,
                "relevance": 100,
                "completeness": 100,
                "consistency": 100
            }
        }
    ]

    final = calculate_screening_score(results)

    assert final["overall_screening_score"] == 90
    assert final["performance_level"] == "Excellent"


def test_empty_screening_results():
    result = calculate_screening_score([])

    assert result["total_questions"] == 0
    assert result["overall_screening_score"] == 0


def test_per_question_explanations():
    answer = "I have 3 years of experience in Python."
    result = score_question(answer, create_sample_result())

    assert len(result["explanations"]) == 4
    assert all(result["explanations"].values())
