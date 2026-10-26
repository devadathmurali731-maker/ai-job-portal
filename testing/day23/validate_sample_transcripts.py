
import json
import sys
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATH = ROOT / "data" / "schemas" / "voice_transcript.schema.json"
SAMPLE_PATH = (
    ROOT
    / "data"
    / "processed"
    / "voice_transcripts"
    / "sample_transcripts.json"
)


def main():
    with SCHEMA_PATH.open(encoding="utf-8") as file:
        schema = json.load(file)

    with SAMPLE_PATH.open(encoding="utf-8") as file:
        records = json.load(file)

    Draft202012Validator.check_schema(schema)

    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    errors_found = False
    seen_ids = set()

    for index, record in enumerate(records, start=1):
        errors = list(validator.iter_errors(record))

        transcript_id = record.get("transcript_id", f"record-{index}")

        if transcript_id in seen_ids:
            print(f"FAIL {transcript_id}: duplicate transcript ID")
            errors_found = True
        seen_ids.add(transcript_id)

        timestamp = record.get("timestamp")
        try:
            parsed = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("Timezone is required")
        except (AttributeError, TypeError, ValueError, OverflowError):
            print(f"FAIL {transcript_id}: invalid ISO 8601 timestamp")
            errors_found = True

        if errors:
            for error in errors:
                print(
                    f"FAIL {transcript_id}: "
                    f"{error.json_path}: {error.message}"
                )
            errors_found = True
        elif timestamp and transcript_id not in seen_ids - {transcript_id}:
            print(f"PASS {transcript_id}: schema validation successful")

    if errors_found:
        sys.exit(1)

    print(f"\nAll {len(records)} sample transcript records passed.")


if __name__ == "__main__":
    main()
