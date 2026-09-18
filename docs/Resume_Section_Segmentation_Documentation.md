# Day 8 – Resume Section Segmentation Documentation

## 1. Objective

The objective of Day 8 is to automatically identify and separate major sections of a resume.

Resume documents contain information in different sections such as:

* Summary
* Skills
* Work Experience
* Education
* Certifications
* Projects
* Achievements
* Languages
* Interests

Separating these sections makes the resume data easier for downstream AI systems to process.

The segmented resume can later be used by:

* ATS scoring
* Candidate screening
* Resume-job matching
* Candidate profiling
* Interview generation
* Skill extraction
* Experience analysis

---

## 2. Problem Statement

A resume is usually an unstructured document.

For example, a resume may contain:

```text
PROFESSIONAL SUMMARY

Software Engineer with 4 years of experience...

TECHNICAL SKILLS

Python
SQL
Docker
Git

WORK EXPERIENCE

ABC Technologies
Software Engineer
2022 - Present

EDUCATION

B.Tech in Computer Science
XYZ University
```

An AI system should not treat this entire document as one large block of text.

Instead, it should understand:

```text
Summary → Professional summary

Skills → Python, SQL, Docker, Git

Work Experience → Company, role, dates and responsibilities

Education → Degree and university
```

Therefore, the Resume Section Segmentation module converts unstructured resume text into structured sections.

---

## 3. Implementation File

The main implementation is:

```text
src/resume_section_classifier.py
```

The testing file is:

```text
src/test_section_classifier.py
```

---

## 4. Supported Resume Sections

The system recognizes the following major sections.

### Core Sections

```text
skills
work_experience
education
certifications
projects
```

### Additional Sections

```text
summary
objective
achievements
awards
languages
interests
references
```

The additional sections improve the system's ability to handle different resume formats.

---

## 5. Section Heading Detection

Different resumes use different names for the same section.

For example, a Skills section may appear as:

```text
Skills
Technical Skills
Core Skills
Key Skills
Technical Expertise
Skill Set
```

Similarly, Work Experience may appear as:

```text
Work Experience
Professional Experience
Employment History
Work History
Career Experience
Professional Background
```

The classifier maintains a list of alternative headings for each standard section.

Example:

```python
SECTION_HEADINGS = {
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "technical proficiencies",
        "skill set"
    ]
}
```

This allows different resume formats to be mapped to the same standardized section name.

---

## 6. Heading Normalization

Before classifying a heading, the system normalizes it.

The normalization process:

1. Removes leading and trailing spaces.
2. Converts text to lowercase.
3. Removes section numbering.
4. Converts `&` to `and`.
5. Converts hyphens to spaces.
6. Converts underscores to spaces.
7. Removes unnecessary punctuation.
8. Removes extra spaces.

For example:

```text
1. Technical Skills
```

becomes:

```text
technical skills
```

Another example:

```text
LICENSES & CERTIFICATIONS
```

becomes:

```text
licenses and certifications
```

This makes heading comparison more reliable.

---

## 7. Exact Heading Matching

After normalization, the classifier first performs exact matching.

For example:

```text
Technical Skills
```

is normalized to:

```text
technical skills
```

The system checks this against its known heading list and maps it to:

```text
skills
```

Exact matching is fast and reliable when the heading is known.

---

## 8. Fuzzy Heading Matching

Resume headings may contain small spelling or formatting differences.

Therefore, the system also supports fuzzy matching using:

```python
SequenceMatcher
```

from Python's:

```python
difflib
```

library.

The system calculates similarity between the detected heading and known headings.

A similarity threshold of:

```text
0.75
```

is used.

For example, a slightly different heading such as:

```text
Tech Skills
```

can potentially be matched with:

```text
Technical Skills
```

when the similarity is sufficiently high.

This improves robustness against variations in resume formatting.

---

## 9. Content-Based Section Detection

