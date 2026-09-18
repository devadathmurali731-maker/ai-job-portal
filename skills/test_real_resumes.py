import json
from pathlib import Path

from skill_extractor import extract_skills


SEGMENTED_DIR = Path("data/processed/segmented")


def test_real_resume_skill_extraction():

    resume_file = SEGMENTED_DIR / "resume_001_sections.json"

    assert resume_file.exists()

    with open(resume_file, "r", encoding="utf-8") as file:
        resume_data = json.load(file)

    # Extract skills from the Skills section
    skills_section = resume_data.get("skills", [])

    text = " ".join(skills_section)

    result = extract_skills(text)

    assert "skills" in result
    assert isinstance(result["skills"], list)

    skills = [
        item["skill"]
        for item in result["skills"]
    ]

    print("\nExtracted Skills:")
    for skill in skills:
        print("-", skill)

    assert "Java" in skills
    assert "Python" in skills
    assert "SQL" in skills
    assert "Spring Boot" in skills
    assert "Docker" in skills
    assert "Git" in skills

def test_all_skill_profiles_exist_and_are_valid():

    output_dir = Path("data/processed/skills")

    profile_files = sorted(
        output_dir.glob("*_skills.json")
    )

    assert len(profile_files) == 4

    for profile_file in profile_files:

        with open(
            profile_file,
            "r",
            encoding="utf-8"
        ) as file:
            profile = json.load(file)

        assert "resume_id" in profile
        assert "skills" in profile
        assert isinstance(profile["skills"], list)

        for item in profile["skills"]:
            assert "skill" in item
            assert "confidence" in item
            assert isinstance(item["skill"], str)
            assert 0 <= item["confidence"] <= 1