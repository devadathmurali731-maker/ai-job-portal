from certification_parser import (
    normalize_certification_name,
    extract_provider,
    detect_relevance_category,
    parse_certification,
    parse_certifications
)


def test_normalize_certification_name():
    result = normalize_certification_name(
        "  Oracle   Java   Certification  "
    )

    assert result == "Oracle Java Certification"


def test_extract_provider():
    assert extract_provider("Oracle Java Certification") == "Oracle"
    assert extract_provider("Docker Certified Associate") == "Docker"
    assert extract_provider("AWS Certified Cloud Practitioner") == "AWS"
    assert extract_provider("Some Unknown Certification") == "Unknown"


def test_detect_relevance_category():
    assert detect_relevance_category(
        "Oracle Java Certification"
    ) == "Programming"

    assert detect_relevance_category(
        "Docker Certified Associate"
    ) == "DevOps"

    assert detect_relevance_category(
        "AWS Certified Cloud Practitioner"
    ) == "Cloud"

    assert detect_relevance_category(
        "Machine Learning Certification"
    ) == "Machine Learning"


def test_parse_certification():
    result = parse_certification(
        "Oracle Java Certification"
    )

    assert result["certification_name"] == "Oracle Java Certification"
    assert result["provider"] == "Oracle"
    assert result["relevance_category"] == "Programming"


def test_parse_certifications():
    certifications = [
        "Oracle Java Certification",
        "Docker Certified Associate"
    ]

    result = parse_certifications(certifications)

    assert len(result) == 2

    assert result[0]["certification_name"] == "Oracle Java Certification"
    assert result[0]["provider"] == "Oracle"
    assert result[0]["relevance_category"] == "Programming"

    assert result[1]["certification_name"] == "Docker Certified Associate"
    assert result[1]["provider"] == "Docker"
    assert result[1]["relevance_category"] == "DevOps"


def test_empty_certifications():
    result = parse_certifications([])

    assert result == []


def test_blank_certification_is_ignored():
    result = parse_certifications([
        "",
        "   ",
        "Python Certification"
    ])

    assert len(result) == 1
    assert result[0]["certification_name"] == "Python Certification"
    