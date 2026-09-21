import json
from pathlib import Path

from experience_parser import (
    parse_work_experience_section,
    calculate_total_experience
)

from experience_timeline import (
    detect_gaps,
    detect_overlaps
)

from experience_relevance import (
    calculate_experience_relevance
)

from role_similarity import (
    calculate_role_similarity
)


INPUT_DIR = Path(
    "data/processed/segmented"
)

OUTPUT_DIR = Path(
    "data/processed/experience"
)


def generate_experience_profile(
    input_file: Path,
    output_file: Path
) -> None:

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        resume_data = json.load(file)

    resume_id = input_file.stem.replace(
        "_sections",
        ""
    )

    work_experience = resume_data.get(
        "work_experience",
        []
    )

    experiences = parse_work_experience_section(
        work_experience
    )

    total_experience = calculate_total_experience(
        experiences
    )

    gaps = detect_gaps(
        experiences
    )

    overlaps = detect_overlaps(
        experiences
    )

    # Baseline target role for Day 10
    target_role = "Software Engineer"

    required_keywords = [
        "Python",
        "SQL",
        "Java",
        "Spring Boot",
        "REST APIs",
        "Docker",
        "Git"
    ]

    # Calculate experience relevance
    relevance_analysis = calculate_experience_relevance(
        experiences=experiences,
        target_role=target_role,
        required_keywords=required_keywords
    )

    # Calculate role-to-role similarity
    role_similarity = []

    for experience in experiences:

        similarity = calculate_role_similarity(
            experience["job_title"],
            target_role
        )

        role_similarity.append(
            similarity
        )

    # Final structured experience object
    structured_output = {
        "resume_id": resume_id,
        "total_experience_years": total_experience,
        "experiences": experiences,
        "gaps": gaps,
        "overlaps": overlaps,
        "relevance_analysis": relevance_analysis,
        "role_similarity": role_similarity
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            structured_output,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    input_files = sorted(
        INPUT_DIR.glob(
            "*_sections.json"
        )
    )

    if not input_files:

        print(
            "No segmented resume files found."
        )

        return

    for input_file in input_files:

        output_file = (
            OUTPUT_DIR
            / f"{input_file.stem.replace('_sections', '')}_experience.json"
        )

        generate_experience_profile(
            input_file,
            output_file
        )

        print(
            f"Created: {output_file}"
        )


if __name__ == "__main__":

    main()