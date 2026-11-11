import json
from pathlib import Path

from src.screening_scoring.question_scorer import score_question
from src.screening_scoring.screening_scoring_engine import (
    calculate_screening_score
)


def run_scoring_pipeline(input_path: str, output_path: str) -> dict:
    """Score all structured candidate answers and save the results."""

    input_file = Path(input_path)
    output_file = Path(output_path)

    with input_file.open("r", encoding="utf-8") as file:
        answers = json.load(file)

    if not isinstance(answers, list):
        raise ValueError("Input must contain a list of structured answers.")

    question_results = []

    for answer in answers:
        original_text = answer.get("original_text", "")

        result = score_question(
            answer=original_text,
            understanding_result=answer
        )

        question_results.append(result)

    screening_result = calculate_screening_score(question_results)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(screening_result, file, indent=4, ensure_ascii=False)

    return screening_result


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data/processed/day25/sample_structured_answers.json"
    )

    output_path = (
        project_root
        / "data/processed/day26/screening_scoring_results.json"
    )

    result = run_scoring_pipeline(input_path, output_path)

    print(json.dumps(result, indent=4))
    print("\nScreening scoring results generated successfully.")