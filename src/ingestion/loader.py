from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from src.domain.document import Document


DOCUMENT_ALIASES: dict[str, list[str]] = {
    "lgpd_leil_13709_2018": [
        "LGPD",
        "Lei 13.709",
        "Lei Geral de Proteção de Dados",
        "Lei Geral Protecao Dados",
    ],
    "guia_anpd_metodos_aplicacao": [
        "Guia ANPD",
        "Guia Metodos Aplicacao",
        "ANPD Guia",
    ],
    "faq_anpd_principal": [
        "FAQ ANPD",
        "FAQ Principal",
        "Perguntas Frequentes ANPD",
    ],
    "codigo_etica_conduta": [
        "Código de Ética",
        "Codigo de Etica",
        "Código Ética e Conduta",
        "Codigo Etica Conduta",
        "Ética",
        "Etica",
    ],
    "organograma_novadata_solutions": [
        "Organograma",
        "Estrutura Organizacional",
        "Hierarquia",
    ],
    "politica_seguranca_informacao": [
        "Política Segurança da Informação",
        "Política Segurança Informação",
        "Política Segurança",
        "Politica Seguranca",
        "PSI",
        "Segurança Informação",
        "Seguranca da Informacao",
        "Seguranca",
    ],
    "politica_privacidade_lgpd": [
        "Política Privacidade",
        "Politica Privacidade",
        "Política Privacidade e LGPD",
        "Privacidade",
        "Privacidade LGPD",
    ],
    "manual_colaborador": [
        "Manual do Colaborador",
        "Manual Colaborador",
        "RH",
        "Recursos Humanos",
    ],
    "politica_controle_acesso": [
        "Política Controle Acesso",
        "Politica Controle Acesso",
        "Política Acesso",
        "Controle de Acesso",
        "Controle Acesso",
        "PCA",
        "Acesso",
    ],
    "plano_resposta_incidentes": [
        "Plano Resposta Incidentes",
        "Plano de Resposta a Incidentes",
        "Plano Resposta Incidente",
        "PRI",
        "Incidentes",
        "Resposta Incidentes",
    ],
    "politica_backup_retenção": [
        "Política Backup",
        "Politica Backup",
        "Política Backup e Retenção",
        "Backup Retenção",
        "Backup",
        "Retenção",
        "Retencao",
        "PBR",
    ],
    "politica_uso_aceitavel": [
        "Política Uso Aceitável",
        "Politica Uso Aceitavel",
        "Política Uso Aceitavel",
        "Uso Aceitável",
        "Uso Aceitavel",
        "PUA",
        "AUP",
    ],
}


def _resolve_aliases(stem: str) -> list[str]:
    aliases = []
    for key, value in DOCUMENT_ALIASES.items():
        if key in stem.lower():
            aliases.extend(value)
    seen = set()
    uniq = []
    for alias in aliases:
        if alias.lower() not in seen:
            uniq.append(alias)
            seen.add(alias.lower())
    return uniq


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

    def _enrich_metadata(self, file_path: Path, base_meta: dict | None) -> dict:
        meta = dict(base_meta or {})
        aliases = _resolve_aliases(file_path.stem)
        if aliases:
            meta["document_aliases"] = aliases
        return meta

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
        base_meta = {"page_count": len(reader.pages)}
        return Document.from_text(
            title=file_path.stem.replace("_", " ").title(),
            content=content,
            source=file_path.name,
            category=category,
            file_path=file_path,
            metadata=self._enrich_metadata(file_path, base_meta),
        )

    def _load_markdown(self, file_path: Path, *, category: str) -> Document:
        content = file_path.read_text(encoding="utf-8")
        return Document.from_text(
            title=file_path.stem.replace("_", " ").title(),
            content=content,
            source=file_path.name,
            category=category,
            file_path=file_path,
            metadata=self._enrich_metadata(file_path, None),
        )
