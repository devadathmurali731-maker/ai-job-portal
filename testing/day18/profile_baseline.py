import json
import statistics
import sys
import time
import traceback
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "testing" / "day18" / "results"
OUTPUT_FILE = RESULTS_DIR / "baseline.json"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "semantic_matching"))

from src.resume_extractor import (
    extract_text,
    clean_text,
    normalize_bullets,
    normalize_section_headings,
    normalize_special_characters,
)


def timed_runs(function, repeats=5):
    samples = []
    result = None

    for _ in range(repeats):
        start = time.perf_counter()
        result = function()
        samples.append((time.perf_counter() - start) * 1000)

    return {
        "runs": repeats,
        "mean_ms": round(statistics.mean(samples), 3),
        "median_ms": round(statistics.median(samples), 3),
        "min_ms": round(min(samples), 3),
        "max_ms": round(max(samples), 3),
    }, result


def normalize_resume_text(text):
    text = clean_text(text)
    text = normalize_bullets(text)
    text = normalize_section_headings(text)
    text = normalize_special_characters(text)
    return clean_text(text)


def read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "report_type": "Day 18 performance baseline",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(ROOT),
        "notes": [
            "Day 17 benchmark was not executed.",
            "Times are local-machine measurements, not production SLA measurements.",
            "Python tracemalloc is not used as a substitute for total native model memory.",
        ],
        "resume_extraction": [],
        "ats_scoring": {},
        "semantic_matching": {},
        "process_memory": {},
    }

    # 1. Optional process memory reading.
    try:
        import psutil
        process = psutil.Process()
        report["process_memory"]["before_mb"] = round(
            process.memory_info().rss / (1024 * 1024), 2
        )
    except ImportError:
        report["process_memory"]["status"] = (
            "psutil is not installed; process RSS was not measured."
        )

    # 2. Profile extraction and normalization for the real sample resumes.
    resume_dir = ROOT / "data" / "raw_resumes"
    resume_files = sorted(
        list(resume_dir.glob("*.pdf")) + list(resume_dir.glob("*.docx"))
    )

    for path in resume_files:
        item = {
            "file": str(path.relative_to(ROOT)),
            "size_bytes": path.stat().st_size,
        }

        try:
            extraction_timing, raw_text = timed_runs(
                lambda p=path: extract_text(p), repeats=5
            )
            normalization_timing, normalized = timed_runs(
                lambda t=raw_text: normalize_resume_text(t), repeats=5
            )

            item["status"] = "success"
            item["extraction_timing"] = extraction_timing
            item["normalization_timing"] = normalization_timing
            item["raw_characters"] = len(raw_text or "")
            item["normalized_characters"] = len(normalized or "")
        except Exception as exc:
            item["status"] = "failed"
            item["error"] = f"{type(exc).__name__}: {exc}"

        report["resume_extraction"].append(item)

    # 3. Profile ATS scoring using production-compatible JSON inputs.
    try:
        from ats_scoring.ats_scoring_engine import ATSScoringEngine

        skills_path = ROOT / "data" / "processed" / "skills" / "resume_001_skills.json"
        experience_path = ROOT / "data" / "processed" / "experience" / "resume_001_experience.json"
        education_path = ROOT / "data" / "processed" / "education" / "resume_001_education.json"
        jd_path = ROOT / "data" / "processed" / "jd_profiles" / "jd_001_data_scientist.json"

        input_paths = [skills_path, experience_path, education_path, jd_path]
        missing_paths = [str(p.relative_to(ROOT)) for p in input_paths if not p.exists()]

        if missing_paths:
            report["ats_scoring"] = {
                "status": "skipped",
                "reason": "Required JSON inputs were not found.",
                "missing_files": missing_paths,
            }
        else:
            skills_data = read_json(skills_path)
            experience_data = read_json(experience_path)
            education_data = read_json(education_path)
            jd_data = read_json(jd_path)

            resume_id = skills_data["resume_id"]
            jd_id = jd_data.get("job_id", jd_path.stem)
            role = jd_data["role"]

            candidate_number = resume_id.split("_")[-1]
            job_number = jd_id.split("_")[1]

            engine = ATSScoringEngine()

            def score_one_pair():
                return engine.calculate_score(
                    candidate_id=f"CAND_{candidate_number}",
                    job_id=f"JOB_{job_number}",
                    role=role,
                    resume_skills=skills_data.get("skills", []),
                    experience_data=experience_data,
                    education_data=education_data,
                    semantic_result=None,
                    jd_skills=jd_data.get("skills", {}),
                    jd_experience=jd_data.get("experience", {}),
                    jd_education=jd_data.get("education", {}),
                )

            timing, score_result = timed_runs(score_one_pair, repeats=5)

            report["ats_scoring"] = {
                "status": "success",
                "input_resume": resume_id,
                "input_job": jd_id,
                "role": role,
                "semantic_result": None,
                "timing": timing,
                "sample_result_type": type(score_result).__name__,
            }

            if isinstance(score_result, dict):
                report["ats_scoring"]["sample_score_result"] = score_result
            elif isinstance(score_result, (str, int, float, bool)) or score_result is None:
                report["ats_scoring"]["sample_score_result"] = score_result

    except Exception as exc:
        report["ats_scoring"] = {
            "status": "failed",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(limit=5),
            "note": "Profiling only; production code and Day 17 results were not modified.",
        }
