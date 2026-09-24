from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    """
    Converts text into semantic embedding vectors.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text):
        """
        Convert a single text into an embedding vector.
        """

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        if not text.strip():
            raise ValueError("Input text cannot be empty.")

        embedding = self.model.encode(text)

        return embedding

    def generate_embeddings(self, texts):
        """
        Convert multiple texts into embedding vectors.
        """

        if not isinstance(texts, list):
            raise TypeError("Input must be a list of strings.")

        if not texts:
            raise ValueError("Input list cannot be empty.")

        if not all(isinstance(text, str) for text in texts):
            raise TypeError("All inputs must be strings.")

        embeddings = self.model.encode(texts)

        return embeddings


if __name__ == "__main__":

    print("Loading embedding model...")

    engine = EmbeddingEngine()

    sample_text = (
        "Python developer with experience in "
        "machine learning and data analysis."
    )

    embedding = engine.generate_embedding(sample_text)

    print("Embedding engine loaded successfully.")
    print("Model:", engine.model_name)
    print("Embedding dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])
    