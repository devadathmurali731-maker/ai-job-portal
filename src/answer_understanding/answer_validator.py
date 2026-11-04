
from src.answer_understanding.information_extractor import extract_information


VAGUE_PHRASES = [
    "i don't know",
    "not sure",
    "maybe",
    "anything",
    "whatever",
    "no idea",
    "good",
    "hardworking",
    "as per company standards"
]


def validate_answer(question_type: str, answer: str) -> dict:
    """Identify missing, vague, or incomplete candidate answers."""

    if not isinstance(answer, str) or not answer.strip():
        return {
            "status": "missing",
            "is_vague": False,
            "missing_fields": ["answer"],
            "reason": "Candidate did not provide an answer"
        }

    text = answer.strip().lower()

    if any(phrase in text for phrase in VAGUE_PHRASES):
        return {
            "status": "vague",
            "is_vague": True,
            "missing_fields": [],
            "reason": "Answer contains vague or uncertain wording"
        }

    information = extract_information(answer)
    question_type = question_type.lower()

    required_fields = {
        "skills": "skills",
        "experience": "experience",
        "availability": "availability",
        "salary": "salary_expectation",
        "salary_expectation": "salary_expectation"
    }

    field = required_fields.get(question_type)

    if field == "skills" and not information["skills"]:
        return {
            "status": "vague",
            "is_vague": True,
            "missing_fields": ["skills"],
            "reason": "No recognizable skills were identified"
        }

    if field == "experience" and information["experience"]["value"] is None:
        return {
            "status": "vague",
            "is_vague": True,
            "missing_fields": ["experience"],
            "reason": "No clear experience duration was identified"
        }

    if field == "availability" and information["availability"]["type"] is None:
        return {
            "status": "vague",
            "is_vague": True,
            "missing_fields": ["availability"],
            "reason": "No clear joining availability was identified"
        }

    if field == "salary" and information["salary_expectation"]["amount"] is None:
        return {
            "status": "vague",
            "is_vague": True,
            "missing_fields": ["salary_expectation"],
            "reason": "No clear salary expectation was identified"
        }

    return {
        "status": "complete",
        "is_vague": False,
        "missing_fields": [],
        "reason": "Answer contains recognizable information"
    }
