Absolutely. Below is a **professional, portfolio-ready Markdown report** that accurately documents what you implemented in Day 12 without overstating the validation results.

Replace the contents of:

`docs/Semantic_Matching_Accuracy_Report.md`

with this:

# Semantic Matching Accuracy Report

## 1. Overview

The Semantic Matching Engine is a core component of the AI Job Portal project. Its purpose is to compare candidate resumes with job descriptions using **semantic similarity rather than relying only on exact keyword matching**.

Traditional keyword matching may fail when a resume and job description express similar concepts using different words. The semantic matching engine addresses this limitation by converting text into numerical embedding vectors and measuring the semantic similarity between them.

The engine evaluates multiple resume and job-description components, including:

* Skills
* Professional experience
* Projects, when comparable project information is available

The resulting component-level similarities are combined into a weighted semantic matching score.

---

## 2. Objective

The objectives of the semantic matching module are to:

1. Convert resume and job-description text into semantic embeddings.
2. Measure semantic similarity between resume and job-description content.
3. Perform component-level matching.
4. Calculate a weighted overall semantic similarity score.
5. Validate the matching engine across multiple resume and job combinations.
6. Evaluate different similarity thresholds.
7. Measure classification performance using:

   * Accuracy
   * Precision
   * Recall
8. Identify an appropriate threshold range for further validation.

---

## 3. Semantic Matching Architecture

The semantic matching pipeline is structured as follows:

```text
                    RESUME
                       |
                       v
              Processed Resume Data
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
      Skills       Experience       Projects
        |              |              |
        +--------------+--------------+
                       |
                       v
              Embedding Engine
                       |
                       v
             Semantic Embeddings
                       |
                       |
                       |       JOB DESCRIPTION
                       |              |
                       |              v
                       |       Structured JD Data
                       |              |
                       |      +-------+-------+
                       |      |       |       |
                       |      v       v       v
                       |    Skills Experience Projects
                       |      |       |       |
                       |      +-------+-------+
                       |              |
                       |              v
                       |       Embedding Engine
                       |              |
                       |              v
                       |       Semantic Embeddings
                       |              |
                       +--------------+
                                      |
                                      v
                              Cosine Similarity
                                      |
                                      v
                           Component Similarities
                                      |
                                      v
                            Weighted Score
                                      |
                                      v
                            Threshold Analysis
                                      |
                                      v
                         Accuracy / Precision /
                                Recall
```

---

## 4. Technologies Used

The implementation uses the following technologies and libraries:

| Technology            | Purpose                       |
| --------------------- | ----------------------------- |
| Python                | Core implementation           |
| Sentence Transformers | Semantic text embeddings      |
| `all-MiniLM-L6-v2`    | Pre-trained embedding model   |
| NumPy                 | Numerical vector operations   |
| scikit-learn          | Cosine similarity calculation |
| JSON                  | Processed data storage        |
| pytest                | Automated testing             |

---

## 5. Embedding Model

The semantic matching engine uses the following Sentence Transformers model:

```text
all-MiniLM-L6-v2
```

The model converts text into a **384-dimensional numerical vector**.

For example:

```text
Resume Text
     |
     v
Sentence Transformer
     |
     v
384-dimensional embedding
```

The same process is applied to job-description text.

The resulting vectors can then be compared mathematically.

---

## 6. Similarity Measurement

The engine uses **cosine similarity** to measure the similarity between two embedding vectors.

Cosine similarity measures the angle between two vectors rather than their absolute magnitude.

The general formula is:

```text
Cosine Similarity =
(A · B) / (||A|| × ||B||)
```

The resulting value is used as the semantic similarity score.

Higher values indicate greater semantic similarity between the compared text representations.

The similarity score is **not a percentage of candidate qualification**. It is a model-specific similarity measurement.

---

## 7. Component-Level Matching

The engine performs semantic matching at the component level.

### 7.1 Skills Matching

The candidate's extracted skills are compared with the skills specified in the job description.

Example:

```text
Resume:
Python, SQL, Docker, Git, Java

JD:
Python, SQL, Machine Learning, Docker, AWS
```

The embedding model evaluates the semantic relationship between the two skill collections.

---

### 7.2 Experience Matching

The candidate's professional experience and responsibilities are compared with the experience requirements of the job description.

The comparison considers the semantic relationship between the available experience descriptions rather than requiring exact phrase matches.

---

### 7.3 Project Matching

Project matching is performed only when comparable project information is available.

If project information is unavailable on one side, the project component is excluded from the weighted calculation rather than artificially assigning a score.

