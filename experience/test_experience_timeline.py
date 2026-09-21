from experience_timeline import (
    detect_gaps,
    detect_overlaps
)


def test_detect_gap():

    experiences = [
        {
            "company": "ABC Technologies",
            "job_title": "Software Engineer",
            "start_date": "2020-01",
            "end_date": "2022-06"
        },
        {
            "company": "XYZ Analytics",
            "job_title": "Data Analyst",
            "start_date": "2022-10",
            "end_date": "2024-12"
        }
    ]

    gaps = detect_gaps(
        experiences
    )

    assert len(gaps) == 1
    assert gaps[0]["duration_months"] == 3


def test_no_gap():

    experiences = [
        {
            "company": "ABC Technologies",
            "job_title": "Software Engineer",
            "start_date": "2020-01",
            "end_date": "2022-12"
        },
        {
            "company": "XYZ Analytics",
            "job_title": "Data Analyst",
            "start_date": "2023-01",
            "end_date": "2024-12"
        }
    ]

    gaps = detect_gaps(
        experiences
    )

    assert gaps == []


def test_detect_overlap():

    experiences = [
        {
            "company": "ABC Technologies",
            "job_title": "Software Engineer",
            "start_date": "2020-01",
            "end_date": "2022-06"
        },
        {
            "company": "XYZ Analytics",
            "job_title": "Data Analyst",
            "start_date": "2022-04",
            "end_date": "2024-12"
        }
    ]

    overlaps = detect_overlaps(
        experiences
    )

    assert len(overlaps) == 1
    assert overlaps[0]["overlap_start"] == "2022-04"
    assert overlaps[0]["overlap_end"] == "2022-06"


def test_no_overlap():

    experiences = [
        {
            "company": "ABC Technologies",
            "job_title": "Software Engineer",
            "start_date": "2020-01",
            "end_date": "2022-06"
        },
        {
            "company": "XYZ Analytics",
            "job_title": "Data Analyst",
            "start_date": "2022-07",
            "end_date": "2024-12"
        }
    ]

    overlaps = detect_overlaps(
        experiences
    )

    assert overlaps == []