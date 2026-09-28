# ATS Scoring Engine

## 1. Overview

The ATS Scoring Engine is the scoring layer of the AI Job Portal.

Its purpose is to calculate a transparent and explainable candidate-job compatibility score using multiple independent scoring components.

The engine combines:

1. Skill Match
2. Experience Relevance
3. Education Alignment
4. Semantic Similarity

The final score is calculated on a 0-100 scale.

The scoring system is designed to be:

- Explainable
- Configurable
- Role-aware
- Robust to missing data
- Modular
- Reproducible

---

# 2. Objective

The primary objective of the ATS Scoring Engine is to convert the outputs of the previous AI Job Portal modules into a structured candidate score.

The engine should answer:

> How strongly does a candidate's profile align with the requirements of a specific job?

The score is not based on a single keyword comparison.

Instead, multiple evidence sources are combined to produce the final score.

---

# 3. Scoring Architecture

The Day 13 scoring architecture contains four major components.

```text
                    Candidate Resume
                           |
                           |
             +-------------+-------------+
             |                           |
       Resume Processing            JD Processing
             |                           |
             +-------------+-------------+
                           |
                           v
                  ATS Scoring Engine
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
   Skill Match       Experience         Education
                     Relevance          Alignment
        |                  |                  |
        +------------------+------------------+
                           |
                           v
                 Semantic Similarity
                           |
                           v
                Dynamic Weight System
                           |
                           v
                 Weighted Contributions
                           |
                           v
                  Final ATS Score
                       0 - 100