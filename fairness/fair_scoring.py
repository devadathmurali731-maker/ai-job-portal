"""
Fair scoring integration layer.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Combine explicit keyword evidence with semantic evidence
and normalize the resulting score.

This module operates independently from the original ATS
scoring engine so the existing scoring pipeline remains intact.
"""

from typing import Dict

from fairness.keyword_reduction import calculate_balanced_score
from fairness.score_normalization import normalize_to_100


DEFAULT_KEYWORD_WEIGHT = 0.60
DEFAULT_SEMANTIC_WEIGHT = 0.40


def calculate_fair_skill_score(
    keyword_score: float,
    semantic_score: float,
    keyword_weight: float = DEFAULT_KEYWORD_WEIGHT,
    semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT,
) -> float:
    """
    Calculate a balanced skill score using both keyword
    and semantic evidence.

    Returns:
        float: Fair skill score on a 0-100 scale.
    """

    return calculate_balanced_score(
        keyword_score=keyword_score,
        semantic_score=semantic_score,
        keyword_weight=keyword_weight,
        semantic_weight=semantic_weight,
    )


def normalize_component_score(
    score: float,
    source_min: float = 0.0,
    source_max: float = 100.0,
) -> float:
    """
    Normalize a component score to the standard 0-100 range.
    """

    return normalize_to_100(
        score=score,
        source_min=source_min,
        source_max=source_max,
    )


def generate_fair_scoring_output(
    keyword_score: float,
    semantic_score: float,
    keyword_weight: float = DEFAULT_KEYWORD_WEIGHT,
    semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT,
) -> Dict[str, float]:
    """
    Generate an explainable fairness-aware scoring output.

    The output preserves both original evidence sources
    and the resulting balanced score.
    """

    fair_skill_score = calculate_fair_skill_score(
        keyword_score=keyword_score,
        semantic_score=semantic_score,
        keyword_weight=keyword_weight,
        semantic_weight=semantic_weight,
    )

    normalized_score = normalize_component_score(
        fair_skill_score
    )

    return {
        "keyword_score": round(float(keyword_score), 2),
        "semantic_score": round(float(semantic_score), 2),
        "keyword_weight": round(float(keyword_weight), 2),
        "semantic_weight": round(float(semantic_weight), 2),
        "fair_skill_score": fair_skill_score,
        "normalized_score": normalized_score,
    }