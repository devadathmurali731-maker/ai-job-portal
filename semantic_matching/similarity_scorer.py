import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityScorer:
    """
    Calculates semantic similarity between embedding vectors.
    """

    @staticmethod
    def cosine_similarity_score(embedding_1, embedding_2):
        """
        Calculate cosine similarity between two embedding vectors.
        """

        vector_1 = np.asarray(embedding_1).reshape(1, -1)
        vector_2 = np.asarray(embedding_2).reshape(1, -1)

        score = cosine_similarity(vector_1, vector_2)[0][0]

        return float(score)

    @staticmethod
    def similarity_matrix(embeddings_1, embeddings_2):
        """
        Calculate pairwise cosine similarity between two groups
        of embedding vectors.
        """

        embeddings_1 = np.asarray(embeddings_1)
        embeddings_2 = np.asarray(embeddings_2)

        return cosine_similarity(embeddings_1, embeddings_2)


if __name__ == "__main__":

    from embedding_engine import EmbeddingEngine

    print("Loading embedding engine...")

    engine = EmbeddingEngine()

    text_1 = "Python developer with machine learning experience."
    text_2 = "Machine learning engineer experienced in Python."
    text_3 = "Graphic designer specializing in visual design."

    embedding_1 = engine.generate_embedding(text_1)
    embedding_2 = engine.generate_embedding(text_2)
    embedding_3 = engine.generate_embedding(text_3)

    scorer = SimilarityScorer()

    score_1 = scorer.cosine_similarity_score(
        embedding_1,
        embedding_2
    )

    score_2 = scorer.cosine_similarity_score(
        embedding_1,
        embedding_3
    )

    print("\nSimilarity Results:")
    print(f"Text 1 ↔ Text 2: {score_1:.4f}")
    print(f"Text 1 ↔ Text 3: {score_2:.4f}")
    