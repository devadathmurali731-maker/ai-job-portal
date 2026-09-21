from datetime import datetime

from experience_parser import (
    parse_experience_date_range,
    calculate_duration_months,
    calculate_total_experience,
    parse_work_experience_section
)


def test_parse_date_range():

    result = parse_experience_date_range(
        "January 2020 - March 2022"
    )

    assert result["start_date"] == "2020-01"
    assert result["end_date"] == "2022-03"


def test_calculate_duration():

    start_date = datetime(
        2020,
        1,
        1
    )

    end_date = datetime(
        2022,
        3,
        1
    )

    duration = calculate_duration_months(
        start_date,
        end_date
    )

    assert duration == 27


def test_parse_work_experience():

    work_experience = [
        "ABC Technologies",
        "Software Engineer",
        "2022 - Present",
        "- Developed REST APIs.",
        "- Worked with SQL."
    ]

    result = parse_work_experience_section(
        work_experience
    )

    assert len(result) == 1
    assert result[0]["company"] == "ABC Technologies"
    assert result[0]["job_title"] == "Software Engineer"


def test_total_experience():

    experiences = [
        {
            "start_date": "2020-01",
            "end_date": "2022-12"
        },
        {
            "start_date": "2023-01",
            "end_date": "2024-12"
        }
    ]

    total = calculate_total_experience(
        experiences
    )

    assert total == 5.0