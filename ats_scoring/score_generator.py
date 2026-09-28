"""
Generate ATS v2 scores from processed project data.
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


def generate_score(
    resume_id,
    jd_filename
):
    """
    Generate one ATS v2 score.
    """

    skills_path = (
        PROCESSED_DIR
        / "skills"
        / f"{resume_id}_skills.json"
    )

    experience_path = (
        PROCESSED_DIR
        / "experience"
        / f"{resume_id}_experience.json"
    )

    education_path = (
        PROCESSED_DIR
        / "education"
        / f"{resume_id}_education.json"
    )

    jd_path = (
        PROCESSED_DIR
        / "jd_profiles"
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

    resume_id = skills_data["resume_id"]

    jd_id = jd_data.get(
        "job_id",
        jd_filename.replace(".json", "")
    )

    role = jd_data["role"]

    # ---------------------------------------------------------
    # Semantic result
    # ---------------------------------------------------------

    semantic_validation_path = (
        PROCESSED_DIR
        / "semantic_matching"
        / "multi_job_validation.json"
    )

    semantic_validation = load_json(
        semantic_validation_path
    )

    semantic_result = None

    for result in semantic_validation:

        if (
            result.get("resume_id") == resume_id
            and result.get("jd_id") == jd_id
        ):

            semantic_result = result
            break

    # ---------------------------------------------------------
    # Run ATS engine
    # ---------------------------------------------------------

    engine = ATSScoringEngine()

    result = engine.calculate_score(

        candidate_id=candidate_id_from_resume(
            resume_id
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
    # Output
    # ---------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_filename = (
        f"{candidate_id_from_resume(resume_id)}_"
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

    print(
        f"ATS score generated successfully:"
        f"\n{output_path}"
    )

    print(
        f"\nFinal ATS Score: "
        f"{result['final_ats_score']}"
    )

    return result


if __name__ == "__main__":

    generate_score(
        resume_id="resume_001",
        jd_filename="jd_001_data_scientist.json"
    )
