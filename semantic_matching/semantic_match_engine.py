from component_matcher import ComponentMatcher
from data_component_extractor import DataComponentExtractor


class SemanticMatchEngine:
    """
    Performs real-data semantic matching between
    processed resumes and job descriptions.
    """

    DEFAULT_WEIGHTS = {
        "skills": 0.50,
        "experience": 0.30,
        "projects": 0.20
    }

    def __init__(self):
        self.component_matcher = ComponentMatcher()
        self.data_extractor = DataComponentExtractor()

    def calculate_weighted_score(
        self,
        component_scores,
        available_components
    ):
        """
        Calculate the final weighted semantic score.

        If a component is unavailable, its weight is
        redistributed proportionally among available components.
        """

        if not available_components:
            raise ValueError(
                "At least one component must be available."
            )

        total_weight = sum(
            self.DEFAULT_WEIGHTS[component]
            for component in available_components
        )

        final_score = 0.0

        for component in available_components:

            normalized_weight = (
                self.DEFAULT_WEIGHTS[component]
                / total_weight
            )

            final_score += (
                component_scores[component]
                * normalized_weight
            )

        return float(final_score)

    def match_resume_to_jd(
        self,
        resume_id,
        jd_id
    ):
        """
        Perform semantic matching between a real
        processed resume and a real processed JD.
        """

        resume_components = (
            self.data_extractor.extract_resume_components(
                resume_id
            )
        )

        jd_components = (
            self.data_extractor.extract_jd_components(
                jd_id
            )
        )

        component_scores = {}
        available_components = []

        for component in [
            "skills",
            "experience",
            "projects"
        ]:

            resume_text = resume_components.get(
                component,
                ""
            )

            jd_text = jd_components.get(
                component,
                ""
            )

            # Compare only when both sides contain
            # genuine information.
            if (
                resume_text
                and resume_text.strip()
                and jd_text
                and jd_text.strip()
            ):

                score = (
                    self.component_matcher
                    .calculate_component_similarity(
                        resume_text,
                        jd_text
                    )
                )

                component_scores[component] = score

                available_components.append(
                    component
                )

        if not available_components:
            raise ValueError(
                "No comparable semantic components found."
            )

        final_score = self.calculate_weighted_score(
            component_scores,
            available_components
        )

        return {
            "resume_id": resume_id,
            "jd_id": jd_id,
            "component_scores": component_scores,
            "available_components": available_components,
            "final_semantic_score": final_score
        }


if __name__ == "__main__":

    print("Initializing Real Semantic Matching Engine...")

    engine = SemanticMatchEngine()

    result = engine.match_resume_to_jd(
        "resume_001",
        "jd_001_data_scientist"
    )

    print("\nSemantic Matching Result:")
    print("-------------------------")

    print(
        f"Resume: {result['resume_id']}"
    )

    print(
        f"Job Description: {result['jd_id']}"
    )

    print("\nComponent Scores:")

    for component, score in result[
        "component_scores"
    ].items():

        print(
            f"{component.title()} similarity: "
            f"{score:.4f}"
        )

    print(
        "\nAvailable Components:",
        ", ".join(
            result["available_components"]
        )
    )

    print(
        "\nFinal Semantic Score:",
        f"{result['final_semantic_score']:.4f}"
    )
    