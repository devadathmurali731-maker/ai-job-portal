from role_similarity import (
    calculate_role_similarity
)


def test_similar_roles():

    result = calculate_role_similarity(
        "Data Analyst",
        "Business Intelligence Analyst"
    )

    assert result["similarity_score"] == 0.5

    assert set(
        result["shared_keywords"]
    ) == {
        "sql",
        "data analysis",
        "reporting",
        "visualization"
    }


def test_identical_roles():

    result = calculate_role_similarity(
        "Software Engineer",
        "Software Engineer"
    )

    assert result["similarity_score"] == 1.0


def test_different_roles():

    result = calculate_role_similarity(
        "Software Engineer",
        "Data Scientist"
    )

    assert result["similarity_score"] == 0.0
    assert result["shared_keywords"] == []


def test_unknown_role():

    result = calculate_role_similarity(
        "Marketing Manager",
        "Software Engineer"
    )

    assert result["similarity_score"] == 0.0
    assert result["shared_keywords"] == []