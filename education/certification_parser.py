import re
from typing import List, Dict


CERTIFICATION_CATEGORIES = {
    "python": "Programming",
    "java": "Programming",
    "javascript": "Programming",
    "sql": "Database",
    "machine learning": "Machine Learning",
    "deep learning": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "data science": "Data Science",
    "data analytics": "Data Analytics",
    "power bi": "Business Intelligence",
    "tableau": "Business Intelligence",
    "aws": "Cloud",
    "azure": "Cloud",
    "google cloud": "Cloud",
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "git": "Development Tools",
    "cybersecurity": "Cybersecurity",
    "project management": "Project Management"
}


CERTIFICATION_PROVIDERS = [
    "Oracle",
    "Microsoft",
    "Amazon",
    "AWS",
    "Google",
    "IBM",
    "Cisco",
    "Docker",
    "Coursera",
    "Udemy",
    "CompTIA",
    "Tableau",
    "Power BI"
]


def normalize_certification_name(
    certification: str
) -> str:
    """
    Normalize certification naming.
    """

    certification = certification.strip()

    certification = re.sub(
        r"\s+",
        " ",
        certification
    )

    return certification


def extract_provider(
    certification: str
) -> str:
    """
    Detect the certification provider.
    """

    normalized = certification.lower()

    for provider in CERTIFICATION_PROVIDERS:

        if provider.lower() in normalized:

            return provider

    return "Unknown"


def detect_relevance_category(
    certification: str
) -> str:
    """
    Assign a broad relevance category
    based on certification keywords.
    """

    normalized = certification.lower()

    for keyword, category in CERTIFICATION_CATEGORIES.items():

        if keyword in normalized:

            return category

    return "General"


def parse_certification(
    certification: str
) -> Dict:
    """
    Convert one certification into
    a structured certification object.
    """

    normalized_name = normalize_certification_name(
        certification
    )

    provider = extract_provider(
        normalized_name
    )

    category = detect_relevance_category(
        normalized_name
    )

    return {
        "certification_name": normalized_name,
        "provider": provider,
        "relevance_category": category
    }


def parse_certifications(
    certifications: List[str]
) -> List[Dict]:
    """
    Parse all certifications from
    the resume certification section.
    """

    results = []

    if not certifications:
        return results

    for certification in certifications:

        certification = certification.strip()

        if not certification:
            continue

        result = parse_certification(
            certification
        )

        results.append(
            result
        )

    return results


if __name__ == "__main__":

    print(
        "Certification Parser loaded successfully."
    )

    sample_certifications = [
        "Oracle Java Certification",
        "Docker Certified Associate"
    ]

    results = parse_certifications(
        sample_certifications
    )

    print("\nStructured certifications:")

    for certification in results:

        print(certification)
        