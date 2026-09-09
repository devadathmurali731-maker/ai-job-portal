from ats_engine.ats_scorer import calculate_ats_score
from screening_ai.candidate_screening import screen_candidate


def test_ats_score():

    resume = """
    Python developer with SQL and
    Machine Learning experience.
    """

    skills = [
        "Python",
        "SQL",
        "Machine Learning"
    ]

    score = calculate_ats_score(
        resume,
        skills
    )

    assert score == 100.0


def test_candidate_screening():

    result = screen_candidate(80)

    assert result == "SHORTLISTED"
    