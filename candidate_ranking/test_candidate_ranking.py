"""
Tests for Candidate Ranking Engine.

Day 14:
Candidate Ranking & Shortlisting
"""

import pytest

from candidate_ranking.ranking_engine import (
    group_scores_by_job,
    rank_candidates,
)


def test_group_scores_by_job():
    """Candidates should be grouped by job ID."""

    records = [
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 45.51,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_002",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 50.40,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_002",
            "role": "Software Engineer",
            "final_ats_score": 84.80,
            "component_scores": {},
        },
    ]

    grouped = group_scores_by_job(records)

    assert len(grouped) == 2
    assert len(grouped["JOB_001"]) == 2
    assert len(grouped["JOB_002"]) == 1


def test_rank_candidates_descending():
    """Candidates should be ranked from highest to lowest score."""

    records = [
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 45.51,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_002",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 50.40,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_003",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 68.53,
            "component_scores": {},
        },
    ]

    ranked = rank_candidates(records)

    assert ranked[0]["candidate_id"] == "CAND_003"
    assert ranked[1]["candidate_id"] == "CAND_002"
    assert ranked[2]["candidate_id"] == "CAND_001"


def test_rank_numbers_are_assigned():
    """Ranks should start at 1 and increase sequentially."""

    records = [
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 40.0,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_002",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 60.0,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_003",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 80.0,
            "component_scores": {},
        },
    ]

    ranked = rank_candidates(records)

    assert [candidate["rank"] for candidate in ranked] == [1, 2, 3]


def test_tie_breaker_is_deterministic():
    """Equal scores should be ordered by candidate ID."""

    records = [
        {
            "candidate_id": "CAND_002",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 70.0,
            "component_scores": {},
        },
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 70.0,
            "component_scores": {},
        },
    ]

    ranked = rank_candidates(records)

    assert ranked[0]["candidate_id"] == "CAND_001"
    assert ranked[1]["candidate_id"] == "CAND_002"


def test_ranked_output_contains_required_fields():
    """Ranked records should contain recruiter-useful fields."""

    records = [
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 75.25,
            "component_scores": {
                "skill_match": 80.0,
                "experience_relevance": 70.0,
            },
        }
    ]

    ranked = rank_candidates(records)

    candidate = ranked[0]

    assert candidate["rank"] == 1
    assert candidate["candidate_id"] == "CAND_001"
    assert candidate["job_id"] == "JOB_001"
    assert candidate["role"] == "Data Scientist"
    assert candidate["ats_score"] == 75.25
    assert "component_scores" in candidate


def test_invalid_score_is_rejected(tmp_path):
    """ATS scores outside 0-100 should raise an error."""

    from candidate_ranking.ranking_engine import load_ats_score

    invalid_file = tmp_path / "invalid.json"

    invalid_file.write_text(
        """
        {
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "final_ats_score": 120,
            "component_scores": {}
        }
        """,
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_ats_score(invalid_file)

from candidate_ranking.shortlisting import (
    classify_candidate,
    apply_shortlisting,
    summarize_decisions,
)

def test_shortlist_threshold():
    """Scores at or above 70 should be shortlisted."""

    assert classify_candidate(70.0) == "SHORTLIST"
    assert classify_candidate(85.0) == "SHORTLIST"
    assert classify_candidate(100.0) == "SHORTLIST"


def test_review_threshold():
    """Scores from 50 up to below 70 should be reviewed."""

    assert classify_candidate(50.0) == "REVIEW"
    assert classify_candidate(55.0) == "REVIEW"
    assert classify_candidate(69.99) == "REVIEW"


def test_reject_threshold():
    """Scores below 50 should be rejected."""

    assert classify_candidate(49.99) == "REJECT"
    assert classify_candidate(25.0) == "REJECT"
    assert classify_candidate(0.0) == "REJECT"


def test_shortlisting_boundaries():
    """Verify exact threshold boundaries."""

    assert classify_candidate(69.999) == "REVIEW"
    assert classify_candidate(70.0) == "SHORTLIST"

    assert classify_candidate(49.999) == "REJECT"
    assert classify_candidate(50.0) == "REVIEW"


def test_invalid_candidate_score():
    """Scores outside 0-100 should raise ValueError."""

    with pytest.raises(ValueError):
        classify_candidate(-1)

    with pytest.raises(ValueError):
        classify_candidate(101)


def test_apply_shortlisting():
    """Candidates should receive decisions and reasons."""

    ranked_candidates = [
        {
            "rank": 1,
            "candidate_id": "CAND_001",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "ats_score": 75.0,
            "component_scores": {},
        },
        {
            "rank": 2,
            "candidate_id": "CAND_002",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "ats_score": 60.0,
            "component_scores": {},
        },
        {
            "rank": 3,
            "candidate_id": "CAND_003",
            "job_id": "JOB_001",
            "role": "Data Scientist",
            "ats_score": 40.0,
            "component_scores": {},
        },
    ]

    results = apply_shortlisting(ranked_candidates)

    assert results[0]["decision"] == "SHORTLIST"
    assert results[1]["decision"] == "REVIEW"
    assert results[2]["decision"] == "REJECT"

    assert "decision_reason" in results[0]
    assert "decision_reason" in results[1]
    assert "decision_reason" in results[2]


def test_summarize_decisions():
    """Decision counts should be calculated correctly."""

    candidates = [
        {"decision": "SHORTLIST"},
        {"decision": "SHORTLIST"},
        {"decision": "REVIEW"},
        {"decision": "REVIEW"},
        {"decision": "REJECT"},
    ]

    summary = summarize_decisions(candidates)

    assert summary["SHORTLIST"] == 2
    assert summary["REVIEW"] == 2
    assert summary["REJECT"] == 1