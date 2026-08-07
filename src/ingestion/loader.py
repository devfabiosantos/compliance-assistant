from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from src.domain.document import Document


class DocumentLoader:
    def __init__(
        self,
        *,
        excluded_names: Optional[Sequence[str]] = None,
        excluded_suffixes: Optional[Sequence[str]] = None,
    ) -> None:
        self._supported_pdf = {".pdf"}
        self._supported_md = {".md"}
        self._excluded_names = {n.lower() for n in (excluded_names or ["README.md", "readme.md"])}
        self._excluded_suffixes = {s.lower() for s in (excluded_suffixes or [])}

    def _should_skip(self, file_path: Path) -> bool:
        if file_path.name.lower() in self._excluded_names:
            return True
        if any(file_path.name.lower().endswith(s) for s in self._excluded_suffixes):
            return True
        return False

    def load_directory(self, directory: Path, *, category: str) -> List[Document]:
        if not directory.exists():
            return []
        docs: List[Document] = []
        for file_path in sorted(directory.iterdir()):
            if not file_path.is_file():
                continue
            if self._should_skip(file_path):
                continue
            if file_path.suffix.lower() in self._supported_pdf:
                docs.append(self._load_pdf(file_path, category=category))
            elif file_path.suffix.lower() in self._supported_md:
                docs.append(self._load_markdown(file_path, category=category))
        return docs

    def load_many(self, directories: Iterable[tuple[Path, str]]) -> List[Document]:
        all_docs: List[Document] = []
        for directory, category in directories:
            all_docs.extend(self.load_directory(directory, category=category))
        return all_docs

    def _load_pdf(self, file_path: Path, *, category: str) -> Document:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ImportError("pypdf package is not installed") from exc
        reader = PdfReader(str(file_path))
        pages: List[str] = []
        for i, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            pages.append(f"[Pagina {i}]\n{text}")
        content = "\n\n".join(pages)
        return Document.from_text(
            title=file_path.stem.replace("_", " ").title(),
            content=content,
            source=file_path.name,
            category=category,
            file_path=file_path,
            metadata={"page_count": len(reader.pages)},
        )

    def _load_markdown(self, file_path: Path, *, category: str) -> Document:
        content = file_path.read_text(encoding="utf-8")
        return Document.from_text(
            title=file_path.stem.replace("_", " ").title(),
            content=content,
            source=file_path.name,
            category=category,
            file_path=file_path,
        )
