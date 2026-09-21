from typing import List, Dict
import re


def normalize_text(text: str) -> str:
    """
    Convert text into a normalized form
    for easier comparison.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def calculate_keyword_match(
    text: str,
    required_keywords: List[str]
) -> Dict:
    """
    Calculate how many required keywords
    appear in the candidate experience.
    """

    normalized_text = normalize_text(text)

    matched = []
    missing = []

    for keyword in required_keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if normalized_keyword in normalized_text:
            matched.append(keyword)
        else:
            missing.append(keyword)

    total = len(required_keywords)

    if total == 0:
        score = 0.0
    else:
        score = len(matched) / total

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "keyword_match_score": round(
            score,
            2
        )
    }


def calculate_role_relevance(
    experience: Dict,
    target_role: str,
    required_keywords: List[str]
) -> Dict:
    """
    Calculate relevance of one employment
    experience to a target job role.
    """

    job_title = experience.get(
        "job_title",
        ""
    )

    responsibilities = experience.get(
        "responsibilities",
        []
    )

    responsibility_text = " ".join(
        responsibilities
    )

    combined_text = (
        job_title
        + " "
        + responsibility_text
    )

    keyword_result = calculate_keyword_match(
        combined_text,
        required_keywords
    )

    normalized_title = normalize_text(
        job_title
    )

    normalized_target = normalize_text(
        target_role
    )

    title_match = (
        normalized_target in normalized_title
        or normalized_title in normalized_target
    )

    if title_match:
        title_score = 1.0
    else:
        title_score = 0.0

    final_score = (
        0.30 * title_score
        + 0.70 * keyword_result[
            "keyword_match_score"
        ]
    )

    return {
        "company": experience.get(
            "company",
            ""
        ),
        "job_title": job_title,
        "target_role": target_role,
        "title_match": title_match,
        "matched_keywords": keyword_result[
            "matched_keywords"
        ],
        "missing_keywords": keyword_result[
            "missing_keywords"
        ],
        "keyword_match_score": keyword_result[
            "keyword_match_score"
        ],
        "relevance_score": round(
            final_score,
            2
        )
    }


def calculate_experience_relevance(
    experiences: List[Dict],
    target_role: str,
    required_keywords: List[str]
) -> List[Dict]:
    """
    Calculate relevance scores for all
    employment experiences.
    """

    results = []

    for experience in experiences:

        result = calculate_role_relevance(
            experience,
            target_role,
            required_keywords
        )

        results.append(result)

    return results

if __name__ == "__main__":

    sample_experience = {
        "company": "ABC Technologies",
        "job_title": "Software Engineer",
        "responsibilities": [
            "Developed REST APIs using Spring Boot.",
            "Worked with MySQL and PostgreSQL databases.",
            "Used Git and Docker in application development.",
            "Participated in Agile software development."
        ]
    }

    target_role = "Software Engineer"

    required_keywords = [
        "Java",
        "Spring Boot",
        "REST APIs",
        "SQL",
        "Docker",
        "Git"
    ]

    result = calculate_role_relevance(
        experience=sample_experience,
        target_role=target_role,
        required_keywords=required_keywords
    )

    print("\nExperience Relevance Result:")
    print(result)