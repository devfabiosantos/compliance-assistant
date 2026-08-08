from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config.settings import get_settings
from src.domain.answer import Answer
from src.providers.cohere_chat import CohereChatProvider
from src.providers.cohere_embeddings import CohereEmbeddingProvider
from src.services.qa_service import QAService
from src.utils.logging import configure_logging


APP_TITLE = "Compliance Assistant"
APP_SUBTITLE = "Enterprise AI Assistant for LGPD Compliance and Corporate Knowledge Retrieval"
COMPANY = "NovaData Solutions"
STACK = "Python · LangChain · Cohere · FAISS · Streamlit · Markdown"
BUILD_TAG = "v0.4.0-rc1 · Sprint 4"


@dataclass
class DocCard:
    file: str
    title: str
    category: str
    version: str
    owners: str
    updated: str


def _doc_cards() -> List[DocCard]:
    return [
        DocCard("lgpd_leil_13709_2018.md", "LGPD — Lei 13.709/2018 (stub)", "Oficial / LGPD", "1.0", "ANPD", "2026-08-07"),
        DocCard("guia_anpd_metodos_aplicacao.md", "Guia ANPD — Métodos de Aplicação (stub)", "Oficial / ANPD", "1.0", "ANPD", "2026-08-07"),
        DocCard("faq_anpd_principal.md", "FAQ ANPD — Principais Perguntas (stub)", "Oficial / ANPD", "1.0", "ANPD", "2026-08-07"),
        DocCard("codigo_etica_conduta.md", "Código de Ética e Conduta", "Empresa / Ética", "1.0", "CCO / Ética", "2026-07-30"),
        DocCard("organograma.md", "Organograma e Papéis de Governança", "Empresa / Governança", "1.0", "Diretoria", "2026-07-30"),
        DocCard("politica_seguranca_informacao.md", "Política de Segurança da Informação", "Empresa / TI", "1.0", "CISO", "2026-08-07"),
        DocCard("politica_privacidade_lgpd.md", "Política de Privacidade e LGPD", "Empresa / Compliance", "1.0", "DPO", "2026-08-07"),
        DocCard("manual_colaborador.md", "Manual do Colaborador", "Empresa / RH", "1.0", "CHRO", "2026-08-07"),
        DocCard("politica_controle_acesso.md", "Política de Controle de Acesso", "Empresa / TI", "1.0", "CISO", "2026-08-07"),
        DocCard("plano_resposta_incidentes.md", "Plano de Resposta a Incidentes (PRI)", "Empresa / Segurança", "1.0", "CISO / SOC", "2026-08-07"),
        DocCard("politica_backup_retenção.md", "Política de Backup e Retenção", "Empresa / Infraestrutura", "1.0", "CTO", "2026-08-07"),
        DocCard("politica_uso_aceitavel.md", "Política de Uso Aceitável", "Empresa / Governança", "1.0", "CISO / RH", "2026-08-07"),
    ]


def _ensure_qa_service() -> QAService | None:
    if "qa_service" in st.session_state and st.session_state.qa_service is not None:
        return st.session_state.qa_service
    try:
        settings = get_settings()
        configure_logging(settings)
        if not settings.cohere_api_key:
            st.error("COHERE_API_KEY não configurada. Copie `.env.example` → `.env` e preencha a chave.")
            return None
        if not (settings.paths.vector_store_dir / "index.faiss").exists():
            st.warning("Índice vetorial não encontrado. Rode antes: `python scripts/index_documents.py`.")
            return None
        embed = CohereEmbeddingProvider(api_key=settings.cohere_api_key, model=settings.cohere_embed_model)
        chat = CohereChatProvider(api_key=settings.cohere_api_key, model=settings.cohere_chat_model)
        service = QAService(settings=settings, chat_provider=chat, embedding_provider=embed)
        st.session_state.qa_service = service
        return service
    except Exception as exc:  # pragma: no cover - UI
        st.exception(exc)
        return None


