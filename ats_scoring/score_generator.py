"""
Generate ATS v2 scores from processed project data.

This module generates ATS scores for every available
resume-JD combination using the Day 13 ATS scoring engine.
"""

import json
from pathlib import Path

from .ats_scoring_engine import ATSScoringEngine


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_DIR = (
    PROCESSED_DIR
    / "ats_scores_v2"
)

SKILLS_DIR = PROCESSED_DIR / "skills"
EXPERIENCE_DIR = PROCESSED_DIR / "experience"
EDUCATION_DIR = PROCESSED_DIR / "education"
JD_DIR = PROCESSED_DIR / "jd_profiles"
SEMANTIC_DIR = PROCESSED_DIR / "semantic_matching"


def load_json(path):
    """Load JSON from disk."""

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def candidate_id_from_resume(resume_id):
    """
    Convert resume_001 to CAND_001.
    """

    number = resume_id.split("_")[-1]

    return f"CAND_{number}"


def job_id_from_jd(jd_id):
    """
    Convert jd_001_data_scientist to JOB_001.
    """

    number = jd_id.split("_")[1]

    return f"JOB_{number}"


def load_semantic_results():
    """
    Load all Day 12 semantic matching results.

    Returns:
        Dictionary keyed by (resume_id, jd_id).
    """

    semantic_path = (
        SEMANTIC_DIR
        / "multi_job_validation.json"
    )

    semantic_results = load_json(
        semantic_path
    )

    semantic_lookup = {}

    for result in semantic_results:

        key = (
            result.get("resume_id"),
            result.get("jd_id")
        )

        semantic_lookup[key] = result

    return semantic_lookup


def generate_score(
    resume_id,
    jd_filename,
    semantic_lookup
):
    """
    Generate one ATS v2 score for one resume-JD pair.
    """

    skills_path = (
        SKILLS_DIR
        / f"{resume_id}_skills.json"
    )

    experience_path = (
        EXPERIENCE_DIR
        / f"{resume_id}_experience.json"
    )

    education_path = (
        EDUCATION_DIR
        / f"{resume_id}_education.json"
    )

    jd_path = (
        JD_DIR
        / jd_filename
    )

    skills_data = load_json(
        skills_path
    )

    experience_data = load_json(
        experience_path
    )

    education_data = load_json(
        education_path
    )

    jd_data = load_json(
        jd_path
    )

    actual_resume_id = skills_data["resume_id"]

    jd_id = jd_data.get(
        "job_id",
        jd_filename.replace(".json", "")
    )

    role = jd_data["role"]

    # ---------------------------------------------------------
    # Semantic result from Day 12
    # ---------------------------------------------------------

    semantic_key = (
        actual_resume_id,
        jd_id
    )

    semantic_result = semantic_lookup.get(
        semantic_key
    )

    # ---------------------------------------------------------
    # Run ATS engine
    # ---------------------------------------------------------

    engine = ATSScoringEngine()

    result = engine.calculate_score(

        candidate_id=candidate_id_from_resume(
            actual_resume_id
        ),

        job_id=job_id_from_jd(
            jd_id
        ),

        role=role,

        resume_skills=skills_data.get(
            "skills",
            []
        ),

        jd_skills=jd_data.get(
            "skills",
            {}
        ),

        experience_data=experience_data,

        jd_experience=jd_data.get(
            "experience",
            {}
        ),

        education_data=education_data,

        jd_education=jd_data.get(
            "education",
            {}
        ),

        semantic_result=semantic_result
    )

    # ---------------------------------------------------------
    # Save output
    # ---------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_filename = (
        f"{candidate_id_from_resume(actual_resume_id)}_"
        f"{job_id_from_jd(jd_id)}.json"
    )

    output_path = (
        OUTPUT_DIR
        / output_filename
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )

    return result


def discover_resumes():
    """
    Discover all resumes that have skill extraction results.
    """

    resume_files = sorted(
        SKILLS_DIR.glob("*_skills.json")
    )

    return [
        file.stem.replace(
            "_skills",
            ""
        )
        for file in resume_files
    ]


def discover_jds():
    """
    Discover all JD profile JSON files.
    """

    return sorted(
        file.name
        for file in JD_DIR.glob("jd_*.json")
    )


def generate_all_scores():
    """
    Generate ATS scores for every resume-JD combination.
    """

    resumes = discover_resumes()

    jd_files = discover_jds()

    semantic_lookup = load_semantic_results()

    print(
        f"Found {len(resumes)} resumes."
    )

    print(
        f"Found {len(jd_files)} job profiles."
    )

    expected_combinations = (
        len(resumes) * len(jd_files)
    )

    print(
        f"Expected ATS combinations: "
        f"{expected_combinations}"
    )

    results = []

    for resume_id in resumes:

        for jd_filename in jd_files:

            result = generate_score(
                resume_id=resume_id,
                jd_filename=jd_filename,
                semantic_lookup=semantic_lookup
            )

            results.append(result)

            print(
                f"Generated: "
                f"{result['candidate_id']} → "
                f"{result['job_id']} "
                f"({result['role']}) "
                f"| Score: "
                f"{result['final_ats_score']}"
            )

    print()
    print(
        f"Successfully generated "
        f"{len(results)} ATS scores."
    )

    return results


if __name__ == "__main__":

    generate_all_scores()