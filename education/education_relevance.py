from typing import List, Dict


ROLE_EDUCATION_MAP = {

    "software engineer": [
        "computer science",
        "computer engineering",
        "information technology",
        "software engineering"
    ],

    "backend developer": [
        "computer science",
        "computer engineering",
        "information technology",
        "software engineering"
    ],

    "data analyst": [
        "statistics",
        "economics",
        "mathematics",
        "computer science",
        "data science",
        "information technology"
    ],

    "business intelligence analyst": [
        "business analytics",
        "business intelligence",
        "statistics",
        "economics",
        "mathematics",
        "computer science",
        "data analytics",
        "information technology"
    ],

    "data scientist": [
        "data science",
        "statistics",
        "mathematics",
        "computer science",
        "economics",
        "machine learning"
    ],

    "machine learning engineer": [
        "computer science",
        "computer engineering",
        "information technology",
        "data science",
        "machine learning"
    ]
}


DEGREE_LEVEL_SCORE = {

    "Doctor of Philosophy": 1.0,
    "Master of Technology": 1.0,
    "Master of Engineering": 1.0,
    "Master of Science": 1.0,
    "Master of Business Administration": 1.0,
    "Master of Arts": 1.0,

    "Bachelor of Technology": 0.9,
    "Bachelor of Engineering": 0.9,
    "Bachelor of Science": 0.9,
    "Bachelor of Commerce": 0.8,
    "Bachelor of Arts": 0.8
}


def normalize_text(
    text: str
) -> str:
    """
    Normalize text for comparison.
    """

    return (
        text
        .lower()
        .strip()
    )


def calculate_field_relevance(
    field_of_study: str,
    target_role: str
) -> Dict:
    """
    Determine whether the field of study
    is relevant to the target role.
    """

    field = normalize_text(
        field_of_study
    )

    role = normalize_text(
        target_role
    )

    relevant_fields = ROLE_EDUCATION_MAP.get(
        role,
        []
    )

    matched_fields = []

    for relevant_field in relevant_fields:

        if relevant_field in field:

            matched_fields.append(
                relevant_field
            )

    if matched_fields:

        field_score = 1.0

    else:

        field_score = 0.0

    return {
        "target_role": target_role,
        "field_of_study": field_of_study,
        "matched_fields": matched_fields,
        "field_relevance_score": field_score
    }


def calculate_degree_level_score(
    degree_type: str
) -> float:
    """
    Assign a baseline score based on
    normalized degree level.
    """

    return DEGREE_LEVEL_SCORE.get(
        degree_type,
        0.0
    )


def calculate_education_relevance(
    education: Dict,
    target_role: str
) -> Dict:
    """
    Calculate the relevance of one
    academic qualification to a target role.
    """

    degree_type = education.get(
        "degree_type",
        ""
    )

    field_of_study = education.get(
        "field_of_study",
        ""
    )

    field_result = calculate_field_relevance(
        field_of_study,
        target_role
    )

    degree_score = calculate_degree_level_score(
        degree_type
    )

    field_score = field_result[
        "field_relevance_score"
    ]

    final_score = (
        0.70 * field_score
        + 0.30 * degree_score
    )

    return {
        "degree_type": degree_type,
        "field_of_study": field_of_study,
        "target_role": target_role,
        "matched_fields": field_result[
            "matched_fields"
        ],
        "field_relevance_score": field_score,
        "degree_level_score": degree_score,
        "education_relevance_score": round(
            final_score,
            2
        )
    }


def calculate_education_relevance_for_all(
    education_records: List[Dict],
    target_role: str
) -> List[Dict]:
    """
    Calculate education relevance for
    all academic qualifications.
    """

    results = []

    for education in education_records:

        result = calculate_education_relevance(
            education,
            target_role
        )

        results.append(
            result
        )

    return results


if __name__ == "__main__":

    print(
        "Education Relevance module loaded successfully."
    )

    sample_education = {
        "degree_type": "Bachelor of Technology",
        "field_of_study": (
            "Computer Science and Engineering"
        ),
        "institution": "XYZ University",
        "graduation_year": 2022
    }

    result = calculate_education_relevance(
        sample_education,
        "Software Engineer"
    )

    print("\nEducation relevance result:")

    print(result)
    