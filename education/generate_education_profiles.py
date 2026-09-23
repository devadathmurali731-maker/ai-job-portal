import json
from pathlib import Path

from education_parser import (
    parse_education_section
)

from certification_parser import (
    parse_certifications
)

from education_relevance import (
    calculate_education_relevance_for_all
)


INPUT_DIR = Path(
    "data/processed/segmented"
)

OUTPUT_DIR = Path(
    "data/processed/education"
)


def generate_education_profile(
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

    education = resume_data.get(
        "education",
        []
    )

    certifications = resume_data.get(
        "certifications",
        []
    )

    # Parse education
    education_records = parse_education_section(
        education
    )

    # Parse certifications
    certification_records = parse_certifications(
        certifications
    )

    # Baseline target role for Day 11
    target_role = "Software Engineer"

    # Calculate education relevance
    education_relevance = (
        calculate_education_relevance_for_all(
            education_records,
            target_role
        )
    )

    structured_output = {
        "resume_id": resume_id,
        "education": education_records,
        "certifications": certification_records,
        "education_relevance": education_relevance
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
            / f"{input_file.stem.replace('_sections', '')}_education.json"
        )

        generate_education_profile(
            input_file,
            output_file
        )

        print(
            f"Created: {output_file}"
        )


if __name__ == "__main__":

    main()