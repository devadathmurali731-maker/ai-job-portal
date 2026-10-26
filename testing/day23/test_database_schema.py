
import sqlite3
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SQL_PATH = ROOT / "data" / "schemas" / "day23_screening_schema.sql"


class DatabaseSchemaTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")

        sql = SQL_PATH.read_text(encoding="utf-8")
        self.connection.executescript(sql)

    def tearDown(self):
        self.connection.close()

    def test_all_four_tables_are_created(self):
        rows = self.connection.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table'
            AND name IN (
                'screening_sessions',
                'voice_transcripts',
                'screening_interactions',
                'transcript_segments'
            )
            """
        ).fetchall()

        self.assertEqual(len(rows), 4)

    def test_valid_transcript_can_be_inserted(self):
        self.connection.execute(
            """
            INSERT INTO voice_transcripts (
                transcript_id, candidate_id, job_id, question_id,
                timestamp, language, transcript_text, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "TR-001", "CAN-001", "JOB-001", "Q-001",
                "2026-10-26T06:30:00Z", "en",
                "Python and SQL experience", 0.96
            ),
        )

        count = self.connection.execute(
            "SELECT COUNT(*) FROM voice_transcripts"
        ).fetchone()[0]

        self.assertEqual(count, 1)

    def test_confidence_above_one_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO voice_transcripts (
                    transcript_id, candidate_id, job_id, question_id,
                    timestamp, language, transcript_text, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "TR-BAD", "CAN-001", "JOB-001", "Q-001",
                    "2026-10-26T06:30:00Z", "en",
                    "Example", 1.5
                ),
            )

    def test_missing_session_foreign_key_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO screening_interactions (
                    interaction_id, session_id, candidate_id, job_id,
                    question_id, asked_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "INT-001", "SESSION-MISSING", "CAN-001", "JOB-001",
                    "Q-001", "2026-10-26T06:29:00Z", "asked"
                ),
            )

    def test_negative_segment_duration_is_rejected(self):
        self.connection.execute(
            """
            INSERT INTO voice_transcripts (
                transcript_id, candidate_id, job_id, question_id,
                timestamp, language, transcript_text, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "TR-001", "CAN-001", "JOB-001", "Q-001",
                "2026-10-26T06:30:00Z", "en", "Example", 0.9
            ),
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO transcript_segments (
                    transcript_id, sequence_number,
                    start_seconds, end_seconds, text
                ) VALUES (?, ?, ?, ?, ?)
                """,
                ("TR-001", 1, 5.0, 2.0, "Invalid segment"),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
