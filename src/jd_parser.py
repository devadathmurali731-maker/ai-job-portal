from pathlib import Path
import re
import json
SKILL_SYNONYMS = {
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",

    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",

    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",

    "powerbi": "Power BI",
    "power bi": "Power BI",

    "ms excel": "Microsoft Excel",
    "excel": "Microsoft Excel",

    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn"
}

ROLE_SYNONYMS = {
    "ml engineer": "Machine Learning Engineer",
    "machine learning engineer": "Machine Learning Engineer",

    "data scientist": "Data Scientist",

    "data analyst": "Data Analyst",

    "bi analyst": "Business Intelligence Analyst",
    "business intelligence analyst": "Business Intelligence Analyst",

    "business analyst": "Business Analyst",

    "software developer": "Software Engineer",
    "software engineer": "Software Engineer",

    "hr exec": "HR Executive",
    "hr executive": "HR Executive"
}
KNOWN_SKILLS = [
    "Python",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "Power BI",
    "Microsoft Excel",
    "Tableau",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "XGBoost",
    "AWS",
    "Azure",
    "Docker",
    "Git",
    "GitHub",
    "Statistics",
    "Data Analysis",
    "Data Visualization",
    "Communication",
    "Recruitment",
    "Talent Acquisition",
    "Payroll"
]

KNOWN_EDUCATION = [
    "Bachelor's degree",
    "B.Tech",
    "B.E.",
    "B.Sc",
    "BCA",
    "Master's degree",
    "M.Tech",
    "M.E.",
    "M.Sc",
    "MCA",
    "MBA",
    "PhD",
    "Doctorate"
]

EDUCATION_FIELDS = [
    "Computer Science",
    "Information Technology",
    "Data Science",
    "Statistics",
    "Mathematics",
    "Economics",
    "Engineering",
    "Business Administration",
    "Human Resources",
    "Finance",
    "Commerce"
]

def normalize_jd_text(text):
    """
    Clean and normalize job description text.
    """

    # Normalize different bullet symbols
    text = re.sub(r"^[•▪◦●*]\s*", "- ", text, flags=re.MULTILINE)

    # Normalize different dash characters
    text = re.sub(
        r"[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]",
        "-",
        text
    )

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove extra spaces
    text = re.sub(r"[ ]+", " ", text)

    # Remove unnecessary spaces at the beginning/end of lines
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines)

def extract_role_name(text):
    """
    Extract and normalize the job role from the JD.
    """

    text_lower = text.lower()

    # First check for role names mentioned in the text
    for role, normalized_role in ROLE_SYNONYMS.items():

        if role in text_lower:
            return normalized_role

    return "Unknown"

