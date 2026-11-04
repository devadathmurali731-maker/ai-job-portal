\# Day 25 – Answer Intent and Understanding Engine



\## 1. Objective



The objective of Day 25 was to develop an Answer Understanding Engine

that analyzes candidate responses to HR screening questions and converts

them into structured information.



The system identifies candidate intent, extracts relevant information,

detects off-topic responses, and identifies missing or vague answers.



\## 2. Implemented Components



\### Intent Classifier

\- Identifies whether an answer relates to skills, experience,

&#x20; availability, or salary expectation.

\- Uses keyword-based classification.

\- Returns the detected intent, confidence score, and matched keywords.



\### Information Extractor

Extracts the following information:

\- Technical and professional skills.

\- Years or months of experience.

\- Joining availability and notice period.

\- Salary expectations.



Salary expressed in LPA is normalized into INR per year.



\### Off-Topic Detector

\- Compares the candidate's response with the expected question category.

\- Identifies responses that do not contain recognizable relevant information.



\### Answer Validator

Identifies:

\- Missing answers.

\- Vague or uncertain answers.

\- Answers without recognizable required information.

\- Complete answers containing recognizable information.



\### Answer Understanding Engine

Combines all components and produces a structured result containing:

\- Candidate answer and question identifiers.

\- Original answer text.

\- Detected intent.

\- Extracted entities.

\- Off-topic status.

\- Answer status.

\- Missing fields and validation reason.



\## 3. Structured Data and Output



The JSON Schema is stored at:



`data/schemas/structured\_answer.schema.json`



Sample structured answers are generated at:



`data/processed/day25/sample\_structured\_answers.json`



The sample dataset contains six cases:



1\. Skills-related answer.

2\. Experience-related answer.

3\. Immediate joining availability.

4\. Salary expectation.

5\. Vague answer.

6\. Off-topic answer.



\## 4. Testing and Validation



Day 25 automated tests were executed using pytest.



Result:

\- Total tests: 36

\- Passed: 36

\- Failed: 0



The generated sample answers were also validated against the

JSON Schema.



Result:

\- Structured answers checked: 6

\- Valid answers: 6

\- Invalid answers: 0



\## 5. Limitations



The current implementation is a rule-based baseline.



\- Intent classification relies on predefined keywords.

\- Skill extraction uses a predefined skill dictionary.

\- Off-topic detection uses keyword matching.

\- Vague-answer detection uses predefined phrases.

\- Experience and salary extraction support common text formats,

&#x20; but may not recognize every possible expression.

\- The system is not yet a trained machine-learning or

&#x20; large-language-model semantic understanding system.



These limitations can be addressed in future development by

introducing NLP models, broader skill dictionaries, and

context-aware classification.



\## 6. Conclusion



Day 25 successfully implemented the foundational Answer Understanding

Engine.



The system can classify candidate answer intent, extract important

candidate information, detect off-topic responses, identify missing

or vague answers, and generate structured JSON output.



All 36 automated tests passed, and all six generated sample answers

passed JSON Schema validation.

