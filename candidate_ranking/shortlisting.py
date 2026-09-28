"""
Candidate Shortlisting Module.

Day 14:
Candidate Ranking & Shortlisting

Applies configurable ATS score thresholds to ranked
candidates and assigns a workflow decision.
"""


from candidate_ranking.ranking_config import (
    REVIEW_THRESHOLD,
    SHORTLIST_THRESHOLD,
    validate_thresholds,
)


def classify_candidate(score):
    """
    Classify a candidate based on ATS score.

    Args:
        score (float): ATS score from 0 to 100.

    Returns:
        str: SHORTLIST, REVIEW, or REJECT.

    Raises:
        ValueError: If score is outside 0-100.
    """

    validate_thresholds()

    if not isinstance(score, (int, float)):
        raise ValueError(
            "Candidate score must be numeric."
        )

    if not 0 <= score <= 100:
        raise ValueError(
            "Candidate score must be between 0 and 100."
        )

    if score >= SHORTLIST_THRESHOLD:
        return "SHORTLIST"

    if score >= REVIEW_THRESHOLD:
        return "REVIEW"

    return "REJECT"


def get_decision_reason(decision):
    """
    Return a recruiter-friendly explanation for a decision.

    Args:
        decision (str): Candidate decision.

    Returns:
        str: Explanation of the workflow zone.
    """

    reasons = {
        "SHORTLIST": (
            "ATS score meets or exceeds the configured "
            "shortlisting threshold."
        ),
        "REVIEW": (
            "ATS score falls within the configured "
            "manual review range."
        ),
        "REJECT": (
            "ATS score is below the configured review "
            "threshold."
        ),
    }

    if decision not in reasons:
        raise ValueError(
            f"Unknown decision: {decision}"
        )

    return reasons[decision]


def apply_shortlisting(ranked_candidates):
    """
    Apply shortlisting decisions to ranked candidates.

    Args:
        ranked_candidates (list): Ranked candidate records.

    Returns:
        list: Candidates with decision and reason fields.
    """

    shortlisted_candidates = []

    for candidate in ranked_candidates:
        score = candidate["ats_score"]

        decision = classify_candidate(score)

        candidate_result = candidate.copy()

        candidate_result["decision"] = decision
        candidate_result["decision_reason"] = (
            get_decision_reason(decision)
        )

        shortlisted_candidates.append(candidate_result)

    return shortlisted_candidates


def summarize_decisions(candidates):
    """
    Count candidates in each decision category.

    Args:
        candidates (list): Candidates with decision fields.

    Returns:
        dict: Decision counts.
    """

    summary = {
        "SHORTLIST": 0,
        "REVIEW": 0,
        "REJECT": 0,
    }

    for candidate in candidates:
        decision = candidate["decision"]

        if decision not in summary:
            raise ValueError(
                f"Unknown decision: {decision}"
            )

        summary[decision] += 1

    return summary