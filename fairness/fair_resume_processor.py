"""
Fairness-aware resume processor.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Create a standardized and privacy-aware representation
of the existing structured resume data.

The original segmented resume files are never modified.
"""

import json
from pathlib import Path
from typing import Any, Dict

from fairness.attribute_masking import mask_personal_attributes
from fairness.normalization import normalize_resume


BASE_DIR = Path(__file__).resolve().parent.parent

SEGMENTED_DIR = (
    BASE_DIR / "data" / "processed" / "segmented"
)

OUTPUT_DIR = (
    BASE_DIR / "data" / "processed" / "fairness" / "resumes"
)


def load_resume(
    file_path: Path,
) -> Dict[str, Any]:
    """
    Load a structured resume JSON file.
    """

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def process_resume(
    resume: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Apply resume normalization followed by
    personal-attribute masking.
    """

    normalized_resume = normalize_resume(
        resume
    )

    masked_resume = mask_personal_attributes(
        normalized_resume
    )

    return masked_resume


def process_all_resumes(
    input_dir: Path = SEGMENTED_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> list[Path]:
    """
    Process all structured resumes and save
    fairness-aware versions.
    """

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Segmented resume directory not found: {input_dir}"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_files = []

    for input_file in sorted(
        input_dir.glob("*_sections.json")
    ):
        resume = load_resume(input_file)

        processed_resume = process_resume(
            resume
        )

        output_file = (
            output_dir
            / input_file.name
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                processed_resume,
                file,
                indent=2,
                ensure_ascii=False,
            )

        generated_files.append(
            output_file
        )

    return generated_files


if __name__ == "__main__":
    print("Processing structured resumes...")

    generated = process_all_resumes()

    print(
        f"Generated fairness-aware resumes: {len(generated)}"
    )
    