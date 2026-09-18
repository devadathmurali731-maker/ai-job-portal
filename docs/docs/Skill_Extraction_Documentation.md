# Skill Extraction Engine Documentation

## 1. Overview

The Skill Extraction Engine is responsible for identifying technical and non-technical skills from resumes.

The engine converts unstructured resume content into structured skill information that can be used by downstream components such as:

- ATS scoring
- Candidate screening
- Candidate-job matching
- Skill gap analysis
- Interview generation
- Candidate ranking

The engine supports exact skill matching, synonym detection, fuzzy spelling correction, skill-stack expansion, normalization, deduplication, and confidence scoring.

---

## 2. Objective

The main objectives of the Skill Extraction Engine are:

1. Extract skills from resume text.
2. Support technical, business, and creative skills.
3. Normalize different representations of the same skill.
4. Detect common skill synonyms.
5. Handle spelling variations and minor spelling mistakes.
6. Expand common technology stacks.
7. Remove duplicate skills.
8. Assign confidence scores to extracted skills.
9. Generate structured JSON skill profiles.

---

## 3. Project Structure

```text
skills/
├── master_skill_dictionary.json
├── skill_extractor.py
├── test_skill_extractor.py
├── test_real_resumes.py
└── generate_skill_profiles.py
