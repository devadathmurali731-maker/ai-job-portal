
"""
Tests for the Day 13 ATS Scoring Engine.

Tests cover:

1. Normal ATS scoring
2. Missing semantic similarity
3. Missing education data
4. Missing experience data
5. Dynamic weight redistribution
6. Explainable scoring output
7. Weighted contribution calculation
8. M.Sc. Master's degree matching
"""

import pytest

from ats_scoring.ats_scoring_engine import ATSScoringEngine


def create_test_data():
    """Create reusable test data."""

    resume_skills = [
        {"skill": "Python", "confidence": 0.99},
        {"skill": "SQL", "confidence": 0.99},
        {"skill": "Docker", "confidence": 0.99}
    ]

    experience_data = {
        "total_experience_years": 4.75,
        "experiences": [
            {
                "company": "ABC Technologies",
                "job_title": "Software Engineer",
                "start_date": "2022-01",
                "end_date": "2026-09",
                "duration_months": 57,
                "experience_years": 4.75,
                "is_current": True,
                "responsibilities": [
                    "Developed REST APIs using Spring Boot.",
                    "Worked with MySQL and PostgreSQL databases.",
                    "Used Git and Docker in application development.",
                    "Participated in Agile software development."
                ]
            }
        ]
    }

    education_data = {
        "education": [
            {
                "degree_type": "Bachelor of Technology",
                "field_of_study": "Computer Science and Engineering",
                "institution": "XYZ University",
                "graduation_year": 2022
            }
        ],
        "certifications": []
    }

    semantic_result = {
        "final_semantic_score": 0.5354455001652241,
        "component_scores": {
            "skills": 0.651990532875061,
            "experience": 0.3412037789821625
        },
        "available_components": [
            "skills",
            "experience"
        ]
    }

    jd_skills = {
        "required": [
            "Python",
            "SQL",
            "Machine Learning",
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "Statistics",
            "Data Analysis"
        ],
        "preferred": [
            "Power BI",
            "Tableau",
            "TensorFlow",
            "XGBoost",
            "AWS",
            "Docker"
        ]
    }

    jd_experience = {
        "minimum_years": 2,
        "maximum_years": 5,
        "is_fresher_allowed": False
    }

    jd_education = {
        "required": [
            "Bachelor's degree",
            "Master's degree"
        ],
        "preferred": [],
        "fields_of_study": [
            "Computer Science",
            "Data Science",
            "Statistics",
            "Mathematics",
            "Economics"
        ]
    }

    return (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    )


def test_normal_ats_scoring():
    """Test normal ATS scoring."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=semantic_result,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    assert "final_ats_score" in result
    assert 0 <= result["final_ats_score"] <= 100


def test_missing_semantic_similarity():
    """Test scoring when semantic similarity is unavailable."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=None,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    assert result["final_ats_score"] >= 0
    assert result["final_ats_score"] <= 100
    assert "semantic_similarity" in result["missing_components"]


def test_missing_education():
    """Test scoring when education data is unavailable."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=None,
        semantic_result=semantic_result,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    assert "education_alignment" in result["missing_components"]


def test_missing_experience():
    """Test scoring when experience data is unavailable."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=None,
        education_data=education_data,
        semantic_result=semantic_result,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    assert "experience_relevance" in result["missing_components"]


def test_weight_redistribution():
    """Test that available components receive redistributed weights."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=None,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    adjusted_weights = result["adjusted_weights"]

    assert abs(sum(adjusted_weights.values()) - 1.0) < 1e-6


def test_explainable_output():
    """Test that the ATS result contains the required explainability fields."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=semantic_result,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    assert "component_scores" in result
    assert "original_weights" in result
    assert "adjusted_weights" in result
    assert "weighted_contributions" in result
    assert "final_ats_score" in result
    assert "available_components" in result
    assert "missing_components" in result
    assert "component_details" in result


def test_weighted_contributions():
    """Verify that component contributions produce the final ATS score."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    result = engine.calculate_score(
        candidate_id="CAND_001",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=semantic_result,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    contributions = result["weighted_contributions"]

    calculated_score = round(
        sum(contributions.values()),
        2
    )

    assert calculated_score == result["final_ats_score"]


def test_msc_matches_masters_degree():
    """M.Sc. should satisfy Master's, but not Bachelor's, requirement."""

    engine = ATSScoringEngine()

    (
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ) = create_test_data()

    # Provide only an M.Sc. qualification.
    education_data["education"] = [
        {
            "degree_type": "M.Sc.",
            "field_of_study": "Data Science",
            "institution": "Example University",
            "graduation_year": 2025
        }
    ]

    result = engine.calculate_score(
        candidate_id="CAND_MSC_TEST",
        job_id="JOB_001",
        role="Data Scientist",
        resume_skills=resume_skills,
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=semantic_result,
        jd_skills=jd_skills,
        jd_experience=jd_experience,
        jd_education=jd_education
    )

    education = result["component_details"]["education_alignment"]

    assert "Master's degree" in education["matched_required_degrees"]
    assert "Bachelor's degree" in education["missing_required_degrees"]
