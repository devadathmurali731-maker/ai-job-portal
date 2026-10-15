# Fairness, Normalization & Bias Reduction

## 1. Overview

The Day 15 fairness layer improves the transparency, consistency, and privacy characteristics of the candidate evaluation pipeline.

The objective is not to claim that the recruitment system is completely free from bias. Instead, the implementation introduces measurable mitigation techniques and diagnostic indicators that make the scoring process more standardized and explainable.

The fairness layer operates independently from the original ATS scoring engine so that the original scoring results remain traceable.

---

## 2. Day 15 Objectives

The implementation addresses five objectives:

1. Normalize resumes to a consistent structure and representation.
2. Reduce unnecessary dependence on exact keyword matching.
3. Normalize scores to a common 0–100 scale.
4. Mask non-essential personal attributes.
5. Evaluate measurable scoring-bias indicators.

---

## 3. Fairness Architecture

The Day 15 architecture is:

```text
Structured Resume
        |
        v
Resume Normalization
        |
        v
Personal Attribute Masking
        |
        v
Fairness-Aware Resume
        |
        +----------------------+
        |                      |
        v                      v
Keyword Evidence       Semantic Evidence
        |                      |
        +----------+-----------+
                   |
                   v
        Keyword-Semantic Balance
                   |
                   v
          Score Normalization
                   |
                   v
        Fairness-Aware Output
                   |
                   v
          Bias Diagnostics
```

The original ATS scoring engine is preserved and is not overwritten by the fairness layer.

---

## 4. Resume Normalization

### File

```text
fairness/normalization.py
```

### Purpose

Resume normalization standardizes the representation of resume information before fairness-aware evaluation.

The normalization layer:

* standardizes section names
* converts text to lowercase
* removes leading and trailing whitespace
* collapses repeated whitespace
* normalizes skill names
* removes duplicate skills
* preserves list structures
* preserves job-relevant information

### Supported section aliases

Examples include:

```text
profile -> summary
professional summary -> summary
technical skills -> skills
professional experience -> work_experience
employment history -> work_experience
academic background -> education
certificates -> certifications
```

### Important implementation detail

The normalization layer preserves the original data type.

For example:

```json
"summary": [
    "Software Engineer with 4 years of experience..."
]
```

becomes:

```json
"summary": [
    "software engineer with 4 years of experience..."
]
```

rather than converting the list into a string representation.

### Validation

Four structured resumes were successfully processed.

The resulting files are stored under:

```text
data/processed/fairness/resumes/
```

Example:

```text
resume_001_sections.json
resume_002_sections.json
resume_003_sections.json
resume_004_sections.json
```

---

## 5. Personal Attribute Masking

### File

```text
fairness/attribute_masking.py
```

### Purpose

The masking layer removes or masks non-essential personal identifiers before fairness-aware processing.

Supported fields include:

* name
* candidate name
* email
* phone number
* mobile number
* address
* LinkedIn
* GitHub
* portfolio
* website
* photo

Masked values are represented using:

```text
[MASKED]
```

### Example

Input:

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "skills": [
        "Python",
        "SQL"
    ]
}
```

Output:

```json
{
    "name": "[MASKED]",
    "email": "[MASKED]",
    "phone": "[MASKED]",
    "skills": [
        "Python",
        "SQL"
    ]
}
```

The verification confirmed that personal identifiers are masked while job-relevant information such as skills remains available.

The four current segmented resumes do not contain these personal identifiers, so no identifier was removed from those particular files. The masking functionality was separately tested with representative personal attributes.

---

## 6. Keyword Dependence Reduction

### File

```text
fairness/keyword_reduction.py
```

Exact keyword matching can overemphasize terminology differences between resumes and job descriptions.

The fairness layer therefore combines keyword evidence with semantic evidence.

Default configuration:

```text
Keyword weight  = 60%
Semantic weight = 40%
```

Formula:

```text
Fair Skill Score =
    Keyword Score × 0.60
    +
    Semantic Score × 0.40
```

The weights are configurable design parameters. They are not presented as a universal definition of fairness.

### Example

For CAND_001 → JOB_001:

```text
Keyword score  = 23.33
Semantic score = 53.54

