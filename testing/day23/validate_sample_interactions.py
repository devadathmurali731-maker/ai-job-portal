
import json
import sys
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATH = ROOT / "data" / "schemas" / "ai_screening_interaction.schema.json"
SAMPLE_PATH = (
    ROOT
    / "data"
    / "processed"
    / "screening_interactions"
    / "sample_interactions.json"
)
TRANSCRIPT_PATH = (
    ROOT
    / "data"
    / "processed"
    / "voice_transcripts"
    / "sample_transcripts.json"
)


def is_valid_datetime(value):
    if not isinstance(value, str) or not value:
        return False

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except (ValueError, OverflowError):
        return False


def main():
    with SCHEMA_PATH.open(encoding="utf-8") as file:
        schema = json.load(file)

    with SAMPLE_PATH.open(encoding="utf-8") as file:
        interactions = json.load(file)

    with TRANSCRIPT_PATH.open(encoding="utf-8") as file:
        transcripts = json.load(file)

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    transcript_ids = {item["transcript_id"] for item in transcripts}
    seen_interaction_ids = set()
    errors_found = False

    for index, record in enumerate(interactions, start=1):
        interaction_id = record.get("interaction_id", f"record-{index}")
        errors = list(validator.iter_errors(record))

        if interaction_id in seen_interaction_ids:
            print(f"FAIL {interaction_id}: duplicate interaction ID")
            errors_found = True
        seen_interaction_ids.add(interaction_id)

        for field in ("asked_at", "answered_at"):
            value = record.get(field)
            if value is not None and not is_valid_datetime(value):
                print(f"FAIL {interaction_id}: invalid {field} timestamp")
                errors_found = True

        transcript_id = record.get("transcript_id")
        if transcript_id is not None and transcript_id not in transcript_ids:
            print(f"FAIL {interaction_id}: transcript {transcript_id} not found")
            errors_found = True

        if record.get("status") == "answered":
            if record.get("answered_at") is None:
                print(f"FAIL {interaction_id}: answered interaction needs answered_at")
                errors_found = True
            if record.get("answer_text") is None:
                print(f"FAIL {interaction_id}: answered interaction needs answer_text")
                errors_found = True

        if errors:
            for error in errors:
                print(f"FAIL {interaction_id}: {error.json_path}: {error.message}")
            errors_found = True

        if not errors:
            print(f"PASS {interaction_id}: schema validation successful")

    if errors_found:
        sys.exit(1)

    print(f"\nAll {len(interactions)} screening interactions passed validation.")


if __name__ == "__main__":
    main()
