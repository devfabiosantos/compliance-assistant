from __future__ import annotations

from typing import List, Optional, Sequence

from src.providers.base import EmbeddingProvider


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
        response = self._client.embed(
            texts=list(texts),
            model=self._model,
            input_type="search_document",
        )
        return _extract_float_embeddings(response)

    def embed_query(self, text: str) -> List[float]:
        response = self._client.embed(
            texts=[text],
            model=self._model,
            input_type="search_query",
        )
        return _extract_float_embeddings(response)[0]
