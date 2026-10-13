# ATS API Integration Flow and Asynchronous Job Handling

## 1. Purpose

This document defines how external applications will interact with the AI Job Portal through the proposed REST API and how the API layer will coordinate with existing ATS processing components.

Resume extraction, structured parsing, semantic matching, ATS scoring, candidate ranking, and shortlisting may require significant processing time. The API should therefore support asynchronous execution for operations that may take longer than a typical HTTP request.

The design separates request acceptance from task execution. A client submits a request, receives a task identifier, and retrieves the result when processing finishes.

This document defines the proposed architecture. It does not indicate that an API server, task queue, background worker system, or persistent task database has already been implemented.

## 2. Architectural Overview

The proposed processing architecture contains the following logical components:

1. API client
2. REST API layer
3. Request validation
4. Resume and job resource management
5. Asynchronous task management
6. Existing ATS processing modules
7. Task status and result storage
8. Logging and error handling

The API layer acts as an adapter between external clients and existing Python modules.

It should reuse the current resume extraction, parsing, semantic matching, scoring, ranking, shortlisting, and fairness components rather than duplicating their business logic.

The implementation must distinguish between the public API contract and the internal file-based interfaces used by the current project.

## 3. High-Level Integration Flow

```text
API Client
    |
    v
REST API Endpoint
    |
    v
Request Validation and Authorization
    |
    +---- Invalid Request ----> Standard Error Response
    |
    v
Create Persistent Task Record
    |
    v
Queue Task
    |
    v
Background Worker
    |
    v
Existing ATS Processing Modules
    |
    +---- Failure -----------> Record Failure
    |
    v
Persist and Validate Result
    |
    +---- Persistence Failure -> Record Failure
    |
    v
Mark Task Completed
    |
    v
Client Retrieves Task Result
```

The task queue, background worker, task database, and REST API are proposed components. Their implementation technologies will be selected during the API implementation stage.

## 4. Asynchronous Request Lifecycle

### 4.1 Request Submission

The client submits a request to an asynchronous endpoint, such as:

`POST /api/v1/resumes/{resume_id}/parse`

The API validates the request, verifies that the caller is authorized to access the relevant resource, checks whether the resume exists, and determines whether the requested operation can be performed.

Invalid requests should receive an appropriate HTTP error response without creating a processing task.

The API must distinguish request validation failures from failures that occur after a task has been accepted.

### 4.2 Task Creation

After successful validation, the system creates a task record containing:

- Task identifier
- Task type
- Associated resume or job identifier
- Initial status
- Creation timestamp
- Last update timestamp
- Result reference, initially empty
- Error information, initially empty
- Attempt or retry metadata, if implemented

The task begins in the `queued` state.

The API returns HTTP `202 Accepted` with the task identifier and the information needed to retrieve the task status.

Task creation and queue submission must be designed to avoid accepted tasks becoming permanently lost if one operation succeeds while the other fails.

### 4.3 Task Execution

A background worker retrieves the queued task and marks it as `running`.

The worker invokes the relevant existing ATS processing module using validated and resolved inputs.

Examples include:

- Resume extraction and structured parsing
- Candidate-job ATS scoring
- Candidate ranking
- Candidate shortlisting
- Fairness analysis, where supported by the defined workflow

The worker should preserve the established input requirements, business rules, and output structures of the existing modules.

### 4.4 Result Storage

When processing succeeds, the system persists the required result and marks the task as `completed`.

When processing fails, the system records a stable machine-readable error code and marks the task as `failed`.

Task status and result updates should be persisted so that clients can retrieve the task state after the original HTTP request has ended.

For operations that produce files, task completion must reflect both successful processing and successful persistence of the required output. If processing succeeds but required persistence fails, the task must not be reported as `completed`.

The implementation must define how the task record, returned result, and persisted output remain consistent, including when a worker stops unexpectedly during processing.

### 4.5 Result Retrieval

The client queries:

`GET /api/v1/tasks/{task_id}`

The API returns the task's current state and, when available, its result or error information.

Clients should not need to keep the original HTTP connection open while the task is running.

The API must verify that the caller is authorized to retrieve the requested task and its associated results.

## 5. Task State Model

The proposed task states are:

| State | Meaning |
|---|---|
| `queued` | The task has been accepted and is waiting to execute |
| `running` | A worker is processing the task |
| `completed` | Processing and required result persistence finished successfully |
| `failed` | Processing or required result persistence ended unsuccessfully |

The intended transitions are:

```text
queued -> running -> completed
                  -> failed
```

A task should not move from `completed` or `failed` back to `running` automatically.

