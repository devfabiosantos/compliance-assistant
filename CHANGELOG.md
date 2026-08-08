# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added (Sprint 2 - em andamento)

- `docs/oficiais/`: stubs Markdown de referência da LGPD (Lei 13.709/2018), Guia ANPD e FAQ ANPD com artigos e seções reais, prontos para complementar com PDFs oficiais quando disponíveis.
- Documentos corporativos da Sprint 2 em `docs/empresa/`:
  - `politica_seguranca_informacao.md` (Segurança / TI)
  - `politica_privacidade_lgpd.md` (Jurídico / Compliance)
  - `manual_colaborador.md` (RH)
  - `politica_controle_acesso.md` (TI)
  - `plano_resposta_incidentes.md` (Segurança / Operações)
  - `politica_backup_retenção.md` (Infraestrutura)
  - `politica_uso_aceitavel.md` (Governança / TI)
- `docs/empresa/README.md`: índice completo dos documentos, com status de versão, responsáveis e prazos de revisão.
- `evaluation/questions.json`: ~22 novos casos Nível 1 cobrindo os 3 documentos oficiais e os 7 novos corporativos, incluindo casos de cross-reference entre Segurança ↔ Privacidade ↔ Incidentes ↔ Organograma.

### Changed

- `docs/adr/`: futuros ADRs para Sprint 3 e 4 (pgvector, Streamlit, OCI) reservados em índice.
- `requirements.txt`: removida dependencia `langchain-cohere==0.1.10` (inexistente no indice publico); o projeto usa o SDK oficial `cohere` diretamente em `src/providers/`. Ajustadas faixas de versao de LangChain para reducao de conflitos e adicionada dependencia explicita de `numpy` (requerida pelo FAISS/embeddings).
- `src/providers/cohere_embeddings.py` e `scripts/verify_cohere.py`: corrigida extracao de embeddings para SDK Cohere v5+, em que `response.embeddings` retorna objeto `EmbedByTypeResponseEmbeddings` com atributo `float_` (alias `float`) contendo a lista de vetores.
- `src/providers/cohere_chat.py`, `src/config/settings.py`, `scripts/verify_cohere.py`, `.env.example`: substituido o modelo de chat padrao de `command-r` (descontinuado em 15/09/2025) por `command-r7b-12-2024`, com fallback automatico para `command-r-08-2024` e alerta caso sejam usados aliases depreciados (`command`, `command-light`, `command-r`, `command-r-plus`).
- `src/ingestion/loader.py`: adicionada filtragem de documentos meta na ingestao por meio de `excluded_names` e `excluded_suffixes`; por padrao, `README.md` nao sao indexados como documentos de conhecimento.
- `src/providers/cohere_chat.py`: prompt de RAG reescrito com cabecalhos de metadados por chunk (TITULO, ARQUIVO, PAGINA, SECAO, SCORE_RELEVANCIA) e regras obrigatorias anti-hallucination, evitando citacao de politicas, secoes ou documentos nao presentes nos blocos recuperados.

### Added

- Estrutura inicial do repositório (src, docs, scripts, tests, evaluation, assets, data).
- `pyproject.toml` com metadados do projeto, versao 0.1.0, nome `compliance-assistant`.
- `requirements.txt` com LangChain, Cohere, FAISS, PyPDF, Click e python-dotenv.
- Arquivos `.env.example` e `.gitignore`.
- Arquivos open source: `LICENSE` (MIT), `CONTRIBUTING.md`, `CHANGELOG.md`.
- Camadas `src/config`, `src/domain`, `src/providers`, `src/ingestion`, `src/retrieval`, `src/services`, `src/cli` e `src/app` com esqueletos executaveis.
- Scripts `scripts/index_documents.py`, `scripts/chat.py` e `scripts/verify_cohere.py`.
- `docs/adr/` com ADRs iniciais (FAISS, Cohere, LangChain).
- `docs/sample_questions.md` com casos de uso iniciais.
- Documentos piloto da Sprint 1.5 em `docs/empresa/`: `codigo_etica_conduta.md` (Código de Ética e Conduta completo, com cross-references) e `organograma.md` (hierarquia, papéis, responsabilidades por tema, casos multi-documento), além de `docs/empresa/README.md` com diretrizes de escrita e cross-reference.
- `evaluation/questions.json` expandido para 22 casos Nível 1 (LGPD/ANPD, Ética, Organograma e cross-reference).
- Runner automático de avaliação Nível 1 em `evaluation/evaluate_retrieval.py` com relatório CLI + JSON e flags `--questions`, `--report`, `--k` e `--fail-on-zero`.
- Sessão `Avaliação da qualidade do RAG` no `README.md` com instruções do runner Nível 1 e visão do Nível 2.

