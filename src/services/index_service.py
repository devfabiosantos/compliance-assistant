from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from src.config.settings import Settings
from src.domain.document import Document
from src.ingestion.loader import DocumentLoader
from src.ingestion.splitter import DocumentSplitter
from src.providers.base import EmbeddingProvider
from src.retrieval.vector_store import VectorStore

logger = logging.getLogger(__name__)


@dataclass
class IndexSummary:
    document_count: int
    chunk_count: int
    embedding_model: str
    vector_store_dir: Path
    generated_at: str


class IndexService:
    def __init__(
        self,
        settings: Settings,
        embedding_provider: EmbeddingProvider,
        loader: DocumentLoader | None = None,
        splitter: DocumentSplitter | None = None,
    ) -> None:
        self._settings = settings
        self._embedding_provider = embedding_provider
        self._loader = loader or DocumentLoader()
        self._splitter = splitter or DocumentSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def build_and_save(self) -> IndexSummary:
        logger.info("starting document ingestion")
        documents: List[Document] = self._loader.load_many(
            [
                (self._settings.paths.docs_official_dir, "oficial"),
                (self._settings.paths.docs_company_dir, "empresa"),
            ]
        )
        if not documents:
            logger.warning("nenhum documento encontrado para indexar")
        logger.info("documents loaded", extra={"count": len(documents)})

        chunks = self._splitter.split_documents(documents)
        if not chunks:
            raise RuntimeError("nenhum chunk gerado a partir dos documentos")
        logger.info("chunks prepared", extra={"count": len(chunks)})

        logger.info("gerando embeddings via %s", self._embedding_provider.name)
        texts = [c.content for c in chunks]
        embeddings = self._embedding_provider.embed_documents(texts)

        store = VectorStore(
            directory=self._settings.paths.vector_store_dir,
            embedding_dimension=len(embeddings[0]),
            embedding_model=self._embedding_provider.name,
        )
        store.build(chunks, embeddings)
        store.save()
        logger.info("indice vetorial salvo", extra={"path": str(store.directory)})

        return IndexSummary(
            document_count=len(documents),
            chunk_count=len(chunks),
            embedding_model=self._embedding_provider.name,
            vector_store_dir=store.directory,
            generated_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )

    def version_info(self) -> Dict:
        version_file = self._settings.paths.vector_store_dir / "version.json"
        if not version_file.exists():
            return {}
        return json.loads(version_file.read_text(encoding="utf-8"))
