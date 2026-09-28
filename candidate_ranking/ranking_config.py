"""
Configuration for candidate ranking and shortlisting.

Day 14:
Candidate Ranking & Shortlisting
"""


SHORTLIST_THRESHOLD = 70.0
REVIEW_THRESHOLD = 50.0


TOP_N_DEFAULT = 5


def validate_thresholds():
    """
    Validate the configured shortlisting thresholds.

    Returns:
        bool: True when the configuration is valid.

    Raises:
        ValueError: If thresholds are invalid.
    """

    if not 0 <= REVIEW_THRESHOLD <= 100:
        raise ValueError(
            "REVIEW_THRESHOLD must be between 0 and 100."
        )

    if not 0 <= SHORTLIST_THRESHOLD <= 100:
        raise ValueError(
            "SHORTLIST_THRESHOLD must be between 0 and 100."
        )

    if REVIEW_THRESHOLD >= SHORTLIST_THRESHOLD:
        raise ValueError(
            "REVIEW_THRESHOLD must be lower than "
            "SHORTLIST_THRESHOLD."
        )

    if TOP_N_DEFAULT <= 0:
        raise ValueError(
            "TOP_N_DEFAULT must be greater than 0."
        )

    return True
