# Day 17 — Human Relevance Review Rubric

## 1. Purpose
Independently evaluate candidate-job relevance and compare human
judgments with the AI Job Portal ATS scores.

## 2. Sources of evidence
- Candidate resume text and documented experience.
- Job description responsibilities and required skills.
- Required education and experience, where specified.
- Relevant projects, certifications, and transferable skills.

Do not assign a label from the ATS score, candidate name, or resume
filename alone.

## 3. Human relevance labels

Relevant:
The resume provides sufficient evidence of alignment with the
job's core requirements, responsibilities, and required qualifications.

Not Relevant:
The resume lacks substantial evidence for the role's essential
requirements or is materially misaligned with the job.

Uncertain:
The available resume or job description does not provide enough
reliable evidence for a defensible decision. Record the reason and
resolve the case through a second review or adjudication before
including it in binary metrics.

## 4. Review procedure
For each candidate-job pair:
1. Read the actual resume.
2. Read the corresponding job description.
3. Compare essential skills, responsibilities, experience, and education.
4. Assign a human relevance label independently of the ATS score.
5. Record a concise evidence-based rationale.
6. Record any apparent ATS mismatch.
7. Change review_status to Completed only after the review is finished.

## 5. ATS decision bands
- Score >= 70: Shortlist.
- Score >= 50 and < 70: Review.
- Score < 50: Not Shortlisted.

These are operational workflow thresholds, not verified relevance labels.

For binary metrics, define ATS-predicted relevant as score >= 70
and ATS-predicted not relevant as score < 70. Preserve the Review
band for separate workflow analysis.

## 6. Job-profile consistency limitation
The structured job profiles and normalized job-description text
have known inconsistencies. Use the original job description text
as the review reference for this initial benchmark, and document
material conflicts in mismatch_notes. Do not silently change the
existing job profiles during evaluation.

## 7. Metrics
After the human labels are complete and uncertain cases are resolved:
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 * Precision * Recall / (Precision + Recall)

Also report the confusion matrix, reviewed-pair count, excluded or
uncertain count, and the number of cases in each ATS decision band.
If a denominator is zero, report the metric as undefined.

## 8. Limitations
This benchmark contains 60 candidate-job pairs from 10 resumes and
6 job profiles. Results describe this sample and should not be
presented as proof of general ATS accuracy.
