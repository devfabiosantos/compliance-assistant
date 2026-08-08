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
            is_separator_regex=False,
        )

        chunks: List[Chunk] = []
        for doc in documents:
            outlines = self._extract_outline(doc.content)
            langchain_docs = splitter.create_documents([doc.content])
            last_section: str | None = None
            for i, lc_doc in enumerate(langchain_docs):
                text = lc_doc.page_content
                page = self._guess_page(text)
                section = self._guess_section(text, outlines, last_section)
                if section:
                    last_section = section
                chunk_meta = {**doc.metadata}
                if outlines:
                    chunk_meta["_outline"] = outlines
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}#{i}",
                        doc_id=doc.doc_id,
                        doc_title=doc.title,
                        source=doc.source,
                        content=text,
                        index=i,
                        page=page,
                        section=section or last_section,
                        metadata=chunk_meta,
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
    def _extract_outline(content: str) -> list[tuple[int, int, str]]:
        import re

        outline: list[tuple[int, int, str]] = []
        lines = content.splitlines()
        for idx, raw in enumerate(lines):
            line = raw.strip()
            m = re.match(r"^(#{1,4})\s+(.+)$", line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                if level == 1:
                    continue
                outline.append((idx, level, title))
                continue
            m2 = re.match(r"^(Seção|Secao|SEÇÃO|SECÃO)\s+(\d+(?:\.\d+)*)\s*(.*)?$", line)
            if m2:
                title_parts = [m2.group(2)]
                if m2.group(3):
                    title_parts.append(m2.group(3).strip(" .:—-"))
                outline.append((idx, 2, " - ".join(p for p in title_parts if p)))
        return outline

    @staticmethod
    def _guess_section(text: str, outlines: list[tuple[int, int, str]] | None, fallback: str | None) -> str | None:
        import re

        candidates = [
            r"^##\s+(.+)$",
            r"^###\s+(.+)$",
            r"^####\s+(.+)$",
            r"^Seção\s+(\d+(?:\.\d+)*)\s*(.+)?$",
            r"^Secao\s+(\d+(?:\.\d+)*)\s*(.+)?$",
        ]
        for line in text.splitlines()[:8]:
            for pattern in candidates:
                m = re.match(pattern, line.strip())
                if m:
                    groups = [g for g in m.groups() if g]
                    return " - ".join(groups)[:120] if groups else None
        if outlines:
            combined = "\n".join(text.splitlines()[:6])[:320]
            for _idx, _lvl, title in outlines:
                tn = title.strip().lower()
                if tn and tn in combined.lower():
                    return title[:120]
        return fallback
