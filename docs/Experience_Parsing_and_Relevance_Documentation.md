# Day 10 – Experience Parsing & Relevance Engine

## 1. Objective

The objective of Day 10 is to understand a candidate's professional experience and convert it into a structured format that can be used by downstream AI-based recruitment components.

The system extracts:

- Company names
- Job titles
- Employment dates
- Employment duration
- Total professional experience
- Employment gaps
- Overlapping employment periods
- Experience relevance to a target role
- Role-to-role similarity

---

## 2. Architecture

```text
Segmented Resume
       |
       v
Work Experience Section
       |
       v
Experience Parser
       |
       v
Structured Experience
       |
       +----------------------+
       |                      |
       v                      v
Experience Metrics       Timeline Analysis
       |                      |
       |                +-----+------+
       |                |            |
       |                v            v
       |              Gaps        Overlaps
       |
       v
Experience Relevance
       |
       v
Keyword Matching
       |
       v
Role Similarity
       |
       v
Final Experience Profile