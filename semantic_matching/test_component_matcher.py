import pytest

from component_matcher import ComponentMatcher


@pytest.fixture(scope="module")
def matcher():
    return ComponentMatcher()


def test_component_matcher_initialization(matcher):
    assert matcher.embedding_engine is not None
    assert matcher.similarity_scorer is not None


def test_component_similarity_returns_valid_score(matcher):
    resume_component = """
    Python, SQL, machine learning and pandas experience.
    """

    jd_component = """
    Required skills include Python, SQL, machine learning
    and pandas.
    """

    score = matcher.calculate_component_similarity(
        resume_component,
        jd_component
    )

    assert isinstance(score, float)
    assert -1.0 <= score <= 1.0


def test_relevant_component_has_higher_similarity(matcher):
    resume_component = """
    Python developer with machine learning,
    SQL and data analysis experience.
    """

    relevant_jd_component = """
    Candidate should have Python, machine learning,
    SQL and data analysis experience.
    """

    unrelated_jd_component = """
    Candidate should have graphic design,
    illustration, typography and visual design experience.
    """

    relevant_score = matcher.calculate_component_similarity(
        resume_component,
        relevant_jd_component
    )

    unrelated_score = matcher.calculate_component_similarity(
        resume_component,
        unrelated_jd_component
    )

    assert relevant_score > unrelated_score


def test_compare_components_returns_all_components(matcher):
    resume_components = {
        "skills": "Python, SQL and machine learning.",
        "experience": "Developed machine learning applications.",
        "projects": "Built a customer churn prediction project."
    }

    jd_components = {
        "skills": "Python, SQL and machine learning required.",
        "experience": "Experience building machine learning solutions.",
        "projects": "Predictive modeling projects are preferred."
    }

    results = matcher.compare_components(
        resume_components,
        jd_components
    )

    assert "skills" in results
    assert "experience" in results
    assert "projects" in results


def test_missing_resume_component_rejected(matcher):
    resume_components = {
        "skills": "Python and SQL.",
        "experience": "Data analysis experience."
    }

    jd_components = {
        "skills": "Python and SQL required.",
        "experience": "Data analysis experience required.",
        "projects": "Machine learning projects preferred."
    }

    with pytest.raises(KeyError):
        matcher.compare_components(
            resume_components,
            jd_components
        )


def test_missing_jd_component_rejected(matcher):
    resume_components = {
        "skills": "Python and SQL.",
        "experience": "Data analysis experience.",
        "projects": "Machine learning project."
    }

    jd_components = {
        "skills": "Python and SQL required.",
        "experience": "Data analysis experience required."
    }

    with pytest.raises(KeyError):
        matcher.compare_components(
            resume_components,
            jd_components
        )


def test_empty_component_rejected(matcher):
    with pytest.raises(ValueError):
        matcher.calculate_component_similarity(
            "",
            "Python and SQL experience."
        )


def test_invalid_component_type_rejected(matcher):
    with pytest.raises(TypeError):
        matcher.calculate_component_similarity(
            123,
            "Python and SQL experience."
        )
        