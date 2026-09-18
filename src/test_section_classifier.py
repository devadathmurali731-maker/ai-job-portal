import json
from pathlib import Path

from resume_section_classifier import (
    normalize_heading,
    classify_heading,
    is_section_heading,
    segment_resume_sections,
    segment_resume_file,
    detect_section_from_content
)


def test_normalize_heading():
    assert normalize_heading("  TECHNICAL SKILLS  ") == "technical skills"
    assert normalize_heading("WORK-EXPERIENCE") == "work experience"
    assert normalize_heading("LICENSES & CERTIFICATIONS") == (
        "licenses and certifications"
    )
    assert normalize_heading("1. SKILLS") == "skills"
    assert normalize_heading("02. EDUCATION") == "education"
    assert normalize_heading("3) PROJECTS") == "projects"
    assert normalize_heading("SKILLS:") == "skills"
    assert normalize_heading("WORK EXPERIENCE:") == "work experience"


def test_classify_skills():
    assert classify_heading("SKILLS") == "skills"
    assert classify_heading("TECHNICAL SKILLS") == "skills"
    assert classify_heading("CORE SKILLS") == "skills"


def test_classify_work_experience():
    assert classify_heading("WORK EXPERIENCE") == "work_experience"
    assert classify_heading("PROFESSIONAL EXPERIENCE") == "work_experience"
    assert classify_heading("EMPLOYMENT HISTORY") == "work_experience"


def test_classify_education():
    assert classify_heading("EDUCATION") == "education"
    assert classify_heading("ACADEMIC QUALIFICATIONS") == "education"


def test_classify_projects():
    assert classify_heading("PROJECTS") == "projects"
    assert classify_heading("ACADEMIC PROJECTS") == "projects"


def test_classify_certifications():
    assert classify_heading("CERTIFICATIONS") == "certifications"
    assert classify_heading("PROFESSIONAL CERTIFICATIONS") == "certifications"


def test_unknown_heading():
    assert classify_heading("RANDOM SECTION") is None

def test_segment_resume_sections():

    resume_text = """
    PRIYA NAIR

    SKILLS
    Python
    SQL
    Machine Learning

    WORK EXPERIENCE
    Data Analyst
    ABC Company
    2024 - Present

    EDUCATION
    M.Sc Data Science
    University of Kerala

    PROJECTS
    Customer Churn Prediction
    """

    sections = segment_resume_sections(resume_text)

    assert "skills" in sections
    assert "work_experience" in sections
    assert "education" in sections
    assert "projects" in sections

    assert "Python" in sections["skills"]
    assert "SQL" in sections["skills"]

    assert "Data Analyst" in sections["work_experience"]

    assert "M.Sc Data Science" in sections["education"]

    assert "Customer Churn Prediction" in sections["projects"]


from pathlib import Path


def test_real_resume_file_exists():

    resume_path = Path("data/processed/resume_001.txt")

    assert resume_path.exists()


def test_real_resume_segmentation():

    resume_path = "data/processed/resume_001.txt"

    sections = segment_resume_file(resume_path)

    assert isinstance(sections, dict)
    assert len(sections) > 0

def test_all_real_resumes_segmentation():

    resume_files = [
        "data/processed/resume_001.txt",
        "data/processed/resume_002.txt",
        "data/processed/resume_003.txt",
        "data/processed/resume_004.txt"
    ]

    for file_path in resume_files:

        sections = segment_resume_file(file_path)

        print(f"\nTesting: {file_path}")
        print("Detected sections:", list(sections.keys()))

        assert isinstance(sections, dict)
        assert len(sections) > 0

def test_alternative_section_headings():

    test_headings = {

        "Technical Proficiencies": "skills",
        "Core Skills": "skills",
        "Employment History": "work_experience",
        "Work History": "work_experience",
        "Academic Background": "education",
        "Educational Qualifications": "education",
        "Licenses & Certifications": "certifications",
        "Professional Certifications": "certifications",
        "Project Experience": "projects",
        "Academic Projects": "projects",
    }

    for heading, expected_section in test_headings.items():

        result = classify_heading(heading)

        print(f"{heading} -> {result}")

        assert result == expected_section

def test_content_based_section_detection():

    test_lines = {
        "Python and SQL": "skills",
        "Machine Learning and Power BI": "skills",
        "M.Sc Data Science": "education",
        "University of Kerala": "education",
        "Software Engineer with 4 years of experience": "work_experience",
        "Data Analyst - 2023 - Present": "work_experience",
        "Customer Churn Prediction Project": "projects",
    }

    for line, expected_section in test_lines.items():

        result = detect_section_from_content(line)

        print(f"{line} -> {result}")

        assert result == expected_section

def test_resume_without_section_headings():

    resume_text = """
    PRIYA NAIR

    Python
    SQL
    Machine Learning
    Power BI

    Software Engineer
    ABC Technologies
    4 years of experience
    2022 - Present

    M.Sc Data Science
    University of Kerala

    Customer Churn Prediction Project
    Developed a machine learning model for customer churn prediction.
    """

    sections = segment_resume_sections(resume_text)

    print("\nDetected sections:")
    print(sections)

    assert "skills" in sections
    assert "work_experience" in sections
    assert "education" in sections
    assert "projects" in sections

def test_table_style_resumes():

    table_style_resumes = [
        "data/processed/resume_002.txt",
        "data/processed/resume_004.txt"
    ]

    for file_path in table_style_resumes:

        sections = segment_resume_file(file_path)

        print(f"\nTable-style resume: {file_path}")
        print("Detected sections:", list(sections.keys()))

        assert isinstance(sections, dict)
        assert len(sections) > 0

def test_fuzzy_heading_matching():

    test_headings = {
        "Professional Experiance": "work_experience",
        "Educaton": "education",
        "Certificats": "certifications",
        "Projcts": "projects",
        "Techncal Skills": "skills",
    }

    for heading, expected_section in test_headings.items():

        result = classify_heading(heading)

        print(f"{heading} -> {result}")

        assert result == expected_section

def test_segmented_json_outputs():

    json_directory = Path("data/processed/segmented")

    resume_files = [
        "resume_001_sections.json",
        "resume_002_sections.json",
        "resume_003_sections.json",
        "resume_004_sections.json"
    ]
    

    for filename in resume_files:

        file_path = json_directory / filename

        assert file_path.exists()

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, dict)
        assert len(data) > 0

        for section_name, content in data.items():
            assert isinstance(section_name, str)
            assert isinstance(content, list)