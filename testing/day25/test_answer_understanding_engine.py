
from src.answer_understanding.answer_understanding_engine import understand_answer


def test_complete_candidate_answer():
    result = understand_answer(
        answer=(
            "I have 3 years of experience in Python and SQL. "
            "I can join immediately. My expected salary is 6 LPA."
        ),
        question_type="experience",
        question_id="Q001",
        answer_id="A001"
    )

    assert result["answer_status"] == "complete"
    assert result["is_off_topic"] is False
    assert result["entities"]["experience"]["value"] == 3
    assert "Python" in result["entities"]["skills"]
    assert result["entities"]["salary_expectation"]["amount"] == 600000


def test_missing_candidate_answer():
    result = understand_answer(
        answer="",
        question_type="skills"
    )

    assert result["answer_status"] == "missing"


def test_vague_candidate_answer():
    result = understand_answer(
        answer="I don't know.",
        question_type="skills"
    )

    assert result["answer_status"] == "vague"
    assert result["is_vague"] is True


def test_off_topic_candidate_answer():
    result = understand_answer(
        answer="My expected salary is 6 LPA.",
        question_type="skills"
    )

    assert result["answer_status"] == "off_topic"
    assert result["is_off_topic"] is True


def test_structured_output_fields():
    result = understand_answer(
        answer="I know Python and SQL.",
        question_type="skills",
        question_id="Q002",
        answer_id="A002"
    )

    required_fields = [
        "answer_id",
        "question_id",
        "question_type",
        "original_text",
        "intent",
        "entities",
        "is_off_topic",
        "answer_status",
        "is_vague",
        "missing_fields"
    ]

    for field in required_fields:
        assert field in result
