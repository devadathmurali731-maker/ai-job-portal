
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "data" / "schemas"


def is_valid_datetime(value):
    """Return True if value is a valid ISO 8601 date-time string."""
    if not isinstance(value, str) or not value:
        return False

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except (ValueError, OverflowError):
        return False


def load_schema(filename):
    """Load a JSON Schema and verify that the schema itself is valid."""
    schema_path = SCHEMA_DIR / filename

    with schema_path.open(encoding="utf-8") as file:
        schema = json.load(file)

    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def current_timestamp():
    """Return the current UTC time in ISO 8601 format."""
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


class TranscriptSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_schema("voice_transcript.schema.json")

    def valid_record(self):
        return {
            "transcript_id": "TR-001",
            "candidate_id": "CAN-001",
            "job_id": "JOB-001",
            "question_id": "Q-001",
            "timestamp": current_timestamp(),
            "language": "en",
            "transcript_text": "I have three years of Python experience.",
            "confidence": 0.95,
        }

    def test_valid_transcript(self):
        record = self.valid_record()
        self.assertTrue(self.validator.is_valid(record))
        self.assertTrue(is_valid_datetime(record["timestamp"]))

    def test_missing_candidate_id_is_invalid(self):
        record = self.valid_record()
        del record["candidate_id"]
        self.assertFalse(self.validator.is_valid(record))

    def test_confidence_above_one_is_invalid(self):
        record = self.valid_record()
        record["confidence"] = 1.2
        self.assertFalse(self.validator.is_valid(record))

    def test_negative_confidence_is_invalid(self):
        record = self.valid_record()
        record["confidence"] = -0.1
        self.assertFalse(self.validator.is_valid(record))

    def test_invalid_timestamp_is_rejected(self):
        record = self.valid_record()
        record["timestamp"] = "not-a-timestamp"

        self.assertTrue(self.validator.is_valid(record))
        self.assertFalse(is_valid_datetime(record["timestamp"]))


class ScreeningInteractionSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_schema(
            "ai_screening_interaction.schema.json"
        )

    def valid_record(self):
        return {
            "interaction_id": "INT-001",
            "session_id": "SES-001",
            "candidate_id": "CAN-001",
            "job_id": "JOB-001",
            "question_id": "Q-001",
            "asked_at": current_timestamp(),
            "answered_at": None,
            "status": "asked",
        }

    def test_valid_interaction(self):
        record = self.valid_record()
        self.assertTrue(self.validator.is_valid(record))
        self.assertTrue(is_valid_datetime(record["asked_at"]))

    def test_missing_session_id_is_invalid(self):
        record = self.valid_record()
        del record["session_id"]
        self.assertFalse(self.validator.is_valid(record))

    def test_invalid_status_is_rejected(self):
        record = self.valid_record()
        record["status"] = "completed"
        self.assertFalse(self.validator.is_valid(record))

    def test_speech_confidence_above_one_is_invalid(self):
        record = self.valid_record()
        record["speech_confidence"] = 1.5
        self.assertFalse(self.validator.is_valid(record))

    def test_invalid_asked_at_is_rejected(self):
        record = self.valid_record()
        record["asked_at"] = "yesterday"

        self.assertTrue(self.validator.is_valid(record))
        self.assertFalse(is_valid_datetime(record["asked_at"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
