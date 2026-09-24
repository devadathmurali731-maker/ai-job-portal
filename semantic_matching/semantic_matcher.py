from embedding_engine import EmbeddingEngine
from similarity_scorer import SimilarityScorer


class SemanticMatcher:
    """
    Performs semantic matching between resume text
    and job description text.
    """

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.similarity_scorer = SimilarityScorer()

    def calculate_similarity(self, resume_text, job_description):
        """
        Calculate semantic similarity between a resume
        and a job description.
        """

        if not isinstance(resume_text, str):
            raise TypeError("Resume text must be a string.")

        if not isinstance(job_description, str):
            raise TypeError("Job description must be a string.")

        if not resume_text.strip():
            raise ValueError("Resume text cannot be empty.")

        if not job_description.strip():
            raise ValueError("Job description cannot be empty.")

        resume_embedding = self.embedding_engine.generate_embedding(
            resume_text
        )

        jd_embedding = self.embedding_engine.generate_embedding(
            job_description
        )

        similarity_score = (
            self.similarity_scorer.cosine_similarity_score(
                resume_embedding,
                jd_embedding
            )
        )

        return similarity_score


if __name__ == "__main__":

    print("Initializing Semantic Matching Engine...")

    matcher = SemanticMatcher()

    resume_text = """
    Software Engineer with experience in Python, SQL, REST APIs,
    Docker, Git and database development.
    """

    job_description = """
    We are looking for a Software Engineer with strong Python,
    SQL, API development, Docker and database skills.
    """

    similarity_score = matcher.calculate_similarity(
        resume_text,
        job_description
    )

    print("\nSemantic Matching Result:")
    print(f"Resume ↔ JD similarity: {similarity_score:.4f}")