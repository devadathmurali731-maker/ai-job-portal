import numpy as np
import pytest

from similarity_scorer import SimilarityScorer


def test_identical_vectors_have_similarity_one():
    vector = np.array([1.0, 2.0, 3.0])

    score = SimilarityScorer.cosine_similarity_score(
        vector,
        vector
    )

    assert score == pytest.approx(1.0)


def test_similar_vectors_have_high_similarity():
    vector_1 = np.array([1.0, 2.0, 3.0])
    vector_2 = np.array([1.1, 2.1, 3.1])

    score = SimilarityScorer.cosine_similarity_score(
        vector_1,
        vector_2
    )

    assert score > 0.99


def test_different_vectors_have_lower_similarity():
    vector_1 = np.array([1.0, 0.0, 0.0])
    vector_2 = np.array([0.0, 1.0, 0.0])

    score = SimilarityScorer.cosine_similarity_score(
        vector_1,
        vector_2
    )

    assert score == pytest.approx(0.0)


def test_similarity_score_is_float():
    vector_1 = np.array([1.0, 2.0, 3.0])
    vector_2 = np.array([3.0, 2.0, 1.0])

    score = SimilarityScorer.cosine_similarity_score(
        vector_1,
        vector_2
    )

    assert isinstance(score, float)


def test_similarity_matrix_shape():
    embeddings_1 = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ])

    embeddings_2 = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 1.0, 0.0]
    ])

    matrix = SimilarityScorer.similarity_matrix(
        embeddings_1,
        embeddings_2
    )

    assert matrix.shape == (2, 3)
    