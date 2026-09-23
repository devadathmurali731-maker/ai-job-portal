from education_relevance import (
    normalize_text,
    calculate_field_relevance,
    calculate_degree_level_score,
    calculate_education_relevance,
    calculate_education_relevance_for_all
)


def test_normalize_text():
    assert normalize_text("  Computer Science  ") == "computer science"


def test_calculate_field_relevance():
    result = calculate_field_relevance(
        "Computer Science and Engineering",
        "Software Engineer"
    )

    assert result["matched_fields"] == ["computer science"]
    assert result["field_relevance_score"] == 1.0


def test_non_relevant_field():
    result = calculate_field_relevance(
        "History",
        "Software Engineer"
    )

    assert result["matched_fields"] == []
    assert result["field_relevance_score"] == 0.0


def test_degree_level_score():
    assert calculate_degree_level_score(
        "Master of Science"
    ) == 1.0

    assert calculate_degree_level_score(
        "Bachelor of Technology"
    ) == 0.9

    assert calculate_degree_level_score(
        "Bachelor of Arts"
    ) == 0.8

    assert calculate_degree_level_score(
        "Unknown Degree"
    ) == 0.0


def test_calculate_education_relevance():
    education = {
        "degree_type": "Bachelor of Technology",
        "field_of_study": "Computer Science and Engineering",
        "institution": "XYZ University",
        "graduation_year": 2022
    }

    result = calculate_education_relevance(
        education,
        "Software Engineer"
    )

    assert result["field_relevance_score"] == 1.0
    assert result["degree_level_score"] == 0.9
    assert result["education_relevance_score"] == 0.97


def test_irrelevant_education():
    education = {
        "degree_type": "Bachelor of Arts",
        "field_of_study": "History",
        "institution": "ABC University",
        "graduation_year": 2020
    }

    result = calculate_education_relevance(
        education,
        "Software Engineer"
    )

    assert result["field_relevance_score"] == 0.0
    assert result["degree_level_score"] == 0.8
    assert result["education_relevance_score"] == 0.24


def test_calculate_education_relevance_for_all():
    education_records = [
        {
            "degree_type": "Bachelor of Technology",
            "field_of_study": "Computer Science and Engineering",
            "institution": "XYZ University",
            "graduation_year": 2022
        },
        {
            "degree_type": "Master of Science",
            "field_of_study": "Data Science",
            "institution": "ABC University",
            "graduation_year": 2024
        }
    ]

    results = calculate_education_relevance_for_all(
        education_records,
        "Software Engineer"
    )

    assert len(results) == 2
    assert results[0]["education_relevance_score"] == 0.97
    assert results[1]["education_relevance_score"] == 0.3
    