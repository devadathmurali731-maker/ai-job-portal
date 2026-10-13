# ATS API Specification

## 1. Overview

The ATS API layer will expose the existing AI Job Portal functionality through standardized REST endpoints. It will allow external applications, frontend interfaces, and backend services to submit resumes, request parsing, obtain candidate-job scores, and retrieve candidate ranking and shortlisting results.

The API layer will act as an interface between external clients and the existing ATS processing modules. Business logic should remain within the relevant processing engines wherever possible.

This specification defines the proposed API contract. It does not indicate that an HTTP server, API routes, authentication middleware, task queue, or background workers have already been implemented.

## 2. API Design Principles

The API will follow these principles:

- REST-style, resource-oriented endpoints.
- Versioned routes using `/api/v1`.
- JSON request and response bodies, except for file-upload requests.
- Consistent request validation and error responses.
- Unique identifiers for resumes, jobs, and asynchronous tasks.
- Structured logging for troubleshooting and auditing.
- Explicit task status for long-running operations.
- Preservation of existing ATS scoring and ranking logic.
- Reuse of existing shortlisting thresholds and decision rules.
- Consistent handling of processing results and filesystem persistence.
- Protection of candidate information and other sensitive data.

## 3. Base Path

`/api/v1`

The base path is a design convention. The endpoints documented below are proposed contracts and are not yet implemented routes.

## 4. Endpoint Definitions

### 4.1 Upload Resume

**Method:** `POST`

**Endpoint:** `/api/v1/resumes`

**Purpose:** Accept a resume file for processing.

**Request content type:** `multipart/form-data`

**Request fields:**

- `file`: Resume document to upload.
- Supported file formats and maximum file size must be configured before implementation.

**Proposed success response:** `201 Created`

```json
{
  "resume_id": "RESUME_001",
  "status": "uploaded",
  "message": "Resume uploaded successfully."
}
```

The returned `resume_id` will identify the uploaded resume in subsequent API requests.

The implementation must validate the uploaded file, generate or assign a unique identifier, and store the file safely. It must define how the external `resume_id` maps to the internal resume identifier and file paths used by the existing processing pipeline.

A successful upload does not mean that the resume has been parsed or is ready for ATS scoring.

### 4.2 Request Resume Parsing

**Method:** `POST`

**Endpoint:** `/api/v1/resumes/{resume_id}/parse`

**Purpose:** Request extraction and structured parsing of an uploaded resume.

**Proposed success response:** `202 Accepted`

```json
{
  "task_id": "TASK_001",
  "resume_id": "RESUME_001",
  "status": "queued",
  "message": "Resume parsing has been queued."
}
```

The task identifier will be used to retrieve the processing status and result.

The API orchestration layer must resolve the uploaded resume to the existing extraction and parsing workflow. It must also define how extracted content, classified resume sections, and downstream skills, experience, and education data become available to later stages.

The `queued` state means that the operation has been accepted for asynchronous processing. It does not guarantee successful completion.

### 4.3 Request Candidate Scoring

**Method:** `POST`

**Endpoint:** `/api/v1/jobs/{job_id}/score`

**Purpose:** Request ATS scoring for a candidate against a specific job.

**Proposed request body:**

```json
{
  "resume_id": "RESUME_001"
}
```

**Proposed success response:** `202 Accepted`

```json
{
  "task_id": "TASK_002",
  "resume_id": "RESUME_001",
  "job_id": "JOB_001",
  "status": "queued"
}
```

The scoring process should use the existing ATS scoring engine rather than introducing a second scoring implementation.

The existing scoring generator exposes the following function:

`ats_scoring.score_generator.generate_score(resume_id, jd_filename, semantic_lookup)`

Before invoking this function, the orchestration layer must:

1. Resolve the external resume and job identifiers to the correct internal inputs.
2. Ensure that the required skills, experience, education, and job-description JSON files are available.
3. Load or resolve the semantic-matching lookup.
4. Validate that the inputs correspond to the requested candidate and job.
5. Invoke the existing scoring generator.

The existing scoring generator returns a result dictionary and also saves the ATS v2 scoring result as a JSON file in its configured output directory.

The API integration must account for this filesystem side effect and ensure that the task status, returned result, and persisted output remain consistent. A task must not be reported as completed if required result persistence fails.

The existing ATS v2 result includes fields such as:

- `candidate_id`
- `job_id`
- `role`
- `component_scores`
- `original_weights`
- `adjusted_weights`
- `weighted_contributions`
- `final_ats_score`
- `available_components`
- `missing_components`
- `component_details`

The API response schema must preserve the meaning of these fields unless an explicitly documented response adapter is introduced.

