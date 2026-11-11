from statistics import mean


def calculate_screening_score(question_results: list) -> dict:
    """
    Aggregate per-question scores into an overall screening score.
    """

    if not isinstance(question_results, list) or not question_results:
        return {
            "total_questions": 0,
            "overall_screening_score": 0,
            "performance_level": "Not Evaluated",
            "question_breakdown": [],
            "parameter_averages": {
                "clarity": 0,
                "relevance": 0,
                "completeness": 0,
                "consistency": 0
            }
        }

    parameter_names = [
        "clarity",
        "relevance",
        "completeness",
        "consistency"
    ]

    question_scores = []
    parameter_scores = {name: [] for name in parameter_names}

    for result in question_results:
        normalized_score = max(
            0,
            min(100, float(result.get("normalized_score", 0)))
        )

        question_scores.append(normalized_score)

        scores = result.get("scores", {})

        for parameter in parameter_names:
            value = max(
                0,
                min(100, float(scores.get(parameter, 0)))
            )
            parameter_scores[parameter].append(value)

    overall_score = round(mean(question_scores), 2)

    parameter_averages = {
        name: round(mean(values), 2) if values else 0
        for name, values in parameter_scores.items()
    }

    if overall_score >= 80:
        performance_level = "Excellent"
    elif overall_score >= 65:
        performance_level = "Good"
    elif overall_score >= 50:
        performance_level = "Average"
    else:
        performance_level = "Needs Improvement"

    return {
        "total_questions": len(question_results),
        "overall_screening_score": overall_score,
        "performance_level": performance_level,
        "question_breakdown": question_results,
        "parameter_averages": parameter_averages
    }