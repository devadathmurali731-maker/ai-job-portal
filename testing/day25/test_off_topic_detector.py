
from src.answer_understanding.off_topic_detector import detect_off_topic


def test_relevant_skills_answer():
    result = detect_off_topic(
        "skills",
        "I know Python, SQL and Excel."
    )
    assert result["is_off_topic"] is False


def test_irrelevant_salary_answer():
    result = detect_off_topic(
        "skills",
        "My expected salary is 6 LPA."
    )
    assert result["is_off_topic"] is True


def test_relevant_experience_answer():
    result = detect_off_topic(
        "experience",
        "I have 3 years of experience."
    )
    assert result["is_off_topic"] is False


def test_irrelevant_experience_answer():
    result = detect_off_topic(
        "experience",
        "I can join immediately."
    )
    assert result["is_off_topic"] is True


def test_relevant_availability_answer():
    result = detect_off_topic(
        "availability",
        "I can join immediately."
    )
    assert result["is_off_topic"] is False


def test_relevant_salary_answer():
    result = detect_off_topic(
        "salary",
        "My expected salary is 6 LPA."
    )
    assert result["is_off_topic"] is False


def test_missing_answer():
    result = detect_off_topic("skills", "")
    assert result["detected_intent"] == "missing"


def test_unknown_question_type():
    result = detect_off_topic(
        "other",
        "I enjoy learning new things."
    )
    assert result["is_off_topic"] is False
