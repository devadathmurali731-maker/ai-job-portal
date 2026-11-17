
def detect_contradictions(answers: list) -> dict:
    """
    Identify conflicting extracted values across a candidate's answers.

    Only compares values when both answers contain usable data.
    """

    contradictions = []

    experience_values = []
    salary_values = []
    availability_values = []

    for answer in answers:
        entities = answer.get("entities", {})
        answer_id = answer.get("answer_id")
        question_id = answer.get("question_id")

        experience = entities.get("experience", {})
        if experience.get("value") is not None:
            experience_values.append({
                "answer_id": answer_id,
                "question_id": question_id,
                "value": experience.get("value"),
                "unit": experience.get("unit")
            })

        salary = entities.get("salary_expectation", {})
        if salary.get("amount") is not None:
            salary_values.append({
                "answer_id": answer_id,
                "question_id": question_id,
                "amount": salary.get("amount"),
                "currency": salary.get("currency"),
                "period": salary.get("period")
            })

        availability = entities.get("availability", {})
        if availability.get("value") is not None:
            availability_values.append({
                "answer_id": answer_id,
                "question_id": question_id,
                "value": availability.get("value"),
                "unit": availability.get("unit")
            })

    def compare_values(records, field, category):
        """Compare values within the same measurement category."""

        for index, first in enumerate(records):
            for second in records[index + 1:]:
                same_unit = (
                    first.get("unit") == second.get("unit")
                    if field == "value"
                    else (
                        first.get("currency") == second.get("currency")
                        and first.get("period") == second.get("period")
                    )
                )

                if (
                    same_unit
                    and first[field] != second[field]
                ):
                    contradictions.append({
                        "category": category,
                        "answer_ids": [
                            first["answer_id"],
                            second["answer_id"]
                        ],
                        "question_ids": [
                            first["question_id"],
                            second["question_id"]
                        ],
                        "values": [
                            first[field],
                            second[field]
                        ],
                        "description": (
                            f"Different {category} values were "
                            "found across answers."
                        )
                    })

    compare_values(
        experience_values,
        "value",
        "experience"
    )

    compare_values(
        salary_values,
        "amount",
        "salary_expectation"
    )

    compare_values(
        availability_values,
        "value",
        "availability"
    )

    return {
        "contradiction_count": len(contradictions),
        "has_contradictions": bool(contradictions),
        "contradictions": contradictions
    }
