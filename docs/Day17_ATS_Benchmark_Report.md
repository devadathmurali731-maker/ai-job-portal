# Day 17 — ATS Benchmark Report

## 1. Objective

Evaluate the ATS scoring engine across multiple candidate resumes and job profiles, verify that all candidate-job pairs produce results, and document a targeted education-matching correction.

## 2. Benchmark Design

- Candidate resumes: 10
- Job profiles: 6
- Expected candidate-job pairs: 60
- Calculation: 10 candidates × 6 job profiles
- Before-fix and after-fix summaries: 60 rows each

The benchmark evaluates each candidate against each job profile. Cross-role comparisons are stress tests and should not be interpreted as proof that the system can accurately identify the best candidate for every role.

## 3. Execution Results

| Metric | Before fix | After fix |
|---|---:|---:|
| Candidate-job pairs | 60 | 60 |
| Successful results | 60 | 60 |
| Missing scores | 0 | 0 |
| Recorded errors | 0 | 0 |
| Minimum ATS score | 14.67 | 14.67 |
| Maximum ATS score | 90.22 | 90.22 |
| Average ATS score | 38.21 | 38.43 |

All 60 candidate-job pairs completed successfully in both runs. The average score increased by 0.22 points after the correction. This average change is descriptive, not an accuracy metric.

## 4. M.Sc. Degree-Matching Correction

The degree-matching logic did not previously recognize M.Sc. or MSc as a master's qualification. The master's-degree condition was updated to recognize both spellings.

### Verified example

Candidate: Arun Kumar  
Job profile: Data Scientist  
Education: M.Sc. Data Science  
Experience: 3 years

| Metric | Before fix | After fix |
|---|---:|---:|
| Education alignment | 60.00 | 80.00 |
| Degree score | 20.00 | 60.00 |
| Required-degree score | 0.00 | 50.00 |
| Education weighted contribution | 12.00 | 16.00 |
| Final ATS score | 62.79 | 66.79 |

Before the correction, the master's qualification was not matched. After the correction, the required master's degree was matched. The bachelor's requirement remained unmatched.

## 5. Candidate-Job Score Comparison

The comparison matched records using both resume ID and job ID.

| Comparison metric | Result |
|---|---:|
| Pairs compared | 60 |
| Scores changed | 4 |
| Scores unchanged | 56 |
| Total change across pairs | +13.34 points |

| Candidate | Job role | Before | After | Change |
|---|---|---:|---:|---:|
| Arun Kumar | Data Scientist | 62.79 | 66.79 | +4.00 |
| Arun Kumar | Software Engineer | 49.11 | 51.78 | +2.67 |
| Arun Kumar | Machine Learning Engineer | 48.81 | 51.48 | +2.67 |
| Arun Kumar | Business Analyst | 39.67 | 43.67 | +4.00 |

The other 56 candidate-job scores remained unchanged. The comparison confirms that the correction affected a limited subset of results rather than changing every score.

## 6. Validation and Reproducibility

The benchmark summaries contain 60 rows each, with no missing scores or recorded errors. The before-fix and after-fix outputs are retained separately to support comparison.

The M.Sc. correction also has a dedicated regression test in the ATS scoring test suite.

## 7. Limitations

- An ATS score is a rule-based ranking score, not a probability of being hired.
- Successful execution does not establish ranking accuracy.
- Precision, recall, and ranking-quality metrics require independently reviewed relevance labels or ground-truth judgments.
- A higher score after a correction demonstrates a change in scoring behavior, not necessarily improved real-world recruitment outcomes.
- A broader evaluation should review degree equivalence, required versus preferred qualifications, role-specific relevance, and potential fairness issues.

## 8. Conclusion

The Day 17 benchmark successfully evaluated 60 candidate-job pairs across 10 candidate resumes and 6 job profiles. All pairs produced scores without recorded errors or missing values. A targeted correction enabled M.Sc./MSc to match a master's-degree requirement, and the before-versus-after comparison found 4 changed scores and 56 unchanged scores.

The benchmark establishes execution completeness and provides regression evidence for the degree-matching fix. Further validation with independently reviewed candidate-job relevance labels is needed before making claims about ATS accuracy or hiring effectiveness.
