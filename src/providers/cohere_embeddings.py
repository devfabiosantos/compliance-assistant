from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from src.providers.base import EmbeddingProvider

COHERE_EMBED_MAX_BATCH = 96


def _iter_batches(items: Sequence[str], batch_size: int) -> Iterable[List[str]]:
    total = len(items)
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield list(items[start:end])


def _extract_float_embeddings(response) -> List[List[float]]:
    by_type = getattr(response, "embeddings", None)
    if by_type is None:
        raise ValueError("resposta do Cohere nao possui campo 'embeddings'")
    vecs: Optional[List[List[float]]] = getattr(by_type, "float_", None)
    if vecs is None:
        try:
            vecs = getattr(by_type, "float", None)
        except Exception:
            vecs = None
    if not vecs:
        raise ValueError(
            "Nao foi possivel extrair embeddings float do Cohere. Verifique a versao do SDK cohere e o modelo configurado."
        )
    return [list(v) for v in vecs]


class CohereEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "embed-multilingual-v3.0") -> None:
        if not api_key:
            raise ValueError("Cohere API key is required")
        try:
            import cohere
        except ImportError as exc:
            raise ImportError("cohere package is not installed") from exc
        self._client = cohere.ClientV2(api_key=api_key)
        self._model = model
        self.name = f"cohere/embed/{model}"
        self._dimension_cache: int | None = None

    @property
    def dimension(self) -> int:
        if self._dimension_cache is not None:
            return self._dimension_cache
        sample = self.embed_query("sample")
        self._dimension_cache = len(sample)
        return self._dimension_cache

    def embed_documents(self, texts: Sequence[str]) -> List[List[float]]:
        if not texts:
            return []
        all_vecs: List[List[float]] = []
        for batch in _iter_batches(texts, COHERE_EMBED_MAX_BATCH):
            response = self._client.embed(
                texts=batch,
                model=self._model,
                input_type="search_document",
            )
            all_vecs.extend(_extract_float_embeddings(response))
        return all_vecs

    def embed_query(self, text: str) -> List[float]:
        response = self._client.embed(
            texts=[text],
            model=self._model,
            input_type="search_query",
        )
        return _extract_float_embeddings(response)[0]
