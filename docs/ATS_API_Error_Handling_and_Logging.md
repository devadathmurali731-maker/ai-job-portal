# ATS API Error Handling and Logging

## 1. Purpose

This document defines the proposed error-handling, logging, monitoring, and recovery standards for the AI Job Portal API.

The API will coordinate existing resume-processing, semantic-matching, ATS scoring, candidate-ranking, and shortlisting components. Failures may occur during request validation, resource lookup, processing, or result persistence.

The API must report failures consistently, protect sensitive candidate information, and maintain accurate task status throughout asynchronous processing.

This document describes the intended API behavior. API routes, background workers, centralized logging, and task persistence remain implementation work unless explicitly implemented and tested.

## 2. Error-Handling Principles

The API should follow these principles:

1. **Consistent responses:** Return a standardized error structure across endpoints.
2. **Appropriate HTTP status codes:** Distinguish client errors, authorization failures, missing resources, and server failures.
3. **Safe error messages:** Provide useful information without exposing private candidate data or internal implementation details.
4. **Traceability:** Associate errors with request and task identifiers where applicable.
5. **Reliable task state:** Record asynchronous failures in the task record.
6. **Persistence awareness:** Do not report an operation as completed when required result storage has failed.
7. **Controlled retries:** Retry only failures that are considered temporary and safe to retry.
8. **Separation of concerns:** Keep public error responses separate from protected diagnostic logs.
9. **Consistent schemas:** Keep error responses aligned with `ATS_API_Schemas.md` and `ATS_API_Specification.md`.

## 3. Standard Error Response

