from __future__ import annotations

from typing import List, Optional, Sequence

from src.domain.source import SourceCitation
from src.providers.base import ChatProvider


DEPRECATED_CHAT_MODEL_ALIASES = {
    "command",
    "command-light",
    "command-r",
    "command-r-plus",
}

FALLBACK_CHAT_MODEL = "command-r7b-12-2024"


class CohereChatProvider(ChatProvider):
    def __init__(self, api_key: str, model: str = "command-r7b-12-2024") -> None:
        if not api_key:
            raise ValueError("Cohere API key is required")
        try:
            import cohere
        except ImportError as exc:
            raise ImportError("cohere package is not installed") from exc
        self._client = cohere.ClientV2(api_key=api_key)
        self._model_primary, self._model_fallback = _resolve_models(model)
        self.name = f"cohere/chat/{self._model_primary}"

    @staticmethod
    def _build_prompt(question: str, context_chunks: Sequence[str], citations: Sequence[SourceCitation]) -> str:
        if len(context_chunks) != len(citations):
            raise ValueError("context_chunks e citations devem ter o mesmo tamanho.")
        blocks: list[str] = []
        for i, (chunk, cite) in enumerate(zip(context_chunks, citations), start=1):
            lines = [f"[DOCUMENTO {i}]"]
            lines.append(f"TITULO: {cite.doc_title}")
            if cite.source:
                lines.append(f"ARQUIVO: {cite.source}")
            if cite.page is not None:
                lines.append(f"PAGINA: {cite.page}")
            if cite.section:
                lines.append(f"SECAO: {cite.section}")
            if cite.score is not None:
                lines.append(f"SCORE_RELEVANCIA: {cite.score:.3f}")
            lines.append("CONTEUDO:")
            lines.append(chunk)
            blocks.append("\n".join(lines))
        ctx = "\n\n".join(blocks) if blocks else "(nenhum documento recuperado)"
        return (
            "Voce e o Compliance Assistant da NovaData Solutions, um assistente especializado "
            "em LGPD, seguranca da informacao e politicas internas. "
            "Responda sempre em portugues do Brasil, de forma objetiva, clara e fundamentada "
            "EXCLUSIVAMENTE nos conteudos dos blocos [DOCUMENTO ...] apresentados abaixo.\n\n"
            "REGRAS OBRIGATORIAS:\n"
            "1. NUNCA invente nomes de politicas, procedimentos, secoes, documentos, paginas, "
            "numeros de documento ou responsaveis que NAO aparecam explicitamente nos "
            "cabeçalhos TITULO / ARQUIVO / PAGINA / SECAO dos blocos.\n"
            "2. Sempre que fizer uma afirmacao, cite a fonte exata usada utilizando "
            "'Titulo — Pagina X' ou 'Titulo — Secao Y' conforme os blocos.\n"
            "3. Se a resposta nao puder ser extraida dos blocos, ou se os blocos estiverem "
            "ausentes, responda exatamente:\n"
            "   'Nao encontrei informacao suficiente nos documentos indexados para responder a esta pergunta com seguranca.'\n"
            "4. Nao use conhecimento externo aos documentos. Nao adicione 'acho que', 'geralmente', "
            "'normalmente' a menos que esteja escrito no bloco.\n\n"
            f"PERGUNTA DO USUARIO: {question}\n\n"
            f"BLOCOS RECUPERADOS PARA ESTA RESPOSTA:\n{ctx}"
        )

    def answer_with_context(
        self,
        question: str,
        context_chunks: Sequence[str],
        citations: Sequence[SourceCitation],
    ) -> str:
        prompt = self._build_prompt(question, context_chunks, citations)
        messages = [{"role": "user", "content": prompt}]

        last_error: Optional[Exception] = None
        for model in (self._model_primary, self._model_fallback):
            try:
                response = self._client.chat(model=model, messages=messages)
            except Exception as exc:
                last_error = exc
                _warn_model_failure(model, exc)
                continue
            self.name = f"cohere/chat/{model}"
            return _extract_chat_text(response)

        assert last_error is not None
        return f"[erro-no-provider] {type(last_error).__name__}: {last_error}"


def _resolve_models(primary: str) -> tuple[str, str]:
    primary = (primary or "").strip() or FALLBACK_CHAT_MODEL
    if primary.lower() in DEPRECATED_CHAT_MODEL_ALIASES:
        _warn_deprecated_model(primary)
        return (FALLBACK_CHAT_MODEL, "command-r-08-2024")
    if primary == FALLBACK_CHAT_MODEL:
        return (primary, "command-r-08-2024")
    return (primary, FALLBACK_CHAT_MODEL)


def _extract_chat_text(response) -> str:
    message = getattr(response, "message", None)
    content = getattr(message, "content", None) or []
    if content and hasattr(content[0], "text"):
        return content[0].text
    if content:
        return str(content[0])
    return "(sem resposta do modelo)"


def _warn_model_failure(model: str, exc: Exception) -> None:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(
        "falha no modelo de chat %s. tentando proximo fallback.",
        model,
        exc_info=exc,
    )


def _warn_deprecated_model(model: str) -> None:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(
        "modelo '%s' esta na lista de aliases depreciados do Cohere. "
        "Usando '%s' como padrao. Atualize COHERE_CHAT_MODEL no .env.",
        model,
        FALLBACK_CHAT_MODEL,
    )
