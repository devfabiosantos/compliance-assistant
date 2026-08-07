from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import click

from src.config.settings import get_settings
from src.providers.cohere_embeddings import CohereEmbeddingProvider
from src.services.index_service import IndexService
from src.utils.logging import configure_logging


@click.command("index-documents")
@click.option("--env-file", type=click.Path(dir_okay=False), default=None, help="Caminho opcional para .env")
def main(env_file: str | None) -> None:
    settings = get_settings(env_file)
    configure_logging(settings)

    if not settings.cohere_api_key:
        raise click.UsageError(
            "COHERE_API_KEY nao configurada. Copie .env.example para .env e preencha a chave."
        )

    embedder = CohereEmbeddingProvider(
        api_key=settings.cohere_api_key,
        model=settings.cohere_embed_model,
    )
    service = IndexService(settings=settings, embedding_provider=embedder)
    summary = service.build_and_save()

    click.echo("Indexacao concluida com sucesso.")
    click.echo(f"  Documentos     : {summary.document_count}")
    click.echo(f"  Chunks gerados : {summary.chunk_count}")
    click.echo(f"  Embedding model: {summary.embedding_model}")
    click.echo(f"  Diretorio      : {summary.vector_store_dir}")
    click.echo(f"  Gerado em      : {summary.generated_at}")


if __name__ == "__main__":
    main()