This prevents missing information from being treated as poor project performance.

---

## 8. Weighted Semantic Score

The current semantic matching engine uses the following default component weights:

| Component  | Weight |
| ---------- | -----: |
| Skills     |    50% |
| Experience |    30% |
| Projects   |    20% |

The weighted score is calculated using the available components.

When a component is unavailable, the remaining component weights are **renormalized**.

For example, if project information is unavailable:

```text
Original weights:

Skills      = 0.50
Experience  = 0.30
Projects    = 0.20

Available:

Skills      = 0.50
Experience  = 0.30

Total available weight = 0.80
```

The normalized weights become:

```text
Skills      = 0.50 / 0.80 = 0.625
Experience  = 0.30 / 0.80 = 0.375
```

Therefore:

```text
Final Score =
(Skills Score × 0.625)
+
(Experience Score × 0.375)
```

This allows the engine to handle incomplete resume information without automatically treating missing components as zero similarity.

---

## 9. Example Semantic Matching Result

An example comparison between `resume_001` and `jd_001_data_scientist` produced:

| Component            |    Similarity |
| -------------------- | ------------: |
| Skills               |        0.6520 |
| Experience           |        0.3412 |
| Projects             | Not available |
| Final Semantic Score |        0.5354 |

The project component was excluded because the resume did not contain a project section.

The final score was calculated using the normalized weights for the available components.

```text
Final Score
=
(0.6520 × 0.625)
+
(0.3412 × 0.375)

= 0.5354
```

The value `0.5354` represents semantic similarity according to the implemented model. It should **not** be interpreted as the candidate having a 53.54% probability of being qualified.

---

# 10. Multi-Job Validation

To evaluate the engine across multiple job types, four processed resumes were compared against six job descriptions.

This produced:

```text
4 resumes × 6 job descriptions = 24 comparisons
```

The job descriptions represented different roles:

* Data Scientist
* Software Engineer
* Machine Learning Engineer
* Data Analyst
* HR Executive
* Business Analyst

This provided a small cross-role validation set for examining how the semantic scoring system behaves across different candidate-role combinations.

---

## 11. Multi-Job Semantic Scores

The generated semantic scores were:

| Resume     | Job Description   | Semantic Score |
| ---------- | ----------------- | -------------: |
| resume_001 | Data Scientist    |         0.5354 |
| resume_001 | Software Engineer |         0.6520 |
| resume_001 | ML Engineer       |         0.5098 |
| resume_001 | Data Analyst      |         0.5218 |
| resume_001 | HR Executive      |         0.3051 |
| resume_001 | Business Analyst  |         0.3423 |
| resume_002 | Data Scientist    |         0.5196 |
| resume_002 | Software Engineer |         0.4208 |
| resume_002 | ML Engineer       |         0.4040 |
| resume_002 | Data Analyst      |         0.7144 |
| resume_002 | HR Executive      |         0.3828 |
| resume_002 | Business Analyst  |         0.5812 |
| resume_003 | Data Scientist    |         0.6363 |
| resume_003 | Software Engineer |         0.3789 |
| resume_003 | ML Engineer       |         0.6262 |
| resume_003 | Data Analyst      |         0.5332 |
| resume_003 | HR Executive      |         0.2436 |
| resume_003 | Business Analyst  |         0.2664 |
| resume_004 | Data Scientist    |         0.4303 |
| resume_004 | Software Engineer |         0.4003 |
| resume_004 | ML Engineer       |         0.3312 |
| resume_004 | Data Analyst      |         0.6291 |
| resume_004 | HR Executive      |         0.3169 |
| resume_004 | Business Analyst  |         0.5192 |

---

## 12. Validation Dataset Statistics

Across the 24 resume-JD comparisons:

| Metric            | Result |
| ----------------- | -----: |
| Total comparisons |     24 |
| Minimum score     | 0.2436 |
| Maximum score     | 0.7144 |
| Average score     | 0.4667 |

The observed scores demonstrate that the model produces different similarity levels across different resume-job combinations.

---

# 13. Threshold Evaluation

A similarity threshold is required to convert the continuous semantic score into a binary classification:

```text
Score >= threshold
        |
        +----> Match
```

```text
Score < threshold
        |
        +----> No Match
```

Multiple thresholds were evaluated rather than selecting a threshold arbitrarily.

The tested thresholds were:

```text
0.30
0.35
0.40
0.45
0.50
0.55
0.60
0.65
0.70
```

---

## 14. Threshold Performance

The following results were obtained on the project's current validation set:

