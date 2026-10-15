# Day 18: Performance and Stability Report

## 1. Objective

Day 18 focuses on production readiness for the AI Job Portal. The goals are to measure existing performance, investigate embedding throughput, improve resume-text normalization, and verify that changes preserve existing functionality.

## 2. Baseline Profiling

The baseline profiling script is located at:

`testing/day18/profile_baseline.py`

The recorded measurements are stored in:

`testing/day18/results/baseline.json`

The initial profiling run recorded the following results:

| Operation | Observed result |
|---|---:|
| DOCX extraction — resume 001 | 7.077 ms mean |
| DOCX extraction — resume 002 | 7.761 ms mean |
| PDF extraction — resume 003 | 44.436 ms mean |
| PDF extraction — resume 004 | 65.297 ms mean |
| Text normalization | Approximately 0.138–0.299 ms mean |
| Isolated ATS scoring without semantic result | 0.087 ms mean |
| Embedding model initialization | Approximately 7.38 seconds |

These measurements are specific to the tested environment and sample files. They are not universal performance guarantees.

The ATS scoring measurement excludes semantic embedding generation. Model initialization is reported separately from encoding time.

Memory usage was not measured because the profiling environment did not have `psutil` installed.

## 3. Batch Embedding Experiment

The experiment is implemented in:

`testing/day18/benchmark_batch_embeddings.py`

The validation results are stored in:

`testing/day18/results/batch_embedding_validation.json`

### Results

| Metric | Result |
|---|---:|
| Successful resume–job pairs | 24/24 |
| Component comparisons | 60 |
| Skipped empty components | 12 |
| Errors | 0 |
| Separate encoding mean | 26.025 ms |
| Batch encoding mean | 25.438 ms |
| Average measured speedup | 2.26% |
| Maximum component-score difference | 0.0000002384 |
| Maximum final-score difference | 0.0000001341 |

### Interpretation

Batch embedding produced a small average speed improvement in this experiment. The observed score differences were extremely small.

However, the measured speedup was only 2.26%. This result alone does not establish a meaningful production-level improvement across larger workloads or different hardware.

### Engineering decision

No production embedding implementation change was adopted based solely on this experiment. Further profiling with larger workloads would be needed before accepting additional complexity for performance gains.

## 4. Resume Text Normalization Improvement

The resume extractor is located at:

`src/resume_extractor.py`

The `normalize_bullets()` function was updated to normalize common bullet symbols, including the white-circle character (Unicode U+25CB), and en/em dash bullets into standard hyphens.

This makes the text-normalization behavior more consistent for resumes that use different bullet styles.

The existing DOCX/PDF extraction, cleaning, section-heading normalization, and special-character normalization functions were retained.

## 5. Regression Testing

A regression test was added to:

`src/test_extractor.py`

The test verifies that a white-circle bullet is converted to a standard hyphen.

### Validation results

| Test run | Result |
|---|---:|
| Targeted extractor tests | 6 passed |
| Full project regression suite | 164 passed |
| Full suite execution time | 45.32 seconds |

The previous full-suite baseline was 163 passing tests. The updated suite contains 164 passing tests after adding the new regression test.

These results demonstrate that the tested code passes the current regression suite. They do not, by themselves, prove the absence of all defects.

## 6. Stability and Limitations

- Existing DOCX and PDF extraction tests passed.
- The new bullet-normalization regression test passed.
- The full project test suite passed.
- Batch embedding was validated against 24 resume–job pairs.
- The observed batch-embedding speedup was modest.
- Memory usage was not measured.
- The profiling sample was small and should not be treated as a production-scale load test.
- No claim of a major production performance improvement is made.

## 7. Conclusion

Day 18 established a measured performance baseline, tested batch embedding against actual processed resume and job data, corrected a resume bullet-normalization edge case, and validated the project with 164 passing tests.

The batch experiment showed near-equivalent scores and a modest speed improvement, so the existing production embedding implementation was retained. The next performance improvements should be driven by repeatable profiling on representative workloads, with correctness and regression tests maintained throughout.
