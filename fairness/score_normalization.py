"""
Score normalization utilities.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Convert scores from different ranges into a common
0-100 scale for consistent downstream evaluation.
"""


def normalize_score(
    score: float,
    source_min: float,
    source_max: float,
    target_min: float = 0.0,
    target_max: float = 100.0,
) -> float:
    """
    Normalize a score from one numerical range to another.

    Example:
        normalize_score(0.75, 0, 1)
        -> 75.0
    """

    if source_max <= source_min:
        raise ValueError(
            "source_max must be greater than source_min."
        )

    if target_max <= target_min:
        raise ValueError(
            "target_max must be greater than target_min."
        )

    if not source_min <= score <= source_max:
        raise ValueError(
            "score must fall within the source range."
        )

    normalized = (
        (score - source_min)
        / (source_max - source_min)
    ) * (target_max - target_min) + target_min

    return round(normalized, 2)


def normalize_to_100(
    score: float,
    source_min: float,
    source_max: float,
) -> float:
    """
    Normalize a score to the standard 0-100 range.
    """

    return normalize_score(
        score=score,
        source_min=source_min,
        source_max=source_max,
        target_min=0.0,
        target_max=100.0,
    )
