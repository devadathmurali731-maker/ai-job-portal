"""Run eligibility decisions against existing ATS output files."""

import json
from pathlib import Path

from eligibility.eligibility_engine import decide_eligibility, load_rules

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "processed"
ATS_DIR = DATA_DIR / "ats_scores_v2"
OUTPUT_DIR = DATA_DIR / "eligibility_results"

CANDIDATE_ID = "CAND_001"
JOB_ID = "JOB_001"


def read_json(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def find_ats_result():
    if not ATS_DIR.exists():
        raise FileNotFoundError(f"ATS output directory not found: {ATS_DIR}")

    for path in ATS_DIR.rglob("*.json"):
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue

        if (
            isinstance(data, dict)
            and data.get("candidate_id") == CANDIDATE_ID
            and data.get("job_id") == JOB_ID
        ):
            print(f"ATS result: {path.relative_to(ROOT)}")
            return data

    raise FileNotFoundError(
        f"No ATS result found for {CANDIDATE_ID} and {JOB_ID} "
        f"inside {ATS_DIR}"
    )


def find_data_file(folder_name, filename):
    folder = DATA_DIR / folder_name
    expected = folder / filename

    if expected.exists():
        return expected

    # Fall back to searching within processed data.
    matches = list(DATA_DIR.rglob(filename))
    matches = [
        path for path in matches
        if folder_name.casefold() in str(path.parent).casefold()
    ]
    if matches:
        return matches[0]

    return None


def extract_skill_names(data):
    """Accept common skill JSON structures."""
    skills = data.get("skills", [])

    if isinstance(skills, dict):
        # Support categories such as technical_skills or soft_skills.
        items = []
        for value in skills.values():
            if isinstance(value, list):
                items.extend(value)
        skills = items

    if not isinstance(skills, list):
        return None

    names = []
    for item in skills:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict):
            name = (
                item.get("skill")
                or item.get("name")
                or item.get("normalized_skill")
            )
            if name:
                names.append(name)

    return names


def main():
    ats_result = find_ats_result()

    # CAND_001 maps to resume_001 for this project demo.
    resume_id = "resume_" + CANDIDATE_ID.split("_")[-1]

    skills_path = find_data_file(
        "skills", f"{resume_id}_skills.json"
    )
    experience_path = find_data_file(
        "experience", f"{resume_id}_experience.json"
    )

    candidate = {}

    if skills_path:
        skills_data = read_json(skills_path)
        skills = extract_skill_names(skills_data)
        if skills is not None:
            candidate["skills"] = skills
        print(f"Skills data: {skills_path.relative_to(ROOT)}")
    else:
        print("Skills file not found; engine will use ATS skill evidence.")

    if experience_path:
        experience_data = read_json(experience_path)
        years = experience_data.get("total_experience_years")
        if years is not None:
            candidate["experience_years"] = years
        print(f"Experience data: {experience_path.relative_to(ROOT)}")
    else:
        print("Experience file not found; engine will use ATS experience evidence.")

    # Location and availability are not inferred when the source data is absent.
    rules = load_rules()
    result = decide_eligibility(
        ats_result=ats_result,
        candidate=candidate,
        rules=rules,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{CANDIDATE_ID}_{JOB_ID}_eligibility.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print("\n--- Eligibility Decision ---")
    print(f"Candidate: {result['candidate_id']}")
    print(f"Job: {result['job_id']}")
    print(f"Role: {result['role']}")
    print(f"ATS score: {result['ats_score']}")
    print(f"Decision: {result['eligibility_status']}")
    print("\nReasons:")
    for reason in result["reasons"]:
        print(f"- {reason}")

    print(f"\nSaved result: {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
