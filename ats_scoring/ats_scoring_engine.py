"""
ATS Scoring Engine.

Combines four explainable scoring components:

1. Skill Match
2. Experience Relevance
3. Education Alignment
4. Semantic Similarity

The engine supports:

- Role-specific weights
- Missing-data handling
- Dynamic weight redistribution
- Explainable component contributions
- Final ATS score from 0-100
"""

from .scoring_config import get_role_weights
from .scoring_components import ScoringComponents


class ATSScoringEngine:
    """Main engine for calculating the final ATS score."""

    COMPONENTS = [
        "skill_match",
        "experience_relevance",
        "education_alignment",
        "semantic_similarity"
    ]

    def __init__(self):
        """Initialize scoring components."""

        self.components = ScoringComponents()

    # ---------------------------------------------------------
    # Dynamic weight redistribution
    # ---------------------------------------------------------

    @staticmethod
    def redistribute_weights(
        original_weights,
        available_components
    ):
        """
        Redistribute weights across available components.

        If a component is missing, its weight is distributed
        proportionally among the remaining available components.
        """

        available_weights = {
            component: original_weights[component]
            for component in available_components
            if component in original_weights
        }

        total_available_weight = sum(
            available_weights.values()
        )

        # -----------------------------------------------------
        # No components available
        # -----------------------------------------------------

        if total_available_weight <= 0:

            return {
                component: 0.0
                for component in original_weights
            }

        # -----------------------------------------------------
        # Normalize available weights
        # -----------------------------------------------------

        adjusted_weights = {}

        for component in original_weights:

            if component in available_weights:

                adjusted_weights[component] = (
                    available_weights[component]
                    / total_available_weight
                )

            else:

                adjusted_weights[component] = 0.0

        return adjusted_weights

    # ---------------------------------------------------------
    # Main ATS scoring method
    # ---------------------------------------------------------

    def calculate_score(
        self,
        candidate_id,
        job_id,
        role,
        resume_skills,
        experience_data,
        education_data,
        semantic_result,
        jd_skills,
        jd_experience,
        jd_education
    ):
        """
        Calculate the complete ATS score.

        Parameters
        ----------
        candidate_id:
            Unique candidate identifier.

        job_id:
            Unique job identifier.

        role:
            Target job role.

        resume_skills:
            Extracted candidate skills.

        experience_data:
            Extracted candidate experience.

        education_data:
            Extracted candidate education.

        semantic_result:
            Day 12 semantic matching result.

        jd_skills:
            Structured JD skill requirements.

        jd_experience:
            Structured JD experience requirements.

        jd_education:
            Structured JD education requirements.

        Returns
        -------
        dict
            Complete explainable ATS scoring result.
        """

        # -----------------------------------------------------
        # 1. Load role-specific weights
        # -----------------------------------------------------

        original_weights = get_role_weights(
            role
        )

        # -----------------------------------------------------
        # 2. Skill Match
        # -----------------------------------------------------

        skill_result = (
            self.components.calculate_skill_match(
                resume_skills,
                jd_skills
            )
        )

        # -----------------------------------------------------
        # 3. Experience Relevance
        #
        # IMPORTANT:
        # We pass the CURRENT role and CURRENT JD skills.
        #
        # This prevents Day 10's old Software Engineer
        # relevance analysis from being incorrectly reused
        # for another role such as Data Scientist.
        # -----------------------------------------------------

        experience_result = (
            self.components.calculate_experience_relevance(
                experience_data,
                jd_experience,
                role,
                jd_skills
            )
        )

        # -----------------------------------------------------
        # 4. Education Alignment
        #
        # Uses the CURRENT JD education requirements.
        # -----------------------------------------------------

        education_result = (
            self.components.calculate_education_alignment(
                education_data,
                jd_education
            )
        )

        # -----------------------------------------------------
        # 5. Semantic Similarity
        #
        # Uses Day 12 semantic matching result.
        # -----------------------------------------------------

        semantic_result_processed = (
            self.components.calculate_semantic_similarity(
                semantic_result
            )
        )

        # -----------------------------------------------------
        # 6. Store component results
        # -----------------------------------------------------

        component_results = {
            "skill_match": skill_result,

            "experience_relevance": (
                experience_result
            ),

            "education_alignment": (
                education_result
            ),

            "semantic_similarity": (
                semantic_result_processed
            )
        }

        # -----------------------------------------------------
        # 7. Determine available components
        # -----------------------------------------------------

        available_components = []

        missing_components = []

        for component in self.COMPONENTS:

            result = component_results[
                component
            ]

            if (
                result.get("available", True)
                and result.get("score") is not None
            ):

                available_components.append(
                    component
                )

            else:

                missing_components.append(
                    component
                )

        # -----------------------------------------------------
        # 8. Dynamically redistribute weights
        # -----------------------------------------------------

        adjusted_weights = (
            self.redistribute_weights(
                original_weights,
                available_components
            )
        )

        # -----------------------------------------------------
        # 9. Calculate weighted contributions
        # -----------------------------------------------------

        weighted_contributions = {}

        for component in self.COMPONENTS:

            result = component_results[
                component
            ]

            score = result.get(
                "score"
            )

            weight = adjusted_weights.get(
                component,
                0.0
            )

            if score is None:

                weighted_contributions[
                    component
                ] = 0.0

            else:

                weighted_contributions[
                    component
                ] = round(
                    score * weight,
                    4
                )

        # -----------------------------------------------------
        # 10. Calculate final ATS score
        # -----------------------------------------------------

        final_ats_score = sum(
            weighted_contributions.values()
        )

        final_ats_score = round(
            final_ats_score,
            2
        )

        # -----------------------------------------------------
        # 11. Component score summary
        # -----------------------------------------------------

        component_scores = {}

        for component in self.COMPONENTS:

            component_scores[
                component
            ] = component_results[
                component
            ].get("score")

        # -----------------------------------------------------
        # 12. Return complete explainable result
        # -----------------------------------------------------

        return {
            "candidate_id": candidate_id,

            "job_id": job_id,

            "role": role,

            "component_scores": (
                component_scores
            ),

            "original_weights": (
                original_weights
            ),

            "adjusted_weights": (
                adjusted_weights
            ),

            "weighted_contributions": (
                weighted_contributions
            ),

            "final_ats_score": (
                final_ats_score
            ),

            "available_components": (
                available_components
            ),

            "missing_components": (
                missing_components
            ),

            "component_details": {

                "skill_match": (
                    skill_result
                ),

                "experience_relevance": (
                    experience_result
                ),

                "education_alignment": (
                    education_result
                ),

                "semantic_similarity": (
                    semantic_result_processed
                )
            }
        }
