import re
from datetime import datetime
from typing import List, Dict, Optional


MONTH_MAP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def parse_date(date_text: str) -> Optional[datetime]:
    """
    Convert a month/year string into a datetime object.

    Supported examples:
    January 2020
    Jan 2020
    01/2020
    2020-01
    """

    if not date_text:
        return None

    text = date_text.strip().lower()

    # Format: YYYY-MM
    match = re.fullmatch(r"(\d{4})-(\d{1,2})", text)

    if match:
        year = int(match.group(1))
        month = int(match.group(2))

        if 1 <= month <= 12:
            return datetime(year, month, 1)

    # Format: MM/YYYY
    match = re.fullmatch(r"(\d{1,2})/(\d{4})", text)

    if match:
        month = int(match.group(1))
        year = int(match.group(2))

        if 1 <= month <= 12:
            return datetime(year, month, 1)

    # Format: Month YYYY
    match = re.fullmatch(
        r"([a-zA-Z]+)\s+(\d{4})",
        text
    )

    if match:
        month_text = match.group(1)
        year = int(match.group(2))

        month = MONTH_MAP.get(month_text)

        if month:
            return datetime(year, month, 1)

    # Format: YYYY
    match = re.fullmatch(r"(\d{4})", text)

    if match:
        return datetime(int(match.group(1)), 1, 1)

    return None


def calculate_duration_months(
    start_date: Optional[datetime],
    end_date: Optional[datetime]
) -> int:
    """
    Calculate employment duration in months.
    """

    if not start_date or not end_date:
        return 0

    months = (
        (end_date.year - start_date.year) * 12
        + (end_date.month - start_date.month)
        + 1
    )

    return max(months, 0)


def calculate_experience_years(
    duration_months: int
) -> float:
    """
    Convert experience duration from months to years.
    """

    return round(duration_months / 12, 2)


def parse_experience_date_range(
    date_range: str
) -> Dict:
    """
    Parse employment date ranges.

    Examples:
    January 2020 - March 2022
    Jan 2020 - Present
    2020-01 - 2022-06
    """

    result = {
        "start_date": None,
        "end_date": None,
        "is_current": False
    }

    if not date_range:
        return result

    text = date_range.strip()

    parts = re.split(
        r"\s*(?:-|–|—|to)\s*",
        text,
        maxsplit=1,
        flags=re.IGNORECASE
    )

    if len(parts) != 2:
        return result

    start_text = parts[0].strip()
    end_text = parts[1].strip()

    start_date = parse_date(start_text)

    if end_text.lower() in {
        "present",
        "current",
        "now"
    }:
        end_date = datetime.now()

        result["is_current"] = True
    else:
        end_date = parse_date(end_text)

    result["start_date"] = (
        start_date.strftime("%Y-%m")
        if start_date
        else None
    )

    result["end_date"] = (
        end_date.strftime("%Y-%m")
        if end_date
        else None
    )

    return result


def extract_company_and_title(line: str) -> Dict:
    """
    Extract company name and job title from a common
    'Job Title | Company' or 'Job Title - Company' format.
    """

    result = {
        "job_title": None,
        "company": None
    }

    if not line:
        return result

    text = line.strip()

    # Job Title | Company
    if "|" in text:
        parts = [part.strip() for part in text.split("|")]

        if len(parts) >= 2:
            result["job_title"] = parts[0]
            result["company"] = parts[1]

            return result

    # Job Title @ Company
    if "@" in text:
        parts = [part.strip() for part in text.split("@")]

        if len(parts) >= 2:
            result["job_title"] = parts[0]
            result["company"] = parts[1]

            return result

    return result


def build_experience_record(
    company: str,
    job_title: str,
    date_range: str,
    responsibilities: Optional[List[str]] = None
) -> Dict:
    """
    Build one structured professional experience record.
    """

    date_info = parse_experience_date_range(date_range)

    start_datetime = parse_date(
        date_info["start_date"]
    )

    end_datetime = parse_date(
        date_info["end_date"]
    )

    if date_info["is_current"]:
        end_datetime = datetime.now()

    duration_months = calculate_duration_months(
        start_datetime,
        end_datetime
    )

    return {
        "company": company,
        "job_title": job_title,
        "start_date": date_info["start_date"],
        "end_date": date_info["end_date"],
        "duration_months": duration_months,
        "experience_years": calculate_experience_years(
            duration_months
        ),
        "is_current": date_info["is_current"],
        "responsibilities": responsibilities or []
    }


def calculate_total_experience(
    experiences: List[Dict]
) -> float:
    """
    Calculate total experience from structured roles.

    Overlapping roles are not double-counted.
    """

    intervals = []

    for experience in experiences:

        start = parse_date(
            experience.get("start_date")
        )

        end = parse_date(
            experience.get("end_date")
        )

        if experience.get("is_current"):
            end = datetime.now()

        if start and end:
            intervals.append((start, end))

    if not intervals:
        return 0.0

    intervals.sort(key=lambda x: x[0])

    merged = []

    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:

        if start <= current_end:

            if end > current_end:
                current_end = end

        else:
            merged.append(
                (current_start, current_end)
            )

            current_start = start
            current_end = end

    merged.append(
        (current_start, current_end)
    )

    total_months = 0

    for start, end in merged:

        months = (
            (end.year - start.year) * 12
            + (end.month - start.month)
            + 1
        )

        total_months += months

    return round(total_months / 12, 2)

def parse_work_experience_section(
    work_experience: List[str]
) -> List[Dict]:
    """
    Parse the structured work_experience section
    produced by the resume section classifier.

    Expected format:

    [
        "Company Name",
        "Job Title",
        "2022 - Present",
        "- Responsibility 1",
        "- Responsibility 2"
    ]
    """

    experiences = []

    if not work_experience:
        return experiences

    i = 0

    while i < len(work_experience):

        # We need at least:
        # company + job title + date range
        if i + 2 >= len(work_experience):
            break

        company = work_experience[i].strip()
        job_title = work_experience[i + 1].strip()
        date_range = work_experience[i + 2].strip()

        # Check whether the third item actually looks
        # like an employment date range.
        if not re.search(
            r"\b\d{4}\b",
            date_range
        ):
            i += 1
            continue

        responsibilities = []

        j = i + 3

        while j < len(work_experience):

            line = work_experience[j].strip()

            # Stop if the next line looks like the
            # beginning of another experience.
            if (
                j + 2 < len(work_experience)
                and re.search(
                    r"\b\d{4}\b",
                    work_experience[j + 2]
                )
                and not line.startswith("-")
            ):
                break

            if line:
                responsibilities.append(
                    line.lstrip("- ").strip()
                )

            j += 1

        experience = build_experience_record(
            company=company,
            job_title=job_title,
            date_range=date_range,
            responsibilities=responsibilities
        )

        experiences.append(experience)

        i = j

    return experiences


if __name__ == "__main__":

    print("Experience Parser loaded successfully.")

    sample_work_experience = [
        "ABC Technologies",
        "Software Engineer",
        "2022 - Present",
        "- Developed REST APIs using Spring Boot.",
        "- Worked with MySQL and PostgreSQL databases.",
        "- Used Git and Docker in application development.",
        "- Participated in Agile software development."
    ]

    experiences = parse_work_experience_section(
        sample_work_experience
    )

    print("\nStructured experience:")

    for experience in experiences:
        print(experience)

    total_experience = calculate_total_experience(
        experiences
    )

    print(
        f"\nTotal experience: "
        f"{total_experience} years"
    )

