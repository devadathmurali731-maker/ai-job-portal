
import json
from pathlib import Path

from src.confidence_analysis.communication_analyzer import (
    analyze_communication
)


def run_communication_pipeline(
    input_path: str,
    output_path: str
) -> dict:
    """Run confidence and sentiment analysis on structured answers."""

    input_file = Path(input_path)
    output_file = Path(output_path)

    with input_file.open("r", encoding="utf-8") as file:
        answers = json.load(file)

    if not isinstance(answers, list):
        raise ValueError("Input must contain a list of answers.")

    result = analyze_communication(answers)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    return result


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data/processed/day25/sample_structured_answers.json"
    )

    output_path = (
        project_root
        / "data/processed/day27/behavioral_indicators_report.json"
    )

    result = run_communication_pipeline(
        input_path,
        output_path
    )

    print(json.dumps(result, indent=4))

    print("\nDay 27 communication analysis completed successfully.")
