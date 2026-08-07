from __future__ import annotations

from typing import List

from src.domain.document import Chunk, Document


class DocumentSplitter:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120) -> None:
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    def split_documents(self, documents: List[Document]) -> List[Chunk]:
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError as exc:
            raise ImportError("langchain-text-splitters is not installed") from exc
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        chunks: List[Chunk] = []
        for doc in documents:
            langchain_docs = splitter.create_documents([doc.content])
            for i, lc_doc in enumerate(langchain_docs):
                text = lc_doc.page_content
                page = self._guess_page(text)
                section = self._guess_section(text)
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}#{i}",
                        doc_id=doc.doc_id,
                        doc_title=doc.title,
                        source=doc.source,
                        content=text,
                        index=i,
                        page=page,
                        section=section,
                        metadata={**doc.metadata},
                    )
                )
        return chunks

    @staticmethod
    def _guess_page(text: str) -> int | None:
        import re

        m = re.search(r"\[Pagina\s+(\d+)\]", text)
        if m:
            return int(m.group(1))
        return None

    @staticmethod
    def _guess_section(text: str) -> str | None:
        import re

        candidates = [
            r"^#\s+(.+)$",
            r"^##\s+(.+)$",
            r"^###\s+(.+)$",
            r"^Seção\s+(\d+(?:\.\d+)*)\s*(.+)?$",
            r"^Secao\s+(\d+(?:\.\d+)*)\s*(.+)?$",
        ]
        for line in text.splitlines()[:8]:
            for pattern in candidates:
                m = re.match(pattern, line.strip())
                if m:
                    groups = [g for g in m.groups() if g]
                    return " - ".join(groups)[:80] if groups else None
        return None
