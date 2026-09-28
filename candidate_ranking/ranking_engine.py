"""
Candidate Ranking Engine.

Day 14:
Candidate Ranking & Shortlisting

This module:
- Loads ATS score files
- Validates ATS score data
- Groups candidates by job
- Sorts candidates by ATS score
- Assigns deterministic ranks
"""


import json
from pathlib import Path


REQUIRED_FIELDS = {
    "candidate_id",
    "job_id",
    "role",
    "final_ats_score",
    "component_scores",
}


def load_ats_score(file_path):
    """
    Load and validate one ATS score JSON file.

    Args:
        file_path (Path): Path to an ATS score JSON file.

    Returns:
        dict: Validated ATS score record.

    Raises:
        ValueError: If required fields or score values are invalid.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    missing_fields = REQUIRED_FIELDS - data.keys()

    if missing_fields:
        raise ValueError(
            f"Missing required fields in {file_path.name}: "
            f"{sorted(missing_fields)}"
        )

    score = data["final_ats_score"]

    if not isinstance(score, (int, float)):
        raise ValueError(
            f"Invalid ATS score in {file_path.name}: "
            "score must be numeric."
        )

    if not 0 <= score <= 100:
        raise ValueError(
            f"Invalid ATS score in {file_path.name}: "
            "score must be between 0 and 100."
        )

    return data


def load_all_ats_scores(scores_dir):
    """
    Load all ATS score JSON files from a directory.

    Args:
        scores_dir (Path): Directory containing ATS score files.

    Returns:
        list: List of validated ATS score records.
    """

    scores_dir = Path(scores_dir)

    if not scores_dir.exists():
        raise FileNotFoundError(
            f"ATS scores directory not found: {scores_dir}"
        )

    files = sorted(scores_dir.glob("*.json"))

    if not files:
        raise FileNotFoundError(
            f"No ATS score JSON files found in: {scores_dir}"
        )

    records = []

    for file_path in files:
        records.append(load_ats_score(file_path))

    return records


def group_scores_by_job(records):
    """
    Group ATS score records by job ID.

    Candidates are ranked separately for each job.

    Args:
        records (list): ATS score records.

    Returns:
        dict: Mapping of job_id to candidate records.
    """

    grouped = {}

    for record in records:
        job_id = record["job_id"]

        if job_id not in grouped:
            grouped[job_id] = []

        grouped[job_id].append(record)

    return grouped


def rank_candidates(records):
    """
    Sort candidates by ATS score in descending order.

    A deterministic candidate ID tie-breaker is used when
    two candidates have the same ATS score.

    Args:
        records (list): Candidates for one job.

    Returns:
        list: Ranked candidate records.
    """

    sorted_records = sorted(
        records,
        key=lambda record: (
            -record["final_ats_score"],
            record["candidate_id"],
        ),
    )

    ranked_candidates = []

    for rank, record in enumerate(sorted_records, start=1):
        ranked_candidates.append(
            {
                "rank": rank,
                "candidate_id": record["candidate_id"],
                "job_id": record["job_id"],
                "role": record["role"],
                "ats_score": round(
                    record["final_ats_score"],
                    2,
                ),
                "component_scores": record["component_scores"],
            }
        )

    return ranked_candidates


def rank_all_jobs(records):
    """
    Rank candidates separately for every job.

    Args:
        records (list): All ATS score records.

    Returns:
        dict: Job-wise ranked candidate lists.
    """

    grouped_records = group_scores_by_job(records)

    rankings = {}

    for job_id, job_records in sorted(grouped_records.items()):
        ranked_candidates = rank_candidates(job_records)

        rankings[job_id] = {
            "job_id": job_id,
            "role": job_records[0]["role"],
            "candidate_count": len(ranked_candidates),
            "ranked_candidates": ranked_candidates,
        }

    return rankings