def extract_required_skills(text):
    """
    Extract skills from the required skills section.
    """

    required_skills = []

    # Find the required skills section
    match = re.search(
        r"required skills\s*(.*?)(?=\npreferred skills|\neducation|\nresponsibilities|\ncertifications|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return required_skills

    required_text = match.group(1).lower()

    # Check known skills
    for skill in KNOWN_SKILLS:

        if skill.lower() in required_text:

            normalized_skill = normalize_skill_name(skill)

            if normalized_skill not in required_skills:
                required_skills.append(normalized_skill)

    # Check skill synonyms
    for synonym, standard_skill in SKILL_SYNONYMS.items():

        if synonym in required_text:

            if standard_skill not in required_skills:
                required_skills.append(standard_skill)

    return required_skills

def extract_preferred_skills(text):
    """
    Extract skills from the preferred skills section.
    """

    preferred_skills = []

    # Find the preferred skills section
    match = re.search(
        r"preferred skills\s*(.*?)(?=\neducation|\nresponsibilities|\ncertifications|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        return preferred_skills

    preferred_text = match.group(1).lower()

    # Check known skills
    for skill in KNOWN_SKILLS:

        if skill.lower() in preferred_text:

            normalized_skill = normalize_skill_name(skill)

            if normalized_skill not in preferred_skills:
                preferred_skills.append(normalized_skill)

    # Check skill synonyms
    for synonym, standard_skill in SKILL_SYNONYMS.items():

        if synonym in preferred_text:

            if standard_skill not in preferred_skills:
                preferred_skills.append(standard_skill)

    return preferred_skills

def extract_experience(text):
    """
    Extract experience requirements from the job description.
    """

    text_lower = text.lower()

    minimum_years = None
    maximum_years = None
    is_fresher_allowed = False

    # Check whether freshers are allowed
    fresher_patterns = [
        "freshers can apply",
        "freshers welcome",
        "freshers are welcome",
        "no experience required",
        "0 years of experience"
    ]

    for pattern in fresher_patterns:
        if pattern in text_lower:
            is_fresher_allowed = True
            minimum_years = 0
            break

    # Look for experience ranges such as 2-4 years
    range_match = re.search(
        r"(\d+)\s*[-–]\s*(\d+)\s*(?:years?|yrs?)",
        text_lower
    )

    if range_match:
        minimum_years = int(range_match.group(1))
        maximum_years = int(range_match.group(2))

    else:
        # Look for minimum experience such as 2+ years
        plus_match = re.search(
            r"(\d+)\s*\+\s*(?:years?|yrs?)",
            text_lower
        )

        if plus_match:
            minimum_years = int(plus_match.group(1))

        else:
            # Look for statements such as "minimum 2 years"
            minimum_match = re.search(
                r"(?:minimum|at least)\s*(\d+)\s*(?:years?|yrs?)",
                text_lower
            )

            if minimum_match:
                minimum_years = int(minimum_match.group(1))

            else:
                # Look for simple statements such as "3 years of experience"
                simple_match = re.search(
                    r"(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*(?:relevant\s*)?experience",
                    text_lower
                )

                if simple_match:
                    minimum_years = int(simple_match.group(1))

    return {
        "minimum_years": minimum_years,
        "maximum_years": maximum_years,
        "is_fresher_allowed": is_fresher_allowed
    }

def extract_education(text):
    """
    Extract education qualifications and fields from the job description.
    """

    text_lower = text.lower()

    required_education = []
    preferred_education = []
    fields_of_study = []

    # Education section
    education_match = re.search(
        r"education\s*(.*?)(?=\nresponsibilities|\ncertifications|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if education_match:
        education_text = education_match.group(1).lower()
    else:
        education_text = text_lower

    # Handle Bachelor's
    if "bachelor's" in education_text or "bachelor" in education_text:
        if "preferred" in education_text:
            preferred_education.append("Bachelor's degree")
        else:
            required_education.append("Bachelor's degree")

    # Handle Master's
    if "master's" in education_text or "master" in education_text:
        if "preferred" in education_text:
            preferred_education.append("Master's degree")
        else:
            required_education.append("Master's degree")

    # Check other education qualifications
    for education in KNOWN_EDUCATION:

        education_lower = education.lower()

        if education_lower in education_text:

            if education not in required_education and education not in preferred_education:

                preferred_context = re.search(
                    rf"(preferred|preferably|desired|nice to have).{{0,100}}{re.escape(education_lower)}",
                    education_text
                )

                if preferred_context:
                    preferred_education.append(education)
                else:
                    required_education.append(education)

    # Extract fields of study
    for field in EDUCATION_FIELDS:

        if field.lower() in education_text:

            if field not in fields_of_study:
                fields_of_study.append(field)

    return {
        "required": list(dict.fromkeys(required_education)),
        "preferred": list(dict.fromkeys(preferred_education)),
        "fields_of_study": list(dict.fromkeys(fields_of_study))
    }

def normalize_skill_name(skill):
    """
    Convert a skill name into its standard form.
    """

    skill_lower = skill.strip().lower()

    return SKILL_SYNONYMS.get(skill_lower, skill.strip())
def normalize_role_name(role):
    """
    Convert a role name into its standard form.
    """

    role_lower = role.strip().lower()

    return ROLE_SYNONYMS.get(role_lower, role.strip())

def parse_job_description(text):
    """
    Convert a raw job description into a structured JD profile.
    """

    # Step 1: Normalize the JD text
    normalized_text = normalize_jd_text(text)

    # Step 2: Extract role
    role = extract_role_name(normalized_text)

    # Step 3: Extract required skills
    required_skills = extract_required_skills(normalized_text)

    # Step 4: Extract preferred skills
    preferred_skills = extract_preferred_skills(normalized_text)

    # Step 5: Extract experience
    experience = extract_experience(normalized_text)

    # Step 6: Extract education
    education = extract_education(normalized_text)

    # Step 7: Create structured JD profile
    jd_profile = {
        "role": role,

        "skills": {
            "required": required_skills,
            "preferred": preferred_skills
        },

        "experience": experience,

        "education": education,

        "normalized_text": normalized_text
    }

    return jd_profile


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

JD_DIR = BASE_DIR / "job_descriptions"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "jd_profiles"


def process_all_job_descriptions():
    """
    Read all JD text files, parse them,
    and save structured JSON profiles.
    """

    # Create output directory if it does not exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all JD text files
    jd_files = sorted(JD_DIR.glob("*.txt"))

    print(f"Found {len(jd_files)} job descriptions.")

    for jd_file in jd_files:

        print(f"Processing: {jd_file.name}")

        # Read JD text
        text = jd_file.read_text(
            encoding="utf-8"
        )

        # Parse JD
        jd_profile = parse_job_description(text)

        # Create JSON output filename
        output_file = OUTPUT_DIR / f"{jd_file.stem}.json"

        # Save structured profile
        output_file.write_text(
            json.dumps(
                jd_profile,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        print(f"Saved: {output_file.name}")


if __name__ == "__main__":
    process_all_job_descriptions()