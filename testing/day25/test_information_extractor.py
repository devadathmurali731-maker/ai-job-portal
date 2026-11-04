
from src.answer_understanding.information_extractor import (
    extract_skills,
    extract_experience,
    extract_availability,
    extract_salary,
    extract_information
)


def test_extract_skills():
    result = extract_skills("I know Python, SQL and Power BI.")
    assert "Python" in result
    assert "SQL" in result
    assert "Power BI" in result


def test_extract_experience_years():
    result = extract_experience("I have 3 years of experience.")
    assert result == {"value": 3.0, "unit": "years"}


def test_extract_experience_months():
    result = extract_experience("I worked for 6 months.")
    assert result == {"value": 6.0, "unit": "months"}


def test_extract_immediate_availability():
    result = extract_availability("I can join immediately.")
    assert result["type"] == "immediate"
    assert result["value"] == 0


def test_extract_notice_period():
    result = extract_availability("My notice period is 30 days.")
    assert result["value"] == 30
    assert result["unit"] == "days"


def test_extract_salary_lpa():
    result = extract_salary("My expected salary is 6 LPA.")
    assert result["amount"] == 600000
    assert result["currency"] == "INR"
    assert result["period"] == "year"


def test_extract_empty_information():
    result = extract_information("")
    assert result["skills"] == []
    assert result["experience"]["value"] is None
    assert result["salary_expectation"]["amount"] is None