def _load_json_report(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def page_home() -> None:
    st.title(f"{COMPANY} · {APP_TITLE}")
    st.caption(APP_SUBTITLE)
    st.caption(f"Versão: **{BUILD_TAG}**  ·  Stack: **{STACK}**")
    st.markdown("---")

    left, right = st.columns([3, 2])
    with left:
        st.header("Sobre o produto")
        st.write(
            "O Compliance Assistant é um assistente baseado em RAG (Retrieval-Augmented Generation) "
            "desenvolvido pela NovaData Solutions para capacitar colaboradores, gestores e equipes "
            "de Compliance com respostas objetivas, auditáveis e 100% baseadas na documentação "
            "interna indexada — políticas da empresa, manuais, Código de Ética, Organograma e "
            "documentos oficiais (LGPD, Guia e FAQ da ANPD)."
        )
        st.subheader("Principais diferenciais")
        st.markdown(
            """
- **Anti-hallucination:** respostas obrigatoriamente citam documentos, seções e scores de relevância recuperados pelo FAISS.
- **Resposta padrão de insuficiência:** quando a base não possui informação suficiente, o assistente sinaliza e orienta procurar DPO, CISO ou RH.
- **Avaliação objetiva em 2 níveis:**
  - **Nível 1 — Retrieval:** % de documento, seção e palavras-chave corretas (48 casos, 100% pass).
  - **Nível 2 — QA final:** faithfulness, context recall, citation precision/recall.
- **Arquitetura em camadas, provider-agnostic:** providers Cohere ficam em `src/providers/`, com substituição fácil para Gemini, OpenAI ou Bedrock.
            """
        )
        st.info("💡 **Experimente:** no menu lateral, escolha **💬 Compliance Assistant** e pergunte sobre LGPD, incidentes de segurança, retenção de documentos ou ética no trabalho.")

    with right:
        st.subheader("Pronto para produção")
        for k, v in {
            "Documentos indexados": "12 (3 oficiais + 9 empresa)",
            "Casos Nível 1": "48 / 48 PASS (100%)",
            "Casos Nível 2": "Runner automático, 4 métricas por caso",
            "Provedor LLM": "Cohere `command-r7b-12-2024`",
            "Embeddings": "Cohere `embed-multilingual-v3.0`",
            "Banco vetorial": "FAISS local (data/vector_store)",
            "Licença": "MIT",
            "Entrega Challenge ONE": "19/08/2026 (com buffer 10 dias)",
        }.items():
            st.write(f"**{k}:** {v}")
        st.subheader("Links úteis")
        st.markdown(
            """
- [Repositório GitHub](https://github.com/devfabiosantos/compliance-assistant)
- [ANPD — LGPD](https://www.gov.br/anpd/pt-br)
- Documentação no README e `docs/adr/`
            """
        )


def _render_citations(answer: Answer) -> None:
    if not answer.citations:
        st.caption("Nenhuma fonte citada.")
        return
    with st.expander(f"📄 Fontes citadas ({len(answer.citations)})", expanded=True):
        data = [
            {
                "Documento": c.doc_title,
                "Seção": c.section or "-",
                "Página": str(c.page) if c.page is not None else "-",
                "Score": f"{c.score:.3f}" if c.score is not None else "-",
                "Snippet (preview)": (c.snippet or "")[:240] + ("…" if len(c.snippet or "") > 240 else ""),
            }
            for c in answer.citations
        ]
        st.dataframe(data, use_container_width=True, hide_index=True)


def _render_metrics(answer: Answer) -> None:
    lat = getattr(answer, "latency", None)
    cols = st.columns(5)
    cols[0].metric("Modelo", (answer.model or "n/d").split("/")[-1][:20])
    cols[1].metric("Embed (ms)", f"{lat.embedding_ms:.0f}" if lat and lat.embedding_ms else "n/d")
    cols[2].metric("Busca (ms)", f"{lat.retrieval_ms + (lat.embedding_ms or 0):.0f}" if lat else f"{answer.retrieval_time_ms or 'n/d'}")
    cols[3].metric("Geração (ms)", f"{lat.generation_ms:.0f}" if lat and lat.generation_ms else f"{answer.generation_time_ms or 'n/d'}")
    cols[4].metric("Total (ms)", f"{answer.total_time_ms:.0f}" if answer.total_time_ms else "n/d")


def page_chat() -> None:
    st.title("💬 Compliance Assistant")
    st.caption("Pergunte em português sobre LGPD, políticas internas, incidentes, retenção de documentos, ética e organização.")
    st.markdown("---")

    service = _ensure_qa_service()
    if service is None:
        st.stop()

    history = st.session_state.setdefault("chat_history", [])
    with st.container(height=420, border=True):
        if not history:
            st.info("💬 Perguntas sugeridas:")
            for q in [
                "Posso compartilhar minha senha com um colega em caso de urgencia?",
                "Em caso de incidente S0 na NovaData Solutions, quanto tempo de SLA e quem aciono?",
                "Por quanto tempo a empresa retem documentos trabalhistas apos desligamento?",
                "Quais os principios da LGPD previstos no artigo 6?",
            ]:
                if st.button(q, use_container_width=True):
                    st.session_state._suggested = q
                    st.rerun()
        for entry in history:
            with st.chat_message("user"):
                st.write(entry["question"])
            with st.chat_message("assistant"):
                if entry.get("insufficient"):
                    st.warning("[ATENÇÃO] Informação insuficiente nos documentos indexados.")
                st.markdown(entry["answer"])
                _render_metrics(entry["answer_obj"]) if False else None
                if entry.get("citations_data"):
                    from src.domain.source import SourceCitation
                    obj = Answer(
                        text=entry["answer"],
                        citations=[SourceCitation(**c) for c in entry["citations_data"]],
                    )
                    _render_citations(obj)

    suggested = st.session_state.pop("_suggested", None)
    prompt = st.chat_input("Digite sua pergunta em português…") or suggested
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Buscando documentos relevantes e gerando resposta…"):
            t0 = time.perf_counter()
            answer = service.answer(prompt)
            elapsed = (time.perf_counter() - t0) * 1000
        with st.chat_message("assistant"):
            if answer.insufficient_information:
                st.warning("[ATENÇÃO] Nao houve recuperacao suficiente nos documentos; esta e a resposta padrao.")
            st.markdown(answer.text)
            _render_metrics(answer)
            _render_citations(answer)
            st.info(answer.disclaimer)
            st.caption(f"Concluído em {elapsed:.0f} ms")

        history.append(
            {
                "question": prompt,
                "answer": answer.text,
                "insufficient": answer.insufficient_information,
                "citations_data": [c.__dict__ for c in answer.citations],
                "answer_obj": answer,
            }
        )
        if len(history) > 20:
            history[:] = history[-20:]

    if st.button("🗑️ Limpar histórico", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()


def page_base() -> None:
    st.title("📚 Base de Conhecimento")
    st.caption(f"{len(_doc_cards())} documentos oficialmente indexados pelo Compliance Assistant.")
    st.markdown("---")

    cards = _doc_cards()
    cols = st.columns(3)
    for i, card in enumerate(cards):
        c = cols[i % 3]
        with c.container(border=True):
            st.markdown(f"**{card.title}**")
            st.caption(f"Categoria: {card.category}  ·  Versão {card.version}")
            st.write(f"**Responsáveis:** {card.owners}")
            st.caption(f"Atualizado em {card.updated}  ·  arquivo: `{card.file}`")


def page_quality() -> None:
    st.title("📊 Qualidade do RAG")
    st.caption("Resultados dos runners Nível 1 (retrieval) e Nível 2 (QA final).")
    st.markdown("---")

    reports_dir = Path("evaluation/reports")
    retrieval = _load_json_report(reports_dir / "retrieval_report.json")
    qa = _load_json_report(reports_dir / "qa_level2_report.json")

    if not retrieval:
        st.warning(
            "Relatório Nível 1 não encontrado. Rode primeiro:\n\n"
            "```bash\npython evaluation/evaluate_retrieval.py --fail-on-zero\n```"
        )
    else:
        s = retrieval.get("summary") or retrieval.get("metrics") or {}
        c1, c2, c3 = st.columns(3)
        c1.metric("Nível 1 · Doc correto", f"{s.get('accuracy_document', s.get('doc_accuracy', 'n/d'))}")
        c2.metric("Nível 1 · Seção correta", f"{s.get('accuracy_section', s.get('section_accuracy', 'n/d'))}")
        c3.metric("Nível 1 · Recall KW", f"{s.get('recall_keywords', s.get('kw_recall', 'n/d'))}")
        st.caption("Meta interna: ≥ 92% em Documento / ≥ 90% em Seção / ≥ 98% em KW.")

    st.markdown("---")

    if not qa:
        st.info(
            "Relatório Nível 2 ainda não gerado. Rode um subconjunto de casos para economizar tokens:\n\n"
            "```bash\npython evaluation/evaluate_qa_level2.py --cases LGPD-001,SEG-005,PRI-002,BKP-002 --fail-below 0.4\n```"
        )
    else:
        s = qa.get("summary", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nível 2 · Faithfulness (média)", f"{s.get('avg_faithfulness', 0)*100:.0f}%")
        c2.metric("Nível 2 · Context Recall (média)", f"{s.get('avg_context_recall', 0)*100:.0f}%")
        c3.metric("Nível 2 · Citation Precision", f"{s.get('avg_citation_precision', 0)*100:.0f}%")
        c4.metric("Nível 2 · Citation Recall", f"{s.get('avg_citation_recall', 0)*100:.0f}%")
        st.caption(
            f"Casos: {s.get('cases', 0)}  ·  "
            f"Passaram: {s.get('passed', 0)} ({s.get('passed_pct', 0)*100:.1f}%)  ·  "
            f"Score médio geral: {s.get('avg_score_geral', 0)*100:.1f}%."
        )
        results = qa.get("results", [])
        if results:
            with st.expander(f"Casos ({len(results)})"):
                st.dataframe(
                    [
                        {
                            "ID": r.get("id"),
                            "Status": "✅ PASS" if r.get("passed") else "❌ FAIL",
                            "Faith": f"{r['metrics']['faithfulness']*100:.0f}%" if r.get("metrics") else "-",
                            "CR": f"{r['metrics']['context_recall']*100:.0f}%" if r.get("metrics") else "-",
                            "CP": f"{r['metrics']['citation_precision']*100:.0f}%" if r.get("metrics") else "-",
                            "CRec": f"{r['metrics']['citation_recall']*100:.0f}%" if r.get("metrics") else "-",
                            "Pergunta": (r.get("question") or "")[:80],
                        }
                        for r in results
                    ],
                    use_container_width=True,
                    hide_index=True,
                )


def page_about() -> None:
    st.title("📘 Sobre · Contato")
    st.caption(f"{COMPANY}  ·  {BUILD_TAG}")
    st.markdown("---")

    st.subheader("Sobre a NovaData Solutions")
    st.write(
        "A NovaData Solutions é uma empresa fictícia criada para o Challenge ONE (Programa Oracle Next Education), "
        "com foco em soluções de governança de dados, privacidade e conformidade com a LGPD. "
        "O Compliance Assistant é seu produto flagship: um assistente de IA corporativa neutro, "
        "orientado a fontes auditáveis, sem inventar políticas ou pareceres jurídicos."
    )

    st.subheader("Arquitetura")
    st.markdown(
        """
- **`src/config/`** — settings centralizadas via `pydantic-settings` + `.env`.
- **`src/domain/`** — modelos de domínio puros (`Document`, `Chunk`, `Question`, `Answer`, `SourceCitation`, `LatencyBreakdown`).
- **`src/providers/`** — Cohere chat e embeddings, trocáveis sem tocar regras de negócio.
- **`src/ingestion/`** — loader (aliases por stem) + splitter (outline H2+ / seção herdada / ignora H1).
- **`src/retrieval/`** — Retriever + VectorStore FAISS local, com score threshold e top_k.
- **`src/services/`** — QAService anti-hallucination e IndexService.
- **`evaluation/`** — runners N1 (`evaluate_retrieval.py`) e N2 (`evaluate_qa_level2.py`), com JSON reports.
- **`tests/`** — pytest. 9 testes QAService + smoke test Streamlit.
- **`scripts/`** — `index_documents.py`, `chat.py`, `verify_cohere.py`.
- **`streamlit_app.py`** — UI institucional 5 abas.
        """
    )

    st.subheader("Equipe / Pontos de contato")
    for role, name, email in [
        ("CTO", "Equipe NovaData Engenharia", "eng@novadatatech.br"),
        ("CISO / Segurança", "SOC NovaData", "soc@novadatatech.br"),
        ("DPO / LGPD", "Compliance NovaData", "dpo@novadatatech.br"),
        ("CCO / Ética", "Canal de Denúncias NovaData", "etica@novadatatech.br"),
        ("CHRO / RH", "People NovaData", "people@novadatatech.br"),
    ]:
        st.write(f"- **{role}** — {name} · `{email}`")

    st.subheader("Citação do produto")
    st.code(
        f"NovaData Solutions. {APP_TITLE} — {APP_SUBTITLE}. "
        f"Versão {BUILD_TAG}, 2026. Disponível em github.com/devfabiosantos/compliance-assistant.",
        language=None,
    )


def main() -> None:
    st.set_page_config(
        page_title=f"{APP_TITLE} · {COMPANY}",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    with st.sidebar:
        st.title(APP_TITLE)
        st.caption(APP_SUBTITLE)
        st.caption(BUILD_TAG)
        choice = st.radio(
            "Navegação",
            [
                "🏠 Home",
                "💬 Compliance Assistant",
                "📚 Base de Conhecimento",
                "📊 Qualidade do RAG",
                "📘 Sobre / Contato",
            ],
        )
        st.markdown("---")
        st.caption(
            "⚠️ Este assistente não substitui parecer jurídico. "
            "Todas as respostas são baseadas exclusivamente nos documentos indexados."
        )

    pages = {
        "🏠 Home": page_home,
        "💬 Compliance Assistant": page_chat,
        "📚 Base de Conhecimento": page_base,
        "📊 Qualidade do RAG": page_quality,
        "📘 Sobre / Contato": page_about,
    }
    pages[choice]()


if __name__ == "__main__":
    main()
