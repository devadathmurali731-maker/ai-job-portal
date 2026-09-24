import pytest

from semantic_matcher import SemanticMatcher


@pytest.fixture(scope="module")
def matcher():
    return SemanticMatcher()


def test_semantic_matcher_initialization(matcher):
    assert matcher.embedding_engine is not None
    assert matcher.similarity_scorer is not None


def test_resume_jd_similarity(matcher):
    resume_text = """
    Software Engineer with experience in Python, SQL,
    REST APIs, Docker and database development.
    """

    job_description = """
    Looking for a Software Engineer with Python, SQL,
    API development, Docker and database skills.
    """

    score = matcher.calculate_similarity(
        resume_text,
        job_description
    )

    assert isinstance(score, float)
    assert -1.0 <= score <= 1.0


def test_similar_resume_and_jd_have_higher_similarity(matcher):
    resume_text = """
    Python developer with machine learning,
    data analysis and SQL experience.
    """

    relevant_jd = """
    We need a machine learning engineer with Python,
    SQL and data analysis experience.
    """

    unrelated_jd = """
    We need a graphic designer with expertise in
    visual design, typography and illustration.
    """

    relevant_score = matcher.calculate_similarity(
        resume_text,
        relevant_jd
    )

    unrelated_score = matcher.calculate_similarity(
        resume_text,
        unrelated_jd
    )

    assert relevant_score > unrelated_score


def test_empty_resume_rejected(matcher):
    with pytest.raises(ValueError):
        matcher.calculate_similarity(
            "",
            "Software Engineer with Python experience."
        )


def test_empty_jd_rejected(matcher):
    with pytest.raises(ValueError):
        matcher.calculate_similarity(
            "Python developer with experience.",
            ""
        )
        