# 4. Profile semantic model startup and single-versus-batch encoding.
    try:
        from embedding_engine import EmbeddingEngine
        from similarity_scorer import SimilarityScorer

        init_start = time.perf_counter()
        embedding_engine = EmbeddingEngine()
        model_init_ms = (time.perf_counter() - init_start) * 1000

        resume_text = (
            "Data scientist skilled in Python, SQL, statistics, pandas, "
            "machine learning, and model evaluation."
        )
        job_text = (
            "We need a data scientist with Python, SQL, statistics, "
            "pandas, machine learning, and model evaluation experience."
        )

        # Warm up the model before repeated measurements.
        embedding_engine.generate_embedding(resume_text)
        embedding_engine.generate_embedding(job_text)

        single_timing, single_embeddings = timed_runs(
            lambda: [
                embedding_engine.generate_embedding(resume_text),
                embedding_engine.generate_embedding(job_text),
            ],
            repeats=5,
        )

        batch_timing, batch_embeddings = timed_runs(
            lambda: embedding_engine.generate_embeddings(
                [resume_text, job_text]
            ),
            repeats=5,
        )

        scorer = SimilarityScorer()
        single_score = scorer.cosine_similarity_score(
            single_embeddings[0], single_embeddings[1]
        )
        batch_score = scorer.cosine_similarity_score(
            batch_embeddings[0], batch_embeddings[1]
        )

        report["semantic_matching"] = {
            "status": "success",
            "model_name": embedding_engine.model_name,
            "model_initialization_ms": round(model_init_ms, 3),
            "single_encoding_pair": single_timing,
            "batch_encoding_pair": batch_timing,
            "single_cosine_score": float(single_score),
            "batch_cosine_score": float(batch_score),
            "absolute_score_difference": round(
                abs(float(single_score) - float(batch_score)), 10
            ),
            "note": (
                "Model initialization is timed separately. Encoding timings "
                "are warm runs on a small fixed text pair."
            ),
        }

    except Exception as exc:
        report["semantic_matching"] = {
            "status": "unavailable_or_failed",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(limit=3),
        }

    # 5. Capture process memory after the measured work, if possible.
    try:
        import psutil
        process = psutil.Process()
        report["process_memory"]["after_mb"] = round(
            process.memory_info().rss / (1024 * 1024), 2
        )
        if "before_mb" in report["process_memory"]:
            report["process_memory"]["change_mb"] = round(
                report["process_memory"]["after_mb"]
                - report["process_memory"]["before_mb"],
                2,
            )
    except ImportError:
        pass
    except Exception as exc:
        report["process_memory"]["after_error"] = str(exc)

    OUTPUT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    print("\n" + "=" * 68)
    print("DAY 18 PERFORMANCE BASELINE")
    print("=" * 68)

    print("\nRESUME EXTRACTION")
    for item in report["resume_extraction"]:
        print(f"\n{item['file']}: {item['status']}")
        if item["status"] == "success":
            print("  Extraction:", item["extraction_timing"])
            print("  Normalization:", item["normalization_timing"])
            print("  Characters:", item["normalized_characters"])
        else:
            print("  Error:", item.get("error"))

    print("\nATS SCORING")
    print(json.dumps(report["ats_scoring"], indent=2, default=str))

    print("\nSEMANTIC MATCHING")
    print(json.dumps(report["semantic_matching"], indent=2, default=str))

    print("\nPROCESS MEMORY")
    print(json.dumps(report["process_memory"], indent=2))

    print("\nReport saved to:")
    print(OUTPUT_FILE)
    print("\nDay 17 benchmark files were not intentionally modified.")


if __name__ == "__main__":
    main()

