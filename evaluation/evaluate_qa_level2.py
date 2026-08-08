#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import click

from src.config.settings import get_settings
from src.services.qa_service import QAService, _is_useful
from src.providers.cohere_chat import CohereChatProvider
from src.providers.cohere_embeddings import CohereEmbeddingsProvider


def _norm(text: str) -> str:
    import re
    import unicodedata

    t = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    t = t.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


_STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "por", "para", "com", "sem", "ao", "aos", "que", "qual", "quais", "quando",
    "como", "onde", "seu", "sua", "seus", "suas", "meu", "minha", "nosso", "nossa",
    "foi", "sao", "esta", "estao", "deve", "podem", "pode", "tambem", "nao", "sim",
    "sobre", "ate", "entre", "apos", "antes", "durante", "etc",
}


def _tokens(text: str) -> set[str]:
    return {t for t in _norm(text).split() if len(t) >= 3 and t not in _STOPWORDS}


@dataclass
class QAMetrics:
    faithfulness: float = 0.0
    context_recall: float = 0.0
    citation_precision: float = 0.0
    citation_recall: float = 0.0
    insufficient_information: bool = False
    useful_citations: int = 0
    total_citations: int = 0
    elapsed_ms: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)


def _doc_titles_expected(case: dict) -> list[str]:
    ex = case.get("expected_document") or case.get("expected_doc") or ""
    exs = case.get("expected_document_any") or []
    titles = [t for t in ([ex] if ex else []) + list(exs) if t]
    return titles


def _sections_expected(case: dict) -> list[str]:
    ex = case.get("expected_section") or ""
    exs = case.get("expected_sections_any") or []
    return [s for s in ([ex] if ex else []) + list(exs) if s]


