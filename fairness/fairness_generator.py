"""
Fairness-aware output generator.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Connect fairness-aware resume processing with the
existing ATS scoring outputs.

This module does not replace the original ATS scoring engine.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from fairness.fair_scoring import (
    generate_fair_scoring_output,
)


BASE_DIR = Path(__file__).resolve().parent.parent

ATS_SCORES_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "ats_scores_v2"
)

FAIR_RESUMES_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "fairness"
    / "resumes"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "fairness"
)


def load_json(
    file_path: Path,
) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents.
    """

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_ats_scores(
    scores_dir: Path = ATS_SCORES_DIR,
) -> List[Dict[str, Any]]:
    """
    Load all ATS score records.
    """

    if not scores_dir.exists():
        raise FileNotFoundError(
            f"ATS score directory not found: {scores_dir}"
        )

    records = []

    for file_path in sorted(
        scores_dir.glob("*.json")
    ):
        records.append(
            load_json(file_path)
        )

    return records


def load_fairness_resume(
    candidate_id: str,
) -> Dict[str, Any]:
    """
    Load the fairness-processed resume
    corresponding to a candidate.
    """

    resume_number = candidate_id.replace(
        "CAND_",
        "",
    )

    resume_file = (
        FAIR_RESUMES_DIR
        / f"resume_{resume_number}_sections.json"
    )

    if not resume_file.exists():
        raise FileNotFoundError(
            f"Fairness resume not found: {resume_file}"
        )

    return load_json(resume_file)


def extract_keyword_score(
    record: Dict[str, Any],
) -> float:
    """
    Extract the existing skill-match score.
    """

    component_scores = record.get(
        "component_scores",
        {},
    )

    score = component_scores.get(
        "skill_match",
        0.0,
    )

    return float(score)


def extract_semantic_score(
    record: Dict[str, Any],
) -> float:
    """
    Extract the existing semantic similarity score.
    """

    component_scores = record.get(
        "component_scores",
        {},
    )

    score = component_scores.get(
        "semantic_similarity",
        0.0,
    )

    return float(score)


def build_fair_score_record(
    record: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build an explainable fairness-aware record.
    """

    candidate_id = record.get(
        "candidate_id"
    )

    fairness_resume = load_fairness_resume(
        candidate_id
    )

    keyword_score = extract_keyword_score(
        record
    )

    semantic_score = extract_semantic_score(
        record
    )

    fair_scoring = (
        generate_fair_scoring_output(
            keyword_score=keyword_score,
            semantic_score=semantic_score,
        )
    )

    return {
        "candidate_id": candidate_id,
        "job_id": record.get(
            "job_id"
        ),
        "role": record.get(
            "role"
        ),
        "original_ats_score": record.get(
            "final_ats_score"
        ),
        "fairness_resume": {
            "source": (
                f"resume_{candidate_id.replace('CAND_', '')}"
                "_sections.json"
            ),
            "normalized": True,
            "personal_attributes_masked": True,
            "sections_available": list(
                fairness_resume.keys()
            ),
        },
        "fair_scoring": fair_scoring,
        "fairness_methods": {
            "resume_normalization": True,
            "personal_attribute_masking": True,
            "keyword_semantic_balancing": True,
            "score_normalization": True,
        },
    }


def generate_fairness_outputs(
    scores_dir: Path = ATS_SCORES_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> List[Path]:
    """
    Generate fairness-aware outputs for all ATS records.
    """

    records = load_ats_scores(
        scores_dir
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_files = []

    for record in records:
        fair_record = build_fair_score_record(
            record
        )

        candidate_id = fair_record[
            "candidate_id"
        ]

        job_id = fair_record[
            "job_id"
        ]

        output_file = (
            output_dir
            / f"{candidate_id}_{job_id}_fairness.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                fair_record,
                file,
                indent=2,
                ensure_ascii=False,
            )

        generated_files.append(
            output_file
        )

    return generated_files


if __name__ == "__main__":
    print(
        "Loading ATS scores..."
    )

    generated = (
        generate_fairness_outputs()
    )

    print(
        f"Generated fairness outputs: "
        f"{len(generated)}"
    )