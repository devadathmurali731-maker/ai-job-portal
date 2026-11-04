
from src.answer_understanding.intent_classifier import classify_intent


def test_skills_intent():
    result = classify_intent("I know Python, SQL and Excel.")
    assert result["intent"] == "skills"


def test_experience_intent():
    result = classify_intent("I have 3 years of professional experience.")
    assert result["intent"] == "experience"


def test_availability_intent():
    result = classify_intent("I can join immediately.")
    assert result["intent"] == "availability"


def test_salary_intent():
    result = classify_intent("My expected salary is 6 LPA.")
    assert result["intent"] == "salary_expectation"


def test_empty_answer():
    result = classify_intent("")
    assert result["intent"] == "missing"


def test_general_answer():
    result = classify_intent("I enjoy learning new things.")
    assert result["intent"] == "general"


def test_confidence_range():
    result = classify_intent("I have Python skills.")
    assert 0 <= result["confidence"] <= 1
