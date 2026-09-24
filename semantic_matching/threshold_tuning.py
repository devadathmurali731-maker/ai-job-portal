import json
from pathlib import Path


VALIDATION_LABELS = {
    "resume_001": {
        "jd_001_data_scientist": 1,
        "jd_002_software_engineer": 1,
        "jd_003_ml_engineer": 1,
        "jd_004_data_analyst": 0,
        "jd_005_hr_executive": 0,
        "jd_006_business_analyst": 0
    },

    "resume_002": {
        "jd_001_data_scientist": 1,
        "jd_002_software_engineer": 0,
        "jd_003_ml_engineer": 0,
        "jd_004_data_analyst": 1,
        "jd_005_hr_executive": 0,
        "jd_006_business_analyst": 1
    },

    "resume_003": {
        "jd_001_data_scientist": 1,
        "jd_002_software_engineer": 0,
        "jd_003_ml_engineer": 1,
        "jd_004_data_analyst": 0,
        "jd_005_hr_executive": 0,
        "jd_006_business_analyst": 0
    },

    "resume_004": {
        "jd_001_data_scientist": 0,
        "jd_002_software_engineer": 0,
        "jd_003_ml_engineer": 0,
        "jd_004_data_analyst": 1,
        "jd_005_hr_executive": 0,
        "jd_006_business_analyst": 1
    }
}


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


def calculate_metrics(results, threshold):

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for result in results:

        resume_id = result["resume_id"]
        jd_id = result["jd_id"]

        actual = VALIDATION_LABELS[
            resume_id
        ][jd_id]

        predicted = int(
            result["final_semantic_score"]
            >= threshold
        )

        if actual == 1 and predicted == 1:
            true_positive += 1

        elif actual == 0 and predicted == 0:
            true_negative += 1

        elif actual == 0 and predicted == 1:
            false_positive += 1

        elif actual == 1 and predicted == 0:
            false_negative += 1

    total = (
        true_positive
        + true_negative
        + false_positive
        + false_negative
    )

    accuracy = (
        (true_positive + true_negative)
        / total
    )

    precision = (
        true_positive
        / (true_positive + false_positive)
        if (true_positive + false_positive)
        else 0.0
    )

    recall = (
        true_positive
        / (true_positive + false_negative)
        if (true_positive + false_negative)
        else 0.0
    )

    return {
        "threshold": threshold,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall
    }


def main():

    results = load_results()

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70
    ]

    print("Semantic Matching Threshold Analysis")
    print("=" * 80)

    print(
        "\nThreshold | Accuracy | Precision | Recall"
    )

    print("-" * 80)

    all_metrics = []

    for threshold in thresholds:

        metrics = calculate_metrics(
            results,
            threshold
        )

        all_metrics.append(metrics)

        print(
            f"{threshold:9.2f} | "
            f"{metrics['accuracy']:.4f}   | "
            f"{metrics['precision']:.4f}    | "
            f"{metrics['recall']:.4f}"
        )

    output_directory = (
        Path("outputs")
        / "semantic_matching"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory
        / "threshold_analysis.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_metrics,
            file,
            indent=4
        )

    print(
        "\nThreshold analysis saved to:"
    )

    print(output_file)


if __name__ == "__main__":
    main()