"""
Bias indicator evaluation generator.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Generate diagnostic fairness indicators from the
existing fairness-aware scoring outputs.

These indicators do not prove discrimination or
absence of discrimination.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from fairness.bias_evaluation import (
    calculate_average_score,
    calculate_score_distribution,
    calculate_keyword_semantic_gap,
)


BASE_DIR = Path(__file__).resolve().parent.parent

FAIRNESS_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "fairness"
)

OUTPUT_FILE = (
    FAIRNESS_DIR
    / "bias_evaluation.json"
)


def load_fairness_records() -> List[Dict[str, Any]]:
    """
    Load generated fairness scoring records.
    """

    records = []

    for file_path in sorted(
        FAIRNESS_DIR.glob(
            "CAND_*_JOB_*_fairness.json"
        )
    ):
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            records.append(
                json.load(file)
            )

    return records


def evaluate_bias_indicators(
    records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Calculate diagnostic bias indicators.
    """

    fair_scores = []
    keyword_scores = []
    semantic_scores = []

    for record in records:
        fair_scoring = record.get(
            "fair_scoring",
            {},
        )

        fair_scores.append(
            fair_scoring.get(
                "normalized_score",
                0.0,
            )
        )

        keyword_scores.append(
            fair_scoring.get(
                "keyword_score",
                0.0,
            )
        )

        semantic_scores.append(
            fair_scoring.get(
                "semantic_score",
                0.0,
            )
        )

    return {
        "records_evaluated": len(records),
        "fair_score": {
            "average": calculate_average_score(
                fair_scores
            ),
            "distribution": calculate_score_distribution(
                fair_scores
            ),
        },
        "keyword_score": {
            "average": calculate_average_score(
                keyword_scores
            ),
        },
        "semantic_score": {
            "average": calculate_average_score(
                semantic_scores
            ),
        },
        "keyword_semantic_gap": (
            calculate_keyword_semantic_gap(
                keyword_scores,
                semantic_scores,
            )
        ),
        "interpretation_note": (
            "These indicators are diagnostic measurements "
            "of scoring behavior. They do not establish "
            "whether discrimination is present or absent."
        ),
    }


def generate_bias_evaluation() -> Dict[str, Any]:
    """
    Generate and save bias evaluation results.
    """

    records = load_fairness_records()

    evaluation = evaluate_bias_indicators(
        records
    )

    FAIRNESS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            evaluation,
            file,
            indent=2,
        )

    return evaluation


if __name__ == "__main__":
    print(
        "Loading fairness outputs..."
    )

    evaluation = generate_bias_evaluation()

    print(
        "Bias evaluation completed."
    )

    print(
        f"Records evaluated: "
        f"{evaluation['records_evaluated']}"
    )
    