| Threshold | Accuracy | Precision |  Recall |
| --------: | -------: | --------: | ------: |
|      0.30 |   50.00% |    45.45% | 100.00% |
|      0.35 |   66.67% |    55.56% | 100.00% |
|      0.40 |   75.00% |    62.50% | 100.00% |
|      0.45 |   91.67% |    83.33% | 100.00% |
|      0.50 |   91.67% |    83.33% | 100.00% |
|      0.55 |   83.33% |   100.00% |  60.00% |
|      0.60 |   79.17% |   100.00% |  50.00% |
|      0.65 |   66.67% |   100.00% |  20.00% |
|      0.70 |   62.50% |   100.00% |  10.00% |

---

## 15. Threshold Analysis

The results demonstrate a clear precision-recall trade-off.

At lower thresholds, the system classifies more resume-JD pairs as matches. This maintains high recall but also increases the number of false positives.

For example:

```text
Threshold = 0.40

Precision = 62.50%
Recall    = 100.00%
```

At higher thresholds, the system becomes more selective.

For example:

```text
Threshold = 0.60

Precision = 100.00%
Recall    = 50.00%
```

At a threshold of `0.70`, recall falls to `10.00%`, indicating that the system is highly restrictive at this threshold on the current validation set.

---

## 16. Observed Threshold Range

Thresholds of `0.45` and `0.50` produced identical observed results on the current validation set:

```text
Accuracy  = 91.67%
Precision = 83.33%
Recall    = 100.00%
```

Therefore, both thresholds represent useful candidate operating points for further validation.

However, these results should not be interpreted as evidence that either threshold is universally optimal.

The current validation dataset contains only 24 comparisons, and the validation labels were manually defined for this project rather than obtained from a large, independently human-labeled recruitment dataset.

A production threshold should therefore be selected only after validation on a substantially larger and independently labeled dataset.

---

# 17. Validation Label Methodology

The threshold experiment required binary labels indicating whether each resume-JD pair was considered a semantic match for evaluation purposes.

The labels used in this project are **project-defined validation labels** based on the roles and content represented in the sample resumes and job descriptions.

They are intended to test the behavior of the matching pipeline.

They should not be interpreted as:

* Verified hiring decisions
* Recruiter judgments
* Industry-standard labels
* Statistically representative hiring outcomes
* Ground truth for real-world recruitment

This distinction is important when interpreting the reported performance metrics.

---

# 18. Performance Metrics

The following classification metrics were used.

### Accuracy

Accuracy measures the proportion of correctly classified resume-JD pairs.

```text
Accuracy =
(TP + TN) / (TP + TN + FP + FN)
```

Where:

* TP = True Positive
* TN = True Negative
* FP = False Positive
* FN = False Negative

---

### Precision

Precision measures how many predicted matches were actually labeled as matches.

```text
Precision =
TP / (TP + FP)
```

Higher precision means fewer false positive matches.

---

### Recall

Recall measures how many of the labeled matching pairs were successfully identified.

```text
Recall =
TP / (TP + FN)
```

Higher recall means fewer potential matching pairs are missed.

---

# 19. Test Coverage

The semantic matching implementation was developed with automated tests covering the major components.

Testing includes:

* Embedding engine initialization
* Single-text embedding generation
* Multiple-text embedding generation
* Input validation
* Cosine similarity calculation
* Similarity validation
* Basic semantic matching
* Component-level matching
* Missing project handling
* Weighted score calculation
* Real processed resume-JD matching
* Multi-component matching behavior

The semantic matching module was tested independently before being integrated with the broader project pipeline.

---

# 20. Key Findings

The current implementation demonstrates that the AI Job Portal can:

1. Convert natural-language resume and job-description content into semantic embeddings.
2. Compare resume and job-description components using cosine similarity.
3. Produce component-level semantic scores.
4. Combine component scores into a weighted semantic score.
5. Handle missing project information without automatically assigning a zero score.
6. Evaluate multiple resume-JD combinations.
7. Test different similarity thresholds.
8. Measure classification performance using accuracy, precision, and recall.

The threshold experiment also demonstrates the expected trade-off between precision and recall as the similarity threshold changes.

---

# 21. Limitations

The current implementation has several limitations.

### 21.1 Small Validation Dataset

Only 24 resume-JD comparisons were used.

This is sufficient for demonstrating the pipeline but is not sufficient to establish production-level model performance.

---

### 21.2 Project-Defined Labels

The validation labels were created specifically for testing this project.

They are not independently verified recruitment ground truth.

---

### 21.3 Limited Job Descriptions

Only six sample job descriptions are currently available.