Retries should follow an explicitly defined policy. Depending on the chosen design, a retry may create a new task or a new attempt associated with the original task. The selected behavior must be documented consistently.

## 6. Task Status Response

A running task may return:

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

A completed task may return:

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

These examples illustrate the proposed contract; they do not assert that the current parsing implementation produces only a `resume_id`.

The final response structure must remain consistent with `ATS_API_Schemas.md`. The result field must contain the documented result schema or a reference to a securely stored result, according to the final implementation.

Failed tasks should return a stable error code and a safe error message. Internal exception details and stack traces must remain in protected logs.

## 7. Failure Handling

Failures may occur during file extraction, parsing, semantic matching, scoring, ranking, shortlisting, or result storage.

The system should distinguish between:

- Invalid client requests
- Missing or inaccessible resources
- Unsupported resume formats
- Processing prerequisites that are not ready
- Temporary processing failures
- Permanent processing failures
- Result persistence failures
- Internal service errors

For a failed task, the system should:

1. Record the failure state.
2. Store a stable machine-readable error code.
3. Preserve a safe, user-facing error message.
4. Record relevant diagnostic details in protected logs.
5. Associate the failure with the request and task identifiers.
6. Avoid returning internal stack traces, sensitive resume content, or private filesystem paths.

A failed task must not be reported as completed or produce a fabricated success result.

The error codes and response formats must remain consistent with `ATS_API_Error_Handling_and_Logging.md` and `ATS_API_Schemas.md`.

## 8. Retry and Idempotency Strategy

Retries should be limited to failures considered temporary.

Potentially retryable failures include transient service interruptions and temporary storage unavailability.

Invalid input, unsupported file formats, missing required inputs, and other permanent validation errors should not be retried automatically.

The implementation should define:

- Maximum retry attempts
- Retry delay and backoff strategy
- Task timeout
- Behavior after worker interruption
- Duplicate request handling
- Idempotency rules
- Whether a retry creates a new task or a new attempt

Where appropriate, an idempotency key can prevent repeated client submissions from unintentionally creating duplicate processing operations.

The system must not assume that every ATS operation is safe to execute more than once without checking its side effects. This is especially important for scoring and ranking operations that generate or overwrite output files.

## 9. Task Persistence

Task records should be stored independently of the lifetime of the HTTP request.

At minimum, a task record should include:

- `task_id`
- `task_type`
- `status`
- `created_at`
- `updated_at`
- Associated resource identifiers
- Result reference or result payload
- Error code and safe error message, if applicable
- Retry or attempt metadata, if implemented

The storage technology is intentionally not fixed at the design stage. It should be selected according to the final task queue, deployment, persistence, and recovery requirements.

The implementation should also define task-result retention, cleanup of temporary files, and recovery of tasks left in the `running` state after a worker interruption.

## 10. Integration with Existing ATS Modules

The API layer should delegate work to existing project components while preserving their established behavior.

### 10.1 Resume Upload and Parsing

The upload endpoint stores an accepted resume and assigns or associates it with a stable identifier. The parsing task invokes the existing extraction and structured parsing pipeline.

The integration must resolve the public resume identifier to the actual stored file and internal identifiers required by the extraction and parsing modules.

The API must not assume that an illustrative parsing response in the schema document exactly matches the current parser output. An adapter should map the existing parser output to the public API response schema.

### 10.2 Candidate Scoring

The scoring task should reuse the existing scoring generator:

`ats_scoring.score_generator.generate_score(resume_id, jd_filename, semantic_lookup)`

Before invoking the generator, the orchestration layer must resolve the external resume and job identifiers to the correct internal inputs.

The existing generator expects the required skills, experience, education, and job-description JSON files to be available. The semantic-matching lookup must also be loaded or resolved according to the existing workflow.

The generator returns a result dictionary and saves the ATS v2 scoring result as a JSON file in its configured output directory. The API integration must account for this filesystem side effect and ensure that the task result refers to the same candidate-job pair as the persisted output.

The task must not be marked `completed` unless processing and required persistence both succeed.

The API must preserve the existing scoring weights, missing-component behavior, component details, and explainable scoring outputs. It must not silently substitute the legacy ATS v1 calculation for ATS v2.

### 10.3 Candidate Ranking

The existing ranking generator loads ATS v2 score files from:

`data/processed/ats_scores_v2`

It ranks candidates by job, applies the configured shortlisting rules, summarizes decisions, and saves job-level ranking results under:

`data/processed/candidate_ranking`

The API orchestration layer should reuse this pipeline where appropriate rather than implementing a separate ranking algorithm.

