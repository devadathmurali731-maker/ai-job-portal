import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from ats_scoring.ats_scoring_engine import ATSScoringEngine

DATA_DIR = PROJECT_ROOT / "data" / "processed"


def load_json(path):
    if not path.is_file():
        raise FileNotFoundError(f"Required input not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    # Demonstration inputs: no output files are written.
    resume_id = "resume_001"
    jd_filename = "jd_001_data_scientist.json"

    skills_data = load_json(
        DATA_DIR / "skills" / f"{resume_id}_skills.json"
    )
    experience_data = load_json(
        DATA_DIR / "experience" / f"{resume_id}_experience.json"
    )
    education_data = load_json(
        DATA_DIR / "education" / f"{resume_id}_education.json"
    )
    jd_data = load_json(DATA_DIR / "jd_profiles" / jd_filename)

    semantic_records = load_json(
        DATA_DIR / "semantic_matching" / "multi_job_validation.json"
    )

    actual_resume_id = skills_data["resume_id"]
    jd_id = jd_filename.removesuffix(".json")
    semantic_result = next(
        (
            item for item in semantic_records
            if item.get("resume_id") == actual_resume_id
            and item.get("jd_id") == jd_id
        ),
        None,
    )

    candidate_number = actual_resume_id.split("_")[-1]
    job_number = jd_id.split("_")[1]

    result = ATSScoringEngine().calculate_score(
        candidate_id=f"CAND_{candidate_number}",
        job_id=f"JOB_{job_number}",
        role=jd_data["role"],
        resume_skills=skills_data.get("skills", []),
        experience_data=experience_data,
        education_data=education_data,
        semantic_result=semantic_result,
        jd_skills=jd_data.get("skills", {}),
        jd_experience=jd_data.get("experience", {}),
        jd_education=jd_data.get("education", {}),
    )

    print("\n" + "=" * 58)
    print("DAY 20 — ATS LIVE SCORING DEMONSTRATION")
    print("=" * 58)
    print(f"Candidate : {result['candidate_id']}")
    print(f"Job       : {result['job_id']}")
    print(f"Role      : {result['role']}")
    print(f"Experience: {experience_data.get('total_experience_years', 'N/A')} years")
    print("\nComponent scores (0–100):")

    for name, score in result["component_scores"].items():
        value = "Unavailable" if score is None else f"{score:.2f}"
        weight = result["adjusted_weights"].get(name, 0.0)
        contribution = result["weighted_contributions"].get(name, 0.0)
        print(
            f"  {name:24} score={value:>11}  "
            f"weight={weight:.3f}  contribution={contribution:.2f}"
        )

    print(f"\nFINAL ATS SCORE: {result['final_ats_score']:.2f}/100")
    print(f"Available components: {', '.join(result['available_components']) or 'None'}")
    print(f"Missing components  : {', '.join(result['missing_components']) or 'None'}")
    print("\nImportant: this is a scoring result, not a hiring decision.")
    print("Review candidate evidence and validate the model before real hiring use.")
    print("\nRead-only demo complete. No score output files were written.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nDEMO FAILED: {type(exc).__name__}: {exc}")
        raise
