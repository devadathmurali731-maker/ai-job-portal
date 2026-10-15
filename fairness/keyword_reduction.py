"""
Keyword-dependence reduction utilities.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Reduce excessive dependence on exact keyword matching by
combining explicit keyword evidence with semantic evidence.
"""

from typing import Union


DEFAULT_KEYWORD_WEIGHT = 0.60
DEFAULT_SEMANTIC_WEIGHT = 0.40


def validate_score(score: Union[int, float]) -> float:
    """
    Validate and normalize a score to the range 0-100.
    """

    if not isinstance(score, (int, float)):
        raise TypeError("score must be numeric.")

    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100.")

    return float(score)


def calculate_balanced_score(
    keyword_score: Union[int, float],
    semantic_score: Union[int, float],
    keyword_weight: float = DEFAULT_KEYWORD_WEIGHT,
    semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT,
) -> float:
    """
    Combine keyword and semantic evidence into a balanced score.

    Both component scores must be between 0 and 100.

    The weights must be non-negative and sum to 1.
    """

    keyword_score = validate_score(keyword_score)
    semantic_score = validate_score(semantic_score)

    if keyword_weight < 0 or semantic_weight < 0:
        raise ValueError("Weights cannot be negative.")

    total_weight = keyword_weight + semantic_weight

    if total_weight <= 0:
        raise ValueError("At least one weight must be greater than zero.")

    # Normalize weights so the function remains safe even if
    # the supplied weights do not sum exactly to 1.
    keyword_weight = keyword_weight / total_weight
    semantic_weight = semantic_weight / total_weight

    balanced_score = (
        keyword_score * keyword_weight
        + semantic_score * semantic_weight
    )

    return round(balanced_score, 2)


def calculate_keyword_dependence(
    keyword_score: Union[int, float],
    semantic_score: Union[int, float],
) -> float:
    """
    Measure the absolute difference between keyword and
    semantic evidence.

    A larger difference indicates greater disagreement between
    the two evidence sources.
    """

    keyword_score = validate_score(keyword_score)
    semantic_score = validate_score(semantic_score)

    return round(abs(keyword_score - semantic_score), 2)
