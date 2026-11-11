# Day 26 - Screening Scoring Configuration

SCORING_WEIGHTS = {
    "clarity": 25,
    "relevance": 30,
    "completeness": 25,
    "consistency": 20
}

MAX_SCORE = 100

MIN_SCORE = 0

SCORING_PARAMETERS = {
    "clarity": {
        "weight": SCORING_WEIGHTS["clarity"],
        "description": "Measures how clearly the candidate communicates."
    },
    "relevance": {
        "weight": SCORING_WEIGHTS["relevance"],
        "description": "Measures how closely the answer matches the question."
    },
    "completeness": {
        "weight": SCORING_WEIGHTS["completeness"],
        "description": "Measures whether the required information is provided."
    },
    "consistency": {
        "weight": SCORING_WEIGHTS["consistency"],
        "description": "Measures whether the answer contains consistent information."
    }
}


def validate_scoring_weights():
    """Ensure scoring weights are valid and total 100."""
    if sum(SCORING_WEIGHTS.values()) != MAX_SCORE:
        raise ValueError("Scoring weights must add up to 100.")

    if any(weight < 0 for weight in SCORING_WEIGHTS.values()):
        raise ValueError("Scoring weights cannot be negative.")

    return True