import pytest

from fairness.normalization import (
    normalize_text,
    normalize_skill_list,
    normalize_section_name,
    normalize_sections,
    normalize_resume,
)


def test_normalize_text():
    assert normalize_text("  Python   SQL  ") == "python sql"


def test_normalize_skill_list():
    skills = ["Python", " python ", "SQL", "", "Power BI"]

    result = normalize_skill_list(skills)

    assert result == ["python", "sql", "power bi"]


def test_normalize_section_name():
    assert normalize_section_name("Work Experience") == "work_experience"
    assert normalize_section_name("TECHNICAL SKILLS") == "skills"


def test_normalize_sections():
    sections = {
        "Work Experience": "  Data Analyst   at Company ",
        "Technical Skills": ["Python", " SQL "],
    }

    result = normalize_sections(sections)

    assert result["work_experience"] == "data analyst at company"
    assert result["skills"] == ["python", "sql"]


def test_normalize_resume():
    resume = {
        "resume_id": " RESUME_001 ",
        "skills": ["Python", " python ", "SQL"],
        "summary": "  Data Analyst   with Python  ",
    }

    result = normalize_resume(resume)

    assert result["resume_id"] == "resume_001"
    assert result["skills"] == ["python", "sql"]
    assert result["summary"] == "data analyst with python"
from fairness.attribute_masking import (
    mask_personal_attributes,
    get_masked_fields,
)


def test_mask_personal_attributes():
    resume = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "9876543210",
        "skills": ["python", "sql"],
    }

    result = mask_personal_attributes(resume)

    assert result["name"] == "[MASKED]"
    assert result["email"] == "[MASKED]"
    assert result["phone"] == "[MASKED]"

    # Job-relevant information must remain unchanged.
    assert result["skills"] == ["python", "sql"]


def test_masking_does_not_modify_original():
    resume = {
        "name": "John Doe",
        "skills": ["python"],
    }

    result = mask_personal_attributes(resume)

    assert resume["name"] == "John Doe"
    assert result["name"] == "[MASKED]"


def test_get_masked_fields():
    resume = {
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["python"],
    }

    result = get_masked_fields(resume)

    assert result == ["email", "name"]
from fairness.keyword_reduction import (
    calculate_balanced_score,
    calculate_keyword_dependence,
)


def test_balanced_score():
    result = calculate_balanced_score(
        keyword_score=80,
        semantic_score=60,
    )

    assert result == 72.0


def test_balanced_score_with_custom_weights():
    result = calculate_balanced_score(
        keyword_score=80,
        semantic_score=60,
        keyword_weight=0.50,
        semantic_weight=0.50,
    )

    assert result == 70.0


def test_weight_normalization():
    result = calculate_balanced_score(
        keyword_score=80,
        semantic_score=60,
        keyword_weight=6,
        semantic_weight=4,
    )

    assert result == 72.0


def test_keyword_dependence():
    result = calculate_keyword_dependence(
        keyword_score=80,
        semantic_score=60,
    )

    assert result == 20.0


def test_invalid_score():
    with pytest.raises(ValueError):
        calculate_balanced_score(
            keyword_score=110,
            semantic_score=60,
        )
from fairness.score_normalization import (
    normalize_score,
    normalize_to_100,
)


def test_normalize_zero_to_one():
    result = normalize_to_100(
        score=0.75,
        source_min=0,
        source_max=1,
    )

    assert result == 75.0


def test_normalize_percentage():
    result = normalize_to_100(
        score=50,
        source_min=0,
        source_max=100,
    )

    assert result == 50.0


def test_normalize_custom_range():
    result = normalize_score(
        score=75,
        source_min=50,
        source_max=100,
    )

    assert result == 50.0


def test_normalize_boundaries():
    assert normalize_to_100(0, 0, 1) == 0.0
    assert normalize_to_100(1, 0, 1) == 100.0


def test_invalid_source_range():
    with pytest.raises(ValueError):
        normalize_to_100(
            score=50,
            source_min=100,
            source_max=100,
        )


def test_score_outside_source_range():
    with pytest.raises(ValueError):
        normalize_to_100(
            score=120,
            source_min=0,
            source_max=100,
        )

from fairness.bias_evaluation import (
    calculate_score_gap,
    calculate_average_score,
    calculate_score_distribution,
    calculate_keyword_semantic_gap,
)


def test_score_gap():
    result = calculate_score_gap(
        group_a_scores=[80, 70, 90],
        group_b_scores=[60, 70, 50],
    )

    assert result == 20.0


def test_average_score():
    result = calculate_average_score(
        [60, 70, 80]
    )

    assert result == 70.0


def test_score_distribution():
    result = calculate_score_distribution(
        [40, 60, 80]
    )

    assert result == {
        "count": 3,
        "average": 60.0,
        "minimum": 40,
        "maximum": 80,
    }


def test_keyword_semantic_gap():
    result = calculate_keyword_semantic_gap(
        keyword_scores=[80, 70],
        semantic_scores=[60, 50],
    )

    assert result == 20.0


def test_empty_group():
    with pytest.raises(ValueError):
        calculate_score_gap([], [50, 60])


def test_empty_scores():
    with pytest.raises(ValueError):
        calculate_average_score([])

from fairness.fair_scoring import (
    calculate_fair_skill_score,
    normalize_component_score,
    generate_fair_scoring_output,
)


def test_fair_skill_score():
    result = calculate_fair_skill_score(
        keyword_score=80,
        semantic_score=60,
    )

    assert result == 72.0


def test_fair_skill_score_custom_weights():
    result = calculate_fair_skill_score(
        keyword_score=80,
        semantic_score=60,
        keyword_weight=0.50,
        semantic_weight=0.50,
    )

    assert result == 70.0


def test_normalize_component_score():
    result = normalize_component_score(75)

    assert result == 75.0


def test_generate_fair_scoring_output():
    result = generate_fair_scoring_output(
        keyword_score=80,
        semantic_score=60,
    )

    assert result["keyword_score"] == 80.0
    assert result["semantic_score"] == 60.0
    assert result["fair_skill_score"] == 72.0
    assert result["normalized_score"] == 72.0
    