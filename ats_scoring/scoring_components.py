"""
ATS Scoring Components.

Contains the individual scoring components used by the
Day 13 ATS Scoring Engine:

1. Skill Match
2. Experience Relevance
3. Education Alignment
4. Semantic Similarity

All component scores are returned on a 0-100 scale.

The implementation is designed to be:

- Transparent
- Explainable
- Role-aware
- Configurable
- Robust to missing data
"""

from typing import Any, Dict, List, Optional


class ScoringComponents:
    """Individual ATS scoring components."""

    # =====================================================
    # Utility Methods
    # =====================================================

    @staticmethod
    def normalize_skill(skill: Any) -> str:
        """
        Normalize a skill or text value for comparison.

        Normalization includes:

        - Converting to string
        - Lowercasing
        - Removing extra whitespace
        - Normalizing hyphens
        """

        if skill is None:
            return ""

        text = str(skill).lower().strip()

        text = text.replace("-", " ")

        text = " ".join(
            text.split()
        )

        return text

    @staticmethod
    def clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 1.0
    ) -> float:
        """Keep a numerical value within a specified range."""

        return max(
            minimum,
            min(
                value,
                maximum
            )
        )

    # =====================================================
    # 1. Skill Match
    # =====================================================

    def calculate_skill_match(
        self,
        resume_skills,
        jd_skills
    ):
        """
        Calculate candidate skill alignment against the
        current job description.

        Required skills contribute 80% of the skill score.

        Preferred skills contribute 20%.

        Skill confidence is preserved for explanation but
        does not dominate the match calculation.

        Returns a score between 0 and 100.
        """

        # -------------------------------------------------
        # Handle missing candidate skills
        # -------------------------------------------------

        if not resume_skills:

            return {
                "available": False,
                "score": None,
                "reason": "Candidate skill data is unavailable."
            }

        # -------------------------------------------------
        # Handle missing JD skill requirements
        # -------------------------------------------------

        if not jd_skills:

            return {
                "available": False,
                "score": None,
                "reason": "JD skill requirements are unavailable."
            }

        # -------------------------------------------------
        # Convert resume skills into normalized lookup
        # -------------------------------------------------

        normalized_resume_skills = {}

        for item in resume_skills:

            if isinstance(item, dict):

                skill_name = item.get(
                    "skill",
                    ""
                )

                confidence = item.get(
                    "confidence"
                )

            else:

                skill_name = str(item)

                confidence = None

            normalized_name = self.normalize_skill(
                skill_name
            )

            if normalized_name:

                normalized_resume_skills[
                    normalized_name
                ] = {
                    "skill": skill_name,
                    "confidence": confidence
                }

        # -------------------------------------------------
        # Read JD skills
        # -------------------------------------------------

        required_skills = jd_skills.get(
            "required",
            []
        )

        preferred_skills = jd_skills.get(
            "preferred",
            []
        )

        # -------------------------------------------------
        # Match required skills
        # -------------------------------------------------

        required_matched = []
        required_missing = []

        for skill in required_skills:

            normalized_jd_skill = self.normalize_skill(
                skill
            )

            if normalized_jd_skill in normalized_resume_skills:

                resume_match = (
                    normalized_resume_skills[
                        normalized_jd_skill
                    ]
                )

                required_matched.append(
                    {
                        "skill": skill,
                        "resume_skill": (
                            resume_match["skill"]
                        ),
                        "confidence": (
                            resume_match["confidence"]
                        )
                    }
                )

            else:

                required_missing.append(
                    skill
                )

        # -------------------------------------------------
        # Match preferred skills
        # -------------------------------------------------

        preferred_matched = []
        preferred_missing = []

        for skill in preferred_skills:

            normalized_jd_skill = self.normalize_skill(
                skill
            )

            if normalized_jd_skill in normalized_resume_skills:

                resume_match = (
                    normalized_resume_skills[
                        normalized_jd_skill
                    ]
                )

                preferred_matched.append(
                    {
                        "skill": skill,
                        "resume_skill": (
                            resume_match["skill"]
                        ),
                        "confidence": (
                            resume_match["confidence"]
                        )
                    }
                )

            else:

                preferred_missing.append(
                    skill
                )

        # -------------------------------------------------
        # Calculate required score
        # -------------------------------------------------

        if required_skills:

            required_score = (
                len(required_matched)
                / len(required_skills)
            )

        else:

            required_score = 1.0

        # -------------------------------------------------
        # Calculate preferred score
        # -------------------------------------------------

        if preferred_skills:

            preferred_score = (
                len(preferred_matched)
                / len(preferred_skills)
            )

        else:

            preferred_score = 1.0

        # -------------------------------------------------
        # Final skill score
        # -------------------------------------------------

        final_score = (
            required_score * 0.80
            + preferred_score * 0.20
        )

        final_score = self.clamp(
            final_score
        )

        return {
            "available": True,
            "score": final_score * 100,
            "required_score": required_score * 100,
            "preferred_score": preferred_score * 100,
            "required_matched": required_matched,
            "required_missing": required_missing,
            "preferred_matched": preferred_matched,
            "preferred_missing": preferred_missing
        }

    # =====================================================
    # 2. Experience Relevance
    # =====================================================

    def calculate_experience_relevance(
        self,
        experience_data,
        jd_experience,
        jd_role=None,
        jd_skills=None
    ):
        """
        Calculate experience relevance against the CURRENT JD.

        Experience score consists of:

            50% -> Experience range fit
            50% -> Role relevance

        Role relevance consists of:

            40% -> Job-title match
            40% -> Required-skill evidence
            20% -> Overall JD-skill evidence

        Missing candidate experience data is handled
        explicitly without crashing the ATS engine.
        """

        # -------------------------------------------------
        # Validate JD experience requirements
        # -------------------------------------------------

        if not jd_experience:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "JD experience requirements "
                    "are unavailable."
                )
            }

        minimum_years = jd_experience.get(
            "minimum_years"
        )

        maximum_years = jd_experience.get(
            "maximum_years"
        )

        # -------------------------------------------------
        # Handle missing candidate experience
        # -------------------------------------------------

        if not experience_data:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Experience data is unavailable."
                )
            }

        # -------------------------------------------------
        # Read candidate experience
        # -------------------------------------------------

        candidate_years = experience_data.get(
            "total_experience_years"
        )

        experiences = experience_data.get(
            "experiences",
            []
        )

        # -------------------------------------------------
        # Validate candidate experience years
        # -------------------------------------------------

        if candidate_years is None:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Candidate experience years "
                    "are unavailable."
                )
            }

        # -------------------------------------------------
        # Calculate experience range fit
        # -------------------------------------------------

        if minimum_years is None:

            range_score = 1.0

        elif candidate_years >= minimum_years:

            range_score = 1.0

        else:

            range_score = (
                candidate_years
                / minimum_years
            )

        range_score = self.clamp(
            range_score
        )

        # -------------------------------------------------
        # Prepare JD skills
        # -------------------------------------------------

        jd_skills = jd_skills or {}

        required_skills = [
            self.normalize_skill(skill)
            for skill in jd_skills.get(
                "required",
                []
            )
        ]

        preferred_skills = [
            self.normalize_skill(skill)
            for skill in jd_skills.get(
                "preferred",
                []
            )
        ]

        all_target_skills = list(
            dict.fromkeys(
                required_skills
                + preferred_skills
            )
        )

        # -------------------------------------------------
        # Analyze experience records
        # -------------------------------------------------

        role_matches = 0

        matched_experience_keywords = []

        matched_required_experience_keywords = []

        for experience in experiences:

            if not isinstance(
                experience,
                dict
            ):
                continue

            job_title = self.normalize_skill(
                experience.get(
                    "job_title",
                    ""
                )
            )

            responsibilities = experience.get(
                "responsibilities",
                []
            )

            responsibility_text = " ".join(
                str(item).lower()
                for item in responsibilities
            )

            # ---------------------------------------------
            # Job title matching
            # ---------------------------------------------

            if jd_role:

                target_role = self.normalize_skill(
                    jd_role
                )

                if (
                    target_role in job_title
                    or job_title in target_role
                ):

                    role_matches += 1

            # ---------------------------------------------
            # Match all JD skills
            # ---------------------------------------------

            for skill in all_target_skills:

                if (
                    skill
                    and skill in responsibility_text
                ):

                    if (
                        skill
                        not in matched_experience_keywords
                    ):

                        matched_experience_keywords.append(
                            skill
                        )

            # ---------------------------------------------
            # Match required JD skills
            # ---------------------------------------------

            for skill in required_skills:

                if (
                    skill
                    and skill in responsibility_text
                ):

                    if (
                        skill
                        not in
                        matched_required_experience_keywords
                    ):

                        matched_required_experience_keywords.append(
                            skill
                        )

        # -------------------------------------------------
        # Calculate title score
        # -------------------------------------------------

        if experiences:

            title_score = (
                role_matches
                / len(experiences)
            )

        else:

            title_score = 0.0

        title_score = self.clamp(
            title_score
        )

        # -------------------------------------------------
        # Calculate required keyword score
        # -------------------------------------------------

        if required_skills:

            required_keyword_score = (
                len(
                    matched_required_experience_keywords
                )
                / len(required_skills)
            )

        else:

            required_keyword_score = 1.0

        required_keyword_score = self.clamp(
            required_keyword_score
        )

        # -------------------------------------------------
        # Calculate overall keyword score
        # -------------------------------------------------

        if all_target_skills:

            keyword_score = (
                len(
                    matched_experience_keywords
                )
                / len(all_target_skills)
            )

        else:

            keyword_score = 1.0

        keyword_score = self.clamp(
            keyword_score
        )

        # -------------------------------------------------
        # Calculate role relevance
        # -------------------------------------------------

        role_relevance = (
            title_score * 0.40
            + required_keyword_score * 0.40
            + keyword_score * 0.20
        )

        role_relevance = self.clamp(
            role_relevance
        )

        # -------------------------------------------------
        # Calculate final experience score
        # -------------------------------------------------

        final_score = (
            range_score * 0.50
            + role_relevance * 0.50
        )

        final_score = self.clamp(
            final_score
        )

        return {
            "available": True,
            "score": final_score * 100,
            "candidate_experience_years": (
                candidate_years
            ),
            "minimum_required_years": (
                minimum_years
            ),
            "maximum_required_years": (
                maximum_years
            ),
            "experience_range_fit": (
                range_score * 100
            ),
            "role_relevance": (
                role_relevance * 100
            ),
            "title_match": (
                role_matches > 0
            ),
            "matched_experience_keywords": (
                matched_experience_keywords
            ),
            "required_experience_keywords": (
                required_skills
            ),
            "matched_required_experience_keywords": (
                matched_required_experience_keywords
            )
        }

    # =====================================================
    # 3. Education Alignment
    # =====================================================

    def calculate_education_alignment(
        self,
        education_data,
        jd_education
    ):
        """
        Calculate education alignment against the CURRENT JD.

        Education alignment consists of:

            50% -> Degree alignment
            50% -> Field-of-study alignment

        Required degrees receive more importance than
        preferred degrees.

        JD fields_of_study are treated as acceptable
        alternatives.

        Missing candidate education data is handled
        explicitly without crashing the ATS engine.
        """

        # -------------------------------------------------
        # Validate JD education requirements
        # -------------------------------------------------

        if not jd_education:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "JD education requirements "
                    "are unavailable."
                )
            }

        # -------------------------------------------------
        # Handle missing candidate education
        # -------------------------------------------------

        if not education_data:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Education data is unavailable."
                )
            }

        # -------------------------------------------------
        # Read candidate education records
        # -------------------------------------------------

        education_records = education_data.get(
            "education",
            []
        )

        if not education_records:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Candidate education records "
                    "are unavailable."
                )
            }

        # -------------------------------------------------
        # Read JD education requirements
        # -------------------------------------------------

        required_degrees = jd_education.get(
            "required",
            []
        )

        preferred_degrees = jd_education.get(
            "preferred",
            []
        )

        required_fields = jd_education.get(
            "fields_of_study",
            []
        )

        # -------------------------------------------------
        # Degree matching helper
        # -------------------------------------------------

        def degree_matches(
            candidate_degree,
            required_degree
        ):

            candidate_degree = (
                str(candidate_degree)
                .lower()
                .strip()
            )

            required_degree = (
                str(required_degree)
                .lower()
                .strip()
            )

            # Bachelor's
            if (
                "bachelor" in required_degree
                and (
                    "bachelor"
                    in candidate_degree
                    or "b.tech"
                    in candidate_degree
                    or "btech"
                    in candidate_degree
                    or "b.e"
                    in candidate_degree
                    or candidate_degree == "be"
                )
            ):

                return True

            # Master's
            if (
                "master" in required_degree
                and (
                    "master"
                    in candidate_degree
                    or "m.tech"
                    in candidate_degree
                    or "mtech"
                    in candidate_degree
                    or "m.e"
                    in candidate_degree
                    or candidate_degree == "me"
                )
            ):

                return True

            # MBA
            if (
                "mba" in required_degree
                and "mba" in candidate_degree
            ):

                return True

            # Generic fallback
            return (
                required_degree
                in candidate_degree
            )

        # -------------------------------------------------
        # Collect candidate degrees
        # -------------------------------------------------

        candidate_degrees = []

        for record in education_records:

            if not isinstance(
                record,
                dict
            ):
                continue

            degree_type = record.get(
                "degree_type",
                ""
            )

            if degree_type:

                candidate_degrees.append(
                    str(degree_type)
                )

        # -------------------------------------------------
        # Required degree matching
        # -------------------------------------------------

        matched_required_degrees = []

        missing_required_degrees = []

        for required_degree in required_degrees:

            matched = any(
                degree_matches(
                    candidate_degree,
                    required_degree
                )
                for candidate_degree
                in candidate_degrees
            )

            if matched:

                matched_required_degrees.append(
                    required_degree
                )

            else:

                missing_required_degrees.append(
                    required_degree
                )

        if required_degrees:

            required_degree_score = (
                len(
                    matched_required_degrees
                )
                / len(required_degrees)
            )

        else:

            required_degree_score = 1.0

        # -------------------------------------------------
        # Preferred degree matching
        # -------------------------------------------------

        matched_preferred_degrees = []

        missing_preferred_degrees = []

        for preferred_degree in preferred_degrees:

            matched = any(
                degree_matches(
                    candidate_degree,
                    preferred_degree
                )
                for candidate_degree
                in candidate_degrees
            )

            if matched:

                matched_preferred_degrees.append(
                    preferred_degree
                )

            else:

                missing_preferred_degrees.append(
                    preferred_degree
                )

        if preferred_degrees:

            preferred_degree_score = (
                len(
                    matched_preferred_degrees
                )
                / len(preferred_degrees)
            )

        else:

            preferred_degree_score = 1.0

        # -------------------------------------------------
        # Combine degree scores
        # -------------------------------------------------

        if required_degrees:

            degree_score = (
                required_degree_score * 0.80
                + preferred_degree_score * 0.20
            )

        elif preferred_degrees:

            degree_score = (
                preferred_degree_score
            )

        else:

            degree_score = 1.0

        # -------------------------------------------------
        # Field-of-study matching
        # -------------------------------------------------

        candidate_fields = []

        for record in education_records:

            if not isinstance(
                record,
                dict
            ):
                continue

            field = record.get(
                "field_of_study",
                ""
            )

            if field:

                candidate_fields.append(
                    str(field)
                    .lower()
                    .strip()
                )

        normalized_required_fields = [
            str(field)
            .lower()
            .strip()
            for field in required_fields
        ]

        matched_fields = []

        for candidate_field in candidate_fields:

            for required_field in (
                normalized_required_fields
            ):

                if (
                    required_field
                    in candidate_field
                    or candidate_field
                    in required_field
                ):

                    if (
                        required_field
                        not in matched_fields
                    ):

                        matched_fields.append(
                            required_field
                        )

        # -------------------------------------------------
        # Fields are alternatives
        # -------------------------------------------------

        if not normalized_required_fields:

            field_relevance_score = 1.0

        elif matched_fields:

            field_relevance_score = 1.0

        else:

            field_relevance_score = 0.0

        # -------------------------------------------------
        # Final education score
        # -------------------------------------------------

        final_score = (
            degree_score * 0.50
            + field_relevance_score * 0.50
        )

        final_score = self.clamp(
            final_score
        )

        return {
            "available": True,
            "score": final_score * 100,
            "degree_score": (
                degree_score * 100
            ),
            "required_degree_score": (
                required_degree_score * 100
            ),
            "preferred_degree_score": (
                preferred_degree_score * 100
            ),
            "field_relevance_score": (
                field_relevance_score * 100
            ),
            "matched_required_degrees": (
                matched_required_degrees
            ),
            "missing_required_degrees": (
                missing_required_degrees
            ),
            "matched_preferred_degrees": (
                matched_preferred_degrees
            ),
            "missing_preferred_degrees": (
                missing_preferred_degrees
            ),
            "matched_fields": (
                matched_fields
            )
        }

    # =====================================================
    # 4. Semantic Similarity
    # =====================================================

    def calculate_semantic_similarity(
        self,
        semantic_result
    ):
        """
        Process the Day 12 semantic matching result.

        Day 12 produces a final semantic score in the
        observed 0-1 range.

        Day 13 converts this to the standard 0-100 scale.

        The Day 12 component scores are preserved for
        explainability.
        """

        # -------------------------------------------------
        # Handle missing semantic result
        # -------------------------------------------------

        if not semantic_result:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Semantic similarity data "
                    "is unavailable."
                )
            }

        # -------------------------------------------------
        # Read final semantic score
        # -------------------------------------------------

        raw_score = semantic_result.get(
            "final_semantic_score"
        )

        if raw_score is None:

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Final semantic similarity score "
                    "is unavailable."
                )
            }

        # -------------------------------------------------
        # Validate and clamp raw score
        # -------------------------------------------------

        try:

            raw_score = float(
                raw_score
            )

        except (
            TypeError,
            ValueError
        ):

            return {
                "available": False,
                "score": None,
                "reason": (
                    "Semantic similarity score "
                    "is not numeric."
                )
            }

        raw_score = self.clamp(
            raw_score
        )

        # -------------------------------------------------
        # Convert 0-1 to 0-100
        # -------------------------------------------------

        final_score = raw_score * 100

        # -------------------------------------------------
        # Preserve Day 12 component scores
        # -------------------------------------------------

        component_scores = semantic_result.get(
            "component_scores",
            {}
        )

        available_components = semantic_result.get(
            "available_components",
            []
        )

        return {
            "available": True,
            "score": final_score,
            "raw_score": raw_score,
            "component_scores": component_scores,
            "available_components": available_components
        }