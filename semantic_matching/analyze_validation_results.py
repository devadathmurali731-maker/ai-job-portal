import json
from pathlib import Path


def load_results():

    file_path = (
        Path("data")
        / "processed"
        / "semantic_matching"
        / "multi_job_validation.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    results = load_results()

    print("Semantic Matching Validation Analysis")
    print("=" * 70)

    scores = [
        result["final_semantic_score"]
        for result in results
    ]

    print(
        f"\nNumber of comparisons: {len(scores)}"
    )

    print(
        f"Minimum score: {min(scores):.4f}"
    )

    print(
        f"Maximum score: {max(scores):.4f}"
    )

    average_score = (
        sum(scores) / len(scores)
    )

    print(
        f"Average score: {average_score:.4f}"
    )

    print("\nScores sorted from highest to lowest:")
    print("-" * 70)

    sorted_results = sorted(
        results,
        key=lambda x: x["final_semantic_score"],
        reverse=True
    )

    for result in sorted_results:

        print(
            f"{result['resume_id']} → "
            f"{result['jd_id']} : "
            f"{result['final_semantic_score']:.4f}"
        )

    print("\nScore Distribution:")
    print("-" * 70)

    thresholds = [
        0.30,
        0.40,
        0.50,
        0.60,
        0.70
    ]

    for threshold in thresholds:

        count = sum(
            score >= threshold
            for score in scores
        )

        print(
            f"Scores >= {threshold:.2f}: "
            f"{count}/{len(scores)}"
        )


if __name__ == "__main__":
    main()
    