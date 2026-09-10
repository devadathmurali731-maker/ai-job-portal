# AI Job Portal – AI Data Entity Design

## 1. Document Overview

This document defines the standardized data entities used by the AI Job Portal.

The purpose of this design is to convert unstructured resumes and job descriptions into structured data that can be processed by AI and machine learning systems.

The four core entities are:

1. Candidate Profile
2. Job Profile
3. Skill Object
4. Experience Object

These entities provide the foundation for resume parsing, job matching, candidate ranking, skill analysis, and recommendation systems.

---

# 2. Candidate Profile

## 2.1 Definition

A Candidate Profile represents a job seeker and contains standardized information extracted from their resume.

## 2.2 Purpose

The Candidate Profile allows the AI system to understand:

- Who the candidate is
- What skills they have
- Their professional experience
- Their educational qualifications
- Their certifications
- Their preferred job roles

## 2.3 Attributes

| Attribute | Description | Data Type |
|---|---|---|
| candidate_id | Unique identifier for the candidate | String |
| name | Candidate's full name | String |
| email | Candidate email address | String |
| phone | Candidate contact number | String |
| location | Candidate location | String |
| summary | Professional summary | String |
| total_experience_years | Total professional experience | Number |
| preferred_roles | Roles preferred by candidate | Array |
| skills | List of candidate skills | Array |
| experience | Professional experience records | Array |
| education | Educational qualifications | Array |
| certifications | Professional certifications | Array |

## 2.4 Example

```json
{
  "candidate_id": "CAND_001",
  "name": "Arun Kumar",
  "location": "India",
  "summary": "Data Scientist with experience in machine learning and data analysis.",
  "total_experience_years": 3,
  "preferred_roles": [
    "Data Scientist",
    "Machine Learning Engineer"
  ]
}