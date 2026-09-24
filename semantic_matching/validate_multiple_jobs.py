import json
from pathlib import Path

from semantic_match_engine import SemanticMatchEngine


RESUME_IDS = [
    "resume_001",
    "resume_002",
    "resume_003",
    "resume_004"
]

JD_IDS = [
    "jd_001_data_scientist",
    "jd_002_software_engineer",
    "jd_003_ml_engineer",
    "jd_004_data_analyst",
    "jd_005_hr_executive",
    "jd_006_business_analyst"
]


def main():

    print("Initializing semantic matching engine...")

    engine = SemanticMatchEngine()

    results = []

    print("\nRunning validation...")
    print("=" * 70)

    for resume_id in RESUME_IDS:

        for jd_id in JD_IDS:

            print(
                f"Matching {resume_id} → {jd_id}..."
            )

            result = engine.match_resume_to_jd(
                resume_id,
                jd_id
            )

            results.append(result)

    output_directory = (
        Path("data")
        / "processed"
        / "semantic_matching"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory
        / "multi_job_validation.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print("\nValidation completed.")

    print(
        f"Total comparisons: {len(results)}"
    )

    print(
        f"Output file: {output_file}"
    )

    print("\nResults:")
    print("=" * 70)

    for result in results:

        print(
            f"{result['resume_id']} → "
            f"{result['jd_id']} : "
            f"{result['final_semantic_score']:.4f}"
        )


if __name__ == "__main__":
    main()
    