The proposed API error format is:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource could not be found.",
    "details": {
      "resource_type": "resume"
    }
  },
  "request_id": "REQ_001"
}
```

### Field definitions

| Field | Type | Description |
|---|---|---|
| `error` | Object | Contains error information |
| `error.code` | String | Stable, machine-readable error code |
| `error.message` | String | Safe, human-readable explanation |
| `error.details` | Object or null | Optional, non-sensitive validation or diagnostic context |
| `request_id` | String | Identifier for the HTTP request |

The `details` field must contain only safe information needed to understand the error. It must not expose raw resume text, personal contact information, credentials, private filesystem paths, environment variables, or stack traces.

The exact structure must remain consistent with the finalized API schemas.

## 4. HTTP Status Code Standards

| HTTP status | Meaning | Example |
|---|---|---|
| `200 OK` | Request succeeded | Retrieving a task's current status, including a task whose state is `failed` |
| `201 Created` | A resource was created | Resume upload completed and a resume resource was created |
| `202 Accepted` | An asynchronous operation was accepted for processing | Resume parsing or ATS scoring task submitted |
| `400 Bad Request` | Request syntax or structure is invalid | Malformed JSON or missing required fields where defined as request errors |
| `401 Unauthorized` | Authentication is missing or invalid | Invalid authentication credentials |
| `403 Forbidden` | The caller is not permitted to perform the operation | Access to another candidate's resume |
| `404 Not Found` | The requested resource does not exist or is not accessible under the API's resource-disclosure policy | Unknown resume, job, or task identifier |
| `409 Conflict` | The request conflicts with the resource's current state | Attempting an operation that is not allowed in the current workflow state |
| `413 Content Too Large` | The uploaded file exceeds the configured limit | Resume upload exceeds the maximum permitted size |
| `415 Unsupported Media Type` | The submitted media type is unsupported | Unsupported upload format |
| `422 Unprocessable Content` | The request is structurally valid but its values fail semantic validation | Invalid score range or incompatible field values |
| `429 Too Many Requests` | The caller has exceeded an applicable rate limit | Excessive task submissions |
| `500 Internal Server Error` | An unexpected error occurred while handling the API request | Unhandled exception during synchronous request processing |
| `503 Service Unavailable` | A required service is temporarily unavailable | Task queue or required processing service is unavailable |

Use `400 Bad Request` for malformed JSON, invalid request structure, or missing required fields where the API contract defines these as request errors. Use `422 Unprocessable Content` for structurally valid requests whose values fail validation, such as an invalid score range. Apply these rules consistently across endpoints.

An asynchronous request that is successfully accepted should return `202 Accepted`. A subsequent background-processing failure must be recorded in the task resource; it must not be confused with the original submission request failing.

Retrieving a task whose state is `failed` should normally return `200 OK` if the task-status request itself succeeds. The response body should report `"status": "failed"` and include the documented error information.

A `500` response for the original submission is appropriate when the API cannot successfully handle the request, such as when it encounters an unexpected error before confirming acceptance. The implementation must avoid reporting successful task acceptance if it cannot reliably create or record the task.

## 5. Standard Error Catalogue

The following codes are proposed for the initial API version. The implementation should use them consistently and document any additional codes before exposing them publicly.

| Error code | Meaning | Typical status or handling |
|---|---|---|
| `INVALID_REQUEST` | Request structure or required fields are invalid | `400` |
| `VALIDATION_ERROR` | A supplied value fails semantic validation | `422` |
| `AUTHENTICATION_REQUIRED` | Valid authentication is required | `401` |
| `ACCESS_DENIED` | The caller is not authorized for the operation | `403` |
| `RESOURCE_NOT_FOUND` | The requested resource does not exist or cannot be disclosed | `404` |
| `RESOURCE_NOT_READY` | Required processing inputs or prerequisites are not yet available | Task failure or an appropriate client response, depending on when detected |
| `RESOURCE_CONFLICT` | The operation conflicts with the current resource state | `409` |
| `UNSUPPORTED_FILE_TYPE` | The uploaded file type is not supported | `415` |
| `FILE_TOO_LARGE` | The uploaded file exceeds the configured limit | `413` |
| `RATE_LIMIT_EXCEEDED` | The caller has exceeded an applicable rate limit | `429` |
| `RESUME_EXTRACTION_FAILED` | Resume text extraction failed | Task failure |
| `RESUME_PARSING_FAILED` | Structured resume parsing failed | Task failure |
| `SEMANTIC_MATCHING_FAILED` | Semantic matching failed | Task failure |
| `ATS_SCORING_FAILED` | ATS score calculation failed | Task failure |
| `RANKING_FAILED` | Candidate ranking failed | Task failure |
| `SHORTLISTING_FAILED` | Candidate decision classification failed | Task failure |
| `RESULT_PERSISTENCE_FAILED` | A required result could not be saved | Task failure |
| `TASK_QUEUE_UNAVAILABLE` | The task could not be reliably submitted to the queue | `503` or another appropriate submission error |
| `TASK_EXECUTION_FAILED` | A background task failed unexpectedly | Task failure |
| `INTERNAL_ERROR` | An unexpected API-level error occurred | `500` |
| `SERVICE_UNAVAILABLE` | A required service is temporarily unavailable | `503` |

These codes describe the proposed API contract. Existing Python modules may raise different exceptions or use different internal error formats. The API integration layer must map those internal failures to the documented public error codes.

The API must not assume that every error code already exists in the current Python implementation.

## 6. Synchronous Error Handling

Synchronous operations should validate their inputs before invoking processing logic.

The proposed handling sequence is:

1. Validate the request structure.
2. Validate the supplied field values.
3. Authenticate the caller and authorize access.
4. Resolve the requested resource.
5. Execute the synchronous operation.
6. Handle and log unexpected exceptions.
7. Return either the documented success response or a standardized error response.

Expected validation and resource errors should be handled explicitly rather than converted into generic internal errors.

Unexpected exceptions should be recorded in protected logs with relevant diagnostic information. The client should receive a safe error response containing a stable error code and request identifier.

For ATS scoring, the implementation must handle failures during both score calculation and result persistence. A successful calculation must not be reported as fully completed if saving the required output fails. The API and task orchestration layer must keep the reported task status and persisted result consistent, and log storage failures using the stable code `RESULT_PERSISTENCE_FAILED`.

## 7. Asynchronous Error Handling

Asynchronous tasks require separate handling for submission errors and processing errors.

### 7.1 Submission errors

If the API cannot validate a request, authorize the operation, create the required task record, or reliably submit the task for execution, it should return an appropriate HTTP error response.

The API must not claim that a task was accepted unless the system can reliably identify and track that task.

### 7.2 Processing errors

If a task has been accepted and subsequently fails, the worker should:

1. Capture the failure.
2. Determine the appropriate stable error code.
3. Record the task state as `failed`.
4. Store a safe error message in the task record.
5. Record diagnostic information in protected logs.
6. Preserve the task and request correlation identifiers.
7. Avoid returning a success result for the failed operation.

### 7.3 Example failed-task response

```json
{
  "task_id": "TASK_001",
  "task_type": "resume_parsing",
  "status": "failed",
  "created_at": "2026-10-13T04:00:00Z",
  "updated_at": "2026-10-13T04:00:08Z",
  "result": null,
  "error": {
    "code": "RESUME_PARSING_FAILED",
    "message": "The resume could not be processed."
  }
}
```

This is an illustrative response. The final field names and structure must match the task schema in `ATS_API_Schemas.md`.

A task-status request can return HTTP `200 OK` with this body because the status lookup succeeded even though the underlying processing task failed.

### 7.4 Missing prerequisites

Some ATS operations depend on outputs generated by earlier stages.

For example, the current ATS v2 scoring generator expects candidate skills, experience, education, job-description data, and a semantic-matching lookup to be available as required by its existing workflow.

If a required input is not yet available, the integration layer must not silently substitute an empty or fabricated input. It should either defer execution according to a defined orchestration policy or fail with an appropriate error such as `RESOURCE_NOT_READY`.

## 8. Retry and Timeout Policy

Retries should be limited to transient failures and should follow a documented policy.

Potentially retryable failures include:

- Temporary service unavailability
- Temporary task-queue interruptions
- Transient storage failures, when retrying is safe
- Temporary worker interruptions

Failures that generally should not be retried automatically include:

- Invalid request fields
- Unsupported file formats
- Missing permanently required inputs
- Invalid resource identifiers
- Authorization failures
- Deterministic parsing or validation errors

The implementation should define:

- Maximum retry attempts
- Retry delay and backoff
- Task execution timeout
- Queue-submission timeout
- Behavior after worker interruption
- Duplicate-submission handling
- Whether a retry creates a new task or another attempt on the same task

The retry mechanism must not create duplicate results or overwrite unrelated outputs.

File-generating operations, including ATS scoring and ranking, require particular care because rerunning a task may write to the same output path. The implementation must ensure that retries remain consistent with the intended candidate-job pair and scoring version.

## 9. Request and Task Correlation

The system should use separate identifiers for HTTP requests and asynchronous tasks.

### Request ID

The `request_id` identifies an individual HTTP request. It should appear in the response and in the logs associated with that request.

### Task ID

The `task_id` identifies an asynchronous operation and is used to retrieve its status and result.

A single request may create a task, and a task may produce log events across multiple workers or execution attempts.

The implementation should propagate the relevant task identifier into background-processing logs. It should also retain the originating request identifier where practical.

A client retry may generate a new request ID. If idempotency is implemented and the retry resolves to an existing task, the API should document how the existing task is identified and returned.

The API must not assume that request IDs and task IDs are interchangeable.

## 10. Logging Standards

Logs should be structured and consistent across API handlers, background workers, and existing ATS integration components.

Where applicable, each event should include:

- Timestamp
- Log severity
- Event name
- Request ID
- Task ID
- Operation type
- Resume ID or candidate ID, where safe and necessary
- Job ID, where safe and necessary
- Processing status
- Error code
- Processing duration
- Retry or attempt number, if applicable

Suggested log levels:

| Level | Intended use |
|---|---|
| `DEBUG` | Detailed development diagnostics that do not expose sensitive information |
| `INFO` | Request acceptance, task transitions, successful processing, and result persistence |
| `WARNING` | Recoverable issues, retries, and unexpected but handled conditions |
| `ERROR` | Failed tasks, result persistence failures, and unexpected processing errors |
| `CRITICAL` | Severe failures that threaten the availability or integrity of the service |

Log messages should describe the event and relevant identifiers without unnecessarily reproducing input data.

For example:

```text
INFO task_id=TASK_001 event=task_started task_type=ats_scoring
ERROR task_id=TASK_001 event=result_persistence_failed error_code=RESULT_PERSISTENCE_FAILED
INFO task_id=TASK_001 event=task_failed error_code=RESULT_PERSISTENCE_FAILED
```

These are illustrative structured-log messages, not evidence that centralized structured logging has already been implemented.

## 11. Sensitive Data Protection

Recruitment documents can contain personal and confidential information. Logging and error responses must minimize exposure of this information.

The implementation must avoid logging or returning:

- Full resume contents
- Personal phone numbers or email addresses
- Home addresses
- Authentication credentials or tokens
- Private configuration values
- Raw uploaded documents
- Sensitive extracted candidate attributes
- Unnecessary filesystem paths
- Full stack traces in public responses

Diagnostic information should be stored only in appropriately protected logs with access controls and retention rules.

The API should return safe messages to clients while preserving enough protected diagnostic detail for authorized developers to investigate failures.

## 12. Operational Events

The system should record important lifecycle events to support troubleshooting and operational monitoring.

Recommended events include:

- `request_received`
- `request_validation_failed`
- `resource_created`
- `task_created`
- `task_queued`
- `task_started`
- `task_retry_scheduled`
- `task_completed`
- `task_failed`
- `result_persisted`
- `result_persistence_failed`
- `worker_interrupted`
- `authorization_failed`
- `rate_limit_exceeded`

The implementation may use different internal event names, but event semantics should remain clear and consistent.

Events should allow an operator to trace a task from acceptance through execution and final persistence.

## 13. Monitoring and Metrics

The API should eventually expose or collect operational metrics such as:

- Number of requests by endpoint and status code
- Number of tasks by type and state
- Task execution duration
- Task failure rate
- Retry frequency
- Queue waiting time
- Result persistence failure rate
- Resume extraction and parsing failure rates
- ATS scoring and ranking failure rates
- Rate-limit events

Metrics should be aggregated where possible and should not contain raw candidate information.

Monitoring thresholds and alerting rules should be configured during implementation based on deployment requirements and expected workload.

## 14. Testing Requirements

Error handling and logging should be validated through automated tests.

The test plan should include:

1. Malformed JSON and invalid request structures.
2. Missing required fields.
3. Invalid field values.
4. Unauthorized access to resources and tasks.
5. Unknown resume, job, and task identifiers.
6. Unsupported file types and oversized uploads.
7. Missing ATS processing prerequisites.
8. Resume extraction and parsing failures.
9. Semantic-matching failures.
10. ATS score calculation failures.
11. Candidate-ranking and shortlisting failures.
12. Result persistence failures after otherwise successful processing.
13. Task-queue submission failures.
14. Worker interruption and recovery.
15. Retry and duplicate-submission behavior.
16. Correct request and task ID correlation.
17. Safe public error responses without sensitive diagnostic details.
18. Correct task status after processing or persistence failures.
19. Consistency between saved ATS v2 scores and task results.
20. Consistency between saved ranking outputs and task results.

Tests should verify observable behavior rather than relying only on log messages.

For asynchronous operations, tests should verify that submission acceptance is distinct from task completion and that a failed background task does not appear as completed.

## 15. Implementation Status

This document defines the proposed error-handling and logging contract.

The following capabilities require implementation and testing unless they already exist in the relevant application layer:

- Standardized API error responses
- API-level request IDs
- Persistent task and task-error records
- Background-worker failure handling
- Retry and timeout policies
- API-specific error-code mapping
- Structured logs and correlation
- Operational metrics and alerting
- Consistency between processing outcomes and persisted results

The existing ATS modules may have their own exceptions, output files, and validation rules. The API layer must integrate with these behaviors explicitly instead of assuming that the proposed API-level mechanisms already exist.

## 16. Summary

Consistent error handling and protected logging are essential for reliable ATS API integration.

The API must distinguish request failures from asynchronous processing failures, use stable error codes, protect candidate information, and maintain accurate task state.

Most importantly, an operation must not be reported as completed unless its required processing and result persistence have succeeded. These rules provide the foundation for a reliable API while preserving the behavior of the existing ATS components.