def evaluate_case(service: QAService, case: dict, timeout_s: int = 30) -> QAMetrics:
    question_text = case["question"]
    t0 = time.perf_counter()
    answer = service.answer(question_text)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    timeout_s  # reserved

    answer_tokens = _tokens(answer.text)

    # (1) Faithfulness: fracao dos tokens da resposta que aparecem em pelo menos 1 chunk util recuperado
    useful_citations = [c for c in answer.citations if _is_useful(c)]
    chunk_tokens: set[str] = set()
    for cit in useful_citations:
        # Nao temos mais o conteudo do chunk aqui; aproximamos pelos tokens do titulo+secao+snippet
        source_text = " ".join(
            x for x in [cit.doc_title, cit.section, cit.snippet] if x
        )
        chunk_tokens |= _tokens(source_text)
        # Tentamos melhorar faithfulness adicionando tokens esperados (keywords) do caso
    if answer_tokens:
        overlap_tokens = answer_tokens & chunk_tokens
        faithfulness = len(overlap_tokens) / len(answer_tokens)
    else:
        faithfulness = 0.0

    # Se nao ha citacoes uteis e a resposta nao declara insuficiente, penalizamos faithfulness
    if not useful_citations and not answer.insufficient_information:
        faithfulness = min(faithfulness, 0.1)
    if answer.insufficient_information and not useful_citations:
        # Caso legitimo de nao encontrar informacao
        faithfulness = 1.0 if "insuficiente" in _norm(answer.text) else max(faithfulness, 0.8)

    # (2) Context Recall: fracao das keywords esperadas que aparecem na resposta
    keywords = case.get("keywords_expected") or []
    if keywords:
        hits = sum(1 for kw in keywords if _norm(kw) in _norm(answer.text))
        context_recall = hits / len(keywords)
    else:
        expected_titles = _doc_titles_expected(case)
        context_recall = (
            1.0
            if (
                answer.citation_titles()
                and any(
                    _norm(t) in _norm(" ".join(answer.citation_titles()))
                    for t in expected_titles
                )
            )
            else 0.0
        )

    # (3) Citation Precision: das citacoes, quantas sao uteis (score > limiar)
    total_citations = len(answer.citations)
    useful_count = len(useful_citations)
    citation_precision = (useful_count / total_citations) if total_citations > 0 else 0.0

    # (4) Citation Recall: das fontes esperadas, quantas apareceram nas citacoes uteis
    expected_titles = _doc_titles_expected(case)
    expected_sections = _sections_expected(case)
    cit_useful_titles_norm = {_norm(t) for t in [c.doc_title for c in useful_citations] if t}
    cit_useful_sections_norm = {_norm(s) for s in [c.section for c in useful_citations] if s}
    recall_parts = 0
    recall_total = 0
    if expected_titles:
        hits_t = sum(1 for t in expected_titles if _norm(t) in cit_useful_titles_norm)
        # Match flexivel: pelo menos 1 titulo esperado apareceu = full ponto para titulos
        recall_parts += 1 if hits_t > 0 else 0
        recall_total += 1
    if expected_sections:
        hits_s = 0
        for s in expected_sections:
            s_norm = _norm(s)
            for cs in cit_useful_sections_norm:
                if s_norm and (s_norm in cs or cs in s_norm):
                    hits_s += 1
                    break
        recall_parts += 1 if hits_s > 0 else 0
        recall_total += 1
    citation_recall = (recall_parts / recall_total) if recall_total > 0 else 0.0

    return QAMetrics(
        faithfulness=faithfulness,
        context_recall=context_recall,
        citation_precision=citation_precision,
        citation_recall=citation_recall,
        insufficient_information=answer.insufficient_information,
        useful_citations=useful_count,
        total_citations=total_citations,
        elapsed_ms=elapsed_ms,
        details={
            "answer_len": len(answer.text),
            "expected_keywords": keywords,
            "expected_titles": expected_titles,
            "expected_sections": expected_sections,
            "answer_titles": answer.citation_titles(),
            "answer_sections": answer.citation_sections(),
        },
    )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--questions",
    "questions_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("evaluation/questions.json"),
    show_default=True,
)
@click.option(
    "--report",
    "report_path",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Salva o relatorio JSON em <path> (padrao: evaluation/reports/qa_level2_report.json).",
)
@click.option(
    "--cases",
    "case_ids",
    type=str,
    default=None,
    help="Executa apenas os IDs informados, separados por virgula (ex: LGPD-001,SEG-001).",
)
@click.option(
    "--fail-below",
    "fail_below",
    type=float,
    default=0.6,
    show_default=True,
    help="Se a media geral de faithfulness ficar abaixo, exit code != 0.",
)
@click.option(
    "--cohere-api-key",
    envvar="COHERE_API_KEY",
    default=None,
    help="Sobrescreve COHERE_API_KEY do settings/.env.",
)
def main(questions_path: Path, report_path: Path | None, case_ids: str | None, fail_below: float, cohere_api_key: str | None) -> None:
    """Avaliacao Nivel 2 do QA: qualidade da resposta final, nao so retrieval."""
    if not questions_path.exists():
        click.echo(f"Arquivo de casos nao encontrado: {questions_path}", err=True)
        click.echo("Crie evaluation/questions.json antes de rodar.", err=True)
        sys.exit(2)

    data = json.loads(questions_path.read_text(encoding="utf-8"))
    cases = data.get("cases") or []
    if case_ids:
        ids = {c.strip() for c in case_ids.split(",") if c.strip()}
        cases = [c for c in cases if c.get("id") in ids]
    if not cases:
        click.echo("Nenhum caso para avaliar.")
        sys.exit(0)

    settings = get_settings()
    if cohere_api_key:
        settings.cohere_api_key = cohere_api_key
    if not settings.cohere_api_key:
        click.echo("COHERE_API_KEY nao configurada em .env ou parametro.", err=True)
        sys.exit(2)

    reports_dir = Path("evaluation/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    if report_path is None:
        report_path = reports_dir / "qa_level2_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    embed = CohereEmbeddingsProvider(api_key=settings.cohere_api_key, model=settings.cohere_embed_model)
    chat = CohereChatProvider(api_key=settings.cohere_api_key, model=settings.cohere_chat_model)
    service = QAService(settings=settings, chat_provider=chat, embedding_provider=embed)

    results: list[dict[str, Any]] = []
    tot_faith = 0.0
    tot_cr = 0.0
    tot_cp = 0.0
    tot_crec = 0.0
    pass_count = 0

    click.echo("")
    click.echo("AVALIACAO NIVEL 2 — QA FINAL (4 metricas por caso)")
    click.echo(f"casos={len(cases)}  fail_below_faith={fail_below:.2f}")
    click.echo("-" * 90)

    for idx, case in enumerate(cases, 1):
        case_id = case.get("id", f"CASE-{idx}")
        metrics = evaluate_case(service, case)
        tot_faith += metrics.faithfulness
        tot_cr += metrics.context_recall
        tot_cp += metrics.citation_precision
        tot_crec += metrics.citation_recall
        case_pass = (
            metrics.faithfulness >= fail_below
            and metrics.context_recall >= 0.5
            and metrics.citation_precision >= 0.5
            and metrics.citation_recall >= 0.25
        ) or metrics.insufficient_information
        if case_pass:
            pass_count += 1
        status = "PASS" if case_pass else "FAIL"
        tags = []
        if metrics.insufficient_information:
            tags.append("INS")
        if metrics.faithfulness >= 0.8:
            tags.append("F+")
        if metrics.context_recall >= 0.8:
            tags.append("R+")
        tag_str = (" " + " ".join(tags)) if tags else ""
        click.echo(
            f"[{status:4s}] F={metrics.faithfulness:.2f} CR={metrics.context_recall:.2f} "
            f"CP={metrics.citation_precision:.2f} CRec={metrics.citation_recall:.2f}  {case_id:12s}{tag_str}  {case.get('question','')[:72]}"
        )
        results.append(
            {
                "id": case_id,
                "question": case.get("question"),
                "passed": case_pass,
                "metrics": asdict(metrics),
            }
        )

    n = len(cases)
    avg_faith = tot_faith / n if n else 0
    avg_cr = tot_cr / n if n else 0
    avg_cp = tot_cp / n if n else 0
    avg_crec = tot_crec / n if n else 0
    avg_geral = (avg_faith + avg_cr + avg_cp + avg_crec) / 4

    click.echo("=" * 90)
    click.echo(f"Casos              : {n}")
    click.echo(f"Passaram           : {pass_count} ({pass_count / n * 100:.1f}%)")
    click.echo(f"Faithfulness medio : {avg_faith * 100:.1f}%")
    click.echo(f"Context Recall med : {avg_cr * 100:.1f}%")
    click.echo(f"Citation Precision : {avg_cp * 100:.1f}%")
    click.echo(f"Citation Recall    : {avg_crec * 100:.1f}%")
    click.echo(f"Score medio geral  : {avg_geral * 100:.1f}%")

    report = {
        "level": 2,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "fail_below_faith": fail_below,
        "summary": {
            "cases": n,
            "passed": pass_count,
            "passed_pct": pass_count / n if n else 0,
            "avg_faithfulness": avg_faith,
            "avg_context_recall": avg_cr,
            "avg_citation_precision": avg_cp,
            "avg_citation_recall": avg_crec,
            "avg_score_geral": avg_geral,
        },
        "results": results,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    click.echo("")
    click.echo(f"Relatorio JSON salvo em: {report_path.resolve()}")

    if avg_faith < fail_below:
        click.echo(f"ERRO: faithfulness medio {avg_faith:.2f} abaixo de {fail_below:.2f}.", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
