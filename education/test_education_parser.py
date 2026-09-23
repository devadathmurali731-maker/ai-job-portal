from education_parser import (
    normalize_degree,
    extract_graduation_year,
    extract_degree_and_field,
    parse_education_section
)


def test_normalize_degree():
    assert normalize_degree("B.Tech") == "Bachelor of Technology"
    assert normalize_degree("M.Sc") == "Master of Science"
    assert normalize_degree("MBA") == "Master of Business Administration"


def test_extract_graduation_year():
    assert extract_graduation_year("2022") == 2022
    assert extract_graduation_year("Graduated in 2024") == 2024
    assert extract_graduation_year("No year available") is None


def test_extract_degree_and_field():
    result = extract_degree_and_field(
        "B.Tech in Computer Science and Engineering"
    )

    assert result["degree_type"] == "Bachelor of Technology"
    assert result["field_of_study"] == "Computer Science and Engineering"


def test_extract_master_degree():
    result = extract_degree_and_field(
        "M.Sc in Data Science"
    )

    assert result["degree_type"] == "Master of Science"
    assert result["field_of_study"] == "Data Science"


def test_parse_education_section():
    education = [
        "B.Tech in Computer Science and Engineering",
        "XYZ University",
        "2022"
    ]

    result = parse_education_section(education)

    assert len(result) == 1
    assert result[0]["degree_type"] == "Bachelor of Technology"
    assert result[0]["field_of_study"] == "Computer Science and Engineering"
    assert result[0]["institution"] == "XYZ University"
    assert result[0]["graduation_year"] == 2022
    