A larger dataset containing more industries, seniority levels, job families, and writing styles would provide stronger validation.

---

### 21.4 Experience Representation

The current semantic experience representation primarily uses the structured experience information available from the processed data.

Future versions can incorporate richer job-description responsibility and domain-context information.

---

### 21.5 Project Representation

Project matching is currently dependent on the availability of genuine project information.

Job descriptions do not currently contain a dedicated structured project field, so project similarity should only be calculated when comparable project information is explicitly available.

---

### 21.6 Embedding Model

The current implementation uses:

```text
all-MiniLM-L6-v2
```

Other embedding models may produce different similarity distributions and may perform differently on recruitment-specific text.

---

# 22. Future Improvements

Potential improvements include:

### Data Improvements

* Collect a larger resume-JD dataset.
* Add recruiter- or expert-labeled matching data.
* Include multiple industries.
* Include different experience levels.
* Include more job descriptions per role.
* Add difficult negative examples.

### Model Improvements

* Evaluate alternative embedding models.
* Compare domain-specific embedding models.
* Experiment with fine-tuned sentence-transformer models.
* Evaluate cross-encoder architectures for higher-precision pairwise matching.

### Matching Improvements

* Improve JD responsibility extraction.
* Improve project-specific extraction.
* Incorporate education relevance.
* Incorporate experience duration.
* Incorporate required versus preferred skills separately.
* Combine semantic similarity with structured ATS features.

### Evaluation Improvements

* Increase the validation dataset size.
* Use independent human annotations.
* Calculate F1-score.
* Analyze confusion matrices.
* Evaluate performance by job category.
* Perform cross-validation where sufficient labeled data is available.
* Monitor false-positive and false-negative cases.

---

# 23. Recommended Future Architecture

A future production-oriented matching architecture could combine multiple signals:

```text
                    Resume
                       |
        +--------------+--------------+
        |              |              |
      Skills       Experience       Education
        |              |              |
        v              v              v
   Structured       Semantic       Structured
    Matching        Matching        Matching
        |              |              |
        +--------------+--------------+
                       |
                       v
              Semantic Similarity
                       |
                       v
               Weighted Scoring
                       |
                       v
              Business Rules /
              Eligibility Rules
                       |
                       v
                 Final ATS Score
                       |
                       v
              Candidate Ranking
```

This hybrid architecture would combine the strengths of:

* Rule-based matching
* Structured feature matching
* Semantic similarity
* Business-specific recruitment rules

---

# 24. Conclusion

The Semantic Matching Engine successfully extends the AI Job Portal beyond simple keyword matching by introducing embedding-based semantic comparison.

The implementation currently supports:

```text
Resume
   ↓
Processed Components
   ↓
Embeddings
   ↓
Cosine Similarity
   ↓
Component Scores
   ↓
Weighted Semantic Score
   ↓
Threshold Classification
   ↓
Performance Evaluation
```

The current validation experiment produced an observed maximum accuracy of **91.67%** at thresholds `0.45` and `0.50`, with **83.33% precision** and **100% recall** on the project's 24-pair validation set.

These results demonstrate the functionality and behavior of the implemented semantic matching pipeline, but they should **not be interpreted as production-level recruitment accuracy** because the validation dataset is small and its labels are project-defined.

Further evaluation using a larger, independently human-labeled resume-JD dataset is required before making claims about real-world recruitment performance or selecting a production threshold.

---

## 25. Project Artifacts

The main semantic matching artifacts include:

```text
semantic_matching/
│
├── embedding_engine.py
├── similarity_scorer.py
├── semantic_matcher.py
├── component_matcher.py
├── data_component_extractor.py
├── semantic_match_engine.py
├── threshold_tuning.py
├── validate_multiple_jobs.py
├── analyze_validation_results.py
│
├── test_embedding_engine.py
├── test_similarity_scorer.py
├── test_semantic_matcher.py
├── test_component_matcher.py
└── test_semantic_match_engine.py
```

Generated validation data:

```text
data/
└── processed/
    └── semantic_matching/
        └── multi_job_validation.json
```

Threshold analysis:

```text
outputs/
└── semantic_matching/
    └── threshold_analysis.json
```

Documentation:

```text
docs/
└── Semantic_Matching_Accuracy_Report.md
```

---

## 26. Final Status

**Semantic Matching Engine: Completed**

The Day 12 implementation successfully adds semantic resume-to-job matching capabilities to the AI Job Portal and provides an initial framework for evaluating similarity thresholds and matching performance.

The implementation is ready for integration with subsequent ATS and candidate-ranking components after further validation and refinement.
