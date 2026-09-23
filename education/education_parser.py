import re
from typing import List, Dict, Optional


DEGREE_NORMALIZATION = {
    "b.tech": "Bachelor of Technology",
    "btech": "Bachelor of Technology",
    "b.e": "Bachelor of Engineering",
    "be": "Bachelor of Engineering",
    "b.sc": "Bachelor of Science",
    "bsc": "Bachelor of Science",
    "b.com": "Bachelor of Commerce",
    "bcom": "Bachelor of Commerce",
    "b.a": "Bachelor of Arts",
    "ba": "Bachelor of Arts",

    "m.tech": "Master of Technology",
    "mtech": "Master of Technology",
    "m.e": "Master of Engineering",
    "me": "Master of Engineering",
    "m.sc": "Master of Science",
    "msc": "Master of Science",
    "m.com": "Master of Commerce",
    "mcom": "Master of Commerce",
    "m.a": "Master of Arts",
    "ma": "Master of Arts",

    "mba": "Master of Business Administration",
    "phd": "Doctor of Philosophy",
    "ph.d": "Doctor of Philosophy"
}


def normalize_degree(degree: str) -> str:
    """
    Normalize degree names into standard naming conventions.
    """

    normalized = degree.lower().strip()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    )

    return DEGREE_NORMALIZATION.get(
        normalized,
        degree.strip()
    )


def extract_graduation_year(
    text: str
) -> Optional[int]:
    """
    Extract a four-digit graduation year.
    """

    match = re.search(
        r"\b(19|20)\d{2}\b",
        text
    )

    if match:
        return int(match.group())

    return None


def extract_degree_and_field(
    education_text: str
) -> Dict:
    """
    Extract degree type and field of study
    from an education description.
    """

    text = education_text.strip()

    normalized_text = text.lower()

    matched_degree = None
    degree_key = None

    # Try longer degree patterns first.
    sorted_degrees = sorted(
        DEGREE_NORMALIZATION.keys(),
        key=len,
        reverse=True
    )

    for degree in sorted_degrees:

        pattern = r"\b" + re.escape(degree) + r"\b"

        if re.search(
            pattern,
            normalized_text
        ):
            matched_degree = DEGREE_NORMALIZATION[
                degree
            ]

            degree_key = degree

            break

    if not matched_degree:

        return {
            "degree_type": None,
            "field_of_study": text
        }

    field_text = re.sub(
        r"\b" + re.escape(degree_key) + r"\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    field_text = re.sub(
        r"^\s*(in|of)\s+",
        "",
        field_text,
        flags=re.IGNORECASE
    )

    field_text = field_text.strip()

    return {
        "degree_type": matched_degree,
        "field_of_study": field_text or None
    }


def parse_education_section(
    education: List[str]
) -> List[Dict]:
    """
    Parse the education section generated
    by the resume section classifier.

    Expected format:

    [
        "B.Tech in Computer Science and Engineering",
        "XYZ University",
        "2022"
    ]
    """

    education_records = []

    if not education:
        return education_records

    i = 0

    while i + 2 < len(education):

        education_text = education[i].strip()
        institution = education[i + 1].strip()
        year_text = education[i + 2].strip()

        degree_data = extract_degree_and_field(
            education_text
        )

        graduation_year = extract_graduation_year(
            year_text
        )

        education_record = {
            "degree_type": degree_data[
                "degree_type"
            ],
            "field_of_study": degree_data[
                "field_of_study"
            ],
            "institution": institution,
            "graduation_year": graduation_year
        }

        education_records.append(
            education_record
        )

        i += 3

    return education_records


if __name__ == "__main__":

    print(
        "Education Parser loaded successfully."
    )

    sample_education = [
        "B.Tech in Computer Science and Engineering",
        "XYZ University",
        "2022"
    ]

    result = parse_education_section(
        sample_education
    )

    print("\nStructured education:")

    for education in result:
        print(education)