from experience_relevance import (
    calculate_keyword_match,
    calculate_role_relevance,
    calculate_experience_relevance
)


def test_keyword_match():

    text = """
    Developed REST APIs using Spring Boot.
    Worked with SQL databases.
    Used Docker and Git.
    """

    required_keywords = [
        "Spring Boot",
        "REST APIs",
        "SQL",
        "Docker",
        "Git"
    ]

    result = calculate_keyword_match(
        text,
        required_keywords
    )

    assert result["keyword_match_score"] == 1.0
    assert len(result["matched_keywords"]) == 5
    assert result["missing_keywords"] == []


def test_keyword_missing():

    text = """
    Developed REST APIs using Spring Boot.
    Worked with SQL databases.
    """

    required_keywords = [
        "Spring Boot",
        "REST APIs",
        "SQL",
        "Python"
    ]

    result = calculate_keyword_match(
        text,
        required_keywords
    )

    assert result["keyword_match_score"] == 0.75
    assert "Python" in result["missing_keywords"]


def test_role_relevance():

    experience = {
        "company": "ABC Technologies",
        "job_title": "Software Engineer",
        "responsibilities": [
            "Developed REST APIs using Spring Boot.",
            "Worked with SQL databases.",
            "Used Docker and Git."
        ]
    }

    result = calculate_role_relevance(
        experience=experience,
        target_role="Software Engineer",
        required_keywords=[
            "Spring Boot",
            "REST APIs",
            "SQL",
            "Docker",
            "Git"
        ]
    )

    assert result["title_match"] is True
    assert result["keyword_match_score"] == 1.0
    assert result["relevance_score"] == 1.0


def test_experience_relevance():

    experiences = [
        {
            "company": "ABC Technologies",
            "job_title": "Software Engineer",
            "responsibilities": [
                "Developed REST APIs.",
                "Worked with SQL."
            ]
        }
    ]

    results = calculate_experience_relevance(
        experiences=experiences,
        target_role="Software Engineer",
        required_keywords=[
            "REST APIs",
            "SQL"
        ]
    )

    assert len(results) == 1
    assert results[0]["title_match"] is True
    assert results[0]["keyword_match_score"] == 1.0
    