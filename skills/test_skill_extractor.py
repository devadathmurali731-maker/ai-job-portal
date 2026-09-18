import json
from pathlib import Path

from skill_extractor import (
    load_skill_dictionary,
    normalize_skill,
    build_skill_lookup,
    build_synonym_lookup,
    find_exact_skills,
    find_synonym_skills,
    find_fuzzy_skills,
    find_skill_stacks,
    deduplicate_skills,
    extract_skills
)


# ---------------------------------------------------------
# Test 1 - Dictionary exists
# ---------------------------------------------------------

def test_skill_dictionary_exists():

    dictionary_path = Path(
        "skills/master_skill_dictionary.json"
    )

    assert dictionary_path.exists()


# ---------------------------------------------------------
# Test 2 - Dictionary is valid JSON
# ---------------------------------------------------------

def test_skill_dictionary_is_valid():

    dictionary_path = Path(
        "skills/master_skill_dictionary.json"
    )

    with open(
        dictionary_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    assert isinstance(data, dict)


# ---------------------------------------------------------
# Test 3 - Required categories exist
# ---------------------------------------------------------

def test_required_categories_exist():

    dictionary = load_skill_dictionary()

    assert "technical" in dictionary
    assert "business" in dictionary
    assert "creative" in dictionary
    assert "synonyms" in dictionary
    assert "skill_stacks" in dictionary


# ---------------------------------------------------------
# Test 4 - Skill normalization
# ---------------------------------------------------------

def test_normalize_skill():

    assert normalize_skill(
        " Power-BI "
    ) == "power bi"


# ---------------------------------------------------------
# Test 5 - Skill lookup
# ---------------------------------------------------------

def test_skill_lookup():

    dictionary = load_skill_dictionary()

    lookup = build_skill_lookup(
        dictionary
    )

    assert "python" in lookup
    assert lookup["python"] == "Python"


# ---------------------------------------------------------
# Test 6 - Synonym lookup
# ---------------------------------------------------------

def test_synonym_lookup():

    dictionary = load_skill_dictionary()

    lookup = build_synonym_lookup(
        dictionary
    )

    assert lookup["py"] == "Python"
    assert lookup["ml"] == "Machine Learning"


# ---------------------------------------------------------
# Test 7 - Exact skill extraction
# ---------------------------------------------------------

def test_exact_skill_extraction():

    dictionary = load_skill_dictionary()

    text = """
    Experienced in Python, SQL and Power BI.
    """

    results = find_exact_skills(
        text,
        dictionary
    )

    skills = [
        skill
        for skill, confidence in results
    ]

    assert "Python" in skills
    assert "SQL" in skills
    assert "Power BI" in skills


# ---------------------------------------------------------
# Test 8 - Synonym extraction
# ---------------------------------------------------------

def test_synonym_skill_extraction():

    dictionary = load_skill_dictionary()

    text = """
    Experienced in py, ml and powerbi.
    """

    results = find_synonym_skills(
        text,
        dictionary
    )

    skills = [
        skill
        for skill, confidence in results
    ]

    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "Power BI" in skills


# ---------------------------------------------------------
# Test 9 - Fuzzy spelling detection
# ---------------------------------------------------------

def test_fuzzy_skill_extraction():

    dictionary = load_skill_dictionary()

    text = """
    Experienced in Pyhton.
    """

    results = find_fuzzy_skills(
        text,
        dictionary
    )

    skills = [
        skill
        for skill, confidence in results
    ]

    assert "Python" in skills


# ---------------------------------------------------------
# Test 10 - MERN stack detection
# ---------------------------------------------------------

def test_skill_stack_detection():

    dictionary = load_skill_dictionary()

    text = """
    Full-stack developer with experience in MERN.
    """

    results = find_skill_stacks(
        text,
        dictionary
    )

    skills = [
        skill
        for skill, confidence in results
    ]

    assert "MERN" in skills
    assert "MongoDB" in skills
    assert "Express.js" in skills
    assert "React" in skills
    assert "Node.js" in skills


# ---------------------------------------------------------
# Test 11 - Deduplication
# ---------------------------------------------------------

def test_skill_deduplication():

    skills = [
        ("Python", 0.99),
        ("Python", 0.95),
        ("Python", 0.88),
        ("SQL", 0.99)
    ]

    results = deduplicate_skills(
        skills
    )

    assert len(results) == 2

    python_result = next(
        item
        for item in results
        if item["skill"] == "Python"
    )

    assert python_result["confidence"] == 0.99


# ---------------------------------------------------------
# Test 12 - Complete extraction
# ---------------------------------------------------------

def test_complete_skill_extraction():

    text = """
    Software Engineer with experience in Python,
    SQL, Power BI, Machine Learning and MERN.

    Worked with Docker and Git.
    """

    result = extract_skills(text)

    assert "skills" in result
    assert isinstance(
        result["skills"],
        list
    )

    skills = [
        item["skill"]
        for item in result["skills"]
    ]

    assert "Python" in skills
    assert "SQL" in skills
    assert "Power BI" in skills
    assert "Machine Learning" in skills
    assert "MERN" in skills
    assert "MongoDB" in skills
    assert "Docker" in skills
    assert "Git" in skills


# ---------------------------------------------------------
# Test 13 - Confidence scoring
# ---------------------------------------------------------

def test_confidence_scores():

    text = """
    Python, SQL and Power BI
    """

    result = extract_skills(text)

    for item in result["skills"]:

        assert "confidence" in item

        assert (
            0 <= item["confidence"] <= 1
        )


# ---------------------------------------------------------
# Test 14 - Empty input
# ---------------------------------------------------------

def test_empty_input():

    result = extract_skills("")

    assert result == {
        "skills": []
    }
    