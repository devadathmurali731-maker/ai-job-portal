
import csv
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------
# 1. Project paths and imports
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ats_scoring.ats_scoring_engine import ATSScoringEngine

MANIFEST_PATH = (
    ROOT / "testing" / "day17" / "benchmark" / "candidate_manifest.csv"
)
JD_DIR = ROOT / "data" / "processed" / "jd_profiles"
RESULTS_DIR = ROOT / "testing" / "day17" / "results_after_msc_fix"


# --------------------------------------------------
# 2. File utilities
# --------------------------------------------------

def read_text(path):
    """Read a UTF-8 text file, supporting an optional BOM."""
    return path.read_text(encoding="utf-8-sig")


def extract_section(text, heading, all_headings):
    """Extract a section between its heading and the next known heading."""
    match = re.search(
        rf"(?im)^\s*{re.escape(heading)}\s*$",
        text,
    )

    if not match:
        return ""

    start = match.end()
    remaining = text[start:]
    next_positions = []

    for next_heading in all_headings:
        next_match = re.search(
            rf"(?im)^\s*{re.escape(next_heading)}\s*$",
            remaining,
        )

        if next_match:
            next_positions.append(next_match.start())

    end = min(next_positions) if next_positions else len(remaining)

    return remaining[:end].strip()


# --------------------------------------------------
# 3. Resume extraction
# --------------------------------------------------

def extract_candidate(text, resume_id):
    """Extract skills, experience, and education for ATS scoring."""

    headings = [
        "PROFESSIONAL SUMMARY",
        "SKILLS",
        "EXPERIENCE",
        "EDUCATION",
        "CERTIFICATIONS",
        "PROJECTS",
        "TOTAL EXPERIENCE",
        "PREFERRED ROLES",
    ]

    skills_text = extract_section(text, "SKILLS", headings)
    experience_text = extract_section(text, "EXPERIENCE", headings)
    education_text = extract_section(text, "EDUCATION", headings)
    total_text = extract_section(text, "TOTAL EXPERIENCE", headings)

    # Extract skills
    skills = []

    for line in skills_text.splitlines():
        line = line.strip()

        if line.startswith("-"):
            value = line.lstrip("- ").strip()

            if value:
                skills.append({
                    "skill": value,
                    "confidence": 1.0,
                })

    if not skills:
        raise ValueError(f"{resume_id}: no skills extracted")

    # Extract total experience
    years_match = re.search(
        r"(\d+(?:\.\d+)?)\s*years?",
        total_text,
        re.IGNORECASE,
    )

    if not years_match:
        raise ValueError(
            f"{resume_id}: could not extract total experience "
            f"from TOTAL EXPERIENCE section: {total_text!r}"
        )

    total_years = float(years_match.group(1))

    # Extract job title
    title_match = re.search(
        r"(?im)^\s*Designation:\s*(.+?)\s*$",
        experience_text,
    )

    job_title = title_match.group(1).strip() if title_match else ""

    # Extract responsibilities
    responsibility_match = re.search(
        r"(?is)Responsibilities:\s*(.*?)(?:\n\s*Skills Used:|\Z)",
        experience_text,
    )

    responsibilities = []

    if responsibility_match:
        for line in responsibility_match.group(1).splitlines():
            line = line.strip()

            if line.startswith("-"):
                responsibilities.append(line.lstrip("- ").strip())

    experience_data = {
        "resume_id": resume_id,
        "total_experience_years": total_years,
        "experiences": (
            [{
                "job_title": job_title,
                "responsibilities": responsibilities,
            }]
            if job_title
            else []
        ),
    }

    if not job_title:
        raise ValueError(f"{resume_id}: no designation extracted")

    # Extract education
    degree_match = re.search(
        r"(?im)^\s*Degree:\s*(.+?)\s*$",
        education_text,
    )

    field_match = re.search(
        r"(?im)^\s*Field:\s*(.+?)\s*$",
        education_text,
    )

    education_records = []

    if degree_match or field_match:
        education_records.append({
            "degree_type": (
                degree_match.group(1).strip()
                if degree_match
                else ""
            ),
            "field_of_study": (
                field_match.group(1).strip()
                if field_match
                else ""
            ),
        })

    if not education_records:
        raise ValueError(f"{resume_id}: no education extracted")

    education_data = {
        "resume_id": resume_id,
        "education": education_records,
    }

    return skills, experience_data, education_data