The API must preserve the existing ranking output structure, including:

- `job_id`
- `role`
- `candidate_count`
- `decision_summary`
- `ranked_candidates`

Each ranked candidate should preserve the relevant fields returned by the current ranking pipeline, including `rank`, `candidate_id`, `job_id`, `role`, `ats_score`, `component_scores`, `decision`, and `decision_reason`, where present.

The integration must ensure that a requested job's ranking is generated from the correct ATS v2 score files and does not unintentionally mix results from different jobs or scoring versions.

### 10.4 Candidate Shortlisting

The shortlisting task should reuse the existing configured decision rules:

- `SHORTLIST_THRESHOLD = 70.0`
- `REVIEW_THRESHOLD = 50.0`

The current rules classify candidates as follows:

| ATS score | Decision |
|---|---|
| Greater than or equal to 70 | `SHORTLIST` |
| Greater than or equal to 50 and below 70 | `REVIEW` |
| Below 50 | `REJECT` |

The initial API contract must use the existing configuration rather than introducing an independent set of thresholds that conflicts with the backend.

The implementation must define whether the shortlisting endpoint triggers ranking generation or operates on an existing ranking result. It should not duplicate classification logic or silently alter the configured thresholds.

### 10.5 Fairness-Aware Processing

Where required by the product workflow, the API may expose fairness-related results through an explicitly documented operation.

Fairness-related operations must reuse the existing fairness components and preserve their established inputs and output schemas.

The fairness layer must remain distinct from the original ATS score. Fairness outputs must not be presented as proof that the recruitment process is free from bias, and the API must not silently reinterpret or alter fairness metrics.

The API contract must explicitly document which fairness results are exposed, how they relate to the relevant candidate and job, and what limitations apply.

## 11. Logging and Observability

Each request and task should be traceable through a request identifier and task identifier.

The system should record:

- Request and task identifiers
- Operation type
- Processing status
- Processing duration
- Retry attempts, if applicable
- Safe error codes
- Worker failures
- Result persistence failures
- Relevant scoring or ranking resource identifiers

Logs must not unnecessarily contain raw resume text, personal contact details, authentication credentials, or other sensitive information.

Request identifiers should be propagated into task execution logs where possible. Diagnostic details must remain in protected logs and must not be exposed through public task responses.

## 12. Security and Resource Protection

The asynchronous design must preserve the security controls of the API layer.

The implementation should:

- Validate uploaded files before processing
- Restrict allowed file types and file sizes
- Prevent unauthorized access to task results
- Check access to associated resume and job resources
- Protect stored resumes and task results
- Limit excessive task submissions
- Avoid exposing internal file paths and exception details
- Validate identifiers and resolve them to authorized internal resources
- Apply appropriate authentication and authorization controls

Task identifiers alone must not be treated as proof that a caller is authorized to access a result.

The API must not allow a caller to access another candidate's resume, scoring result, or ranking data merely by supplying a different identifier.

## 13. Proposed Implementation Sequence

The implementation should proceed in the following order:

1. Finalize request and response schemas.
2. Define task and resource data models.
3. Define identifier mapping between public API resources and internal files.
4. Implement request validation and authorization.
5. Implement persistent task creation and retrieval.
6. Add a task execution mechanism.
7. Connect tasks to existing ATS modules through explicit adapters.
8. Implement result persistence and task-state consistency.
9. Add standardized error handling and structured logging.
10. Test successful processing, failures, retries, and duplicate requests.
11. Validate that ranking and shortlisting preserve existing configuration.
12. Document operational requirements and API behavior.

## 14. Design Limitations

This document specifies the intended integration flow rather than a deployed asynchronous processing system.

The REST API, task queue, background workers, persistent task database, retry policy, timeout configuration, authentication layer, and API-specific adapters remain implementation work.

The current ATS modules use existing Python interfaces and file-based inputs and outputs. Integrating them into an asynchronous API will require explicit resource resolution, input validation, and output mapping.

The API integration will be considered complete only after the relevant components have been implemented and validated through automated tests.

## 15. Summary

The asynchronous integration design enables external applications to submit long-running ATS operations without maintaining a single open request until processing finishes.

A task identifier provides a stable way to track processing. Persistent task state, structured errors, controlled retries, and consistent logging provide the foundation for reliable backend integration.

The design preserves the existing ATS engines and introduces a clear boundary between external API contracts and internal recruitment-processing logic. The final implementation must preserve the existing ATS v2 scoring, ranking, shortlisting, and fairness behavior while ensuring that task state accurately reflects processing and result-persistence outcomes.