\# Day 22 – HR Screening Dataset Creation



\## 1. Objective



Create a structured, reusable, AI-ready HR screening question bank for automated candidate screening calls across multiple job roles.



\## 2. Deliverables



1\. `data/processed/hr\_screening/hr\_screening\_questions.json` – primary question bank.

2\. `data/processed/hr\_screening/question\_category\_mapping.json` – category definitions, answer types, and scoring importance levels.

3\. `data/processed/hr\_screening/ai\_conversation\_questions.json` – question objects with prompts and conversation metadata.

4\. `screening\_ai/create\_hr\_question\_dataset.py` – dataset generation script.

5\. `testing/test\_day22\_hr\_screening\_dataset.py` – automated validation tests.



\## 3. Dataset Summary



\- Total questions: 28

\- Categories: 7

\- Supported job roles: 6

\- Default question language: English

\- Dataset version: 1.0.0



\### Categories



\- Introduction

\- Education

\- Experience

\- Skills

\- Location

\- Salary

\- Notice period



\## 4. Question Metadata



Each question includes:



\- Unique question ID

\- Category

\- Reusable question template

\- Applicable job roles

\- Expected answer type

\- Mandatory/optional flag

\- Scoring importance and weight

\- Language and translation metadata

\- Template variables

\- Active status



Conversation-ready objects additionally include the prompt, empty-answer reprompt, skip policy, and structured-answer capture flag.



\## 5. Multilingual Readiness



The dataset uses language metadata with English (`en`) as the source language and supports adding Malayalam (`ml`) translations later. Translation entries are currently empty; translated question text has not yet been supplied or validated.



\## 6. Validation and Testing



All three JSON files were successfully parsed. Validation confirmed 28 questions, 28 unique question IDs, seven categories, and six job roles.



Automated test results:



`8 passed, 28 subtests passed`



Tests cover JSON loading, unique IDs, category coverage, role configuration, required metadata, category mapping, conversation-question consistency, and conversation metadata.



\## 7. Responsible Screening Design



Mandatory information collection is kept separate from candidate-quality scoring. Salary, location, and notice-period responses should be evaluated against relevant job requirements rather than treated as automatic measures of candidate quality. Optional questions may be skipped.



\## 8. Limitations and Future Improvements



\- English is the only populated question language at this stage.

\- Question templates have not yet been evaluated in live screening sessions.

\- Role-specific skill lists and validation rules can be refined further.

\- Future work can add Malayalam translations, localized prompts, response validation, and integration with the screening workflow.



\## 9. Completion Status



The Day 22 dataset, category mapping, conversation-ready objects, generation script, and automated tests have been created and validated.