Some resumes may not contain clear section headings.

For example:

```text
Python
SQL
Machine Learning
Power BI
Docker
```

may appear without a heading such as `Skills`.

To handle this situation, the system uses content-based detection.

The classifier checks for representative keywords.

### Skills

Examples:

```text
Python
SQL
Machine Learning
Docker
Git
Power BI
Tableau
```

### Education

Examples:

```text
B.Tech
Bachelor
Master
University
College
Degree
```

### Work Experience

Examples:

```text
Software Engineer
Data Analyst
Data Scientist
Developer
Manager
Intern
Present
Years of experience
```

### Projects

Examples:

```text
Project
Developed
Prediction
Classification
Forecasting
Dashboard
```

This provides a fallback mechanism when explicit section headings are missing.

---

## 10. Handling Resumes With Headings

When a resume contains recognized section headings, the system primarily relies on those headings to determine section boundaries.

For example:

```text
SUMMARY
...

SKILLS
Python
SQL
Docker

WORK EXPERIENCE
ABC Technologies
Software Engineer

EDUCATION
B.Tech
XYZ University
```

The system produces:

```json
{
    "summary": [...],
    "skills": [...],
    "work_experience": [...],
    "education": [...]
}
```

This prevents content keywords from incorrectly moving text between already identified sections.

---

## 11. Handling Resumes Without Headings

When no recognized section headings are found, the system enables content-based detection.

For example:

```text
Python
SQL
Machine Learning

B.Tech Computer Science
XYZ University

Software Engineer
ABC Technologies
2022 - Present
```

The system analyzes the content and attempts to assign each block to an appropriate section.

This is useful for resumes with unusual or minimal formatting.

---

## 12. Handling Table-Style Resumes

Resume information may be extracted from DOCX or PDF tables.

After text extraction, the table contents are represented as text lines.

The segmentation module processes these lines just like other extracted text.

This allows table-based resumes to be passed into the same section classification pipeline.

The project was tested using table-style resume inputs.

---

## 13. Handling Different Resume Layouts

The system is designed to work with different extracted resume layouts, including:

* Normal text resumes
* Bullet-based resumes
* Table-style resumes
* Resumes with alternative headings
* Resumes with missing headings
* Resumes with slightly different heading spellings

The system operates on cleaned text generated by the Resume Text Extraction Engine developed in Day 5.

---

## 14. Section Segmentation Process

The overall process is:

```text
Raw Resume
     ↓
Resume Text Extraction
     ↓
Cleaned Resume Text
     ↓
Heading Normalization
     ↓
Exact Heading Matching
     ↓
Fuzzy Heading Matching
     ↓
Content-Based Detection
     ↓
Section Classification
     ↓
Structured JSON Output
```

---

## 15. Output Format

The segmented resume is stored as JSON.

Example:

```json
{
    "summary": [
        "Software Engineer with 4 years of experience building backend applications and REST APIs."
    ],
    "skills": [
        "Java",
        "Python",
        "SQL",
        "Spring Boot",
        "REST APIs",
        "Git",
        "Docker"
    ],
    "work_experience": [
        "ABC Technologies",
        "Software Engineer",
        "2022 - Present",
        "- Developed REST APIs using Spring Boot."
    ],
    "education": [
        "B.Tech in Computer Science and Engineering",
        "XYZ University",
        "2022"
    ],
    "certifications": [
        "Oracle Java Certification",
        "Docker Certified Associate"
    ]
}
```

---

## 16. Output Location

The generated segmented resume files are stored in:

```text
data/processed/segmented/
```

Current output files:

```text
resume_001_sections.json
resume_002_sections.json
resume_003_sections.json
resume_004_sections.json
```

---

## 17. Testing

The section segmentation system contains unit and integration tests.

Test file:

```text
src/test_section_classifier.py
```

The tests cover:

