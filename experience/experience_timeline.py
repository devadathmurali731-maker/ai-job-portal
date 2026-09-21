from typing import List, Dict


def date_to_month_index(date_string: str) -> int:
    """
    Convert YYYY-MM into a single month index.

    This makes date comparison easier.
    """

    year, month = map(
        int,
        date_string.split("-")
    )

    return year * 12 + month


def month_index_to_date(month_index: int) -> str:
    """
    Convert a month index back into YYYY-MM.
    """

    year = month_index // 12
    month = month_index % 12

    if month == 0:
        year -= 1
        month = 12

    return f"{year:04d}-{month:02d}"


def detect_gaps(
    experiences: List[Dict]
) -> List[Dict]:
    """
    Detect gaps between employment periods.
    """

    gaps = []

    if len(experiences) < 2:
        return gaps

    sorted_experiences = sorted(
        experiences,
        key=lambda x: x["start_date"]
    )

    for i in range(len(sorted_experiences) - 1):

        current = sorted_experiences[i]
        next_role = sorted_experiences[i + 1]

        current_end = date_to_month_index(
            current["end_date"]
        )

        next_start = date_to_month_index(
            next_role["start_date"]
        )

        gap_months = (
            next_start
            - current_end
            - 1
        )

        if gap_months > 0:

            gaps.append(
                {
                    "gap_start": current["end_date"],
                    "gap_end": next_role["start_date"],
                    "duration_months": gap_months
                }
            )

    return gaps


def detect_overlaps(
    experiences: List[Dict]
) -> List[Dict]:
    """
    Detect overlapping employment periods.

    Overlaps are reported for analysis and
    are not automatically considered errors.
    """

    overlaps = []

    if len(experiences) < 2:
        return overlaps

    sorted_experiences = sorted(
        experiences,
        key=lambda x: x["start_date"]
    )

    for i in range(len(sorted_experiences) - 1):

        role_1 = sorted_experiences[i]
        role_2 = sorted_experiences[i + 1]

        start_1 = date_to_month_index(
            role_1["start_date"]
        )

        end_1 = date_to_month_index(
            role_1["end_date"]
        )

        start_2 = date_to_month_index(
            role_2["start_date"]
        )

        end_2 = date_to_month_index(
            role_2["end_date"]
        )

        overlap_start = max(
            start_1,
            start_2
        )

        overlap_end = min(
            end_1,
            end_2
        )

        if overlap_start <= overlap_end:

            overlaps.append(
                {
                    "role_1": role_1["company"],
                    "role_2": role_2["company"],
                    "overlap_start": (
                        month_index_to_date(
                            overlap_start
                        )
                    ),
                    "overlap_end": (
                        month_index_to_date(
                            overlap_end
                        )
                    )
                }
            )

    return overlaps

if __name__ == "__main__":

    sample_experiences = [
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
        },
        {
            "company": "Data Solutions Ltd",
            "job_title": "Senior Data Analyst",
            "start_date": "2024-06",
            "end_date": "2026-09"
        }
    ]

    gaps = detect_gaps(
        sample_experiences
    )

    overlaps = detect_overlaps(
        sample_experiences
    )

    print("\nDetected Gaps:")
    print(gaps)

    print("\nDetected Overlaps:")
    print(overlaps)