
import json
from pathlib import Path

OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "hr_screening"
)

ROLES = [
    "Data Scientist",
    "Software Engineer",
    "Machine Learning Engineer",
    "Data Analyst",
    "HR Executive",
    "Business Analyst",
]

CATEGORY_MAPPING = {
    "introduction": {
        "label": "Introduction",
        "description": "Candidate introduction and job motivation.",
        "default_scoring_importance": "low",
    },
    "education": {
        "label": "Education",
        "description": "Qualifications relevant to the role.",
        "default_scoring_importance": "medium",
    },
    "experience": {
        "label": "Experience",
        "description": "Relevant work history and responsibilities.",
        "default_scoring_importance": "high",
    },
    "skills": {
        "label": "Skills",
        "description": "Role-related skills and practical experience.",
        "default_scoring_importance": "high",
    },
    "location": {
        "label": "Location",
        "description": "Work location, relocation, and work arrangement.",
        "default_scoring_importance": "low",
    },
    "salary": {
        "label": "Salary",
        "description": "Compensation expectations and alignment.",
        "default_scoring_importance": "low",
    },
    "notice_period": {
        "label": "Notice period",
        "description": "Availability and potential joining date.",
        "default_scoring_importance": "low",
    },
}

QUESTION_TEMPLATES = [
    ("introduction", "INTRO_001",
     "Could you briefly introduce yourself and describe your professional background?",
     "text", False, "low", "all"),
    ("introduction", "INTRO_002",
     "What interests you about the {role} position?",
     "text", False, "medium", "all"),
    ("introduction", "INTRO_003",
     "What are you looking for in your next role?",
     "text", False, "low", "all"),
    ("introduction", "INTRO_004",
     "Which of your strengths are most relevant to this position?",
     "text", False, "medium", "all"),

    ("education", "EDU_001",
     "What is your highest completed qualification?",
     "single_line_text", True, "medium", "all"),
    ("education", "EDU_002",
     "What was your field of study?",
     "single_line_text", False, "low", "all"),
    ("education", "EDU_003",
     "Do you hold any certifications relevant to this role? Please describe them.",
     "text", False, "medium", "all"),
    ("education", "EDU_004",
     "Are you currently pursuing any additional qualifications?",
     "yes_no_with_details", False, "low", "all"),

    ("experience", "EXP_001",
     "How many years of relevant professional experience do you have?",
     "number", True, "high", "all"),
    ("experience", "EXP_002",
     "Please describe your most relevant previous role and responsibilities.",
     "text", True, "high", "all"),
    ("experience", "EXP_003",
     "Describe a project or achievement relevant to this position.",
     "text", False, "high", "all"),
    ("experience", "EXP_004",
     "Have you worked in a similar role before?",
     "yes_no_with_details", False, "medium", "all"),

    ("skills", "SKILL_001",
     "Which of the following job-related skills have you used professionally: {required_skills}?",
     "multi_select_with_details", True, "high", "all"),
    ("skills", "SKILL_002",
     "How have you applied {key_skill} in a project or at work?",
     "text", False, "high", "all"),
    ("skills", "SKILL_003",
     "Which tools or technologies do you use most confidently for this role?",
     "text", False, "medium", "all"),
    ("skills", "SKILL_004",
     "Would you be comfortable completing a role-relevant technical or practical assessment?",
     "yes_no_with_details", False, "medium", "all"),

    ("location", "LOC_001",
     "What city or region are you currently based in?",
     "single_line_text", True, "low", "all"),
    ("location", "LOC_002",
     "Are you able to work from {work_location} under the advertised work arrangement?",
     "yes_no_with_details", True, "low", "all"),
    ("location", "LOC_003",
     "Would you be willing to relocate if the role requires it?",
     "yes_no_with_details", False, "low", "all"),
    ("location", "LOC_004",
     "Do you require any specific work arrangement, such as remote, hybrid, or on-site?",
     "single_choice_with_details", False, "low", "all"),

    ("salary", "SAL_001",
     "What is your expected annual compensation in {currency}?",
     "number_with_currency", True, "low", "all"),
    ("salary", "SAL_002",
     "What is your preferred compensation structure, if any?",
     "single_choice_with_details", False, "low", "all"),
    ("salary", "SAL_003",
     "Is your expected compensation negotiable depending on the role and overall package?",
     "yes_no_with_details", False, "low", "all"),
    ("salary", "SAL_004",
     "Would you like to share any additional compensation expectations?",
     "text", False, "low", "all"),

    ("notice_period", "NOTICE_001",
     "What is your current notice period, if applicable?",
     "single_choice_with_details", True, "low", "all"),
    ("notice_period", "NOTICE_002",
     "What is the earliest date you could join?",
     "date_or_text", True, "low", "all"),
    ("notice_period", "NOTICE_003",
     "Would you be able to join by {target_joining_date}?",
     "yes_no_with_details", False, "low", "all"),
    ("notice_period", "NOTICE_004",
     "Would you need to serve a notice period or complete other commitments before joining?",
     "yes_no_with_details", False, "low", "all"),
]


