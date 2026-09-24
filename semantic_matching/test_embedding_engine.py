import numpy as np
import pytest

from embedding_engine import EmbeddingEngine


@pytest.fixture(scope="module")
def embedding_engine():
    return EmbeddingEngine()


def test_embedding_engine_initialization(embedding_engine):
    assert embedding_engine.model is not None
    assert embedding_engine.model_name == "all-MiniLM-L6-v2"


def test_single_text_embedding(embedding_engine):
    text = "Python developer with machine learning experience."

    embedding = embedding_engine.generate_embedding(text)

    assert embedding is not None
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (384,)


def test_multiple_text_embeddings(embedding_engine):
    texts = [
        "Python developer",
        "Machine learning engineer",
        "Business analyst"
    ]

    embeddings = embedding_engine.generate_embeddings(texts)

    assert embeddings is not None
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (3, 384)


def test_empty_text_rejected(embedding_engine):
    with pytest.raises(ValueError):
        embedding_engine.generate_embedding("")


def test_invalid_text_type_rejected(embedding_engine):
    with pytest.raises(TypeError):
        embedding_engine.generate_embedding(123)
        