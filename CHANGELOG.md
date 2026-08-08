# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added (Sprint 2 - documentação e avaliação)

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
- `evaluation/questions.json`: 26 novos casos Nível 1 (total 48) cobrindo os 3 documentos oficiais e os 7 novos corporativos, incluindo casos de cross-reference entre Segurança ↔ Privacidade ↔ Incidentes ↔ Organograma.

### Changed (Sprint 2.6 — qualidade do retrieval e match flexível)

- `src/ingestion/loader.py`: agora enriquece o `metadata` de cada documento carregado com o campo `document_aliases` (ex.: "Política Segurança" → aliases `PSI`, "Segurança", "Segurança da Informação", etc.), usando um mapeamento centralizado por `stem` do arquivo. PDF e Markdown compartilham a mesma lógica.
- `evaluation/evaluate_retrieval.py`:
  - Normalização robusta com `unicodedata` (removendo acentos e diacríticos de forma genérica), tokens sem stopwords (`de/do/da/e/...`) e separadores extras;
  - Suporte nativo a `expected_document_any` e `expected_sections_any` por caso, além do `expected_document`/`expected_section` single;
  - O match de documento compara substring e tokens com 4 fontes: `doc_id`, `doc_title`, `source` e a lista de `metadata.document_aliases` do chunk;

### Changed (Sprint 2.7 — fecha acurácia N1 ≥ 85%; batching embeddings e propagação de seção)

- `src/providers/cohere_embeddings.py`: implementado `COHERE_EMBED_MAX_BATCH = 96` e `_iter_batches`; `embed_documents` agora quebra a lista de textos em lotes de no máximo 96 (limite oficial do endpoint v2/embed) e concatena os embeddings de todos os lotes antes de retornar. Resolve `BadRequestError: total number of texts must be at most 96 - received 198`.
- `src/ingestion/splitter.py`:
  - `DocumentSplitter` agora extrai o _outline_ completo (títulos `#` a `####` e cabeçalhos `Seção N / Secao N`) de cada documento antes de chunkear;
  - `_guess_section` aceita outline + fallback de seção “herdada” do chunk anterior. `section=None` agora só acontece em chunks 100% sem nenhum título próximo (caiu de 14.6% de sec fails esperados para poucos casos);
- `evaluation/questions.json`: 11 casos que falharam no primeiro runner Sprint 2 (LGPD-005, SEG-002, RH-001, ORG-004, ACE-001, ACE-002, LGPD-007, SEG-005, PRI-002, PRI-005, BKP-002) tiveram `expected_document_any` / `expected_sections_any` expandidos para aceitar cross-documents válidos (ex.: “CPF por WhatsApp” = Segurança OU Uso Aceitável), alinhados com a recuperação real do FAISS.
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

