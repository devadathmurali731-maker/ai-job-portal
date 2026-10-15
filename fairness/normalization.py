"""
Resume normalization utilities.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Standardize resume-derived structured data before downstream
fairness-aware evaluation.
"""

from typing import Any, Dict, List


SECTION_ALIASES = {
    "summary": "summary",
    "profile": "summary",
    "professional summary": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "work experience": "work_experience",
    "professional experience": "work_experience",
    "employment history": "work_experience",
    "experience": "work_experience",
    "education": "education",
    "academic background": "education",
    "projects": "projects",
    "project experience": "projects",
    "certifications": "certifications",
    "certificates": "certifications",
}


def normalize_text(value: Any) -> str:
    """
    Normalize a single text value.

    Operations:
    - Convert scalar values to string
    - Remove leading/trailing whitespace
    - Collapse repeated whitespace
    - Convert to lowercase
    """

    if value is None:
        return ""

    text = str(value).strip()

    # Collapse repeated whitespace.
    text = " ".join(text.split())

    return text.lower()


def normalize_skill(skill: Any) -> str:
    """
    Normalize an individual skill name.
    """

    return normalize_text(skill)


def normalize_skill_list(skills: Any) -> List[str]:
    """
    Normalize a list of skills.

    Removes:
    - Empty values
    - Duplicate skills
    """

    if skills is None:
        return []

    if isinstance(skills, str):
        skills = [skills]

    if not isinstance(skills, list):
        return []

    normalized = []

    for skill in skills:
        value = normalize_skill(skill)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


def normalize_text_list(values: Any) -> List[str]:
    """
    Normalize a list of text values while preserving
    the list structure.
    """

    if values is None:
        return []

    if isinstance(values, str):
        values = [values]

    if not isinstance(values, list):
        return []

    normalized = []

    for value in values:
        normalized_value = normalize_text(value)

        if normalized_value:
            normalized.append(normalized_value)

    return normalized


def normalize_section_name(section_name: Any) -> str:
    """
    Convert different section-name representations
    into a standard section name.
    """

    normalized = normalize_text(section_name)

    return SECTION_ALIASES.get(
        normalized,
        normalized.replace(" ", "_"),
    )


def normalize_sections(sections: Any) -> Dict[str, Any]:
    """
    Normalize resume section names and values.
    """

    if not isinstance(sections, dict):
        return {}

    normalized_sections = {}

    for section_name, content in sections.items():
        standard_name = normalize_section_name(
            section_name
        )

        if isinstance(content, list):
            normalized_content = normalize_text_list(
                content
            )

        elif isinstance(content, str):
            normalized_content = normalize_text(
                content
            )

        else:
            normalized_content = content

        normalized_sections[
            standard_name
        ] = normalized_content

    return normalized_sections


def normalize_resume(
    resume: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize a structured resume record.

    The function preserves the original information
    structure while standardizing text and skills.
    """

    if not isinstance(resume, dict):
        raise TypeError(
            "resume must be a dictionary."
        )

    normalized = dict(resume)

    # Normalize common identifier fields.
    for field in (
        "resume_id",
        "candidate_id",
    ):
        if field in normalized:
            normalized[field] = normalize_text(
                normalized[field]
            )

    # Normalize summary/profile while preserving
    # their original data type.
    for field in (
        "summary",
        "profile",
    ):
        if field not in normalized:
            continue

        if isinstance(
            normalized[field],
            list,
        ):
            normalized[field] = normalize_text_list(
                normalized[field]
            )

        else:
            normalized[field] = normalize_text(
                normalized[field]
            )

    # Normalize skills.
    if "skills" in normalized:
        normalized["skills"] = normalize_skill_list(
            normalized["skills"]
        )

    # Normalize common list-based resume sections.
    for field in (
        "work_experience",
        "education",
        "projects",
        "certifications",
    ):
        if field in normalized:
            normalized[field] = normalize_text_list(
                normalized[field]
            )

    # Normalize nested sections if present.
    if "sections" in normalized:
        normalized["sections"] = normalize_sections(
            normalized["sections"]
        )

    return normalized