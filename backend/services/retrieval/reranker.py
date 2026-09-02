from sentence_transformers import CrossEncoder

from models import SearchResult

_model: CrossEncoder | None = None


def get_model() -> CrossEncoder:
    global _model

    if _model is None:
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

    return _model


def rerank(
    question: str,
    result: SearchResult,
    top_k: int = 5,
) -> SearchResult:

    try:
        model = get_model()
    except Exception as e:
        print(f"Error occurred while initializing the reranker model: {e}")
        raise

    pairs = [
        [question, chunk.text]
        for chunk in result.chunks
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(result.chunks, scores),
        key=lambda x: x[1],
        reverse=True,
    )
    try:
        for chunk, score in ranked:
            chunk.rerank_score = float(score)
    except Exception as e:
        print(f"Error occurred while processing reranked results: {e}")
        raise

    return SearchResult(
    chunks=[chunk for chunk, _ in ranked[:top_k]]
    )