* Heading normalization
* Skills classification
* Work experience classification
* Education classification
* Projects classification
* Certifications classification
* Unknown headings
* Resume segmentation
* Real resume files
* Multiple resume files
* Alternative section headings
* Content-based section detection
* Resumes without section headings
* Table-style resumes
* Fuzzy heading matching
* JSON output validation

---

## 18. Test Results

The complete project test suite was executed using:

```powershell
python -m pytest -v
```

Result:

```text
28 passed in 22.29s
```

There were:

```text
28 tests passed
0 tests failed
```

The Day 8 section segmentation tests successfully passed along with the existing Day 6 JD parser and project tests.

---

## 19. Example Segmented Resume

For `resume_001.txt`, the generated structure contains:

```text
summary
skills
work_experience
education
certifications
```

The sections are stored independently so that downstream AI components can access only the information they require.

For example:

```text
ATS Engine
    ↓
Skills + Work Experience + Education
```

Candidate screening can use:

```text
Skills + Work Experience + Projects
```

Interview generation can use:

```text
Skills + Work Experience + Projects
```

---

## 20. Role in the AI Job Portal

Resume Section Segmentation is an important preprocessing stage.

The overall pipeline becomes:

```text
Resume File
     ↓
Text Extraction
     ↓
Text Cleaning
     ↓
Section Segmentation
     ↓
Structured Resume
     ↓
Resume Profile
     ↓
ATS Matching
     ↓
Candidate Screening
     ↓
Interview Generation
```

The segmentation stage improves the quality of information provided to downstream AI modules.

---

## 21. Benefits

The segmentation system provides several benefits:

### Structured Data

Unstructured resume text becomes organized into meaningful sections.

### Better AI Processing

AI models can process relevant sections separately.

### Improved Matching

Skills and experience can be compared against job requirements more effectively.

### Reusability

The same segmented resume can be used by multiple modules.

### Robustness

The system supports multiple heading variations and some resumes without explicit headings.

### Explainability

The system can show where information came from within the resume.

---

## 22. Limitations

The current implementation is a prototype rule-based and lightweight NLP approach.

Content-based detection relies on predefined keywords.

Therefore, highly unusual resumes may require additional logic.

Fuzzy matching can also produce incorrect classifications when two headings are very similar.

Complex multi-column PDF layouts may require more advanced document-layout analysis.

Future versions can improve this using:

* NLP-based classification
* Named Entity Recognition
* Transformer-based models
* Layout-aware document models
* PDF coordinate analysis
* Machine-learning-based section classification

---

## 23. Future Improvements

Potential improvements include:

1. Machine-learning-based section classification.
2. Transformer-based resume understanding.
3. Better multi-column detection.
4. Layout-aware PDF processing.
5. Semantic similarity instead of keyword matching.
6. Automatic section confidence scores.
7. Detection of additional sections.
8. Improved handling of unusual resume formats.
9. Integration with the Resume Profile Generator.
10. Integration with ATS and candidate screening modules.

---

## 24. Day 8 Deliverables

The following deliverables have been completed:

### Source Code

```text
src/resume_section_classifier.py
```

### Test Code

```text
src/test_section_classifier.py
```

### Segmented Resume Outputs

```text
data/processed/segmented/
```

Containing:

```text
resume_001_sections.json
resume_002_sections.json
resume_003_sections.json
resume_004_sections.json
```

### Documentation

```text
docs/Resume_Section_Segmentation_Documentation.md
```

### Validation

```text
28 passed in 22.29s
```

---

## 25. Conclusion

The Resume Section Segmentation module successfully converts cleaned resume text into structured sections.

The system combines:

* Rule-based heading detection
* Heading normalization
* Exact matching
* Fuzzy matching
* Content-based detection
* Support for missing headings
* Support for table-style extracted text
* JSON-based structured output

This provides a structured foundation for the next stages of the AI Job Portal, including resume profiling, ATS matching, candidate screening, and AI-powered interview generation.
