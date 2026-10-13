# ATS API Input and Output Schemas

## 1. Purpose

This document defines the proposed request and response schemas for the AI Job Portal REST API.

The schemas establish the expected structure, field types, validation rules, and response formats for resume upload, resume parsing, candidate scoring, ranking, shortlisting, and asynchronous task tracking.

These schemas are API design contracts. They do not imply that the corresponding HTTP endpoints, task infrastructure, or API middleware have already been implemented.

## 2. Common Conventions

### 2.1 Data Format

JSON is the default format for API request and response bodies. Resume uploads use `multipart/form-data`.

### 2.2 Identifier Format

Identifiers are represented as strings.

Examples:

- `RESUME_001`
- `CAND_001`
- `JOB_001`
- `TASK_001`
- `REQ_001`

These examples are illustrative. The implementation must define how identifiers are generated, how external identifiers map to internal project identifiers, and how uniqueness is enforced.

### 2.3 Numeric Scores

Final ATS scores and normalized component scores must be numeric values between 0 and 100 when the component's documented scale is 0–100.

Raw similarity values may use a range of 0–1. The API must preserve the distinction between raw similarity values, normalized component scores, and the final ATS score.

The API must not silently rescale component scores unless that behavior is explicitly documented.

### 2.4 Timestamp Format

Timestamps should use ISO 8601 format with an explicit timezone, preferably UTC.

Example:

`2026-10-13T04:00:00Z`

### 2.5 Asynchronous Operations

Asynchronous submission responses indicate that a task has been accepted, not that processing has completed successfully.

The proposed task states are:

- `queued`
- `running`
- `completed`
- `failed`

The task-status endpoint may return HTTP `200 OK` when it successfully retrieves a task whose processing state is `failed`.

## 3. Resume Upload Request Schema

### Endpoint

`POST /api/v1/resumes`

### Content Type

`multipart/form-data`

### Request Fields

| Field | Type | Required | Validation |
|---|---|---|---|
| `file` | File | Yes | Must be a supported resume document |
| `metadata` | JSON object or string | No | Supported only if a metadata contract is defined |

The initial implementation should support only explicitly configured file types and enforce a maximum upload size.

### Success Response

HTTP status: `201 Created`

