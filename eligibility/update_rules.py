import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
profiles_dir = root / "data" / "processed" / "jd_profiles"
rules_path = root / "eligibility" / "rules.json"

with open(rules_path, "r", encoding="utf-8-sig") as f:
    rules = json.load(f)

# Keep a backup before changing the configuration.
backup_path = rules_path.with_suffix(".json.bak")
shutil.copy2(rules_path, backup_path)

roles = rules.setdefault("roles", {})
defaults = rules.setdefault(
    "default_thresholds",
    {"eligible_min_score": 70, "review_min_score": 50}
)

profile_count = 0

for path in sorted(profiles_dir.glob("jd_*.json")):
    with open(path, "r", encoding="utf-8-sig") as f:
        jd = json.load(f)

    role = jd.get("role")
    if not role:
        print(f"SKIPPED {path.name}: missing role field")
        continue

    skills_data = jd.get("skills", {})
    required_skills = skills_data.get("required", [])
    experience_data = jd.get("experience", {})

    existing = roles.get(role, {})
    location_rules = existing.get(
        "location",
        {
            "required": False,
            "allowed_locations": [],
            "review_if_unknown": True
        }
    )
    availability_rules = existing.get(
        "availability",
        {
            "required": False,
            "review_if_unknown": True
        }
    )

    roles[role] = {
        "eligible_min_score": existing.get(
            "eligible_min_score", defaults.get("eligible_min_score", 70)
        ),
        "review_min_score": existing.get(
            "review_min_score", defaults.get("review_min_score", 50)
        ),
        "mandatory_skills": required_skills,
        "experience": {
            "minimum_years": experience_data.get("minimum_years", 0),
            "maximum_years": experience_data.get("maximum_years")
        },
        "location": location_rules,
        "availability": availability_rules
    }

    profile_count += 1
    print(
        f"Configured: {role} | "
        f"Required skills: {len(required_skills)} | "
        f"Experience: {experience_data.get('minimum_years', 0)}-"
        f"{experience_data.get('maximum_years', 'unspecified')} years"
    )

with open(rules_path, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"\nUpdated {profile_count} role profiles.")
print(f"Backup saved to: {backup_path.name}")
