"""Rule-based and ATS-score-based candidate eligibility decisions."""

import json
from pathlib import Path
from datetime import datetime, timezone


RULES_PATH = Path(__file__).resolve().parent / "rules.json"


def load_rules(path=RULES_PATH):
    """Load eligibility rules from JSON."""
    with open(path, "r", encoding="utf-8-sig") as file:
        rules = json.load(file)

    if not isinstance(rules.get("roles"), dict):
        raise ValueError("Rules must contain a roles object.")

    return rules


def normalize(value):
    """Normalize text for case-insensitive comparisons."""
    return " ".join(str(value).strip().casefold().split())


def decide_eligibility(
    ats_result,
    candidate=None,
    job=None,
    rules=None,
):
    """
    Decide eligibility for one candidate-job combination.

    ats_result: Existing ATS result dictionary.
    candidate: Optional candidate data (skills, experience, location,
               availability).
    job: Optional job profile dictionary.
    rules: Optional rule configuration dictionary.
    """
    candidate = candidate or {}
    job = job or {}
    rules = rules or load_rules()

    candidate_id = ats_result.get("candidate_id")
    job_id = ats_result.get("job_id")
    role = ats_result.get("role") or job.get("role")

    if not candidate_id or not job_id or not role:
        raise ValueError(
            "ATS result must include candidate_id, job_id, and role."
        )

    role_rules = rules.get("roles", {}).get(role)
    if role_rules is None:
        return _result(
            candidate_id,
            job_id,
            role,
            "Review",
            None,
            ["No eligibility rules configured for this role."],
            ["Configure job-specific eligibility rules."],
        )

    default_thresholds = rules.get("default_thresholds", {})
    eligible_min = role_rules.get(
        "eligible_min_score",
        default_thresholds.get("eligible_min_score", 70),
    )
    review_min = role_rules.get(
        "review_min_score",
        default_thresholds.get("review_min_score", 50),
    )

    if not (
        isinstance(eligible_min, (int, float))
        and isinstance(review_min, (int, float))
        and 0 <= review_min < eligible_min <= 100
    ):
        raise ValueError(f"Invalid score thresholds for role: {role}")

    reasons = []
    failed_checks = []
    review_checks = []
    passed_checks = []

    # ATS score
    score = ats_result.get("final_ats_score")
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        review_checks.append("ATS score is missing or invalid.")
    elif not 0 <= score <= 100:
        review_checks.append("ATS score is outside the valid 0-100 range.")
    elif score >= eligible_min:
        passed_checks.append("ATS score meets the eligibility threshold.")
    elif score >= review_min:
        review_checks.append(
            f"ATS score {score:.2f} is in the review range."
        )
    else:
        failed_checks.append(
            f"ATS score {score:.2f} is below the review threshold."
        )

    # Required skills: prefer explicit candidate data, otherwise use
    # the ATS component's required_matched/required_missing evidence.
    required_skills = role_rules.get(
        "mandatory_skills",
        job.get("skills", {}).get("required", []),
    )
    candidate_skills = candidate.get("skills")

    if candidate_skills is not None:
        normalized_skills = {normalize(skill) for skill in candidate_skills}
        missing_skills = [
            skill for skill in required_skills
            if normalize(skill) not in normalized_skills
        ]
        if missing_skills:
            failed_checks.append(
                "Missing mandatory skills: " + ", ".join(missing_skills)
            )
        else:
            passed_checks.append("All mandatory skills are present.")
    elif required_skills:
        details = ats_result.get("component_details", {}).get(
            "skill_match", {}
        )
        missing_from_ats = details.get("required_missing")
        matched_from_ats = details.get("required_matched")

        if isinstance(missing_from_ats, list) and isinstance(
            matched_from_ats, list
        ):
            missing_set = {normalize(skill) for skill in missing_from_ats}
            matched_set = {
                normalize(item.get("skill", ""))
                for item in matched_from_ats
                if isinstance(item, dict)
            }
            unknown = [
                skill for skill in required_skills
                if normalize(skill) not in missing_set
                and normalize(skill) not in matched_set
            ]
            if missing_from_ats:
                failed_checks.append(
                    "Missing mandatory skills: "
                    + ", ".join(missing_from_ats)
                )
            elif unknown:
                review_checks.append(
                    "ATS skill evidence does not cover configured skills: "
                    + ", ".join(unknown)
                )
            else:
                passed_checks.append("ATS evidence confirms mandatory skills.")
        else:
            review_checks.append(
                "Mandatory skills could not be verified from available data."
            )
    else:
        passed_checks.append("No mandatory skills configured.")

    # Experience range
    exp_rules = role_rules.get("experience", {})
    minimum_years = exp_rules.get("minimum_years")
    maximum_years = exp_rules.get("maximum_years")
    experience_years = candidate.get("experience_years")

    if experience_years is None:
        experience_years = (
            ats_result.get("component_details", {})
            .get("experience_relevance", {})
            .get("candidate_experience_years")
        )

    if experience_years is None:
        review_checks.append("Candidate experience is unknown.")
    elif not isinstance(experience_years, (int, float)) or isinstance(
        experience_years, bool
    ) or experience_years < 0:
        review_checks.append("Candidate experience value is invalid.")
    elif (
        minimum_years is not None and experience_years < minimum_years
    ) or (
        maximum_years is not None and experience_years > maximum_years
    ):
        failed_checks.append(
            f"Experience {experience_years} years is outside the configured "
            f"range ({minimum_years}-{maximum_years} years)."
        )
    else:
        passed_checks.append("Experience is within the configured range.")

    # Location: only enforce when the job requires it.
    location_rules = role_rules.get("location", {})
    if location_rules.get("required", False):
        location = candidate.get("location")
        allowed = location_rules.get("allowed_locations", [])

        if not location:
            review_checks.append("Candidate location is unknown.")
        elif allowed and normalize(location) not in {
            normalize(item) for item in allowed
        }:
            failed_checks.append(
                f"Candidate location '{location}' is not in the allowed list."
            )
        else:
            passed_checks.append("Location requirement is satisfied.")
    elif not candidate.get("location") and location_rules.get(
        "review_if_unknown", True
    ):
        review_checks.append(
            "Candidate location is unknown; confirm location requirements."
        )

    # Availability: do not infer availability from other profile fields.
    availability_rules = role_rules.get("availability", {})
    if availability_rules.get("required", False):
        availability = candidate.get("availability")
        accepted = availability_rules.get(
            "accepted_values", ["available"]
        )

        if availability is None:
            review_checks.append("Candidate availability is unknown.")
        elif normalize(availability) not in {
            normalize(item) for item in accepted
        }:
            failed_checks.append(
                f"Availability '{availability}' does not meet job rules."
            )
        else:
            passed_checks.append("Availability requirement is satisfied.")
    elif candidate.get("availability") is None and availability_rules.get(
        "review_if_unknown", True
    ):
        review_checks.append(
            "Candidate availability is unknown; confirm before screening."
        )

    # Explicit failures override score-only outcomes. Uncertainty triggers
    # review unless a confirmed failure exists.
    if failed_checks:
        status = "Rejected"
    elif review_checks:
        status = "Review"
    else:
        status = "Eligible"

    reasons.extend(failed_checks)
    reasons.extend(review_checks)
    if not reasons:
        reasons.append("All configured eligibility checks passed.")

    return _result(
        candidate_id,
        job_id,
        role,
        status,
        score if isinstance(score, (int, float)) and not isinstance(
            score, bool
        ) else None,
        reasons,
        passed_checks,
        failed_checks=failed_checks,
        review_checks=review_checks,
    )


def _result(
    candidate_id,
    job_id,
    role,
    status,
    ats_score,
    reasons,
    passed_checks,
    failed_checks=None,
    review_checks=None,
):
    """Create a consistent eligibility result structure."""
    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "role": role,
        "eligibility_status": status,
        "ats_score": ats_score,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks or [],
        "review_checks": review_checks or [],
        "reasons": reasons,
        "decision_timestamp": datetime.now(timezone.utc).isoformat(),
        "engine_version": "1.0.0",
    }
