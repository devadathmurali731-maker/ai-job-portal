
import json
from pathlib import Path

from src.answer_understanding.answer_understanding_engine import understand_answer


samples = [
    {
        "answer_id": "A001",
        "question_id": "Q001",
        "question_type": "skills",
        "answer": "I have strong skills in Python, SQL and Power BI."
    },
    {
        "answer_id": "A002",
        "question_id": "Q002",
        "question_type": "experience",
        "answer": "I have 3 years of experience in data analysis."
    },
    {
        "answer_id": "A003",
        "question_id": "Q003",
        "question_type": "availability",
        "answer": "I can join immediately."
    },
    {
        "answer_id": "A004",
        "question_id": "Q004",
        "question_type": "salary",
        "answer": "My expected salary is 6 LPA."
    },
    {
        "answer_id": "A005",
        "question_id": "Q005",
        "question_type": "skills",
        "answer": "I don't know."
    },
    {
        "answer_id": "A006",
        "question_id": "Q006",
        "question_type": "skills",
        "answer": "My expected salary is 6 LPA."
    }
]


results = []

for sample in samples:
    result = understand_answer(
        answer=sample["answer"],
        question_type=sample["question_type"],
        question_id=sample["question_id"],
        answer_id=sample["answer_id"]
    )

    results.append(result)


output_path = Path(__file__).with_name("sample_structured_answers.json")

with output_path.open("w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print(f"Successfully generated {len(results)} structured answers.")
print(f"Output saved to: {output_path}")
