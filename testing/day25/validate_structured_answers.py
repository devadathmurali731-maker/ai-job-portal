import json
from pathlib import Path

from jsonschema import validate, ValidationError


PROJECT_ROOT = Path(__file__).resolve().parents[2]

schema_path = PROJECT_ROOT / "data" / "schemas" / "structured_answer.schema.json"
answers_path = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "day25"
    / "sample_structured_answers.json"
)

with schema_path.open("r", encoding="utf-8") as file:
    schema = json.load(file)

with answers_path.open("r", encoding="utf-8") as file:
    answers = json.load(file)

try:
    for index, answer in enumerate(answers, start=1):
        validate(instance=answer, schema=schema)

        print(f"Answer {index}: VALID")

    print(f"\nAll {len(answers)} structured answers passed schema validation.")

except ValidationError as error:
    print("\nSCHEMA VALIDATION FAILED")
    print(f"Error: {error.message}")
    print(f"Location: {list(error.absolute_path)}")