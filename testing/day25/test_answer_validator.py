
from src.answer_understanding.answer_validator import validate_answer


def test_missing_answer():
    result = validate_answer("skills", "")
    assert result["status"] == "missing"


def test_vague_answer():
    result = validate_answer("skills", "I don't know.")
    assert result["status"] == "vague"
    assert result["is_vague"] is True


def test_valid_skills_answer():
    result = validate_answer("skills", "I know Python and SQL.")
    assert result["status"] == "complete"


def test_valid_experience_answer():
    result = validate_answer("experience", "I have 3 years of experience.")
    assert result["status"] == "complete"


def test_invalid_experience_answer():
    result = validate_answer("experience", "I am hardworking.")
    assert result["status"] == "vague"


def test_valid_availability_answer():
    result = validate_answer("availability", "I can join immediately.")
    assert result["status"] == "complete"


def test_valid_salary_answer():
    result = validate_answer("salary", "My expected salary is 6 LPA.")
    assert result["status"] == "complete"


def test_invalid_salary_answer():
    result = validate_answer("salary", "I expect a good package.")
    assert result["status"] == "vague"


def test_missing_fields_for_skills():
    result = validate_answer("skills", "I enjoy learning.")
    assert "skills" in result["missing_fields"]
