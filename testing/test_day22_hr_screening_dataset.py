
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed" / "hr_screening"

EXPECTED_CATEGORIES = {
    "introduction",
    "education",
    "experience",
    "skills",
    "location",
    "salary",
    "notice_period",
}


class TestHRScreeningDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = json.loads(
            (DATA_DIR / "hr_screening_questions.json").read_text(
                encoding="utf-8"
            )
        )
        cls.mapping = json.loads(
            (DATA_DIR / "question_category_mapping.json").read_text(
                encoding="utf-8"
            )
        )
        cls.conversation = json.loads(
            (DATA_DIR / "ai_conversation_questions.json").read_text(
                encoding="utf-8"
            )
        )

    def test_all_json_files_load(self):
        self.assertTrue(self.bank)
        self.assertTrue(self.mapping)
        self.assertTrue(self.conversation)

    def test_question_count_and_unique_ids(self):
        questions = self.bank["questions"]
        ids = [q["question_id"] for q in questions]
        self.assertEqual(len(questions), 28)
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_required_categories_present(self):
        actual = {q["category"] for q in self.bank["questions"]}
        self.assertEqual(actual, EXPECTED_CATEGORIES)

    def test_all_six_roles_configured(self):
        self.assertEqual(len(self.bank["roles"]), 6)
        for question in self.bank["questions"]:
            self.assertTrue(question["applicable_roles"])
            self.assertTrue(
                set(question["applicable_roles"]).issubset(
                    set(self.bank["roles"])
                )
            )

    def test_required_question_metadata(self):
        for question in self.bank["questions"]:
            with self.subTest(question=question["question_id"]):
                self.assertIn("question_template", question)
                self.assertIn("expected_answer", question)
                self.assertIn("mandatory", question)
                self.assertIn("scoring", question)
                self.assertIn("language", question)
                self.assertIn(
                    question["scoring"]["importance"],
                    {"low", "medium", "high"},
                )
                self.assertTrue(question["expected_answer"]["type"])

    def test_category_mapping_complete(self):
        self.assertEqual(
            set(self.mapping["categories"]),
            EXPECTED_CATEGORIES,
        )

    def test_conversation_questions_match_bank(self):
        bank_ids = {
            q["question_id"] for q in self.bank["questions"]
        }
        conversation_ids = {
            q["question_id"] for q in self.conversation["questions"]
        }
        self.assertEqual(bank_ids, conversation_ids)

    def test_conversation_metadata_present(self):
        for question in self.conversation["questions"]:
            self.assertIn("conversation", question)
            self.assertIn(
                "prompt", question["conversation"]
            )
            self.assertIn(
                "allow_skip", question["conversation"]
            )


if __name__ == "__main__":
    unittest.main()
