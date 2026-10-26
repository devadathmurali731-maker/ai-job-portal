
# Day 23 – Metadata Standards and Transcript Normalization

## 1. Purpose

Define consistent metadata, transcript storage, and normalization rules for AI-powered HR screening conversations.

## 2. Metadata Standards

| Field | Data Type | Required | Standard |
|---|---|---|---|
| transcript_id | String | Yes | Unique ID for each transcript record |
| interaction_id | String | Yes | Unique ID for each screening interaction |
| session_id | String | Yes | Groups interactions in one screening session |
| candidate_id | String | Yes | Stable candidate identifier |
| job_id | String | Yes | Stable job identifier |
| question_id | String | Yes | Must reference an existing screening question |
| timestamp | ISO 8601 string | Yes | UTC timestamp, such as 2026-10-26T11:45:00Z |
| language | BCP 47 string | Yes for transcript | Language tag such as en or ml-IN |
| confidence | Number | Yes for transcript | Speech recognition confidence between 0 and 1 |
| transcript_text | String | Yes | Normalized speech-to-text result |
| status | Enum | Yes for interaction | asked, answered, skipped, no_response, transcription_failed |

### Identifier Rules

- IDs must be non-empty strings.
- IDs must be stable across related records.
- Each transcript_id and interaction_id must be unique.
- Do not use a candidate's name, email address, or phone number as an identifier.
- Foreign-key references must point to existing candidate, job, question, transcript, or session records where applicable.

### Timestamp Rules

- Store timestamps in UTC.
- Use ISO 8601 date-time format.
- Use the `Z` suffix for UTC timestamps.
- Record the time the question was asked and the time the response was received separately.
- Do not substitute processing time for the original event time.

### Confidence Rules

- Store speech recognition confidence as a number from 0 to 1.
- A value of 0 means the lowest confidence reported; 1 means the highest.
- Preserve the score reported by the speech recognition engine.
- If the score is unavailable, store null where the schema permits it.
- Do not interpret speech confidence as candidate competence, honesty, or suitability.

## 3. Transcript Normalization Rules

1. Preserve the original raw transcript separately when available.
2. Store the normalized transcript in transcript_text.
3. Trim leading and trailing whitespace.
4. Normalize repeated whitespace without joining separate words.
5. Use Unicode normalization consistently (NFC).
6. Preserve the candidate's intended meaning and wording.
7. Do not silently rewrite grammar or paraphrase answers.
8. Preserve meaningful punctuation where available.
9. Do not remove negations, numbers, dates, technical terms, or named entities.
10. Preserve the original language; do not translate automatically during normalization.
11. Represent missing answers as null in answer fields rather than inventing text.
12. Record the normalization version for reproducibility.
13. Keep segment timestamps non-negative and ensure end time is not earlier than start time.
14. Keep transcript segments in chronological order.
15. If transcription is uncertain, retain the available transcript and confidence metadata rather than guessing missing words.

## 4. AI Screening Data Structure

A screening session can contain multiple screening interactions. Each interaction links:

- candidate_id
- job_id
- question_id
- session_id
- asked_at and answered_at
- status and answer_text
- transcript_id, where a voice transcript exists

A transcript stores recognized text, language, timestamp, speech confidence, and optional timed segments.

The transcript and interaction should be linked by transcript_id. The question_id should reference the Day 22 HR screening question bank.

## 5. Recommended Database Tables

### screening_sessions

- session_id (Primary Key)
- candidate_id
- job_id
- started_at
- ended_at
- session_status

### screening_interactions

- interaction_id (Primary Key)
- session_id (Foreign Key)
- candidate_id
- job_id
- question_id
- asked_at
- answered_at
- status
- answer_text
- transcript_id (Nullable Foreign Key)

### voice_transcripts

- transcript_id (Primary Key)
- candidate_id
- job_id
- question_id
- timestamp
- language
- transcript_text
- confidence
- normalization_version

### transcript_segments

- segment_id (Primary Key)
- transcript_id (Foreign Key)
- sequence_number
- start_seconds
- end_seconds
- text
- confidence

## 6. Data Quality and Privacy

- Validate records against the corresponding JSON Schema before storage.
- Enforce primary-key uniqueness and foreign-key integrity.
- Restrict access to candidate transcripts to authorized users.
- Avoid storing unnecessary personal or sensitive information in metadata.
- Define retention and deletion policies before production deployment.
- Treat automated transcripts as potentially imperfect and allow correction where appropriate.
- Do not use speech recognition confidence as an employment decision score.

## 7. Versioning

- Initial normalization version: 1.0
- Store the schema version with production records or in a versioned schema registry.
- Introduce a new version when a change affects the interpretation or structure of stored data.
- Keep older records interpretable under their original schema version.

## 8. Day 23 Deliverables

1. data/schemas/voice_transcript.schema.json
2. data/schemas/ai_screening_interaction.schema.json
3. docs/Day23_Metadata_Standards.md

The database table definitions are logical architecture specifications. They do not create or migrate a production database.
