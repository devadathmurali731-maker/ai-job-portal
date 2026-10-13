# Day 17 — Job Profile Consistency Audit

## Purpose

Compare structured job-profile fields against the normalized job-description text before evaluating ATS ranking quality.

## Findings

### JD-001 — Data Scientist

- The structured and text-based requirements are broadly aligned.
- The normalized text explicitly mentions Exploratory Data Analysis and Feature Engineering, which are not included in the structured required-skills list.
- Review skill normalization and completeness.

### JD-002 — Software Engineer

- The structured required-skills list contains Python, SQL, and Git.
- The normalized text additionally requires Java, Object-Oriented Programming, Data Structures, Algorithms, REST APIs, and Spring Boot.
- SQL appears in both structured required and preferred skills.
- The structured profile does not fully represent the normalized job description.

### JD-003 — Machine Learning Engineer

- The structured profile lists TensorFlow and PyTorch as separate required skills.
- The normalized text permits PyTorch or TensorFlow.
- Machine Learning appears in both structured required and preferred skills.
- Review alternative-skill logic and duplicate-skill handling.

### JD-004 — Data Analyst

- The structured profile omits several skills explicitly listed in the normalized text, including Data Cleaning, Statistical Analysis, Pivot Tables, and Power Query.
- SQL appears in both structured required and preferred skills.
- Review requirement completeness and duplicate handling.

### JD-005 — HR Executive

- The structured profile lists MBA as required.
- The normalized text requires a bachelor's degree and describes an MBA in Human Resources as preferred.
- This is a material education-requirement contradiction that could affect candidate scores.

### JD-006 — Business Analyst

- The structured profile lists SQL, Power BI, Microsoft Excel, and Communication as required.
- The normalized text additionally lists Requirements Gathering, Business Process Analysis, Stakeholder Management, Problem Solving, and Business Documentation.
- Review the completeness of the structured required-skills list.

## Evaluation Decision

1. Preserve the original job profiles.
2. Resolve or explicitly document conflicts between structured fields and normalized descriptions.
3. Define independent human-review criteria before assigning relevance labels.
4. Do not calculate ATS precision, recall, or accuracy until the benchmark labels and score-to-candidate mappings are verified.

## Important Limitation

This is a preliminary consistency audit based on the displayed job-profile JSON content. It does not establish that the ATS scoring engine is defective, nor does it measure ATS accuracy.
