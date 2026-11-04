
import re


KNOWN_SKILLS = [
    "Python", "Java", "SQL", "Excel", "Power BI", "Tableau",
    "Machine Learning", "Deep Learning", "Data Analysis",
    "Communication", "Leadership", "C++", "JavaScript",
    "HTML", "CSS", "AWS", "Azure", "Git"
]


def extract_skills(text: str) -> list:
    """Extract recognized skills from a candidate's answer."""
    if not isinstance(text, str):
        return []

    found = []

    for skill in KNOWN_SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)

    return found


def extract_experience(text: str) -> dict:
    """Extract years or months of experience."""
    if not isinstance(text, str):
        return {"value": None, "unit": None}

    pattern = (
        r"(\d+(?:\.\d+)?)\s*"
        r"(years?|yrs?|months?|mos?)\b"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return {"value": None, "unit": None}

    value = float(match.group(1))
    unit_text = match.group(2).lower()

    unit = (
        "months"
        if unit_text.startswith(("month", "mo"))
        else "years"
    )

    return {
        "value": value,
        "unit": unit
    }


def extract_availability(text: str) -> dict:
    """Extract joining availability or notice period."""
    if not isinstance(text, str):
        return {"type": None, "value": None, "unit": None}

    lowered = text.lower()

    if "immediately" in lowered or "immediate" in lowered:
        return {
            "type": "immediate",
            "value": 0,
            "unit": "days"
        }

    match = re.search(
        r"(?:notice period\s*(?:is|of)?\s*|"
        r"join(?:ing)?\s+in\s+|"
        r"available\s+in\s+)"
        r"(\d+)\s*(days?|weeks?|months?)",
        lowered
    )

    if not match:
        return {"type": None, "value": None, "unit": None}

    return {
        "type": "notice_period",
        "value": int(match.group(1)),
        "unit": match.group(2)
    }


def extract_salary(text: str) -> dict:
    """Extract salary and normalize LPA to INR per year."""
    if not isinstance(text, str):
        return {"amount": None, "currency": None, "period": None}

    lowered = text.lower()

    lpa_match = re.search(
        r"(?:₹\s*)?(\d+(?:\.\d+)?)\s*"
        r"(?:lpa|lakhs?\s*(?:per annum|pa|/year)?)",
        lowered
    )

    if lpa_match:
        amount = float(lpa_match.group(1)) * 100000

        return {
            "amount": int(amount),
            "currency": "INR",
            "period": "year"
        }

    rupee_match = re.search(
        r"(?:₹|rs\.?\s*)(\d[\d,]*)",
        lowered
    )

    if rupee_match:
        return {
            "amount": int(rupee_match.group(1).replace(",", "")),
            "currency": "INR",
            "period": None
        }

    return {
        "amount": None,
        "currency": None,
        "period": None
    }


def extract_information(text: str) -> dict:
    """Extract all supported candidate information."""
    return {
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "availability": extract_availability(text),
        "salary_expectation": extract_salary(text)
    }
