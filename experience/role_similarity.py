from typing import List, Dict
import re


ROLE_SKILL_MAP = {
    "software engineer": [
        "programming",
        "software development",
        "api",
        "database",
        "git",
        "testing"
    ],

    "backend developer": [
        "programming",
        "backend",
        "api",
        "database",
        "server",
        "git"
    ],

    "data analyst": [
        "sql",
        "data analysis",
        "statistics",
        "reporting",
        "visualization",
        "excel"
    ],

    "business intelligence analyst": [
        "sql",
        "data analysis",
        "reporting",
        "visualization",
        "dashboard",
        "business intelligence"
    ],

    "data scientist": [
        "python",
        "machine learning",
        "statistics",
        "data analysis",
        "sql",
        "modeling"
    ],

    "machine learning engineer": [
        "python",
        "machine learning",
        "modeling",
        "deployment",
        "api",
        "docker"
    ]
}


def normalize_role(role: str) -> str:
    """
    Normalize a job role name.
    """

    role = role.lower()

    role = re.sub(
        r"[^a-z0-9\s]",
        " ",
        role
    )

    role = re.sub(
        r"\s+",
        " ",
        role
    ).strip()

    return role


def calculate_role_similarity(
    role_1: str,
    role_2: str
) -> Dict:
    """
    Calculate similarity between two job roles
    using their associated skill/keyword profiles.
    """

    normalized_role_1 = normalize_role(
        role_1
    )

    normalized_role_2 = normalize_role(
        role_2
    )

    skills_1 = set(
        ROLE_SKILL_MAP.get(
            normalized_role_1,
            []
        )
    )

    skills_2 = set(
        ROLE_SKILL_MAP.get(
            normalized_role_2,
            []
        )
    )

    if not skills_1 or not skills_2:
        return {
            "role_1": role_1,
            "role_2": role_2,
            "shared_keywords": [],
            "similarity_score": 0.0
        }

    shared_keywords = sorted(
        skills_1.intersection(skills_2)
    )

    union_size = len(
        skills_1.union(skills_2)
    )

    similarity_score = (
        len(shared_keywords)
        / union_size
    )

    return {
        "role_1": role_1,
        "role_2": role_2,
        "shared_keywords": shared_keywords,
        "similarity_score": round(
            similarity_score,
            2
        )
    }
if __name__ == "__main__":

    result_1 = calculate_role_similarity(
        "Data Analyst",
        "Business Intelligence Analyst"
    )

    result_2 = calculate_role_similarity(
        "Software Engineer",
        "Data Scientist"
    )

    print("\nData Analyst vs Business Intelligence Analyst:")
    print(result_1)

    print("\nSoftware Engineer vs Data Scientist:")
    print(result_2)