"""
Bias indicator evaluation utilities.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Measure potential bias indicators in candidate scoring data.

These metrics are diagnostic indicators. They do not prove
the presence or absence of discrimination.
"""

from typing import Dict, List


def calculate_score_gap(
    group_a_scores: List[float],
    group_b_scores: List[float],
) -> float:
    """
    Calculate the difference between two groups' average scores.
    """

    if not group_a_scores or not group_b_scores:
        raise ValueError("Both groups must contain scores.")

    average_a = sum(group_a_scores) / len(group_a_scores)
    average_b = sum(group_b_scores) / len(group_b_scores)

    return round(abs(average_a - average_b), 2)


def calculate_average_score(scores: List[float]) -> float:
    """
    Calculate the average candidate score.
    """

    if not scores:
        raise ValueError("scores cannot be empty.")

    return round(sum(scores) / len(scores), 2)


def calculate_score_distribution(
    scores: List[float],
) -> Dict[str, float]:
    """
    Calculate basic score-distribution statistics.
    """

    if not scores:
        raise ValueError("scores cannot be empty.")

    average = sum(scores) / len(scores)

    minimum = min(scores)
    maximum = max(scores)

    return {
        "count": len(scores),
        "average": round(average, 2),
        "minimum": round(minimum, 2),
        "maximum": round(maximum, 2),
    }


def calculate_keyword_semantic_gap(
    keyword_scores: List[float],
    semantic_scores: List[float],
) -> float:
    """
    Measure the difference between average keyword and
    semantic scores.

    A large gap indicates that the two evidence sources
    behave differently and may warrant further investigation.
    """

    if not keyword_scores or not semantic_scores:
        raise ValueError(
            "Both keyword and semantic scores are required."
        )

    keyword_average = (
        sum(keyword_scores) / len(keyword_scores)
    )

    semantic_average = (
        sum(semantic_scores) / len(semantic_scores)
    )

    return round(
        abs(keyword_average - semantic_average),
        2,
    )
