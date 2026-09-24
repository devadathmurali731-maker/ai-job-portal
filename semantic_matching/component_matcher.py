from embedding_engine import EmbeddingEngine
from similarity_scorer import SimilarityScorer


class ComponentMatcher:
    """
    Performs semantic matching for individual resume
    and job-description components.
    """

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.similarity_scorer = SimilarityScorer()

    def calculate_component_similarity(
        self,
        resume_component,
        jd_component
    ):
        """
        Calculate semantic similarity between two text components.
        """

        if not isinstance(resume_component, str):
            raise TypeError("Resume component must be a string.")

        if not isinstance(jd_component, str):
            raise TypeError("JD component must be a string.")

        if not resume_component.strip():
            raise ValueError("Resume component cannot be empty.")

        if not jd_component.strip():
            raise ValueError("JD component cannot be empty.")

        resume_embedding = (
            self.embedding_engine.generate_embedding(
                resume_component
            )
        )

        jd_embedding = (
            self.embedding_engine.generate_embedding(
                jd_component
            )
        )

        score = (
            self.similarity_scorer.cosine_similarity_score(
                resume_embedding,
                jd_embedding
            )
        )

        return score

    def compare_components(
        self,
        resume_components,
        jd_components
    ):
        """
        Compare corresponding resume and JD components.

        Expected keys:
        - skills
        - experience
        - projects
        """

        required_components = [
            "skills",
            "experience",
            "projects"
        ]

        for component in required_components:

            if component not in resume_components:
                raise KeyError(
                    f"Missing resume component: {component}"
                )

            if component not in jd_components:
                raise KeyError(
                    f"Missing JD component: {component}"
                )

        results = {}

        for component in required_components:

            results[component] = (
                self.calculate_component_similarity(
                    resume_components[component],
                    jd_components[component]
                )
            )

        return results


if __name__ == "__main__":

    print("Initializing Component Matching Engine...")

    matcher = ComponentMatcher()

    resume_components = {
        "skills": """
        Python, SQL, machine learning, pandas,
        NumPy, scikit-learn and Docker.
        """,

        "experience": """
        Developed data applications using Python and SQL.
        Built machine learning models and worked with
        production data pipelines.
        """,

        "projects": """
        Developed a machine learning project for predicting
        customer churn using Python and scikit-learn.
        """
    }

    jd_components = {
        "skills": """
        Required skills include Python, SQL, machine learning,
        pandas, NumPy, scikit-learn and Docker.
        """,

        "experience": """
        Candidate should have experience developing Python
        applications, working with SQL and building machine
        learning solutions.
        """,

        "projects": """
        Experience with machine learning projects,
        predictive modeling and Python-based data science
        applications is preferred.
        """
    }

    results = matcher.compare_components(
        resume_components,
        jd_components
    )

    print("\nComponent Semantic Similarity:")

    for component, score in results.items():
        print(f"{component.title()} similarity: {score:.4f}")