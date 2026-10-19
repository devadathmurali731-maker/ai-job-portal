# Day 20 — Management Demo Guide

## 1. Purpose

Demonstrate the existing AI-assisted Applicant Tracking System (ATS), explain its scoring logic, and summarize the current benchmark and evaluation evidence.

This is a controlled project demonstration, not a claim of production readiness or validated hiring effectiveness.

## 2. Live demonstration

From the project root, with the project virtual environment activated, run:

```powershell
python .\testing\day20\live_demo.py
```

The read-only demo loads the processed candidate data, job profile, and semantic matching result, then calls the existing ATS scoring engine. It does not write ATS score files.

### Demonstrated example

- Candidate: CAND_001
- Job: JOB_001
- Role: Data Scientist
- Recorded experience: 4.75 years
- Final ATS score: 45.51/100

| Component | Score | Adjusted weight | Contribution |
|---|---:|---:|---:|
| Skill match | 23.33 | 0.400 | 9.33 |
| Experience relevance | 53.93 | 0.200 | 10.79 |
| Education alignment | 80.00 | 0.150 | 12.00 |
| Semantic similarity | 53.54 | 0.250 | 13.39 |

The weighted contributions sum to the final score, subject to displayed rounding.

## 3. Explain the scoring logic

The engine calculates four component scores on a 0–100 scale and combines them using role-specific weights. When a component is unavailable, the engine can redistribute weights across available components.

Explain that the result is a ranking aid, not a hiring decision. Recruiters must review source evidence and use consistent, job-related criteria.

## 4. Benchmark evidence

The Day 20 benchmark summary contains 60 records:
- Successful records: 60
- Failed records: 0
- Average ATS score: 38.434
- Minimum ATS score: 14.67
- Maximum ATS score: 90.22

The benchmark runner used no semantic result for its scoring calls. Therefore, these benchmark figures do not independently validate semantic matching.

## 5. Testing evidence

A previous recorded project test run reported 164 tests passing. This is historical test evidence; rerun the test suite before a release if a fresh result is required.

The existing Day 18 performance report records small-sample component timings and embedding comparisons. It does not establish production-scale throughput, memory use, or load capacity.

## 6. Evaluation caveats

The earlier human-reviewed relevance evaluation reported:
- Precision: 100%
- Recall: 31.25%
- F1: 47.62%
- Accuracy: 81.67%

The evaluation was small and not blinded, and its relevance threshold was not validated on a held-out test set. The low recall indicates that relevant candidates may be missed. These figures should be treated as preliminary, not proof of hiring accuracy.

## 7. Architecture and deployment status

The project contains modular parsing, skill, experience, education, semantic matching, scoring, ranking, and fairness-related components.

The documented REST API is a proposed specification, not evidence of implemented and deployed API routes. The root `main.py` is a startup smoke test rather than a complete web application.

## 8. Fairness, privacy, and human oversight

Before real hiring use:
- Validate job-relatedness and outcomes across representative candidate groups.
- Investigate false negatives and possible proxy variables.
- Define data access, retention, deletion, and security controls.
- Obtain appropriate legal and privacy review.
- Keep human review and an appeal/correction process.
- Avoid using protected characteristics to score candidates.

## 9. Recommended next steps

1. Conduct blinded evaluation with multiple reviewers.
2. Tune thresholds on development data and validate on a held-out test set.
3. Measure ranking quality and false-negative patterns.
4. Add representative-scale load, memory, security, and failure-recovery tests.
5. Implement and test an authenticated API/UI before describing the system as deployable.
6. Document model/data versions and a repeatable release process.

## 10. Closing statement

The project demonstrates an implemented ATS scoring pipeline, a successful 60-record benchmark run, a recorded automated test result, and a read-only live scoring example. Further validation, deployment engineering, security controls, and human oversight are required before operational hiring use.
