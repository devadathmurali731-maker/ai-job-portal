"""
Candidate Ranking and Shortlisting Generator.

Day 14:
Candidate Ranking & Shortlisting

This module connects:
- Day 13 ATS scoring
- Day 14 ranking
- Day 14 shortlisting

It generates one recruiter-friendly ranking file
for each job.
"""

import json
from pathlib import Path

from candidate_ranking.ranking_engine import (
    load_all_ats_scores,
    rank_all_jobs,
)

from candidate_ranking.shortlisting import (
    apply_shortlisting,
    summarize_decisions,
)


BASE_DIR = Path(__file__).resolve().parent.parent

ATS_SCORES_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "ats_scores_v2"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "candidate_ranking"
)


def generate_job_ranking(job_data):
    """
    Apply shortlisting decisions to one job's ranking.

    Args:
        job_data (dict): Ranked candidates for one job.

    Returns:
        dict: Complete recruiter-friendly job output.
    """

    ranked_candidates = job_data["ranked_candidates"]

    candidates_with_decisions = apply_shortlisting(
        ranked_candidates
    )

    decision_summary = summarize_decisions(
        candidates_with_decisions
    )

    return {
        "job_id": job_data["job_id"],
        "role": job_data["role"],
        "candidate_count": job_data["candidate_count"],
        "decision_summary": decision_summary,
        "ranked_candidates": candidates_with_decisions,
    }


def save_job_ranking(job_data):
    """
    Save one job's ranking to a JSON file.

    Args:
        job_data (dict): Complete job ranking output.

    Returns:
        Path: Path to the generated JSON file.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    job_id = job_data["job_id"]

    output_file = (
        OUTPUT_DIR
        / f"{job_id}_ranked_candidates.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            job_data,
            file,
            indent=4,
        )

    return output_file


def generate_all_rankings():
    """
    Generate rankings and shortlisting decisions for all jobs.

    Returns:
        list: Generated output file paths.
    """

    print("Loading ATS scores...")

    records = load_all_ats_scores(
        ATS_SCORES_DIR
    )

    print(
        f"Found {len(records)} ATS score files."
    )

    rankings = rank_all_jobs(records)

    print(
        f"Found {len(rankings)} jobs."
    )

    generated_files = []

    total_shortlisted = 0
    total_review = 0
    total_rejected = 0

    for job_id, job_data in rankings.items():

        final_output = generate_job_ranking(
            job_data
        )

        output_file = save_job_ranking(
            final_output
        )

        generated_files.append(output_file)

        summary = final_output[
            "decision_summary"
        ]

        total_shortlisted += summary[
            "SHORTLIST"
        ]

        total_review += summary[
            "REVIEW"
        ]

        total_rejected += summary[
            "REJECT"
        ]

        print(
            f"Generated {job_id} "
            f"({final_output['role']})"
        )

        print(
            f"  SHORTLIST: "
            f"{summary['SHORTLIST']}"
        )

        print(
            f"  REVIEW: "
            f"{summary['REVIEW']}"
        )

        print(
            f"  REJECT: "
            f"{summary['REJECT']}"
        )

    print()
    print(
        f"Generated ranked outputs: "
        f"{len(generated_files)}"
    )

    print(
        f"Total shortlisted: "
        f"{total_shortlisted}"
    )

    print(
        f"Total review: "
        f"{total_review}"
    )

    print(
        f"Total rejected: "
        f"{total_rejected}"
    )

    return generated_files


if __name__ == "__main__":
    generate_all_rankings()