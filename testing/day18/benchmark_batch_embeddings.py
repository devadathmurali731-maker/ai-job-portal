import json
import sys
import time
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "semantic_matching"))

from data_component_extractor import DataComponentExtractor
from embedding_engine import EmbeddingEngine
from similarity_scorer import SimilarityScorer


RESUME_IDS = [
    "resume_001",
    "resume_002",
    "resume_003",
    "resume_004",
]

JD_IDS = [
    "jd_001_data_scientist",
    "jd_002_software_engineer",
    "jd_003_ml_engineer",
    "jd_004_data_analyst",
    "jd_005_hr_executive",
    "jd_006_business_analyst",
]

WEIGHTS = {
    "skills": 0.50,
    "experience": 0.30,
    "projects": 0.20,
}

REPEATS = 5


def mean(values):
    return statistics.mean(values) if values else 0.0


def weighted_score(scores):
    available = [name for name in WEIGHTS if name in scores]

    if not available:
        return None

    total_weight = sum(WEIGHTS[name] for name in available)

    return float(sum(
        scores[name] * WEIGHTS[name] / total_weight
        for name in available
    ))


def main():
    output_dir = ROOT / "testing" / "day18" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "batch_embedding_validation.json"

    print("Initializing Day 18 real-data benchmark...")
    print("This benchmark does not modify existing validation results.")

    extractor = DataComponentExtractor(project_root=ROOT)
    embedding_engine = EmbeddingEngine()
    scorer = SimilarityScorer()

    # Warm up the model before collecting timings.
    embedding_engine.generate_embeddings([
        "Python SQL machine learning",
        "Data analysis and predictive modeling",
    ])

    pair_results = []
    separate_times = []
    batch_times = []
    component_count = 0
    skipped_components = 0
    errors = []

    for resume_id in RESUME_IDS:
        try:
            resume_components = extractor.extract_resume_components(
                resume_id
            )
        except Exception as exc:
            errors.append({
                "resume_id": resume_id,
                "error": f"Resume extraction failed: {exc}",
            })
            continue

        for jd_id in JD_IDS:
            try:
                jd_components = extractor.extract_jd_components(jd_id)
            except Exception as exc:
                errors.append({
                    "resume_id": resume_id,
                    "jd_id": jd_id,
                    "error": f"JD extraction failed: {exc}",
                })
                continue

            component_results = {}
            component_timings = {}

            for component in WEIGHTS:
                resume_text = resume_components.get(component, "")
                jd_text = jd_components.get(component, "")

                if (
                    not isinstance(resume_text, str)
                    or not isinstance(jd_text, str)
                    or not resume_text.strip()
                    or not jd_text.strip()
                ):
                    skipped_components += 1
                    continue

                separate_durations = []
                batch_durations = []
                separate_scores = []
                batch_scores = []

                try:
                    for _ in range(REPEATS):
                        # Current approach: two separate model.encode calls.
                        start = time.perf_counter()
                        resume_embedding = (
                            embedding_engine.generate_embedding(resume_text)
                        )
                        jd_embedding = (
                            embedding_engine.generate_embedding(jd_text)
                        )
                        separate_durations.append(
                            (time.perf_counter() - start) * 1000
                        )

                        separate_scores.append(
                            scorer.cosine_similarity_score(
                                resume_embedding,
                                jd_embedding,
                            )
                        )

                        # Candidate approach: one batched model.encode call.
                        start = time.perf_counter()
                        embeddings = embedding_engine.generate_embeddings([
                            resume_text,
                            jd_text,
                        ])
                        batch_durations.append(
                            (time.perf_counter() - start) * 1000
                        )

                        batch_scores.append(
                            scorer.cosine_similarity_score(
                                embeddings[0],
                                embeddings[1],
                            )
                        )

                    separate_ms = mean(separate_durations)
                    batch_ms = mean(batch_durations)
                    separate_score = mean(separate_scores)
                    batch_score = mean(batch_scores)
                    difference = abs(separate_score - batch_score)

                    component_results[component] = {
                        "separate_score": separate_score,
                        "batch_score": batch_score,
                        "absolute_score_difference": difference,
                    }

                    component_timings[component] = {
                        "separate_mean_ms": separate_ms,
                        "batch_mean_ms": batch_ms,
                        "speedup_percent": (
                            (separate_ms - batch_ms) / separate_ms * 100
                            if separate_ms > 0 else 0.0
                        ),
                    }

                    separate_times.append(separate_ms)
                    batch_times.append(batch_ms)
                    component_count += 1

                except Exception as exc:
                    errors.append({
                        "resume_id": resume_id,
                        "jd_id": jd_id,
                        "component": component,
                        "error": str(exc),
                    })

            if component_results:
                separate_component_scores = {
                    name: result["separate_score"]
                    for name, result in component_results.items()
                }
                batch_component_scores = {
                    name: result["batch_score"]
                    for name, result in component_results.items()
                }

                pair_results.append({
                    "resume_id": resume_id,
                    "jd_id": jd_id,
                    "available_components": list(component_results),
                    "component_results": component_results,
                    "component_timings": component_timings,
                    "separate_final_score": weighted_score(
                        separate_component_scores
                    ),
                    "batch_final_score": weighted_score(
                        batch_component_scores
                    ),
                    "final_score_absolute_difference": abs(
                        weighted_score(separate_component_scores)
                        - weighted_score(batch_component_scores)
                    ),
                })

    average_separate = mean(separate_times)
    average_batch = mean(batch_times)

    summary = {
        "benchmark": "Day 18 real-data batch embedding validation",
        "model": "all-MiniLM-L6-v2",
        "resume_count_requested": len(RESUME_IDS),
        "jd_count_requested": len(JD_IDS),
        "maximum_pairs": len(RESUME_IDS) * len(JD_IDS),
        "successful_pairs": len(pair_results),
        "successful_component_comparisons": component_count,
        "skipped_empty_components": skipped_components,
        "repeats_per_component": REPEATS,
        "average_separate_encoding_ms": average_separate,
        "average_batch_encoding_ms": average_batch,
        "average_speedup_percent": (
            (average_separate - average_batch) / average_separate * 100
            if average_separate > 0 else 0.0
        ),
        "maximum_component_score_difference": max(
            (
                result["absolute_score_difference"]
                for pair in pair_results
                for result in pair["component_results"].values()
            ),
            default=0.0,
        ),
        "maximum_final_score_difference": max(
            (
                pair["final_score_absolute_difference"]
                for pair in pair_results
            ),
            default=0.0,
        ),
        "errors": errors,
        "pairs": pair_results,
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print("\n" + "=" * 60)
    print("DAY 18 BATCH EMBEDDING VALIDATION")
    print("=" * 60)
    print(f"Successful resume-JD pairs: {len(pair_results)}/24")
    print(f"Component comparisons: {component_count}")
    print(f"Skipped empty components: {skipped_components}")
    print(f"Errors: {len(errors)}")
    print(f"Separate encoding mean: {average_separate:.3f} ms")
    print(f"Batch encoding mean:    {average_batch:.3f} ms")
    print(f"Average speedup:        {summary['average_speedup_percent']:.2f}%")
    print(
        "Max component score difference: "
        f"{summary['maximum_component_score_difference']:.10f}"
    )
    print(
        "Max final score difference:     "
        f"{summary['maximum_final_score_difference']:.10f}"
    )
    print(f"\nSaved report: {output_file}")

    if errors:
        print("\nFirst errors:")
        for error in errors[:5]:
            print(error)


if __name__ == "__main__":
    main()