def make_question(category, question_id, template, answer_type,
                  mandatory, importance, role_scope):
    roles = ROLES if role_scope == "all" else role_scope

    return {
        "question_id": question_id,
        "category": category,
        "question_template": template,
        "applicable_roles": roles,
        "expected_answer": {
            "type": answer_type,
            "required": mandatory,
            "allow_unknown": not mandatory,
        },
        "mandatory": mandatory,
        "scoring": {
            "importance": importance,
            "weight": {
                "low": 1,
                "medium": 2,
                "high": 3,
            }[importance],
            "use_for_candidate_quality_score": category in {
                "education", "experience", "skills"
            },
        },
        "language": {
            "default": "en",
            "translations": {},
            "translation_status": "english_source_only",
        },
        "template_variables": [
            part.split("}")[0]
            for part in template.split("{")[1:]
            if "}" in part
        ],
        "response_validation": {},
        "active": True,
    }


def validate_dataset(questions):
    ids = [q["question_id"] for q in questions]
    assert len(ids) == len(set(ids)), "Duplicate question IDs found."

    expected_categories = set(CATEGORY_MAPPING)
    actual_categories = {q["category"] for q in questions}
    assert actual_categories == expected_categories, (
        f"Category mismatch: {actual_categories}"
    )

    for question in questions:
        assert question["expected_answer"]["type"]
        assert question["scoring"]["importance"] in {
            "low", "medium", "high"
        }
        assert question["applicable_roles"]

    assert len(questions) == 28, "Expected 28 questions."
    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    questions = [
        make_question(*template)
        for template in QUESTION_TEMPLATES
    ]
    validate_dataset(questions)

    dataset = {
        "dataset_name": "AI Job Portal HR Screening Question Bank",
        "dataset_version": "1.0.0",
        "language_default": "en",
        "supported_language_structure": ["en", "ml"],
        "roles": ROLES,
        "question_count": len(questions),
        "categories": list(CATEGORY_MAPPING),
        "questions": questions,
    }

    conversation_dataset = {
        "dataset_name": "AI Screening Conversation Questions",
        "dataset_version": "1.0.0",
        "language_default": "en",
        "conversation_flow": [
            "introduction",
            "education",
            "experience",
            "skills",
            "location",
            "salary",
            "notice_period",
        ],
        "questions": [
            {
                **q,
                "conversation": {
                    "prompt": q["question_template"],
                    "reprompt_if_empty": (
                        "Would you like to provide an answer, or skip "
                        "this question if it is optional?"
                    ),
                    "allow_skip": not q["mandatory"],
                    "capture_structured_answer": True,
                },
            }
            for q in questions
        ],
    }

    outputs = {
        "hr_screening_questions.json": dataset,
        "question_category_mapping.json": {
            "mapping_version": "1.0.0",
            "categories": CATEGORY_MAPPING,
            "answer_types": [
                "text",
                "single_line_text",
                "number",
                "yes_no_with_details",
                "multi_select_with_details",
                "single_choice_with_details",
                "number_with_currency",
                "date_or_text",
            ],
            "scoring_importance_levels": {
                "low": 1,
                "medium": 2,
                "high": 3,
            },
            "note": (
                "Mandatory information does not automatically mean "
                "the answer should affect candidate quality scoring."
            ),
        },
        "ai_conversation_questions.json": conversation_dataset,
    }

    for filename, content in outputs.items():
        path = OUTPUT_DIR / filename
        path.write_text(
            json.dumps(content, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Created: {path}")

    print(f"\nValidated {len(questions)} questions.")
    print(f"Categories: {len(CATEGORY_MAPPING)}")
    print(f"Applicable roles: {len(ROLES)}")


if __name__ == "__main__":
    main()
