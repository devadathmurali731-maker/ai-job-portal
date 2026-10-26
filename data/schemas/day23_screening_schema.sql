
-- Day 23: AI Screening Transcript Database Schema
-- Compatible with SQLite 3.
-- This file defines the schema; it does not create a database by itself.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS screening_sessions (
    session_id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    session_status TEXT NOT NULL
        CHECK (session_status IN (
            'in_progress',
            'completed',
            'cancelled',
            'failed'
        )),
    CHECK (ended_at IS NULL OR ended_at >= started_at)
);

CREATE TABLE IF NOT EXISTS voice_transcripts (
    transcript_id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    language TEXT NOT NULL,
    transcript_text TEXT NOT NULL,
    confidence REAL NOT NULL
        CHECK (confidence >= 0.0 AND confidence <= 1.0),
    normalization_version TEXT NOT NULL DEFAULT '1.0',
    source TEXT NOT NULL DEFAULT 'speech_to_text'
        CHECK (source IN ('speech_to_text', 'manual_transcription'))
);

CREATE TABLE IF NOT EXISTS screening_interactions (
    interaction_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    asked_at TEXT NOT NULL,
    answered_at TEXT,
    status TEXT NOT NULL
        CHECK (status IN (
            'asked',
            'answered',
            'skipped',
            'no_response',
            'transcription_failed'
        )),
    answer_text TEXT,
    transcript_id TEXT UNIQUE,
    language TEXT,
    speech_confidence REAL
        CHECK (
            speech_confidence IS NULL
            OR speech_confidence BETWEEN 0.0 AND 1.0
        ),
    duration_seconds REAL
        CHECK (
            duration_seconds IS NULL
            OR duration_seconds >= 0.0
        ),
    normalization_version TEXT NOT NULL DEFAULT '1.0',

    FOREIGN KEY (session_id)
        REFERENCES screening_sessions(session_id),
    FOREIGN KEY (transcript_id)
        REFERENCES voice_transcripts(transcript_id),

    CHECK (answered_at IS NULL OR answered_at >= asked_at)
);

CREATE TABLE IF NOT EXISTS transcript_segments (
    segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transcript_id TEXT NOT NULL,
    sequence_number INTEGER NOT NULL CHECK (sequence_number >= 1),
    start_seconds REAL NOT NULL CHECK (start_seconds >= 0.0),
    end_seconds REAL NOT NULL CHECK (end_seconds >= start_seconds),
    text TEXT NOT NULL,
    confidence REAL
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0.0 AND 1.0
        ),

    FOREIGN KEY (transcript_id)
        REFERENCES voice_transcripts(transcript_id)
        ON DELETE CASCADE,

    UNIQUE (transcript_id, sequence_number)
);

CREATE INDEX IF NOT EXISTS idx_interactions_candidate_job
    ON screening_interactions(candidate_id, job_id);

CREATE INDEX IF NOT EXISTS idx_interactions_session
    ON screening_interactions(session_id);

CREATE INDEX IF NOT EXISTS idx_transcripts_candidate_job
    ON voice_transcripts(candidate_id, job_id);

CREATE INDEX IF NOT EXISTS idx_segments_transcript
    ON transcript_segments(transcript_id);
