from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from src.domain.document import Chunk


class VectorStore:
    def __init__(self, directory: Path, embedding_dimension: int, embedding_model: str) -> None:
        self._directory = directory
        self._embedding_dimension = embedding_dimension
        self._embedding_model = embedding_model
        self._faiss_index = None
        self._chunks: List[Chunk] = []
        self._index_path = directory / "index.faiss"
        self._chunks_path = directory / "chunks.json"
        self._version_path = directory / "version.json"

    @property
    def directory(self) -> Path:
        return self._directory

    def build(self, chunks: Sequence[Chunk], embeddings: Sequence[Sequence[float]]) -> None:
        try:
            import faiss
            import numpy as np
        except ImportError as exc:
            raise ImportError("faiss-cpu is not installed") from exc

        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings length mismatch")
        if not chunks:
            raise ValueError("cannot build vector store with zero chunks")

        vectors = np.asarray(embeddings, dtype=np.float32)
        if vectors.shape[1] != self._embedding_dimension:
            raise ValueError(
                f"embedding dimension mismatch: got {vectors.shape[1]}, "
                f"expected {self._embedding_dimension}"
            )
        index = faiss.IndexFlatIP(vectors.shape[1])
        try:
            faiss.normalize_L2(vectors)
        except Exception:
            pass
        index.add(vectors)

        self._faiss_index = index
        self._chunks = list(chunks)

    def save(self) -> None:
        if self._faiss_index is None:
            raise RuntimeError("index has not been built yet")
        self._directory.mkdir(parents=True, exist_ok=True)
        try:
            import faiss
        except ImportError as exc:
            raise ImportError("faiss-cpu is not installed") from exc
        faiss.write_index(self._faiss_index, str(self._index_path))
        self._chunks_path.write_text(
            json.dumps([self._chunk_to_dict(c) for c in self._chunks], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._write_version(len(self._chunks))

    def load(self) -> None:
        if not self._index_path.exists() or not self._chunks_path.exists():
            raise FileNotFoundError("index not found")
        try:
            import faiss
        except ImportError as exc:
            raise ImportError("faiss-cpu is not installed") from exc
        self._faiss_index = faiss.read_index(str(self._index_path))
        raw_chunks = json.loads(self._chunks_path.read_text(encoding="utf-8"))
        self._chunks = [self._dict_to_chunk(c) for c in raw_chunks]

    def search(self, query_vector: Sequence[float], top_k: int) -> List[tuple[Chunk, float]]:
        if self._faiss_index is None:
            raise RuntimeError("index is not loaded")
        try:
            import numpy as np
        except ImportError as exc:
            raise ImportError("numpy is required") from exc
        vec = np.asarray([query_vector], dtype=np.float32)
        try:
            import faiss
            faiss.normalize_L2(vec)
        except Exception:
            pass
        scores, ids = self._faiss_index.search(vec, k=top_k)
        results: List[tuple[Chunk, float]] = []
        for idx, score in zip(ids[0].tolist(), scores[0].tolist()):
            if 0 <= idx < len(self._chunks):
                results.append((self._chunks[idx], float(score)))
        return results

    def version_info(self) -> Dict:
        if self._version_path.exists():
            return json.loads(self._version_path.read_text(encoding="utf-8"))
        return {}

    def _write_version(self, document_count: int) -> None:
        data = {
            "index_version": "1.0.0",
            "documents": document_count,
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "embedding_model": self._embedding_model,
            "embedding_dimension": self._embedding_dimension,
        }
        self._version_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _chunk_to_dict(chunk: Chunk) -> Dict:
        return {
            "chunk_id": chunk.chunk_id,
            "doc_id": chunk.doc_id,
            "doc_title": chunk.doc_title,
            "source": chunk.source,
            "content": chunk.content,
            "index": chunk.index,
            "page": chunk.page,
            "section": chunk.section,
            "metadata": chunk.metadata,
        }

    @staticmethod
    def _dict_to_chunk(data: Dict) -> Chunk:
        return Chunk(
            chunk_id=data["chunk_id"],
            doc_id=data["doc_id"],
            doc_title=data["doc_title"],
            source=data["source"],
            content=data["content"],
            index=data.get("index", 0),
            page=data.get("page"),
            section=data.get("section"),
            metadata=data.get("metadata") or {},
        )
