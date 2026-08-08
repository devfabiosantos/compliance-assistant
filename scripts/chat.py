from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import click

from src.config.settings import get_settings
from src.providers.cohere_chat import CohereChatProvider
from src.providers.cohere_embeddings import CohereEmbeddingProvider
from src.services.qa_service import QAService
from src.utils.logging import configure_logging


def _print_answer(answer) -> None:
    click.echo("=" * 72)
    click.echo("PERGUNTA")
    click.echo("-" * 72)
    click.echo("...")
    click.echo("")
    click.echo("RESPOSTA")
    click.echo("-" * 72)
    click.echo(answer.text)
    click.echo("")
    click.echo("FONTES CONSULTADAS")
    click.echo("-" * 72)
    click.echo(answer.sources_text())
    click.echo("")
    click.echo("METRICAS")
    click.echo("-" * 72)
    click.echo(f"  Modelo              : {answer.model}")
    click.echo(f"  Tempo de busca (ms) : {answer.retrieval_time_ms}")
    click.echo(f"  Tempo de geracao(ms): {answer.generation_time_ms}")
    click.echo(f"  Tempo total    (ms) : {answer.total_time_ms}")
    click.echo("")
    click.echo("AVISO")
    click.echo("-" * 72)
    click.echo(answer.disclaimer)
    click.echo("=" * 72)


@click.command("chat")
@click.argument("question", required=False)
@click.option("--env-file", type=click.Path(dir_okay=False), default=None)
def main(question: str | None, env_file: str | None) -> None:
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

    chat_provider = CohereChatProvider(
        api_key=settings.cohere_api_key,
        model=settings.cohere_chat_model,
    )
    embedder = CohereEmbeddingProvider(
        api_key=settings.cohere_api_key,
        model=settings.cohere_embed_model,
    )
    qa = QAService(
        settings=settings,
        chat_provider=chat_provider,
        embedding_provider=embedder,
    )

    if question:
        answer = qa.answer(question)
        # Patch para mostrar a pergunta no header
        answer._question_display = question
        _print_answer_patched(answer, question)
        return

    click.echo("Compliance Assistant - modo interativo (digite /sair para encerrar)")
    while True:
        try:
            user_input = click.prompt("Voce", prompt_suffix=" > ")
        except (EOFError, click.Abort):
            click.echo("")
            return
        if user_input.strip().lower() in {"/sair", "/exit", "sair", "exit"}:
            return
        if not user_input.strip():
            continue
        answer = qa.answer(user_input)
        _print_answer_patched(answer, user_input)


def _print_answer_patched(answer, question: str) -> None:
    lat = getattr(answer, "latency", None)
    embed_ms = getattr(lat, "embedding_ms", None) if lat is not None else None
    ret_ms = getattr(lat, "retrieval_ms", None) if lat is not None else None
    busca_total_ms = None
    if ret_ms is not None or embed_ms is not None:
        busca_total_ms = (ret_ms or 0.0) + (embed_ms or 0.0)

    click.echo("=" * 72)
    click.echo("PERGUNTA")
    click.echo("-" * 72)
    click.echo(question)
    click.echo("")
    click.echo("RESPOSTA")
    click.echo("-" * 72)
    click.echo(answer.text)
    if getattr(answer, "insufficient_information", False):
        click.echo("")
        click.echo("[ATENCAO] Nao houve recuperacao suficiente nos documentos; esta e a resposta padrao.")
    click.echo("")
    click.echo("FONTES CONSULTADAS")
    click.echo("-" * 72)
    click.echo(answer.sources_text())
    click.echo("")
    click.echo("METRICAS")
    click.echo("-" * 72)
    click.echo(f"  Modelo               : {answer.model}")
    if embed_ms is not None:
        click.echo(f"  Tempo embed    (ms)  : {embed_ms:.1f}")
    if busca_total_ms is not None:
        click.echo(f"  Tempo de busca  (ms) : {busca_total_ms:.1f}")
    else:
        click.echo(f"  Tempo de busca  (ms) : {answer.retrieval_time_ms}")
    click.echo(f"  Tempo de geracao(ms) : {answer.generation_time_ms}")
    click.echo(f"  Tempo total    (ms)  : {answer.total_time_ms}")
    click.echo("")
    click.echo("AVISO")
    click.echo("-" * 72)
    click.echo(answer.disclaimer)
    click.echo("=" * 72)


if __name__ == "__main__":
    main()
