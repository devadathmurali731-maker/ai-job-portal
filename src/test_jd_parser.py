from pathlib import Path
import json

from jd_parser import parse_job_description


BASE_DIR = Path(__file__).resolve().parent.parent

JD_DIR = BASE_DIR / "job_descriptions"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "jd_profiles"


def test_jd_files_exist():
    """
    Check that all job description files exist.
    """

    jd_files = list(JD_DIR.glob("*.txt"))

    assert len(jd_files) >= 6


def test_parser_returns_dictionary():
    """
    Check that the parser returns a dictionary.
    """

    jd_file = JD_DIR / "jd_001_data_scientist.txt"

    text = jd_file.read_text(
        encoding="utf-8"
    )

    result = parse_job_description(text)

    assert isinstance(result, dict)


def test_required_sections_exist():
    """
    Check that the structured JD contains
    all major sections.
    """

    jd_file = JD_DIR / "jd_001_data_scientist.txt"

    text = jd_file.read_text(
        encoding="utf-8"
    )

    result = parse_job_description(text)

    assert "role" in result
    assert "skills" in result
    assert "experience" in result
    assert "education" in result
    assert "normalized_text" in result


def test_data_scientist_role():
    """
    Check whether the Data Scientist role
    is extracted correctly.
    """

    jd_file = JD_DIR / "jd_001_data_scientist.txt"

    text = jd_file.read_text(
        encoding="utf-8"
    )

    result = parse_job_description(text)

    assert result["role"] == "Data Scientist"


def test_required_skill_extraction():
    """
    Check whether required skills are extracted.
    """

    jd_file = JD_DIR / "jd_001_data_scientist.txt"

    text = jd_file.read_text(
        encoding="utf-8"
    )

    result = parse_job_description(text)

    required_skills = result["skills"]["required"]

    assert "Python" in required_skills
    assert "SQL" in required_skills
    assert "Machine Learning" in required_skills


def test_preferred_skill_extraction():
    """
    Check whether preferred skills are extracted.
    """

    jd_file = JD_DIR / "jd_001_data_scientist.txt"

    text = jd_file.read_text(
        encoding="utf-8"
    )

    result = parse_job_description(text)

    preferred_skills = result["skills"]["preferred"]

    assert "Power BI" in preferred_skills
    assert "TensorFlow" in preferred_skills


def test_experience_extraction():
    """
    Check whether experience requirements
    are extracted correctly.
    """

    jd_file = JD_DIR / "jd_001_data_scientist.txt"

    text = jd_file.read_text(
        encoding="utf-8"
    )

    result = parse_job_description(text)

    experience = result["experience"]

    assert experience["minimum_years"] == 2
    assert experience["maximum_years"] == 5


def test_json_outputs_exist():
    """
    Check whether structured JSON profiles
    have been created.
    """

    json_files = list(OUTPUT_DIR.glob("*.json"))

    assert len(json_files) >= 6


def test_json_files_are_valid():
    """
    Check that generated JSON files are valid.
    """

    json_files = list(OUTPUT_DIR.glob("*.json"))

    for json_file in json_files:

        data = json.loads(
            json_file.read_text(
                encoding="utf-8"
            )
        )

        assert isinstance(data, dict)