**Score field distinction:** The ATS v2 scoring engine uses `final_ats_score`. The ranking output uses `ats_score`. These field names belong to different output schemas and must not be treated as interchangeable without an explicit mapping. Legacy ATS v1 output may also contain `ats_score` and must be distinguished from ATS v2 results.

### 4.4 Retrieve Candidate Rankings

**Method:** `GET`

**Endpoint:** `/api/v1/jobs/{job_id}/rankings`

**Purpose:** Retrieve candidates ranked for a particular job.

**Proposed success response:** `200 OK`

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
      "decision": "REVIEW",
      "decision_reason": "Illustrative reason from the ranking pipeline"
    }
  ]
}
```

The response is illustrative. The actual number of candidates and their scores and decisions depend on the stored scoring results.

The response structure aligns with the existing ranking output, which includes:

- `job_id`
- `role`
- `candidate_count`
- `decision_summary`
- `ranked_candidates`

Each ranked candidate can include `rank`, `candidate_id`, `job_id`, `role`, `ats_score`, `component_scores`, `decision`, and `decision_reason`, according to the existing ranking output.

The existing ranking generator reads ATS v2 scoring files from `data/processed/ats_scores_v2` and saves job-level ranking results under `data/processed/candidate_ranking`.

The API should reuse this pipeline where appropriate rather than reimplementing candidate ranking. The implementation must define how the requested job's ranking is generated, refreshed, and retrieved.

If no ranking result exists for a valid job, the API must define whether to generate the ranking or return an appropriate resource or processing-state response. It must not fabricate ranking results.

### 4.5 Apply Shortlisting

**Method:** `POST`

**Endpoint:** `/api/v1/jobs/{job_id}/shortlist`

**Purpose:** Apply the configured shortlisting rules to candidates scored for a particular job.

**Request body:** No threshold field is required for the initial API version.

The API should use the existing shortlisting configuration:

- `SHORTLIST_THRESHOLD = 70.0`
- `REVIEW_THRESHOLD = 50.0`

The existing decision rules are:

| ATS score | Decision |
|---|---|
| Score greater than or equal to 70 | `SHORTLIST` |
| Score greater than or equal to 50 and below 70 | `REVIEW` |
| Score below 50 | `REJECT` |

Scores must be valid numeric values in the supported range of 0 to 100.

**Proposed success response:** `200 OK`

```json
{
  "job_id": "JOB_001",
  "status": "completed",
  "shortlisted_count": 0,
  "review_count": 2,
  "rejected_count": 2
}
```

The response summarizes the decision counts produced by the existing ranking and shortlisting pipeline. The counts above are illustrative.

The existing implementation classifies candidates using the configured thresholds and generates decision reasons and summary counts. The API orchestration layer should reuse these rules rather than introducing an independent set of thresholds.

The API must define whether shortlisting triggers ranking generation or applies decisions to an existing ranking result. It must also ensure that the response reflects the persisted output and the correct job.

## 5. Asynchronous Task Status

**Method:** `GET`

**Endpoint:** `/api/v1/tasks/{task_id}`

**Purpose:** Retrieve the status and result of an asynchronous operation.

**Proposed response while processing:** `200 OK`

```json
{
  "task_id": "TASK_001",
  "status": "running",
  "result": null,
  "error": null
}
```

Supported task states are proposed as:

- `queued`
- `running`
- `completed`
- `failed`

The task-status endpoint should return `200 OK` when the task record is successfully retrieved, even when the task's processing state is `failed`.

A completed task should return its result. The result structure depends on the task type and must follow the corresponding response schema. A task that is queued or running should normally have a `null` result. A failed task should have a `null` result and a structured error object.

A proposed failed-task response is:

```json
{
  "task_id": "TASK_001",
  "status": "failed",
  "result": null,
  "error": {
    "code": "RESUME_PARSING_FAILED",
    "message": "The resume could not be processed.",
    "request_id": "REQ_001"
  }
}
```

A request for a nonexistent task should return `404 Not Found`.

The task queue, task persistence, worker execution, retry mechanism, and task-status endpoint remain proposed implementation features.

## 6. HTTP Status Codes

The API should use consistent HTTP status codes:

- `200 OK`: A successful retrieval or completed synchronous operation.
- `201 Created`: A resource was created successfully.
- `202 Accepted`: An asynchronous task was accepted for processing.
- `400 Bad Request`: The request is malformed or has an invalid structure.
- `401 Unauthorized`: Authentication is missing or invalid, if authentication is enabled.
- `403 Forbidden`: The caller lacks permission.
- `404 Not Found`: The requested resource does not exist.
- `409 Conflict`: The request conflicts with the resource's current state.
- `413 Content Too Large`: The uploaded file exceeds the configured limit.
- `415 Unsupported Media Type`: The submitted file or content type is unsupported.
- `422 Unprocessable Content`: The request is syntactically valid but fails semantic validation.
- `429 Too Many Requests`: A rate limit has been exceeded.
- `500 Internal Server Error`: An unexpected server-side error occurred.
- `503 Service Unavailable`: A required service is temporarily unavailable.

Use `400 Bad Request` for malformed request bodies or missing required fields where the API contract classifies these as request errors. Use `422 Unprocessable Content` for structurally valid requests whose values fail semantic validation, such as an invalid score range.

An asynchronous submission returning `202 Accepted` confirms that the request has been accepted, not that the underlying processing has succeeded. A later processing failure must be recorded in the task state and error fields.

## 7. Error Response Standard

Errors should use a consistent JSON structure.

```json
{
  "error": {
    "code": "INVALID_RESUME_FORMAT",
    "message": "The uploaded resume format is not supported.",
    "details": null,
    "request_id": "REQ_001"
  }
}
```

The error object contains:

- `code`: Stable, machine-readable error identifier.
- `message`: Safe explanation of the failure.
- `details`: Optional validation details containing only safe and relevant information.
- `request_id`: Identifier used to correlate the request with operational logs.

Error messages must be useful to API consumers without revealing filesystem paths, credentials, personal information, unrestricted internal exception traces, or other sensitive implementation details.

The API should use stable error codes for validation failures, missing resources, parsing failures, scoring failures, ranking failures, shortlisting failures, storage errors, and unexpected internal failures.

Asynchronous task failures should use the same error-code conventions as synchronous API errors wherever applicable.

## 8. Logging Standards

Each API request should record appropriate operational metadata:

- Request ID.
- HTTP method and route template.
- Response status.
- Processing duration.
- Task ID, where applicable.
- Error code for failed operations.
- Relevant event name and timestamp.

The request ID identifies an individual HTTP request. The task ID identifies a background processing operation. Their relationship should be preserved in logs when a request starts an asynchronous task.

Retries and subsequent status requests may produce additional request IDs while referring to the same task, depending on the implemented idempotency and correlation design.

Logs should avoid storing raw resume contents, unnecessary personal data, credentials, authentication tokens, secret configuration values, or other sensitive information.

The implementation should use structured logs and define suitable access controls and retention policies.

## 9. Security Considerations

The implementation should validate uploaded files, restrict supported formats and file sizes, use safe file handling, and prevent path traversal.

Authentication and authorization requirements must be defined before exposing the API beyond a trusted development environment.

Sensitive resume data must be protected during storage, processing, and transmission. API responses and logs must not expose unnecessary candidate information.

The implementation should also define rate limits, input validation rules, access controls for candidate and job resources, and appropriate handling of duplicate submissions.

## 10. Integration with Existing ATS Modules

The API should orchestrate existing processing modules rather than duplicate their business logic.

### Scoring integration

The API should call the existing ATS scoring generator after resolving the required inputs and ensuring that the prerequisite data is available.

The orchestration layer must account for the generator's JSON output side effect and preserve consistency between the calculation result, persisted scoring output, and asynchronous task status.

### Ranking and shortlisting integration

The API should reuse the existing ranking and shortlisting pipeline, including its configured thresholds, ranking output structure, decision classification, decision reasons, and summary counts.

The implementation must define how ranking and shortlisting results are generated, stored, refreshed, and retrieved for the requested job.

### Identifier mapping

External API identifiers such as `RESUME_001` must be mapped consistently to internal identifiers and files used by the existing project. The API must validate that candidate inputs, job descriptions, scores, and ranking results refer to the intended candidate-job pair.

## 11. Implementation Status

This document defines the proposed API contract for Day 16.

The following features remain proposed and must not be treated as implemented solely because they are documented:

- HTTP server and API routes.
- Resume upload endpoint.
- API-level resume parsing endpoint.
- API-level scoring endpoint.
- API-level ranking and shortlisting endpoints.
- Asynchronous task queue and task persistence.
- Background workers and retry handling.
- API authentication and authorization.
- Request and task correlation middleware.
- API-specific error handling and structured logging.
- API integration tests.

The existing resume-processing, ATS scoring, ranking, and shortlisting modules are separate from the proposed API layer. API integration must reuse and validate their actual interfaces and output schemas.

Implementation should begin only after the API contract, schemas, integration flow, error handling, and testing requirements have been reviewed for consistency.

## 12. Summary

The proposed ATS API provides a standardized interface for resume processing, candidate-job scoring, ranking, shortlisting, and asynchronous task monitoring.

The design preserves the existing ATS scoring and ranking logic, including the v2 scoring output, configured shortlisting thresholds, decision rules, and job-level ranking structure.

Before implementation, the API layer must define identifier mapping, prerequisite validation, asynchronous task handling, result persistence, error handling, security, and integration testing. All routes and infrastructure described in this document remain proposed until they have been implemented and validated.
