from pathlib import Path

from resume_extractor import (
    extract_text,
    clean_text,
    normalize_bullets,
    normalize_section_headings,
    normalize_special_characters
)


BASE_DIR = Path(__file__).resolve().parent.parent

RESUME_DIR = BASE_DIR / "data" / "raw_resumes"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def test_resume_directory_exists():
    assert RESUME_DIR.exists()
    assert RESUME_DIR.is_dir()


def test_resume_files_exist():
    resume_files = [
        file
        for file in RESUME_DIR.iterdir()
        if file.suffix.lower() in [".docx", ".pdf"]
    ]

    assert len(resume_files) > 0


def test_extract_text_from_resumes():
    resume_files = [
        file
        for file in RESUME_DIR.iterdir()
        if file.suffix.lower() in [".docx", ".pdf"]
    ]

    assert len(resume_files) > 0

    for resume_file in resume_files:
        extracted_text = extract_text(resume_file)

        assert extracted_text is not None
        assert isinstance(extracted_text, str)
        assert len(extracted_text.strip()) > 0


def test_clean_and_normalize_resume_text():
    resume_files = [
        file
        for file in RESUME_DIR.iterdir()
        if file.suffix.lower() in [".docx", ".pdf"]
    ]

    assert len(resume_files) > 0

    for resume_file in resume_files:
        extracted_text = extract_text(resume_file)

        cleaned_text = clean_text(extracted_text)
        normalized_text = normalize_bullets(cleaned_text)
        normalized_text = normalize_section_headings(normalized_text)
        final_text = normalize_special_characters(normalized_text)

        assert final_text is not None
        assert isinstance(final_text, str)
        assert len(final_text.strip()) > 0


def test_processed_directory_exists():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    assert PROCESSED_DIR.exists()
    assert PROCESSED_DIR.is_dir()