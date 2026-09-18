"""
Skill Extraction Engine

Day 9 - AI Job Portal

This module:
1. Loads the master skill dictionary.
2. Extracts technical, business and creative skills.
3. Handles skill synonyms.
4. Handles skill stacks such as MERN and MEAN.
5. Handles common spelling variations.
6. Deduplicates extracted skills.
7. Assigns confidence scores.
"""

import json
import re
from pathlib import Path
from difflib import SequenceMatcher


# ---------------------------------------------------------
# File location
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DICTIONARY_FILE = BASE_DIR / "master_skill_dictionary.json"


# ---------------------------------------------------------
# Load master skill dictionary
# ---------------------------------------------------------

def load_skill_dictionary():
    """Load the master skill dictionary."""

    with open(DICTIONARY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------
# Normalize skill
# ---------------------------------------------------------

def normalize_skill(skill):
    """
    Normalize a skill name for comparison.

    Example:
        "Power-BI" -> "power bi"
        " PYTHON " -> "python"
    """

    if not skill:
        return ""

    skill = skill.lower().strip()

    skill = skill.replace("&", "and")
    skill = skill.replace("-", " ")
    skill = skill.replace("_", " ")

    skill = re.sub(r"[^\w\s.#+]", " ", skill)

    skill = " ".join(skill.split())

    return skill


# ---------------------------------------------------------
# Build skill lookup
# ---------------------------------------------------------

def build_skill_lookup(skill_dictionary):
    """Create normalized skill lookup."""

    lookup = {}

    for category, groups in skill_dictionary.items():

        if category in ["synonyms", "skill_stacks"]:
            continue

        for skills in groups.values():

            for skill in skills:

                normalized = normalize_skill(skill)

                lookup[normalized] = skill

    return lookup


# ---------------------------------------------------------
# Build synonym lookup
# ---------------------------------------------------------

def build_synonym_lookup(skill_dictionary):
    """Create normalized synonym lookup."""

    synonyms = skill_dictionary.get("synonyms", {})

    lookup = {}

    for synonym, canonical_skill in synonyms.items():

        normalized_synonym = normalize_skill(synonym)

        lookup[normalized_synonym] = canonical_skill

    return lookup


# ---------------------------------------------------------
# Exact skill matching
# ---------------------------------------------------------

def find_exact_skills(text, skill_dictionary):
    """Find skills that directly appear in the text."""

    lookup = build_skill_lookup(skill_dictionary)

    normalized_text = normalize_skill(text)

    extracted = []

    for normalized_skill, canonical_skill in lookup.items():

        pattern = rf"(?<!\w){re.escape(normalized_skill)}(?!\w)"

        if re.search(pattern, normalized_text):

            extracted.append(
                (canonical_skill, 0.99)
            )

    return extracted


# ---------------------------------------------------------
# Synonym matching
# ---------------------------------------------------------

def find_synonym_skills(text, skill_dictionary):
    """
    Find skills through synonyms.

    Example:
        py -> Python
        ml -> Machine Learning
    """

    synonym_lookup = build_synonym_lookup(skill_dictionary)

    normalized_text = normalize_skill(text)

    extracted = []

    for synonym, canonical_skill in synonym_lookup.items():

        pattern = rf"(?<!\w){re.escape(synonym)}(?!\w)"

        if re.search(pattern, normalized_text):

            extracted.append(
                (canonical_skill, 0.95)
            )

    return extracted


# ---------------------------------------------------------
# Fuzzy spelling matching
# ---------------------------------------------------------

def find_fuzzy_skills(text, skill_dictionary, threshold=0.80):
    lookup = build_skill_lookup(skill_dictionary)

    words = re.findall(r"\b[\w+#.]+\b", text.lower())

    extracted = []

    for word in words:
        normalized_word = normalize_skill(word)

        if not normalized_word:
            continue

        for normalized_skill, canonical_skill in lookup.items():

            # Avoid fuzzy matching very short skills
            if len(normalized_skill) < 3:
                continue

            # Fuzzy matching is mainly useful for single-word skills
            if " " in normalized_skill:
                continue

            score = SequenceMatcher(
                None,
                normalized_word,
                normalized_skill
            ).ratio()

            if (
                score >= threshold
                and normalized_word != normalized_skill
            ):
                confidence = round(score, 2)

                extracted.append(
                    (canonical_skill, confidence)
                )

    return extracted

# ---------------------------------------------------------
# Skill stack detection
# ---------------------------------------------------------

def find_skill_stacks(text, skill_dictionary):
    """
    Detect technology stacks.

    Example:
        MERN

    becomes:

        MERN
        MongoDB
        Express.js
        React
        Node.js
    """

    stacks = skill_dictionary.get(
        "skill_stacks",
        {}
    )

    normalized_text = normalize_skill(text)

    extracted = []

    for stack_name, components in stacks.items():

        normalized_stack = normalize_skill(
            stack_name
        )

        pattern = (
            rf"(?<!\w)"
            rf"{re.escape(normalized_stack)}"
            rf"(?!\w)"
        )

        if re.search(pattern, normalized_text):

            extracted.append(
                (stack_name, 0.95)
            )

            for component in components:

                extracted.append(
                    (component, 0.90)
                )

    return extracted


# ---------------------------------------------------------
# Deduplicate skills
# ---------------------------------------------------------

def deduplicate_skills(skills):
    """
    Remove duplicate skills.

    If the same skill appears multiple times,
    keep the highest confidence score.
    """

    unique_skills = {}

    for skill, confidence in skills:

        normalized = normalize_skill(skill)

        if normalized not in unique_skills:

            unique_skills[normalized] = {
                "skill": skill,
                "confidence": confidence
            }

        else:

            if (
                confidence
                > unique_skills[normalized]["confidence"]
            ):

                unique_skills[normalized][
                    "confidence"
                ] = confidence

    return list(unique_skills.values())


# ---------------------------------------------------------
# Main skill extraction function
# ---------------------------------------------------------

def extract_skills(text):
    """
    Extract skills from resume text.

    Pipeline:

        Exact matching
        Synonym matching
        Fuzzy matching
        Stack detection
        Deduplication
    """

    if not text:

        return {
            "skills": []
        }

    skill_dictionary = load_skill_dictionary()

    extracted = []

    # 1. Exact matches
    extracted.extend(
        find_exact_skills(
            text,
            skill_dictionary
        )
    )

    # 2. Synonym matches
    extracted.extend(
        find_synonym_skills(
            text,
            skill_dictionary
        )
    )

    # 3. Spelling variations
    extracted.extend(
        find_fuzzy_skills(
            text,
            skill_dictionary
        )
    )

    # 4. Skill stacks
    extracted.extend(
        find_skill_stacks(
            text,
            skill_dictionary
        )
    )

    # 5. Deduplicate
    final_skills = deduplicate_skills(
        extracted
    )

    # Highest confidence first
    final_skills.sort(
        key=lambda item: item["confidence"],
        reverse=True
    )

    return {
        "skills": final_skills
    }


# ---------------------------------------------------------
# Command-line test
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_resume = """
    Software Engineer with experience in Pyhton, SQL,
    Power BI, Machine Learning and MERN stack.

    Worked with Git, Docker and MongoDB.
    """

    result = extract_skills(sample_resume)

    print("\nSkill Extraction Result")
    print("=" * 50)

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )