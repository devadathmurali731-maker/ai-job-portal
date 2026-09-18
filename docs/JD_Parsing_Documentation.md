# Job Description Parsing System

## 1. Overview

The Job Description Parsing System converts unstructured job descriptions into structured, AI-readable job requirement profiles.

The system is designed to extract important information from job descriptions such as:

- Job role
- Required skills
- Preferred skills
- Experience requirements
- Education qualifications
- Fields of study
- Normalized job description text

The structured output is stored in JSON format and can later be used by the ATS engine and candidate-job matching system.

---

## 2. Objective

The main objective of the JD parsing system is to convert raw job description text into a standardized structure.

### Input

Raw job description:

```text
Job Title: Data Scientist

Required Skills:
- Python
- SQL
- Pandas
- NumPy
- Machine Learning

Preferred Skills:
- TensorFlow
- AWS

Experience:
2-5 years

Education:
Bachelor's or Master's degree