# --------------------------------------------------
# 4. Benchmark execution
# --------------------------------------------------

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load candidate manifest
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"Candidate manifest not found: {MANIFEST_PATH}"
        )

    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        candidates = list(csv.DictReader(handle))

    if not candidates:
        raise ValueError("Candidate manifest contains no candidates.")

    # Load available job profile paths
    jd_paths = sorted(JD_DIR.glob("jd_*.json"))

    if not jd_paths:
        raise FileNotFoundError(
            f"No job profiles found in: {JD_DIR}"
        )

    # Validate job profiles before benchmarking
    job_profiles = []

    for jd_path in jd_paths:
        try:
            jd = json.loads(read_text(jd_path))

            for required_key in ("role", "skills", "experience", "education"):
                if required_key not in jd:
                    raise ValueError(
                        f"Missing required field: {required_key}"
                    )

            job_profiles.append((jd_path, jd))

        except Exception as exc:
            print(f"INVALID JOB PROFILE | {jd_path.name} | {exc}")

    if not job_profiles:
        raise ValueError("No valid job profiles are available.")

    engine = ATSScoringEngine()

    summary_rows = []
    successful = 0
    failed = 0

    print("=" * 65)
    print("DAY 17 ATS BENCHMARK")
    print("=" * 65)
    print(f"Candidates: {len(candidates)}")
    print(f"Valid job profiles: {len(job_profiles)}")
    print(
        "Maximum candidate-job pairs: "
        f"{len(candidates) * len(job_profiles)}"
    )
    print()

    # Process every candidate
    for candidate in candidates:
        resume_id = candidate.get("resume_id", "").strip()
        candidate_name = candidate.get("candidate_name", "")
        source_file = candidate.get("source_file", "")
        role_category = candidate.get("role_category", "")

        if not resume_id or not source_file:
            error = "Missing resume_id or source_file in manifest."
            print(f"FAILED CANDIDATE | {candidate_name} | {error}")

            for jd_path, jd in job_profiles:
                failed += 1

                summary_rows.append({
                    "resume_id": resume_id,
                    "candidate_name": candidate_name,
                    "role_category": role_category,
                    "job_id": jd_path.stem,
                    "job_role": jd["role"],
                    "status": "invalid_manifest_entry",
                    "final_ats_score": "",
                    "semantic_similarity_status": "unavailable",
                    "error": error,
                })

            continue

        resume_path = ROOT / "resumes" / source_file

        # Extract resume once per candidate
        try:
            if not resume_path.exists():
                raise FileNotFoundError(
                    f"Resume not found: {resume_path}"
                )

            resume_text = read_text(resume_path)

            skills, experience_data, education_data = extract_candidate(
                resume_text,
                resume_id,
            )

        except Exception as exc:
            print(f"FAILED EXTRACTION | {resume_id} | {exc}")

            for jd_path, jd in job_profiles:
                failed += 1

                summary_rows.append({
                    "resume_id": resume_id,
                    "candidate_name": candidate_name,
                    "role_category": role_category,
                    "job_id": jd_path.stem,
                    "job_role": jd["role"],
                    "status": "extraction_failed",
                    "final_ats_score": "",
                    "semantic_similarity_status": "unavailable",
                    "error": str(exc),
                })

            continue

        # Score candidate against each valid job profile
        for jd_path, jd in job_profiles:
            job_id = jd_path.stem

            try:
                # No stale semantic scores are reused.
                # Semantic similarity is unavailable in this benchmark.
                result = engine.calculate_score(
                    candidate_id=resume_id,
                    job_id=job_id,
                    role=jd["role"],
                    resume_skills=skills,
                    experience_data=experience_data,
                    education_data=education_data,
                    semantic_result=None,
                    jd_skills=jd["skills"],
                    jd_experience=jd["experience"],
                    jd_education=jd["education"],
                )

                if not isinstance(result, dict):
                    raise TypeError(
                        "ATS scoring engine did not return a dictionary."
                    )

                score = result.get("final_ats_score")

                if score is None:
                    raise ValueError(
                        "Scoring result has no final_ats_score."
                    )

                # Save individual candidate-job result
                output = {
                    "benchmark_version": "day17_benchmark_v1",
                    "candidate": {
                        "resume_id": resume_id,
                        "candidate_name": candidate_name,
                        "source_file": source_file,
                        "role_category": role_category,
                    },
                    "job": {
                        "job_id": job_id,
                        "role": jd["role"],
                        "source_file": jd_path.name,
                    },
                    "input_extraction": {
                        "skills_count": len(skills),
                        "skills": skills,
                        "experience_years": (
                            experience_data["total_experience_years"]
                        ),
                        "job_title": (
                            experience_data["experiences"][0]["job_title"]
                            if experience_data["experiences"]
                            else ""
                        ),
                        "education": education_data["education"],
                        "semantic_similarity_status": (
                            "unavailable_not_reused"
                        ),
                    },
                    "score_result": result,
                }

                output_path = (
                    RESULTS_DIR / f"{resume_id}_{job_id}.json"
                )

                output_path.write_text(
                    json.dumps(
                        output,
                        indent=2,
                        ensure_ascii=False,
                        default=str,
                    ),
                    encoding="utf-8",
                )

                summary_rows.append({
                    "resume_id": resume_id,
                    "candidate_name": candidate_name,
                    "role_category": role_category,
                    "job_id": job_id,
                    "job_role": jd["role"],
                    "status": "success",
                    "final_ats_score": score,
                    "semantic_similarity_status": (
                        "unavailable_not_reused"
                    ),
                    "error": "",
                })

                successful += 1

                print(
                    f"OK | {resume_id} | {jd['role']} | "
                    f"ATS score: {score}"
                )

            except Exception as exc:
                failed += 1

                summary_rows.append({
                    "resume_id": resume_id,
                    "candidate_name": candidate_name,
                    "role_category": role_category,
                    "job_id": job_id,
                    "job_role": jd["role"],
                    "status": "scoring_failed",
                    "final_ats_score": "",
                    "semantic_similarity_status": "unavailable",
                    "error": str(exc),
                })

                print(
                    f"FAILED SCORING | {resume_id} | "
                    f"{jd['role']} | {exc}"
                )

    # --------------------------------------------------
    # 5. Save summary CSV
    # --------------------------------------------------

    summary_path = RESULTS_DIR / "benchmark_summary.csv"

    fieldnames = [
        "resume_id",
        "candidate_name",
        "role_category",
        "job_id",
        "job_role",
        "status",
        "final_ats_score",
        "semantic_similarity_status",
        "error",
    ]

    with summary_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    # --------------------------------------------------
    # 6. Final report
    # --------------------------------------------------

    total_pairs = len(summary_rows)

    print()
    print("=" * 65)
    print("DAY 17 BENCHMARK COMPLETE")
    print("=" * 65)
    print(f"Candidates in manifest: {len(candidates)}")
    print(f"Valid job profiles: {len(job_profiles)}")
    print(f"Successful candidate-job pairs: {successful}")
    print(f"Failed candidate-job pairs: {failed}")
    print(f"Total pairs recorded: {total_pairs}")
    print(f"Summary CSV: {summary_path.relative_to(ROOT)}")
    print(f"Individual JSON results: {RESULTS_DIR.relative_to(ROOT)}")
    print()
    print("IMPORTANT:")
    print("- ATS scores are not ground-truth hiring decisions.")
    print("- Precision and recall require manually verified labels.")
    print("- Semantic similarity was not reused or independently measured.")
    print("- Cross-role scores are stress tests, not proof of role accuracy.")


if __name__ == "__main__":
    main()

