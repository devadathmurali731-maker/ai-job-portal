
from src.confidence_analysis.confidence_analyzer import (
    analyze_confidence
)

from src.confidence_analysis.contradiction_detector import (
    detect_contradictions
)

from src.sentiment_analysis.sentiment_scorer import (
    analyze_sentiment
)


def analyze_communication(answers: list) -> dict:
    """
    Analyze candidate communication signals across all answers.

    Generates confidence, sentiment, behavioral indicators,
    and cross-answer contradiction results.
    """

    if not isinstance(answers, list):
        raise ValueError("Answers must be provided as a list.")

    answer_results = []

    for answer_data in answers:
        original_text = answer_data.get("original_text", "")

        confidence_result = analyze_confidence(
            original_text,
            answer_data
        )

        sentiment_result = analyze_sentiment(
            original_text
        )

        answer_results.append({
            "answer_id": answer_data.get("answer_id"),
            "question_id": answer_data.get("question_id"),
            "original_text": original_text,
            "confidence_analysis": confidence_result,
            "sentiment_analysis": sentiment_result
        })

    contradiction_result = detect_contradictions(answers)

    if answer_results:
        average_confidence = round(
            sum(
                item["confidence_analysis"]["confidence_score"]
                for item in answer_results
            ) / len(answer_results),
            2
        )

        average_sentiment = round(
            sum(
                item["sentiment_analysis"]["sentiment_score"]
                for item in answer_results
            ) / len(answer_results),
            2
        )
    else:
        average_confidence = 0
        average_sentiment = 0

    if average_confidence >= 80:
        communication_strength = "Strong"
    elif average_confidence >= 60:
        communication_strength = "Moderate"
    else:
        communication_strength = "Needs Improvement"

    return {
        "total_answers": len(answer_results),
        "average_confidence_score": average_confidence,
        "average_sentiment_score": average_sentiment,
        "communication_strength": communication_strength,
        "answer_analysis": answer_results,
        "behavioral_indicators": {
            "total_hesitation_instances": sum(
                item["confidence_analysis"]["hesitation_count"]
                for item in answer_results
            ),
            "total_uncertainty_instances": sum(
                item["confidence_analysis"]["uncertainty_count"]
                for item in answer_results
            ),
            "contradiction_analysis": contradiction_result
        },
        "limitations": [
            "Confidence is estimated from text-based indicators, not psychology.",
            "Sentiment uses predefined vocabulary.",
            "Speaking pace and vocal hesitation require audio timing or acoustic analysis.",
            "Different extracted values are potential conflicts, not automatically genuine contradictions."
        ]
    }
