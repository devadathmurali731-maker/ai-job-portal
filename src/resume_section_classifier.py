import json
from pathlib import Path

"""
Resume Section Classifier

Day 8 - Resume Section Segmentation

This module identifies and separates major sections
from cleaned resume text.
"""

# Common resume heading variations mapped to standard section names.

SECTION_HEADINGS = {

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "technical proficiencies",
        "skill set",
        "technical expertise",
        "professional skills",
        "areas of expertise"
    ],

    "work_experience": [
        "work experience",
        "experience",
        "professional experience",
        "employment history",
        "work history",
        "career experience",
        "professional background"
    ],

    "education": [
        "education",
        "educational qualifications",
        "academic qualifications",
        "academic background",
        "educational background",
        "academic history"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
        "licenses and certifications",
        "licenses & certifications",
        "certification"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
        "project experience",
        "project work"
    ],

    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "profile",
        "professional profile"
    ],

    "objective": [
        "objective",
        "career objective",
        "professional objective"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "key achievements"
    ],

    "awards": [
        "awards",
        "honors",
        "honours"
    ],

    "languages": [
        "languages",
        "language skills"
    ],

    "interests": [
        "interests",
        "hobbies",
        "hobbies and interests"
    ],

    "references": [
        "references",
        "professional references"
    ]
}

def normalize_heading(heading):
    """
    Normalize a resume heading so that it can be
    compared with the known section headings.
    """

    if not heading:
        return ""

    heading = heading.strip()
    heading = heading.lower()

    # Remove numbering at the beginning.
    # Examples:
    # "1. Skills" -> "Skills"
    # "02. Education" -> "Education"
    # "3) Projects" -> "Projects"
    import re

    heading = re.sub(r"^\s*\d+\s*[\.\):\-]\s*", "", heading)

    # Replace common separators with spaces
    heading = heading.replace("&", "and")
    heading = heading.replace("-", " ")
    heading = heading.replace("_", " ")

    # Remove common punctuation
    heading = heading.replace(":", "")
    heading = heading.replace(".", "")

    # Remove extra spaces
    heading = " ".join(heading.split())

    return heading

from difflib import SequenceMatcher

def classify_heading(heading):
    """
    Identify the standard section name for a resume heading.

    Uses:
    1. Exact normalized matching.
    2. Fuzzy matching for slightly different headings.

    Returns:
        Canonical section name if matched.
        None if the heading is unknown.
    """

    normalized_heading = normalize_heading(heading)

    if not normalized_heading:
        return None

    # First try exact matching
    for section_name, headings in SECTION_HEADINGS.items():

        normalized_headings = [
            normalize_heading(item)
            for item in headings
        ]

        if normalized_heading in normalized_headings:
            return section_name

    # If exact matching fails, use fuzzy matching
    best_section = None
    best_score = 0

    for section_name, headings in SECTION_HEADINGS.items():

        for item in headings:

            normalized_item = normalize_heading(item)

            score = SequenceMatcher(
                None,
                normalized_heading,
                normalized_item
            ).ratio()

            if score > best_score:
                best_score = score
                best_section = section_name

    # Accept only reasonably similar headings
    if best_score >= 0.75:
        return best_section

    return None

def is_section_heading(line):
    """
    Check whether a line is a recognized resume section heading.

    Returns:
        True if the line is a known section heading.
        False otherwise.
    """

    if not line:
        return False

    return classify_heading(line) is not None
def segment_resume_sections(text):
    """
    Divide resume text into logical sections.

    Uses explicit headings when available.
    For resumes without headings, uses content-based detection.
    """

    sections = {}
    current_section = None
    has_explicit_heading = False

    lines = text.splitlines()

    # Check whether the resume contains any recognized heading
    for line in lines:
        line = line.strip()

        if line and classify_heading(line):
            has_explicit_heading = True
            break

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # --------------------------------------------------
        # 1. Explicit heading
        # --------------------------------------------------

        section_name = classify_heading(line)

        if section_name:
            current_section = section_name

            if current_section not in sections:
                sections[current_section] = []

            continue

        # --------------------------------------------------
        # 2. Content-based detection
        # --------------------------------------------------

        detected_section = detect_section_from_content(line)

        if not has_explicit_heading and detected_section:

            if detected_section != current_section:

                current_section = detected_section

                if current_section not in sections:
                    sections[current_section] = []

        # --------------------------------------------------
        # 3. Add content
        # --------------------------------------------------

        if current_section:
            sections[current_section].append(line)

    return sections

def segment_resume_file(file_path):
    """
    Read a cleaned resume text file and divide it into sections.

    Args:
        file_path: Path to the cleaned resume TXT file.

    Returns:
        Dictionary containing detected resume sections.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return segment_resume_sections(text)

def detect_section_from_content(line):
    """
    Detect a possible resume section from the content itself
    when an explicit section heading is missing.

    Returns:
        Section name if detected.
        None otherwise.
    """

    if not line:
        return None

    text = line.lower()

    # Skills indicators
    skill_keywords = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "power bi",
        "tableau",
        "java",
        "docker",
        "git"
    ]

    if any(keyword in text for keyword in skill_keywords):
        return "skills"

    # Education indicators
    education_keywords = [
        "b.tech",
        "b.e",
        "bachelor",
        "m.tech",
        "m.sc",
        "mca",
        "master",
        "university",
        "college",
        "degree"
    ]

    if any(keyword in text for keyword in education_keywords):
        return "education"

    # Work experience indicators
    experience_keywords = [
        "years of experience",
        "software engineer",
        "data analyst",
        "data scientist",
        "business analyst",
        "developer",
        "manager",
        "intern",
        "present"
    ]

    if any(keyword in text for keyword in experience_keywords):
        return "work_experience"

    # Project indicators
    project_keywords = [
        "project",
        "developed",
        "prediction",
        "classification",
        "forecasting",
        "dashboard"
    ]

    if any(keyword in text for keyword in project_keywords):
        return "projects"

    return None

def save_segmented_resume(sections, output_path):
    """
    Save segmented resume sections as a JSON file.

    Args:
        sections: Dictionary containing resume sections.
        output_path: Location where the JSON file will be saved.
    """

    output_path = Path(output_path)

    # Create the parent directory if it does not exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            sections,
            file,
            indent=4,
            ensure_ascii=False
        )

if __name__ == "__main__":

    input_directory = Path("data/processed")
    output_directory = Path("data/processed/segmented")

    resume_files = [
        "resume_001.txt",
        "resume_002.txt",
        "resume_003.txt",
        "resume_004.txt"
    ]

    print("\nResume Section Segmentation")
    print("=" * 50)

    for resume_file in resume_files:

        input_path = input_directory / resume_file

        # Create output filename
        output_filename = input_path.stem + "_sections.json"
        output_path = output_directory / output_filename

        # Segment resume
        sections = segment_resume_file(input_path)

        # Save as JSON
        save_segmented_resume(sections, output_path)

        print(f"\nProcessed: {resume_file}")
        print(f"Sections: {list(sections.keys())}")
        print(f"Saved: {output_path}")