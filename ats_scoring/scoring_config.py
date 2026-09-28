"""
Role-specific ATS scoring configuration.

Each role uses the same four scoring components,
but the importance of each component can vary by role.
"""

ROLE_WEIGHTS = {
    "Data Scientist": {
        "skill_match": 0.40,
        "experience_relevance": 0.20,
        "education_alignment": 0.15,
        "semantic_similarity": 0.25
    },

    "Software Engineer": {
        "skill_match": 0.40,
        "experience_relevance": 0.25,
        "education_alignment": 0.10,
        "semantic_similarity": 0.25
    },

    "Machine Learning Engineer": {
        "skill_match": 0.45,
        "experience_relevance": 0.20,
        "education_alignment": 0.10,
        "semantic_similarity": 0.25
    },

    "Data Analyst": {
        "skill_match": 0.40,
        "experience_relevance": 0.25,
        "education_alignment": 0.10,
        "semantic_similarity": 0.25
    },

    "HR Executive": {
        "skill_match": 0.35,
        "experience_relevance": 0.30,
        "education_alignment": 0.20,
        "semantic_similarity": 0.15
    },

    "Business Analyst": {
        "skill_match": 0.35,
        "experience_relevance": 0.25,
        "education_alignment": 0.15,
        "semantic_similarity": 0.25
    }
}


def get_role_weights(role):
    """
    Return scoring weights for a specific role.
    """

    if role not in ROLE_WEIGHTS:
        raise ValueError(
            f"No scoring configuration found for role: {role}"
        )

    weights = ROLE_WEIGHTS[role].copy()

    total = sum(weights.values())

    if abs(total - 1.0) > 1e-9:
        raise ValueError(
            f"Weights for {role} must sum to 1.0. "
            f"Current total: {total}"
        )

    return weights
