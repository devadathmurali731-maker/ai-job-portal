# AI Job Portal - Metadata Standards

## 1. Overview

This document defines the metadata standards used throughout the AI Job Portal.

Metadata allows the system to identify, track, and trace AI data throughout
the complete hiring pipeline.

The four core metadata fields are:

1. Candidate ID
2. Job ID
3. Model Version
4. Timestamp

These fields should be used consistently across the system.

---

## 2. Candidate ID

### Purpose

The Candidate ID uniquely identifies a candidate within the AI Job Portal.

### Standard Format

CAND_###

Where:

- CAND = Candidate identifier
- ### = Three-digit unique number

### Examples

CAND_001
CAND_002
CAND_003
CAND_100

### Example

{
    "candidate_id": "CAND_001"
}

### Rules

1. Every candidate must have a unique Candidate ID.
2. Candidate IDs should not depend on the candidate's name.
3. Candidate IDs should remain consistent throughout the candidate lifecycle.
4. The same Candidate ID should be used for resume parsing, ATS scoring,
   screening, and interview evaluation.

---

## 3. Job ID

### Purpose

The Job ID uniquely identifies a job opening or job description.

### Standard Format

JOB_###

Where:

- JOB = Job identifier
- ### = Three-digit unique number

### Examples

JOB_001
JOB_002
JOB_003
JOB_100

### Current Project Mapping

JOB_001 = Data Scientist
JOB_002 = Software Engineer
JOB_003 = Data Analyst
JOB_004 = ML Engineer
JOB_005 = Business Analyst
JOB_006 = HR Executive

### Rules

1. Every job opening must have a unique Job ID.
2. Job IDs should not depend on the job title.
3. The Job ID should remain associated with the same job opening.
4. Job IDs should be used when connecting candidates with job requirements.

---

## 4. Candidate-Job Relationship

Candidate ID and Job ID must be stored together whenever data represents
a candidate applying for or being evaluated against a specific job.

Example:

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001"
}

This represents:

Candidate 001
        +
Job 001

The combination identifies a specific candidate-job evaluation.

---

## 5. Model Version

### Purpose

Model Version identifies the version of the AI or ML component that
generated a particular result.

### Standard Format

<module>_v<major>.<minor>

### Examples

ats_v1.0
ats_v2.0
screening_ai_v1.0
interview_ai_v1.0
resume_parser_v1.0

### Version Components

Example:

ats_v1.0

ats
    = Module name

v
    = Version indicator

1
    = Major version

0
    = Minor version

---

## 6. Major and Minor Versions

### Major Version

A major version represents a significant change to the model or system.

Example:

ats_v1.0
    ↓
ats_v2.0

Possible reasons:

- Major model architecture change
- Significant feature changes
- Major scoring logic changes
- Major preprocessing changes

### Minor Version

A minor version represents a smaller improvement.

Example:

ats_v1.0
    ↓
ats_v1.1

Possible reasons:

- Small bug fixes
- Minor preprocessing improvement
- Small feature enhancement
- Parameter or configuration improvements

---

## 7. Timestamp

### Purpose

Timestamp records when a data object or AI result was created or generated.

### Standard Format

ISO 8601 date-time format.

Example:

2026-09-17T10:15:00

### Structure

YYYY-MM-DDTHH:MM:SS

Example:

2026-09-17T10:15:00

Where:

YYYY = Year
MM = Month
DD = Day
T = Date/time separator
HH = Hour
MM = Minute
SS = Second

---

## 8. Why Timestamps Are Important

Timestamps support:

- Data tracking
- Auditing
- Debugging
- Model monitoring
- Reproducibility
- Data versioning
- AI decision traceability

Example:

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001",
    "model_version": "ats_v1.0",
    "timestamp": "2026-09-17T10:15:00"
}

This tells the system:

- Which candidate?
- Which job?
- Which model?
- When was the result generated?

---

## 9. Standard Metadata Object

A standard AI output should contain the following metadata:

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001",
    "model_version": "ats_v1.0",
    "timestamp": "2026-09-17T10:15:00"
}

Not every data object requires every field.

For example, a standalone resume profile may only require:

{
    "candidate_id": "CAND_001",
    "resume_id": "RESUME_001",
    "parser_version": "resume_parser_v1.0",
    "timestamp": "2026-09-17T10:00:00"
}

A candidate-job evaluation should contain both Candidate ID and Job ID.

---

## 10. Metadata by AI Pipeline Stage

### Resume Processing

Example:

{
    "candidate_id": "CAND_001",
    "resume_id": "RESUME_001",
    "parser_version": "resume_parser_v1.0",
    "timestamp": "2026-09-17T10:00:00"
}

### ATS

Example:

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001",
    "model_version": "ats_v1.0",
    "timestamp": "2026-09-17T10:15:00"
}

### Screening

Example:

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001",
    "model_version": "screening_ai_v1.0",
    "timestamp": "2026-09-17T10:30:00"
}

### Interview

Example:

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001",
    "model_version": "interview_ai_v1.0",
    "timestamp": "2026-09-17T11:30:00"
}

---

## 11. Traceability

Metadata allows the complete AI decision process to be traced.

Example:

CAND_001
    ↓
JOB_001
    ↓
ATS
    ↓
ats_v1.0
    ↓
ATS Score
    ↓
Screening AI
    ↓
screening_ai_v1.0
    ↓
Screening Report
    ↓
Interview AI
    ↓
interview_ai_v1.0
    ↓
Interview Result

This provides end-to-end traceability.

---

## 12. Dataset Version Metadata

Training datasets should also contain version information.

Example:

{
    "dataset_version": "v1.0",
    "dataset_name": "job_matching_training_data",
    "created_at": "2026-09-17T12:00:00",
    "number_of_records": 1000,
    "source": "AI Job Portal"
}

Dataset versions should not be overwritten when a new version is created.

---

## 13. Model-to-Dataset Traceability

A trained model should be linked to the dataset used to train it.

Example:

Dataset:

training_v1

        ↓

Model:

ats_v1.0

Later:

training_v2

        ↓

Model:

ats_v2.0

This allows the development team to identify which dataset produced
a particular model version.

---

## 14. Metadata Quality Rules

The following rules should be followed:

1. IDs must be unique.
2. IDs should remain stable throughout the lifecycle.
3. Candidate IDs should not be based on names.
4. Job IDs should not be based on job titles.
5. Model versions must be recorded for AI-generated outputs.
6. Timestamps should use ISO 8601 format.
7. Metadata should be stored together with the corresponding data.
8. Historical metadata should not be removed when models are updated.
9. Dataset versions should be preserved when reproducibility is required.
10. Metadata should support end-to-end traceability.

---

## 15. Example Complete ATS Metadata

{
    "candidate_id": "CAND_001",
    "job_id": "JOB_001",
    "ats_score": 87,
    "model_version": "ats_v1.0",
    "timestamp": "2026-09-17T10:15:00"
}

This record can be traced to:

Candidate:
CAND_001

Job:
JOB_001

Model:
ats_v1.0

Generated:
2026-09-17T10:15:00

---

## 16. Conclusion

The metadata standards provide a consistent method for identifying and
tracking candidates, jobs, AI models, and generated results.

The four core metadata standards are:

Candidate ID
    CAND_###

Job ID
    JOB_###

Model Version
    <module>_vX.Y

Timestamp
    ISO 8601

These standards support scalability, debugging, auditing, reproducibility,
and end-to-end AI data traceability within the AI Job Portal.