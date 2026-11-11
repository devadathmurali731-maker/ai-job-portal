
from src.screening_scoring.scoring_config import (
    SCORING_WEIGHTS,
    MAX_SCORE
)


def calculate_clarity(answer: str) -> tuple:
    """Evaluate answer clarity."""

    if not isinstance(answer, str) or not answer.strip():
        return 0, "Answer is missing."

    words = answer.strip().split()
    word_count = len(words)

    if word_count < 3:
        return 30, "Answer is too short to demonstrate sufficient clarity."

    if word_count < 8:
        return 60, "Answer communicates basic information but needs more detail."

    if word_count <= 60:
        return 100, "Answer is clearly expressed with sufficient detail."

    return 80, "Answer is understandable but may be unnecessarily lengthy."


def calculate_relevance(understanding_result: dict) -> tuple:
    """Evaluate whether the answer is relevant to the question."""

    status = understanding_result.get("answer_status")

    if status == "missing":
        return 0, "No answer was provided."

    if status == "off_topic" or understanding_result.get("is_off_topic", False):
        return 0, "Answer does not match the expected question category."

    if status == "vague":
        return 40, "Answer contains insufficient recognizable information."

    return 100, "Answer contains information relevant to the question."


def calculate_completeness(understanding_result: dict) -> tuple:
    """Evaluate whether the answer contains required information."""

    status = understanding_result.get("answer_status")

    if status == "missing":
        return 0, "Answer is missing."

    if status == "off_topic" or understanding_result.get("is_off_topic", False):
        return 0, "Off-topic answer does not provide the required information."

    if status == "vague":
        return 40, "Answer does not provide sufficient details."

    if understanding_result.get("missing_fields"):
        return 40, "Some required information is missing."

    return 100, "Required information is present."


def calculate_consistency(understanding_result: dict) -> tuple:
    """Check basic consistency using extracted information."""

    status = understanding_result.get("answer_status")

    if status == "missing":
        return 0, "Consistency cannot be evaluated because the answer is missing."

    entities = understanding_result.get("entities", {})

    experience = entities.get("experience", {})
    availability = entities.get("availability", {})
    salary = entities.get("salary_expectation", {})

    experience_value = experience.get("value")

    if experience_value is not None and experience_value < 0:
        return 0, "Experience duration cannot be negative."

    salary_amount = salary.get("amount")

    if salary_amount is not None and salary_amount < 0:
        return 0, "Salary expectation cannot be negative."

    availability_value = availability.get("value")

    if availability_value is not None and availability_value < 0:
        return 0, "Notice period cannot be negative."

    return 100, "No basic consistency issues were identified."


def normalize_score(raw_score: float) -> float:
    """Normalize a raw score to the 0-100 range."""

    return round(
        max(0, min(MAX_SCORE, raw_score)),
        2
    )


def score_question(
    answer: str,
    understanding_result: dict
) -> dict:
    """Calculate an explainable screening score for one question."""

    clarity, clarity_reason = calculate_clarity(answer)

    relevance, relevance_reason = calculate_relevance(
        understanding_result
    )

    completeness, completeness_reason = calculate_completeness(
        understanding_result
    )

    consistency, consistency_reason = calculate_consistency(
        understanding_result
    )

    component_scores = {
        "clarity": clarity,
        "relevance": relevance,
        "completeness": completeness,
        "consistency": consistency
    }

    explanations = {
        "clarity": clarity_reason,
        "relevance": relevance_reason,
        "completeness": completeness_reason,
        "consistency": consistency_reason
    }

    weighted_score = sum(
        component_scores[name] * weight / 100
        for name, weight in SCORING_WEIGHTS.items()
    )

    final_score = normalize_score(weighted_score)

    return {
        "question_id": understanding_result.get("question_id"),
        "answer_id": understanding_result.get("answer_id"),
        "scores": component_scores,
        "weights": SCORING_WEIGHTS.copy(),
        "weighted_score": final_score,
        "normalized_score": final_score,
        "explanations": explanations
    }
