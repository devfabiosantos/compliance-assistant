from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import click

from src.config.settings import get_settings
from src.providers.cohere_embeddings import CohereEmbeddingProvider
from src.retrieval.retriever import Retriever, RetrievedChunk
from src.retrieval.vector_store import VectorStore
from src.utils.logging import configure_logging


DEFAULT_QUESTIONS_FILE = ROOT / "evaluation" / "questions.json"
DEFAULT_REPORT_FILE = ROOT / "evaluation" / "reports" / "retrieval_report.json"


@dataclass
class CaseResult:
    id: str
    category: str
    question: str
    expected_document: str | None
    expected_section: str | None
    expected_keywords: list[str]
    hit_document: bool
    hit_section: bool
    hit_keywords: bool
    passed: bool
    top_k_chunks: list[dict[str, Any]]


@dataclass
class Summary:
    total: int
    passed: int
    failed: int
    document_accuracy: float
    section_accuracy: float
    keyword_recall: float


def _load_cases(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise click.FileError(str(path), hint="Arquivo de casos nao encontrado.")
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        raise click.UsageError(f"Nenhum caso definido em {path}. Campo 'cases' vazio.")
    return cases


def _normalize(text: str | None) -> str:
    if not text:
        return ""
    return (
        text.strip()
        .lower()
        .replace("ç", "c")
        .replace("ã", "a")
        .replace("õ", "o")
        .replace("á", "a")
        .replace("à", "a")
        .replace("â", "a")
        .replace("ê", "e")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("ú", "u")
        .replace("_", " ")
        .replace("-", " ")
    )


def _case_doc_matches(expected: str | None, chunks: Iterable[RetrievedChunk]) -> bool:
    if not expected:
        return True
    expected_norm = _normalize(expected)
    for chunk in chunks:
        citation = chunk.to_citation()
        haystacks = [
            citation.doc_id,
            citation.doc_title,
            citation.source,
        ]
        if any(expected_norm in _normalize(h) for h in haystacks):
            return True
    return False


def _case_section_matches(expected: str | None, chunks: Iterable[RetrievedChunk]) -> bool:
    if not expected:
        return True
    expected_norm = _normalize(expected)
    for chunk in chunks:
        citation = chunk.to_citation()
        haystacks = [
            citation.section or "",
            chunk.chunk.content,
        ]
        if expected_norm in _normalize("\n".join(haystacks)):
            return True
    return False


def _case_keywords_matches(keywords: list[str], chunks: Iterable[RetrievedChunk]) -> bool:
    if not keywords:
        return True
    combined = "\n".join(chunk.chunk.content for chunk in chunks)
    combined_norm = _normalize(combined)
    return any(_normalize(k) in combined_norm for k in keywords)


def _evaluate_case(
    case: dict[str, Any],
    retriever: Retriever,
    embedder: CohereEmbeddingProvider,
    k: int,
) -> CaseResult:
    case_id = str(case.get("id", ""))
    category = str(case.get("category", ""))
    question = str(case.get("question", ""))
    expected_document = case.get("expected_document")
    expected_section = case.get("expected_section")
    keywords = [str(x) for x in (case.get("expected_keywords") or [])]

    qvec = embedder.embed_query(question)
    results = retriever.retrieve(qvec)[:k]

    hit_doc = _case_doc_matches(expected_document, results)
    hit_section = _case_section_matches(expected_section, results)
    hit_keywords = _case_keywords_matches(keywords, results)

    passed = hit_doc and hit_section and hit_keywords

    top_k = []
    for rank, r in enumerate(results, start=1):
        citation = r.to_citation()
        top_k.append(
            {
                "rank": rank,
                "score": round(r.score, 4) if r.score is not None else None,
                "doc_id": citation.doc_id,
                "doc_title": citation.doc_title,
                "page": citation.page,
                "section": citation.section,
                "snippet": (citation.snippet or r.chunk.content)[:280],
            }
        )

    return CaseResult(
        id=case_id,
        category=category,
        question=question,
        expected_document=expected_document,
        expected_section=expected_section,
        expected_keywords=keywords,
        hit_document=hit_doc,
        hit_section=hit_section,
        hit_keywords=hit_keywords,
        passed=passed,
        top_k_chunks=top_k,
    )


def _build_summary(results: list[CaseResult]) -> Summary:
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    doc_acc = (sum(1 for r in results if r.hit_document) / total) if total else 0.0
    sec_acc = (sum(1 for r in results if r.hit_section) / total) if total else 0.0
    kw_recall = (sum(1 for r in results if r.hit_keywords) / total) if total else 0.0
    return Summary(
        total=total,
        passed=passed,
        failed=failed,
        document_accuracy=round(doc_acc, 4),
        section_accuracy=round(sec_acc, 4),
        keyword_recall=round(kw_recall, 4),
    )


def _print_cli(results: list[CaseResult], summary: Summary, k: int) -> None:
    click.echo("=" * 90)
    click.echo("RELATORIO DE AVALIACAO NIVEL 1 — RETRIEVAL")
    click.echo(f"top_k={k}    casos={summary.total}    pass={summary.passed}    fail={summary.failed}")
    click.echo("-" * 90)
    click.echo(
        f"Acuracia (documento correto) : {summary.document_accuracy*100:5.1f}%"
    )
    click.echo(
        f"Acuracia (secao correta)     : {summary.section_accuracy*100:5.1f}%"
    )
    click.echo(
        f"Recall  (palavras-chave)     : {summary.keyword_recall*100:5.1f}%"
    )
    click.echo("=" * 90)

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        parts = []
        parts.append("DOC" if r.hit_document else "---")
        parts.append("SEC" if r.hit_section else "---")
        parts.append("KW " if r.hit_keywords else "---")
        tags = " ".join(parts)
        click.echo(f"[{status}] {tags}  {r.id:<12} {r.question}")
        if not r.passed and r.top_k_chunks:
            top = r.top_k_chunks[0]
            click.echo(
                f"          -> top1: {top.get('doc_title') or top.get('doc_id')} "
                f"(page={top.get('page')}, section={top.get('section')}, score={top.get('score')})"
            )
    click.echo("=" * 90)


@click.command("evaluate-retrieval")
@click.option(
    "--questions",
    "questions_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_QUESTIONS_FILE,
    show_default=True,
)
@click.option(
    "--report",
    "report_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_REPORT_FILE,
    show_default=True,
)
@click.option(
    "--k",
    type=click.IntRange(1, 50),
    default=None,
    help="Sobrescreve RETRIEVER_TOP_K para avaliacao. Padrao: usar valor do .env",
)
@click.option(
    "--fail-on-zero",
    is_flag=True,
    default=False,
    help="Retorna exit code > 0 se houver algum caso reprovado.",
)
@click.option(
    "--env-file",
    type=click.Path(dir_okay=False),
    default=None,
)
def main(
    questions_path: Path,
    report_path: Path,
    k: int | None,
    fail_on_zero: bool,
    env_file: str | None,
) -> None:
    """Avaliacao Nivel 1 de retrieval: documento + secao + palavras-chave."""
    settings = get_settings(env_file)
    configure_logging(settings)

    if not settings.cohere_api_key:
        raise click.UsageError(
            "COHERE_API_KEY nao configurada. Copie .env.example para .env e preencha a chave."
        )
    if not (settings.paths.vector_store_dir / "index.faiss").exists():
        raise click.UsageError(
            "Indice vetorial nao encontrado. Execute antes: python scripts/index_documents.py"
        )

    cases = _load_cases(questions_path)

    embedder = CohereEmbeddingProvider(
        api_key=settings.cohere_api_key,
        model=settings.cohere_embed_model,
    )
    store = VectorStore(
        directory=settings.paths.vector_store_dir,
        embedding_dimension=0,
        embedding_model=embedder.name,
    )
    store.load()
    top_k = k if k is not None else settings.retriever_top_k
    retriever = Retriever(
        vector_store=store,
        top_k=top_k,
        score_threshold=settings.retriever_score_threshold,
    )

    results: list[CaseResult] = []
    with click.progressbar(cases, label="Avaliando retrieval", show_pos=True) as bar:
        for case in bar:
            results.append(_evaluate_case(case, retriever, embedder, top_k))

    summary = _build_summary(results)
    _print_cli(results, summary, top_k)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "level": 1,
        "top_k": top_k,
        "embedding_model": embedder.name,
        "questions_file": str(questions_path.resolve()),
        "vector_store_dir": str(settings.paths.vector_store_dir.resolve()),
        "summary": asdict(summary),
        "cases": [asdict(r) for r in results],
    }
    report_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    click.echo(f"Relatorio JSON salvo em: {report_path}")

    if fail_on_zero and summary.failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