```json
{
  "resume_id": "RESUME_001",
  "status": "uploaded",
  "message": "Resume uploaded successfully."
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `resume_id` | String | Identifier assigned to the uploaded resume |
| `status` | String | Upload processing state |
| `message` | String | Human-readable confirmation |

A successful upload does not mean that resume parsing or ATS scoring has succeeded.

The implementation must define how `resume_id` maps to the internal resume files and identifiers used by the existing processing modules.

## 4. Resume Parsing Request Schema

### Endpoint

`POST /api/v1/resumes/{resume_id}/parse`

### Request Body

No body is required in the initial contract. The resume identifier is supplied in the path.

### Validation Rules

- `resume_id` must be a valid identifier.
- The referenced resume must exist.
- The uploaded file must be available for processing.
- Duplicate parsing requests must follow a documented conflict or idempotency policy.

### Accepted Response

HTTP status: `202 Accepted`

```json
{
  "task_id": "TASK_001",
  "resume_id": "RESUME_001",
  "status": "queued",
  "message": "Resume parsing has been queued."
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `task_id` | String | Identifier for the asynchronous task |
| `resume_id` | String | Resume being processed |
| `status` | String | Current task state |
| `message` | String | Human-readable status message |

The queued state means the task has been accepted for processing. It does not guarantee successful parsing.

## 5. Resume Parsing Result Schema

A completed parsing task should return structured resume information using the existing extraction and parsing modules.

### Illustrative Result

```json
{
  "resume_id": "RESUME_001",
  "status": "completed",
  "result": {
    "skills": [
      "python",
      "sql",
      "machine learning"
    ],
    "education": [],
    "work_experience": [],
    "projects": [],
    "certifications": []
  }
}
```

### Schema Rules

- `resume_id` is a string.
- `status` is a task state.
- `result` is an object containing the parsed resume representation.
- Collection fields must use consistent array structures.
- Missing or unavailable information must be represented consistently according to the parsing contract.

The example is illustrative. The final field structure must be aligned with the actual output of the existing resume-processing pipeline. It must not be treated as a claim that every parser currently returns exactly these fields.

## 6. Candidate Scoring Request Schema

### Endpoint

`POST /api/v1/jobs/{job_id}/score`

### Request Body

```json
{
  "resume_id": "RESUME_001"
}
```

### Validation Rules

- `job_id` must refer to an available job description.
- `resume_id` must refer to an uploaded and sufficiently processed resume.
- The required skills, experience, education, and job-description JSON inputs must be available.
- The semantic-matching lookup must be loaded or resolved as required by the scoring workflow.
- Candidate and job identifiers must resolve to the intended candidate-job pair.
- Missing scoring components must follow the existing scoring engine's availability and weight-redistribution rules.

### Accepted Response

HTTP status: `202 Accepted`

```json
{
  "task_id": "TASK_002",
  "resume_id": "RESUME_001",
  "job_id": "JOB_001",
  "status": "queued"
}
```

The response confirms task acceptance only. The final score must be retrieved through the completed task result or the documented scoring-result retrieval contract.

## 7. Candidate Scoring Result Schema

The completed scoring result must reflect the output of the existing ATS v2 scoring engine.

### Illustrative Result

```json
{
  "candidate_id": "CAND_001",
  "job_id": "JOB_001",
  "role": "Data Scientist",
  "component_scores": {
    "skill_match": 23.3333,
    "experience_relevance": 53.9286,
    "education_alignment": 80.0,
    "semantic_similarity": 53.54455
  },
  "original_weights": {
    "skill_match": 0.4,
    "experience_relevance": 0.2,
    "education_alignment": 0.15,
    "semantic_similarity": 0.25
  },
  "adjusted_weights": {
    "skill_match": 0.4,
    "experience_relevance": 0.2,
    "education_alignment": 0.15,
    "semantic_similarity": 0.25
  },
  "weighted_contributions": {
    "skill_match": 9.3333,
    "experience_relevance": 10.7857,
    "education_alignment": 12.0,
    "semantic_similarity": 13.3861
  },
  "final_ats_score": 45.51,
  "available_components": [
    "skill_match",
    "experience_relevance",
    "education_alignment",
    "semantic_similarity"
  ],
  "missing_components": [],
  "component_details": {
    "skill_match": {},
    "experience_relevance": {},
    "education_alignment": {},
    "semantic_similarity": {}
  }
}
```

The component detail objects above are abbreviated for readability. Actual values must come from the scoring engine.

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `candidate_id` | String | Candidate identifier used by the scoring pipeline |
| `job_id` | String | Job identifier used by the scoring pipeline |
| `role` | String | Job role associated with the score |
| `component_scores` | Object | Scores calculated for individual components |
| `original_weights` | Object | Configured component weights before redistribution |
| `adjusted_weights` | Object | Component weights after availability handling |
| `weighted_contributions` | Object | Weighted contribution of each component |
| `final_ats_score` | Number | Final combined ATS score |
| `available_components` | Array of strings | Components available for scoring |
| `missing_components` | Array of strings | Components unavailable for scoring |
| `component_details` | Object | Detailed component-level calculation information |

### Validation Rules

- `final_ats_score` must be numeric and within 0–100.
- Component scores must follow their documented scales.
- Weights and weighted contributions must reflect the scoring engine's calculation.
- Missing components must follow the existing weight-redistribution logic.
- The API must preserve the distinction between the final score and its contributing components.
- The result must retain the candidate and job identifiers used for the calculation.

### Score Field Compatibility

The ATS v2 scoring output uses `final_ats_score`.

The candidate-ranking output uses `ats_score`.

Legacy ATS v1 output may also use `ats_score`, but its schema and calculation may differ from v2. The API must identify the relevant version and must not treat these fields as interchangeable without an explicit mapping.

### Persistence Requirement

The existing scoring generator returns a result dictionary and saves a JSON output file.

The API implementation must handle both calculation and persistence. A scoring task must not be reported as completed if the required output cannot be saved successfully.

## 8. Candidate Ranking Response Schema

### Endpoint

`GET /api/v1/jobs/{job_id}/rankings`

### Proposed Response

```json
{
  "job_id": "JOB_001",
  "role": "Data Scientist",
  "candidate_count": 4,
  "decision_summary": {
    "SHORTLIST": 0,
    "REVIEW": 2,
    "REJECT": 2
  },
  "ranked_candidates": [
    {
      "rank": 1,
      "candidate_id": "CAND_003",
      "job_id": "JOB_001",
      "role": "Data Scientist",
      "ats_score": 68.53,
      "component_scores": {
        "skill_match": 40.0,
        "experience_relevance": 75.0,
        "education_alignment": 80.0,
        "semantic_similarity": 70.0
      },
      "decision": "REVIEW",
      "decision_reason": "Illustrative reason from the ranking pipeline"
    }
  ]
}
```

The example illustrates the structure. The candidate component values and decision reason are placeholders and must be taken from actual ranking output when returning real results.

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `job_id` | String | Job for which ranking was generated |
| `role` | String | Role associated with the ranking |
| `candidate_count` | Integer | Number of candidates included in the ranking |
| `decision_summary` | Object | Counts of shortlisted, review, and rejected candidates |
| `ranked_candidates` | Array | Candidates ranked for the job |
| `rank` | Integer | Position within the job-specific ranking |
| `candidate_id` | String | Candidate identifier |
| `ats_score` | Number | Final ATS score as represented in the ranking output |
| `component_scores` | Object | Component scores carried into the ranking output |
| `decision` | String | Shortlisting decision |
| `decision_reason` | String | Explanation produced by the shortlisting pipeline |

The existing ranking output includes `job_id`, `role`, `candidate_count`, `decision_summary`, and `ranked_candidates`. Individual candidate entries can include rank, identifiers, score, component scores, decision, and decision reason.

Candidates must be ranked within the relevant job rather than compared across unrelated roles by default.

The API must reuse the existing ranking and shortlisting pipeline rather than independently reimplementing ranking rules.

## 9. Shortlisting Request Schema

### Endpoint

`POST /api/v1/jobs/{job_id}/shortlist`

### Request Body

No threshold field is required for the initial API version.

The API must use the existing backend configuration:

- `SHORTLIST_THRESHOLD = 70.0`
- `REVIEW_THRESHOLD = 50.0`

### Decision Rules

| Score | Decision |
|---|---|
| Score greater than or equal to 70 | `SHORTLIST` |
| Score greater than or equal to 50 and below 70 | `REVIEW` |
| Score below 50 | `REJECT` |

Scores must be numeric values within 0–100.

### Validation Rules

- `job_id` must refer to a valid job.
- The required ranking or scoring results must be available.
- The existing configured thresholds must be applied consistently.
- The API must not introduce a separate threshold that conflicts with backend configuration.
- Each decision must retain the score and decision reason used by the existing pipeline.

The initial contract does not allow callers to override the configured thresholds. Any future threshold customization must be separately designed, authorized, validated, and documented.

## 10. Shortlisting Response Schema

### Proposed Response

```json
{
  "job_id": "JOB_001",
  "status": "completed",
  "shortlisted_count": 0,
  "review_count": 2,
  "rejected_count": 2
}
```

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `job_id` | String | Job associated with the decisions |
| `status` | String | Operation status |
| `shortlisted_count` | Integer | Number of shortlisted candidates |
| `review_count` | Integer | Number of candidates requiring review |
| `rejected_count` | Integer | Number of rejected candidates |

The counts are illustrative. Actual values must come from the existing shortlisting pipeline.

The response must accurately represent the decisions for the requested job. The implementation must define whether the endpoint generates rankings before applying shortlisting or operates on an existing ranking result.

## 11. Asynchronous Task Schema

### Endpoint

`GET /api/v1/tasks/{task_id}`

### Running Task Response

```json
{
  "task_id": "TASK_001",
  "task_type": "resume_parsing",
  "status": "running",
  "created_at": "2026-10-13T04:00:00Z",
  "updated_at": "2026-10-13T04:00:05Z",
  "result": null,
  "error": null
}
```

### Completed Task Response

```json
{
  "task_id": "TASK_001",
  "task_type": "resume_parsing",
  "status": "completed",
  "created_at": "2026-10-13T04:00:00Z",
  "updated_at": "2026-10-13T04:00:10Z",
  "result": {
    "resume_id": "RESUME_001"
  },
  "error": null
}
```

The completed result shown here is illustrative. The actual `result` must follow the output contract for the relevant task type.

### Failed Task Response

```json
{
  "task_id": "TASK_001",
  "task_type": "resume_parsing",
  "status": "failed",
  "created_at": "2026-10-13T04:00:00Z",
  "updated_at": "2026-10-13T04:00:10Z",
  "result": null,
  "error": {
    "code": "RESUME_PARSING_FAILED",
    "message": "The resume could not be processed.",
    "request_id": "REQ_001"
  }
}
```

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `task_id` | String | Unique task identifier |
| `task_type` | String | Type of operation being executed |
| `status` | String | Current task state |
| `created_at` | String | Task creation timestamp |
| `updated_at` | String | Most recent task update timestamp |
| `result` | Object or null | Task-specific result when completed |
| `error` | Object or null | Safe error information when failed |

### Task State Rules

The proposed states are:

- `queued`
- `running`
- `completed`
- `failed`

While a task is queued or running, `result` should be `null`. A completed task should contain its task-specific result and have `error` set to `null`. A failed task should have `result` set to `null` and contain a structured error.

The implementation must define retry behavior, timeout handling, task expiration, duplicate request handling, idempotency, and task persistence before asynchronous processing is deployed.

A task-status request that successfully retrieves a failed task should normally return HTTP `200 OK`. A nonexistent task should return `404 Not Found`.

## 12. Standard Error Schema

All API errors should use a consistent structure.

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request could not be processed.",
    "details": null,
    "request_id": "REQ_001"
  }
}
```

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `code` | String | Stable machine-readable error identifier |
| `message` | String | Safe human-readable explanation |
| `details` | Object, array, or null | Safe additional validation information |
| `request_id` | String | Identifier for tracing the request in logs |

The API must not return internal stack traces, secrets, filesystem paths, or sensitive resume content in error responses.

Proposed error codes include:

- `INVALID_REQUEST`
- `MISSING_REQUIRED_FIELD`
- `INVALID_IDENTIFIER`
- `INVALID_SCORE_RANGE`
- `RESUME_NOT_FOUND`
- `INVALID_RESUME_FORMAT`
- `RESUME_TOO_LARGE`
- `RESUME_PARSING_FAILED`
- `JOB_NOT_FOUND`
- `RESUME_NOT_READY`
- `SCORING_FAILED`
- `RANKING_FAILED`
- `SHORTLISTING_FAILED`
- `TASK_NOT_FOUND`
- `STORAGE_UNAVAILABLE`
- `PROCESSING_SERVICE_UNAVAILABLE`
- `INTERNAL_ERROR`

The implementation must map internal exceptions to stable public error codes and safe messages.

## 13. Schema Validation Requirements

The API implementation should validate requests before invoking the existing ATS engines.

Validation must cover:

- Required fields.
- Data types.
- Allowed identifier formats.
- File types and file size.
- Numeric score ranges.
- Supported task states.
- Existence of referenced resumes and jobs.
- Availability of required scoring inputs.
- Consistency between request identifiers and stored resources.
- Safe error response structure.

Invalid requests must return standardized errors and must not initiate downstream processing.

## 14. Compatibility with Existing ATS Modules

The API layer should act as an adapter around the existing project components:

- Resume extraction and structured parsing.
- Skill extraction.
- Experience and education processing.
- Semantic matching.
- ATS scoring.
- Candidate ranking.
- Shortlisting.
- Fairness-aware processing.

The API should translate external requests into the input formats expected by these modules and translate their results into stable response schemas.

It must not duplicate scoring formulas, ranking rules, or shortlisting logic.

Before implementation, each proposed schema must be checked against actual generated JSON files and existing Python function signatures. Where an adapter is required, its input, output, and mapping rules must be documented.

## 15. Implementation Status

This document defines proposed API schemas for the Day 16 design stage.

The following remain proposed until implemented and tested:

- HTTP request and response validation.
- Resume upload and parsing API endpoints.
- Scoring, ranking, and shortlisting API endpoints.
- Asynchronous task persistence and status retrieval.
- Background task execution and retry handling.
- API-specific error handling and logging.
- Authentication and authorization.
- API integration and contract tests.

The existing extraction, parsing, scoring, ranking, and shortlisting modules are separate from the proposed API layer. Their current outputs and behavior must be preserved and validated during integration.

The API should not be considered complete until the schemas, endpoint specification, integration flow, error-handling standards, and tests agree with the actual implementation.

## 16. Summary

These schemas define a proposed contract for resume processing, ATS scoring, ranking, shortlisting, and asynchronous task monitoring.

They preserve the existing ATS v2 scoring result structure, the ranking output structure, the configured shortlisting thresholds, and the distinction between task acceptance and task completion.

Before implementation, the API layer must define identifier mapping, input readiness checks, result persistence, task lifecycle management, error handling, security, and integration tests.