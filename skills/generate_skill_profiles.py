import json
from pathlib import Path

from skill_extractor import extract_skills


SEGMENTED_DIR = Path("data/processed/segmented")
OUTPUT_DIR = Path("data/processed/skills")


def generate_skill_profile(resume_file):
    with open(resume_file, "r", encoding="utf-8") as file:
        resume_data = json.load(file)

    # Combine important resume sections
    sections = []

    for section_name in [
        "skills",
        "work_experience",
        "projects",
        "summary"
    ]:
        section = resume_data.get(section_name, [])

        if isinstance(section, list):
            sections.extend(section)

        elif isinstance(section, str):
            sections.append(section)

    resume_text = " ".join(sections)

    # Extract skills
    result = extract_skills(resume_text)

    profile = {
        "resume_id": resume_file.stem.replace("_sections", ""),
        "skills": result["skills"]
    }

    return profile


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    resume_files = sorted(
        SEGMENTED_DIR.glob("*_sections.json")
    )

    if not resume_files:
        print("No segmented resume files found.")
        return

    for resume_file in resume_files:

        profile = generate_skill_profile(resume_file)

        output_file = (
            OUTPUT_DIR /
            f"{profile['resume_id']}_skills.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
    