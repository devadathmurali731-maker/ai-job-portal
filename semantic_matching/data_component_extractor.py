import json
from pathlib import Path


class DataComponentExtractor:
    """
    Extracts semantic matching components from the
    processed resume and JD JSON files.
    """

    def __init__(self, project_root=None):
        if project_root is None:
            project_root = Path(__file__).resolve().parent.parent

        self.project_root = Path(project_root)

        self.skills_path = (
            self.project_root
            / "data"
            / "processed"
            / "skills"
        )

        self.experience_path = (
            self.project_root
            / "data"
            / "processed"
            / "experience"
        )

        self.segmented_path = (
            self.project_root
            / "data"
            / "processed"
            / "segmented"
        )

        self.jd_path = (
            self.project_root
            / "data"
            / "processed"
            / "jd_profiles"
        )

    @staticmethod
    def load_json(file_path):
        """
        Load a JSON file.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def extract_resume_components(self, resume_id):
        """
        Extract skills, experience and project information
        from processed resume data.
        """

        skills_file = (
            self.skills_path
            / f"{resume_id}_skills.json"
        )

        experience_file = (
            self.experience_path
            / f"{resume_id}_experience.json"
        )

        segmented_file = (
            self.segmented_path
            / f"{resume_id}_sections.json"
        )

        skills_data = self.load_json(skills_file)
        experience_data = self.load_json(experience_file)
        segmented_data = self.load_json(segmented_file)

        # -------------------------
        # Skills
        # -------------------------

        skills = [
            item["skill"]
            for item in skills_data.get("skills", [])
        ]

        skills_text = ", ".join(skills)

        # -------------------------
        # Experience
        # -------------------------

        experience_parts = []

        for experience in experience_data.get(
            "experiences",
            []
        ):

            job_title = experience.get(
                "job_title",
                ""
            )

            company = experience.get(
                "company",
                ""
            )

            responsibilities = experience.get(
                "responsibilities",
                []
            )

            experience_parts.append(
                f"Job Title: {job_title}"
            )

            experience_parts.append(
                f"Company: {company}"
            )

            experience_parts.extend(
                responsibilities
            )

        experience_text = " ".join(
            experience_parts
        )

        # -------------------------
        # Projects
        # -------------------------

        projects = segmented_data.get(
            "projects",
            []
        )

        project_text = " ".join(
            projects
        )

        return {
            "skills": skills_text,
            "experience": experience_text,
            "projects": project_text
        }

    def extract_jd_components(self, jd_id):
        """
        Extract semantic matching components from
        a processed JD profile.
        """

        jd_file = (
            self.jd_path
            / f"{jd_id}.json"
        )

        jd_data = self.load_json(jd_file)

        # -------------------------
        # Skills
        # -------------------------

        required_skills = jd_data.get(
            "skills",
            {}
        ).get(
            "required",
            []
        )

        preferred_skills = jd_data.get(
            "skills",
            {}
        ).get(
            "preferred",
            []
        )

        all_skills = (
            required_skills
            + preferred_skills
        )

        skills_text = ", ".join(
            all_skills
        )

        # -------------------------
        # Experience
        # -------------------------

        experience_data = jd_data.get(
            "experience",
            {}
        )

        minimum_years = experience_data.get(
            "minimum_years"
        )

        maximum_years = experience_data.get(
            "maximum_years"
        )

        experience_text = (
            f"Required experience: "
            f"{minimum_years} to "
            f"{maximum_years} years. "
            f"Role: {jd_data.get('role', '')}."
        )

        # -------------------------
        # Projects
        # -------------------------

        normalized_text = jd_data.get(
            "normalized_text",
            ""
        )

        project_text = normalized_text

        return {
            "skills": skills_text,
            "experience": experience_text,
            "projects": project_text
        }


if __name__ == "__main__":

    print("Testing real data component extraction...")

    extractor = DataComponentExtractor()

    resume_components = (
        extractor.extract_resume_components(
            "resume_001"
        )
    )

    jd_components = (
        extractor.extract_jd_components(
            "jd_001_data_scientist"
        )
    )

    print("\nResume Components:")

    for component, text in resume_components.items():

        print(
            f"\n{component.title()}:"
        )

        print(
            text if text else "[Not available]"
        )

    print("\n\nJD Components:")

    for component, text in jd_components.items():

        print(
            f"\n{component.title()}:"
        )

        print(
            text if text else "[Not available]"
        )
        