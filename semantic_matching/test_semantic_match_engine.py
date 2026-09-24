import pytest

from semantic_match_engine import SemanticMatchEngine


@pytest.fixture(scope="module")
def engine():
    return SemanticMatchEngine()


def test_engine_initialization(engine):
    assert engine.component_matcher is not None
    assert engine.data_extractor is not None


def test_weighted_score_with_all_components(engine):
    component_scores = {
        "skills": 0.80,
        "experience": 0.70,
        "projects": 0.60
    }

    available_components = [
        "skills",
        "experience",
        "projects"
    ]

    score = engine.calculate_weighted_score(
        component_scores,
        available_components
    )

    expected_score = (
        (0.80 * 0.50)
        + (0.70 * 0.30)
        + (0.60 * 0.20)
    )

    assert score == pytest.approx(
        expected_score
    )


def test_weighted_score_without_projects(engine):
    component_scores = {
        "skills": 0.80,
        "experience": 0.60
    }

    available_components = [
        "skills",
        "experience"
    ]

    score = engine.calculate_weighted_score(
        component_scores,
        available_components
    )

    expected_score = (
        (0.80 * 0.625)
        + (0.60 * 0.375)
    )

    assert score == pytest.approx(
        expected_score
    )


def test_weighted_score_requires_component(engine):
    with pytest.raises(ValueError):
        engine.calculate_weighted_score(
            {},
            []
        )


def test_real_resume_jd_matching(engine):
    result = engine.match_resume_to_jd(
        "resume_001",
        "jd_001_data_scientist"
    )

    assert result["resume_id"] == "resume_001"

    assert (
        result["jd_id"]
        == "jd_001_data_scientist"
    )

    assert "skills" in result["component_scores"]

    assert "experience" in result["component_scores"]

    assert (
        "projects"
        not in result["component_scores"]
    )

    assert (
        result["final_semantic_score"]
        >= -1.0
    )

    assert (
        result["final_semantic_score"]
        <= 1.0
    )


def test_missing_projects_are_handled(engine):
    result = engine.match_resume_to_jd(
        "resume_001",
        "jd_001_data_scientist"
    )

    assert (
        "projects"
        not in result["available_components"]
    )

    assert (
        "projects"
        not in result["component_scores"]
    )
    