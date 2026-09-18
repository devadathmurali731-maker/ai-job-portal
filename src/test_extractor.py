from pathlib import Path
import logging

from resume_extractor import (
    extract_text,
    clean_text,
    normalize_bullets,
    normalize_section_headings,
    normalize_special_characters
)


# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of test resumes
RESUME_DIR = BASE_DIR / "data" / "raw_resumes"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
# Location for test logs
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "extraction_test.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("========== Resume Extraction Test Started ==========")


# Test every resume
for resume_file in RESUME_DIR.iterdir():

    if resume_file.suffix.lower() in [".docx", ".pdf"]:

        print("\n" + "=" * 60)
        print(f"FILE: {resume_file.name}")
        print("=" * 60)
        logging.info(f"Processing file: {resume_file.name}")
        extracted_text = extract_text(resume_file)
        cleaned_text = clean_text(extracted_text)
        normalized_text = normalize_bullets(cleaned_text)
        normalized_text = normalize_section_headings(normalized_text)
        final_text = normalize_special_characters(normalized_text)
        output_file = PROCESSED_DIR / f"{resume_file.stem}.txt"
        output_file.write_text(final_text, encoding="utf-8")
        logging.info(
    f"SUCCESS: {resume_file.name} -> {output_file.name}"
)
        print(final_text)
logging.info("========== Resume Extraction Test Completed ==========")

        


        



        