Fair Skill Score = 35.42
```

The resulting score gives semantic similarity meaningful influence rather than relying entirely on exact keyword overlap.

---

## 7. Score Normalization

### File

```text
fairness/score_normalization.py
```

The normalization layer provides conversion of scores into a common 0–100 scale.

This allows scoring components represented in different numerical ranges to be compared consistently.

Boundary validation prevents invalid source ranges and scores outside the declared source range.

The fairness output stores the normalized score explicitly.

---

## 8. Fair Scoring Integration

### File

```text
fairness/fair_scoring.py
```

The integrated fairness scoring output contains:

```json
{
    "keyword_score": 23.33,
    "semantic_score": 53.54,
    "keyword_weight": 0.6,
    "semantic_weight": 0.4,
    "fair_skill_score": 35.42,
    "normalized_score": 35.42
}
```

The original ATS score remains available separately.

Example:

```text
Original ATS Score: 45.51
Fair Skill Score:   35.42
```

These values represent different metrics and should not be interpreted as a direct before/after replacement.

The Day 15 fair score specifically represents the fairness-aware keyword/semantic scoring component.

---

## 9. Fairness-Aware Resume Processing

### File

```text
fairness/fair_resume_processor.py
```

The processor reads the existing structured resume files:

```text
data/processed/segmented/
```

and generates separate fairness-aware versions:

```text
data/processed/fairness/resumes/
```

The original resume files are not modified.

Four fairness-aware resume outputs were generated successfully.

---

## 10. Fairness Output Generator

### File

```text
fairness/fairness_generator.py
```

The generator connects:

```text
ATS scoring outputs
+
fairness-aware resume processing
+
keyword-semantic balancing
+
score normalization
```

It generated:

```text
24 fairness outputs
```

corresponding to:

```text
4 candidates × 6 jobs = 24 candidate-job combinations
```

Each output records:

* candidate ID
* job ID
* role
* original ATS score
* fairness-aware resume source
* normalization status
* masking status
* keyword score
* semantic score
* fairness-aware score
* normalization status

---

## 11. Bias Indicator Evaluation

### Files

```text
fairness/bias_evaluation.py
fairness/bias_generator.py
```

The bias evaluation layer provides diagnostic measurements of scoring behavior.

It does not claim that the system is biased or unbiased.

The current dataset does not contain demographic-group information. Therefore, demographic disparity analysis was not fabricated.

Instead, the evaluation focuses on measurable scoring indicators.

---

## 12. Bias Evaluation Results

The evaluation covered:

```text
Records evaluated: 24
```

### Fairness-aware score

```text
Average: 40.48
Minimum: 9.74
Maximum: 83.08
```

### Keyword score

```text
Average: 36.35
```

### Semantic score

```text
Average: 46.67
```

### Keyword-semantic gap

```text
10.32
```

The semantic component averaged 10.32 points higher than the keyword component across the evaluated records.

This is a diagnostic observation about the scoring behavior of the current dataset. It is not evidence by itself of demographic discrimination.

---

## 13. Interpretation Limitations

The current bias evaluation has several important limitations.

### No demographic attributes

The available resume dataset does not contain reliable demographic-group labels.

Therefore, the current implementation cannot make claims about score disparities between demographic groups.

### Diagnostic indicators are not proof of discrimination

A score gap or distribution difference can identify an area for investigation, but it does not independently establish discrimination.

### Dataset dependence

The measured values are specific to the current:

```text
4 candidates
6 jobs
24 candidate-job combinations
```

They should not be interpreted as representative of a larger hiring population.

### Configurable scoring weights

The 60/40 keyword-semantic weighting is a project design choice. It should be validated against appropriate recruitment data and requirements before being treated as an operational policy.

---

## 14. Explainability

The fairness layer maintains explainability by recording the individual components used to produce the fairness-aware score.

Instead of storing only one final number, the system preserves:

```text
Keyword evidence
Semantic evidence
Keyword weight
Semantic weight
Fair skill score
Normalized score
Original ATS score
```

This allows an evaluator to understand how the fairness-aware component was calculated.

---

## 15. Data Preservation

The Day 15 implementation does not overwrite the existing ATS scoring outputs.

Original outputs remain under:

```text
data/processed/ats_scores_v2/
```

Fairness-aware outputs are stored separately under:

```text
data/processed/fairness/
```

This separation provides traceability between:

```text
Original ATS evaluation
```

and:

```text
Fairness-aware evaluation
```

---

## 16. Testing

Day 15 introduced 29 fairness-specific tests.

The complete project regression suite currently reports:

```text
162 passed
```

This confirms that the fairness implementation and the previously completed pipeline components pass the current automated test suite together.

---

## 17. Day 15 Deliverables

| Deliverable                    | Status     |
| ------------------------------ | ---------- |
| Resume normalization           | Completed  |
| Personal attribute masking     | Completed  |
| Keyword-dependence reduction   | Completed  |
| Score normalization            | Completed  |
| Bias indicator evaluation      | Completed  |
| Fair scoring integration       | Completed  |
| Fairness-aware resume outputs  | Completed  |
| Fairness candidate-job outputs | Completed  |
| Bias evaluation output         | Completed  |
| Automated fairness tests       | 29 passed  |
| Full project regression        | 162 passed |

---

## 18. Final Design Principle

The Day 15 fairness layer is designed as a **bias-reduction and transparency layer**, not as a guarantee of bias-free hiring.

The implementation focuses on:

* consistent resume representation
* protection of non-essential personal identifiers
* reduced dependence on exact keyword matching
* standardized scoring
* explainable fairness outputs
* diagnostic bias measurements
* preservation of the original ATS results
* reproducible automated testing

Future fairness work could incorporate larger evaluation datasets, validated demographic-group data where legally and ethically appropriate, subgroup performance analysis, calibration analysis, and independent fairness validation.
