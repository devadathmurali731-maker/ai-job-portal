
from src.answer_understanding.intent_classifier import classify_intent
from src.answer_understanding.information_extractor import extract_information
from src.answer_understanding.off_topic_detector import detect_off_topic
from src.answer_understanding.answer_validator import validate_answer


def understand_answer(
    answer: str,
    question_type: str,
    question_id: str = None,
    answer_id: str = None
) -> dict:
    """Analyze a candidate answer and return structured semantic data."""

    intent_result = classify_intent(answer)
    extracted_information = extract_information(answer)

    topic_result = detect_off_topic(question_type, answer)
    validation_result = validate_answer(question_type, answer)

    # Explicitly vague wording takes priority over off-topic detection.
    explicitly_vague = (
        validation_result["reason"]
        == "Answer contains vague or uncertain wording"
    )

    if validation_result["status"] == "missing":
        final_status = "missing"

    elif explicitly_vague:
        final_status = "vague"

    elif topic_result["is_off_topic"]:
        final_status = "off_topic"

    elif validation_result["status"] == "vague":
        final_status = "vague"

    else:
        final_status = "complete"

    return {
        "answer_id": answer_id,
        "question_id": question_id,
        "question_type": question_type,
        "original_text": answer if isinstance(answer, str) else "",
        "intent": intent_result,
        "entities": extracted_information,
        "is_off_topic": topic_result["is_off_topic"],
        "off_topic_reason": topic_result["reason"],
        "answer_status": final_status,
        "is_vague": validation_result["is_vague"],
        "missing_fields": validation_result["missing_fields"],
        "validation_reason": validation_result["reason"]
    }


if __name__ == "__main__":
    import json

    sample_answer = (
        "I have 3 years of experience in Python and SQL. "
        "I can join immediately. My expected salary is 6 LPA."
    )

    result = understand_answer(
        answer=sample_answer,
        question_type="experience",
        question_id="Q001",
        answer_id="A001"
    )

    print(json.dumps(result, indent=4))
