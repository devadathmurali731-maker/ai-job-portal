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

## 9. Human-Reviewed Relevance Evaluation

### 9.1 Review Dataset

- Candidate resumes: 10
- Job profiles: 6
- Candidate-job pairs reviewed: 60
- Completed reviews: 60
- Pending reviews: 0
- Missing relevance labels: 0

Each candidate-job pair received a binary human relevance label: Relevant or Not Relevant. The review rationale and mismatch notes document the evidence supporting each judgment.

### 9.2 Evaluation Method

For binary evaluation, the ATS score was converted into a prediction using a fixed threshold:

- ATS score >= 70: Predicted Relevant
- ATS score < 70: Predicted Not Relevant

The predicted label was compared with the human relevance label. The existing ATS decision bands (Shortlist, Review, and Not Shortlisted) remain separate from this binary evaluation rule.

### 9.3 Confusion Matrix

| Outcome | Count |
|---|---:|
| True Positives (TP) | 5 |
| False Positives (FP) | 0 |
| True Negatives (TN) | 44 |
| False Negatives (FN) | 11 |
| Total | 60 |

### 9.4 Classification Metrics

| Metric | Result |
|---|---:|
| Accuracy | 81.67% |
| Precision | 100.00% |
| Recall | 31.25% |
| F1 Score | 47.62% |

Definitions:

- Accuracy = (TP + TN) / Total
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 Score = 2 × Precision × Recall / (Precision + Recall)

### 9.5 Interpretation

The ATS correctly classified 49 of the 60 candidate-job pairs at the threshold of 70, producing an accuracy of 81.67%.

Precision was 100.00% because none of the five pairs predicted as Relevant was labelled Not Relevant by the reviewer. However, recall was 31.25%: the ATS identified 5 of the 16 human-labelled relevant pairs and missed 11.

The results suggest that the current threshold is conservative on this sample. The high accuracy must be interpreted alongside recall and the distribution of labels: 16 pairs were labelled Relevant and 44 were labelled Not Relevant.

### 9.6 Limitations and Threats to Validity

- Human relevance labels involve judgment and may differ between reviewers.
- The review CSV contains ATS scores, so this review process was not a fully blinded assessment. Future evaluations should hide ATS scores and predictions from reviewers until labels are finalized.
- The benchmark contains 60 pairs drawn from only 10 resumes and 6 job profiles. It is a limited evaluation sample and may not represent real-world recruitment data.
- The fixed threshold of 70 is an evaluation rule, not a validated optimal threshold.
- Accuracy, precision, recall, and F1 measure binary classification against the current labels; they do not directly evaluate ranking quality, fairness, or hiring outcomes.
- The results should not be generalized to all candidates or job markets without a larger, independently reviewed test set.

### 9.7 Recommended Next Steps

1. Conduct a blinded review of candidate-job pairs without displaying ATS scores or decisions.
2. Have a second reviewer assess a subset of pairs and resolve disagreements using a documented rubric.
3. Investigate the 11 false negatives to identify relevant candidates receiving scores below 70.
4. Evaluate alternative thresholds on a development set, then confirm the selected threshold on a separate held-out set.
5. Report ranking metrics such as Precision@K or NDCG only after defining an appropriate ranked-candidate evaluation protocol.
6. Retain the human-review CSV, benchmark outputs, and evaluation script for reproducibility.

### 9.8 Human-Review Evaluation Conclusion

The completed review provides an initial relevance-based evaluation of the ATS across 60 candidate-job pairs. At a score threshold of 70, the system achieved 81.67% accuracy, 100.00% precision, 31.25% recall, and a 47.62% F1 score against the current human labels.

The principal observed limitation is low recall, with 11 human-labelled relevant pairs missed by the threshold. These findings are preliminary and should be validated through blinded, multi-reviewer assessment and a broader test set before making claims about real-world ATS performance.


