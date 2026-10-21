import pytest

from eligibility.eligibility_engine import decide_eligibility


RULES = {
    "default_thresholds": {
        "eligible_min_score": 70,
        "review_min_score": 50
    },
    "roles": {
        "Data Scientist": {
            "eligible_min_score": 70,
            "review_min_score": 50,
            "mandatory_skills": ["Python", "SQL", "Machine Learning"],
            "experience": {"minimum_years": 2, "maximum_years": 5},
            "location": {
                "required": False,
                "allowed_locations": ["Bangalore, India"],
                "review_if_unknown": True
            },
            "availability": {
                "required": False,
                "review_if_unknown": True
            }
        }
    }
}


def make_ats_result(score=85, role="Data Scientist"):
    return {
        "candidate_id": "CAND_TEST_001",
        "job_id": "JOB_TEST_001",
        "role": role,
        "final_ats_score": score,
        "component_details": {
            "skill_match": {
                "required_matched": [
                    {"skill": "Python"},
                    {"skill": "SQL"},
                    {"skill": "Machine Learning"}
                ],
                "required_missing": []
            },
            "experience_relevance": {
                "candidate_experience_years": 3
            }
        }
    }


def make_candidate():
    return {
        "skills": ["Python", "SQL", "Machine Learning"],
        "experience_years": 3,
        "location": "Bangalore, India",
        "availability": "available"
    }


def test_candidate_is_eligible_when_all_checks_pass():
    result = decide_eligibility(
        make_ats_result(score=85),
        candidate=make_candidate(),
        rules=RULES
    )
    assert result["eligibility_status"] == "Eligible"
    assert result["failed_checks"] == []
    assert result["review_checks"] == []


def test_candidate_in_score_review_band_needs_review():
    result = decide_eligibility(
        make_ats_result(score=60),
        candidate=make_candidate(),
        rules=RULES
    )
    assert result["eligibility_status"] == "Review"


def test_candidate_below_review_threshold_is_rejected():
    result = decide_eligibility(
        make_ats_result(score=40),
        candidate=make_candidate(),
        rules=RULES
    )
    assert result["eligibility_status"] == "Rejected"


def test_missing_mandatory_skill_is_rejected():
    candidate = make_candidate()
    candidate["skills"] = ["Python", "SQL"]

    result = decide_eligibility(
        make_ats_result(score=85),
        candidate=candidate,
        rules=RULES
    )
    assert result["eligibility_status"] == "Rejected"
    assert any("Machine Learning" in reason for reason in result["failed_checks"])


def test_experience_outside_configured_range_is_rejected():
    candidate = make_candidate()
    candidate["experience_years"] = 7

    result = decide_eligibility(
        make_ats_result(score=85),
        candidate=candidate,
        rules=RULES
    )
    assert result["eligibility_status"] == "Rejected"


def test_unknown_location_and_availability_require_review():
    candidate = make_candidate()
    candidate.pop("location")
    candidate.pop("availability")

    result = decide_eligibility(
        make_ats_result(score=85),
        candidate=candidate,
        rules=RULES
    )
    assert result["eligibility_status"] == "Review"


def test_unconfigured_role_requires_review():
    result = decide_eligibility(
        make_ats_result(score=85, role="Unknown Role"),
        candidate=make_candidate(),
        rules=RULES
    )
    assert result["eligibility_status"] == "Review"


def test_invalid_thresholds_raise_error():
    bad_rules = {
        "roles": {
            "Data Scientist": {
                "eligible_min_score": 40,
                "review_min_score": 50,
                "mandatory_skills": []
            }
        }
    }

    with pytest.raises(ValueError):
        decide_eligibility(
            make_ats_result(),
            candidate=make_candidate(),
            rules=bad_rules
        )

def test_all_six_job_roles_are_configured():
    from eligibility.eligibility_engine import load_rules

    configured_rules = load_rules()
    expected_roles = {
        "Data Scientist",
        "Software Engineer",
        "Machine Learning Engineer",
        "Data Analyst",
        "HR Executive",
        "Business Analyst",
    }

    assert expected_roles.issubset(configured_rules["roles"].keys())


def test_all_configured_role_thresholds_are_valid():
    from eligibility.eligibility_engine import load_rules

    configured_rules = load_rules()
    for role, role_rules in configured_rules["roles"].items():
        eligible = role_rules["eligible_min_score"]
        review = role_rules["review_min_score"]

        assert 0 <= review < eligible <= 100, (
            f"Invalid thresholds configured for {role}"
        )
        assert isinstance(role_rules["mandatory_skills"], list)
        assert "minimum_years" in role_rules["experience"]
