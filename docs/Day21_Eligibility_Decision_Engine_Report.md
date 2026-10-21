# Day 21 – Eligibility Decision Engine

## Objective
Automatically classify candidates for AI screening calls using ATS scores and recruiter-defined, role-specific rules.

## Implementation
- `eligibility/eligibility_engine.py` – decision logic and result structure.
- `eligibility/rules.json` – configurable eligibility thresholds and job rules.
- `eligibility/run_eligibility.py` – integration runner for existing ATS results.
- `eligibility/test_eligibility_engine.py` – automated tests.
- `eligibility/update_rules.py` – initializes role rules from existing JD profiles.
- `data/processed/eligibility_results/` – generated eligibility decisions.

## Configured Roles
1. Data Scientist
2. Software Engineer
3. Machine Learning Engineer
4. Data Analyst
5. HR Executive
6. Business Analyst

## Decision Rules
- **Eligible:** ATS score meets the eligible threshold and all configured checks pass.
- **Review:** score falls within the review range, relevant information is unknown, or role rules are unavailable.
- **Rejected:** ATS score is below the review threshold or a configured mandatory requirement fails.
- Confirmed failures take precedence over review flags.
- Unknown location and availability are flagged for review when configured, rather than automatically treated as failures.

Default thresholds:
- Eligible minimum: 70
- Review minimum: 50
- Rejected: below 50, subject to other confirmed rule failures also resulting in rejection.

Thresholds and checks can be configured per role in `eligibility/rules.json`.

## Candidate Decision Structure
Each saved JSON result includes:
- `candidate_id`
- `job_id`
- `role`
- `eligibility_status`
- `ats_score`
- `passed_checks`
- `failed_checks`
- `review_checks`
- `reasons`
- `decision_timestamp`
- `engine_version`

## Integration Verification
The integration runner successfully loaded the existing ATS result for `CAND_001` and `JOB_001`, along with the available skills and experience data.

Observed result:
- ATS score: 45.51
- Decision: Rejected
- Reasons include a score below the review threshold and mandatory skills not matched by the available ATS evidence.
- Missing location and availability were flagged for review.
- Output saved to `data/processed/eligibility_results/CAND_001_JOB_001_eligibility.json`.

This decision reflects the configured rules and current evidence; unmatched skills are not proof that a candidate definitively lacks those skills.

## Testing
- 8 core eligibility tests passed.
- 2 additional configuration validation tests passed.
- Total: 10 passing tests.

Command:
`python -m pytest .\eligibility -q`

## Deliverables Checklist
- [x] Eligibility decision engine
- [x] JSON rule configuration
- [x] Per-role thresholds and mandatory skills
- [x] Experience range checks
- [x] Location and availability review flags
- [x] ATS integration runner
- [x] Structured eligibility decision output
- [x] Automated tests
- [x] Six job roles configured
- [x] Completion report

## Limitations and Future Improvements
- Location and availability need to be supplied by candidate or recruiter data to evaluate them fully.
- Skill decisions depend on ATS matching evidence and should support recruiter review.
- The integration runner currently demonstrates one candidate-job pair; batch processing can be added later.
- Recruiters should review decisions before using them as the sole basis for hiring actions.

## Status
Day 21 implementation and initial verification completed.
