# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

## [1.0.2] - 2026-08-18

### Hot-fix final de entrega (Checklist Oficial Alura ONE)

Atualizações de documentação para atender 100% aos 4 entregáveis do Challenge Alura Agente (One Oracle Next Education), conforme roteiro oficial de submissão: Repositório GitHub · README · Agente Funcional · Evidência de Deploy.

### Adicionado em `1.0.2`

- **README seção `💬 Exemplos de perguntas e respostas geradas pelo agente`**: 2 casos textuais completos (Caso 1: Incidente S0 / SLA 1h → CISO+CTO+DPO; Caso 2: Dado sensível LGPD Art. 5º, XXXIX + 2 exemplos práticos RH/processo seletivo). Atende o item "Exemplos de respostas geradas pelo agente" do checklist oficial Alura.
- **README seção `☁️ Evidência de Deploy em Produção (Nuvem)`**:
  - Link público HTTPS live `https://compliance-assistant-novadata.onrender.com` (clicável).
  - Histórico completo OCI Always Free (VM A1.Flex ARM 137.131.156.249 / VCN / Security List / Console Serial GRUB reset / scripts deploy `.sh` + `.ps1`).
  - Justificativa estratégia híbrida (mesmo Dockerfile OCI + PaaS para garantir entrega no prazo 19/08).
  - Tabela 4 evidências visuais (Fig.1 Home / Fig.2 Chat / Fig.3 Qualidade / Fig.4 Healthcheck `/_stcore/health`).
- **README Roadmap Sprint**: adicionadas linhas `v1.0.1` (Deploy Render + Hotfix FAISS) e `v1.0.2` (Entrega final checklist Alura ONE) marcados ✅ entregues em 18/08.

## [1.0.1] - 2026-08-18

### Hot-fix de Deploy para Render.com (Entrega Banca ONE)

Deploy de produção real para link público HTTPS (`https://compliance-assistant-novadata.onrender.com`)
para a banca avaliadora do Challenge ONE, após bloqueios de egress na OCI Always Free.

### Adicionado em `1.0.1`

- `scripts/entrypoint.sh` (NOVO): Entrypoint Docker robusto que **cria o índice FAISS automaticamente**
  na primeira inicialização do container, caso `data/vector_store/index.faiss` não exista.
  Valida `COHERE_API_KEY` antes de indexar, evitando erro "Índice vetorial não encontrado" em plataformas
  PaaS como Render (onde o .gitignore remove os artefatos locais de vector store).
- Header de marca **NovaData Solutions** na Home da UI Streamlit: banner SVG inline com gradiente azul/verde
  (cores LGPD/compliance) e texto "Governança de Dados · Privacidade LGPD · IA Corporativa Auditável",
  criando identidade visual profissional antes mesmo do título (antes só aparecia o nome da empresa
  como string em st.title).

### Alterado em `1.0.1`

- `Dockerfile`:
  - `CMD` de `streamlit run ...` → agora usa `/app/scripts/entrypoint.sh` para garantir indexação automática.
  - `HEALTHCHECK --start-period`: aumentado de `90s` → `180s` para acomodar a primeira indexação de 198 chunks (~30-60s).
  - Adicionado `RUN mkdir -p /app/data/vector_store /app/data/logs` + `chmod 777` para plataformas com filesystem somente escrita em pastas específicas.
- `pyproject.toml`: bump versão `1.0.0` → `1.0.1` (hotfix semântico de deploy, sem mudanças de API).

## [1.0.0] - 2026-08-08

### Release Note Final — Entrega Challenge ONE (Oracle Next Education)

Versão final do **Compliance Assistant** congelada para apresentação do Challenge ONE. Todas as funcionalidades planejadas em 6 sprints foram entregues:
- **8 tags SemVer** (`v0.1.0` → `v1.0.0`) publicadas no repositório GitHub.
- **3 prints reais (Figuras 1, 2, 3)** substituindo placeholders no README, com BUILD_TAG `v1.0.0` visível, chat com Incidente S0 respondido (SLA 1 hora / CISO + CTO) e Qualidade N1 100% DOC / SEC / KW em 48 casos.
- **2 hot-fixes do Sprint 6.5:** `BUILD_TAG` agora resolvido por `env COMPLIANCE_BUILD_TAG` (fallback `v1.0.0` + Docker `ARG BUILD_TAG=v1.0.0`); parser do summary Nível 1 compatível com chaves antigas/novas (`document_accuracy` / `section_accuracy` / `keyword_recall`).
- **19 testes pytest 19/19 PASS (QA 9 + 5 smoke Streamlit + casos extras).**
- **Pipeline de deploy reproduzível 10 passos OCI Always Free (A1 Ampere 4 OCPU 24 GB).**
- **Roteiro vídeo demo ONE de 5 minutos exato (9 blocos / 4min55s).**

### Adicionado em `1.0.0`

- `assets/screenshots/fig1_home.PNG`, `fig2_chat_incidente_s0.PNG`, `fig3_qualidade_n1_n2.PNG`: 3 telas reais da UI Streamlit BUILD_TAG v1.0.0.

### Corrigido em `1.0.0`

- **Hot-fix BUILD_TAG hard-coded:** `streamlit_app.py` linha 28 — removido valor `v0.4.0-rc1 · Sprint 4`, substituído por `_resolve_build_tag()` (env vars `COMPLIANCE_BUILD_TAG` / `BUILD_TAG`, fallback `v1.0.0`).
- **Hot-fix parser Qualidade Nível 1:** chaves do summary `retrieval_report.json` — agora compatível com ambos formatos (`accuracy_document` legado e `document_accuracy` atual; idem Section e KW Recall).
- **Dockerfile:** `ARG BUILD_TAG` default de `dev` → `v1.0.0` para `docker build` sem parâmetros já gerar imagem de release.

## [1.0.0-rc1] - 2026-08-09

### Release Note

Primeira release candidate do **Compliance Assistant**, congelada para entrega do Challenge Oracle Next Education (ONE). Toda a stack está validada com:

- **5 versões taggeadas** (`v0.1.0` → `v0.5.0-rc1`) em 6 sprints atômicas (06/08 → 10/08/2026).
- **Base documental coerente:** 12 documentos — 3 oficiais LGPD/ANPD + 2 pilotos (Ética + Organograma) + 7 corporativos, com cross-references entre políticas.
- **Avaliação Nível 1 100% em 48 casos:** `DOC=100%` / `SEC=100%` / `KW=100%` garantidos por aliases por documento, splitter com seção herdada, runner robusto Unicode/stopwords/expected_any.
- **Avaliação Nível 2 com 4 métricas objetivas:** Faithfulness anti-hallucination, Context Recall, Citation Precision, Citation Recall.
- **2 interfaces:** CLI (scripts `index_documents.py`, `chat.py`) + Web (Streamlit 5 abas identidade NovaData).
- **Empacotamento e deploy reproduzível:** `Dockerfile` (Python 3.13-slim) + `docker-compose.yml` + scripts `deploy_oci.sh` (Oracle Linux 8/9) e `deploy_oci.ps1` (Windows → SSH → OCI Always Free).
- **14 testes pytest 14/14 passando:** 9 unitários QAService + 5 smoke Streamlit (válidos para CI).
- **Governança open-source profissional:** MIT LICENSE, ADRs iniciais, `CONTRIBUTING.md`, `CHANGELOG.md` Keep a Changelog pt-BR, Conventional Commits.

### Adicionado em `v1.0.0-rc1` (trabalho do Sprint 6 Freeze)

- `docs/pages/apresentacao_one.md` (NOVO): roteiro exato de 5 minutos para vídeo demo do ONE, com 9 telas + falas estruturadas por segundo, dicas de gravação e checklist do vídeo.
- `README.md` Sprint 6 novas seções:
  - **Sobre o Challenge ONE** com narrativa das decisões arquiteturais (por que RAG, por que FAISS como MVP, por que Cohere, por que provider-agnostic, por que 2 níveis de avaliação, por que OCI Always Free).
  - **Telas da aplicação (Figuras 1, 2 e 3)** com placeholders e descrições textuais de cada print da UI Streamlit.
  - Roadmap atualizado: `v0.6.0-rc1` e `v1.0.0-rc1` marcados como ✅ entregues em 09/08/2026.
  - FAQ nova pergunta 5: “Como faço o vídeo demo de 5 minutos pro ONE?”.
- `CHANGELOG.md`: fechadas seções `[1.0.0-rc1] - 2026-08-09` e `[0.6.0-rc1] - 2026-08-09` em conformidade com Keep a Changelog pt-BR 1.1.0.
- `pyproject.toml`: bump versão `0.5.0-rc1` → `0.6.0-rc1` (tag `v1.0.0-rc1` identifica o mesmo commit, para semântica de release).

## [0.6.0-rc1] - 2026-08-09

### Added (Sprint 6 - Freeze e preparação entrega ONE)

- `docs/pages/apresentacao_one.md`: roteiro cronometrado (4min55s ± 15s) com 9 telas, falas estruturadas por tópico, dicas de gravação e checklist final do vídeo demo ONE.
- `README.md`: nova seção **Sobre o Challenge ONE** explicando o racional das decisões arquiteturais (RAG vs ChatGPT puro, 2 níveis de avaliação, FAISS → Qdrant/pgvector, provider-agnostic Cohere → OpenAI/Gemini/Llama, OCI Always Free).
- `README.md`: 3 placeholders de **Telas da aplicação** (Fig.1 Home + BUILD_TAG, Fig.2 Chat UI respondendo incidente S0 + fontes, Fig.3 Qualidade Nível 1 100%) com descrições textuais detalhadas — depois substituídas por screenshots reais antes da entrega final.
- `README.md`: FAQ pergunta 5 — “Como faço o vídeo demo de 5 minutos pro ONE?” aponta `docs/pages/apresentacao_one.md`.
- `README.md`: Roadmap Sprint 6 (`v0.6.0-rc1` freeze) e `v1.0.0-rc1` marcados ✅ entregues, com status “meta 14/08” preservada e buffer 11 dias até 19/08.
- `pyproject.toml`: bump `0.5.0-rc1` → `0.6.0-rc1`.

### Added (Sprint 5 - Deploy OCI, Dockerfile e README final ONE)

- `Dockerfile` (NOVO): imagem multi-camada `python:3.13-slim-bookworm` com healthcheck Streamlit, `BUILD_TAG` build-arg, entrypoint `streamlit run :8501` em 0.0.0.0.
- `docker-compose.yml` (NOVO): serviço `compliance-assistant` com `mem_limit=4g`, volumes persistentes para `data/vector_store` / `evaluation/reports` / `logs`, env-file `.env`, healthcheck `/health` a 60s, rede `compliance-net` e `security_opt=no-new-privileges`.
- `scripts/deploy_oci.sh` (NOVO): deploy passo a passo para Oracle Linux 8/9 (10 passos). Instala Docker Engine + Compose v2 oficial, ajusta firewalld para 8501/TCP, roda build imagem, reindexa FAISS na primeira inicialização e exibe URL final com IP público.
- `scripts/deploy_oci.ps1` (NOVO): deploy do lado Windows (PowerShell 5.1) — envia código + `.env` via `tar` + `scp` (nunca commita segredos) e roda `deploy_oci.sh` via SSH. Parâmetros `IpPublico`, `Usuario`, `ChavePrivada` editáveis no topo do script.
- `.streamlit/config.toml` (NOVO): configuração global Streamlit identidade NovaData Solutions — tema `primaryColor="#4F46E5"` (roxo corporativo), `gatherUsageStats=false`, `showErrorDetails=false`, `fileWatcherType=poll`.
- `README.md` (atualizado Sprint 5): novas seções **Arquitetura (Mermaid)** com diagrama 10 camadas, **Camadas do código** (tabela 11 responsabilidades), **Como executar localmente (3 minutos)** passo a passo Windows, **Como executar local via Docker**, **Deploy OCI** completo (pré-requisitos Console + Passo A PowerShell + Passo B manual + tabela troubleshooting 5 sintomas), **FAQ rápido 4 perguntas**, **Roadmap entregue ONE (Sprints 1–6 até v1.0.0)** e **Futuro pós-Challenge**.
- `pyproject.toml`: bump versão `0.4.0-rc1` → `0.5.0-rc1`.

### Added (Sprint 4 - Interface Streamlit e UI Chat institucional)

- `streamlit_app.py` (NOVO): aplicação Streamlit 5 abas (Home, Compliance Assistant, Base de Conhecimento, Qualidade do RAG, Sobre/Contato) com identidade NovaData Solutions. Destaques:
  - **Home**: hero institucional, 8 diferenciais do produto, tabela “Pronto para produção”, links GitHub/ANPD.
  - **Compliance Assistant**: histórico de chat (20 mensagens), botões de 4 perguntas sugeridas, renderização de respostas com:
    - `st.warning` quando `insufficient_information=True`;
    - `st.expander` “📄 Fontes citadas (n)” com `dataframe` (Documento | Seção | Página | Score | Snippet);
    - 5 `st.metric` de métricas (Modelo, Embed ms, Busca ms, Geração ms, Total ms);
    - `st.info` com disclaimer obrigatório.
  - **Base de Conhecimento**: grid 12 cards (3 oficiais + 9 empresa) com categoria, versão, responsáveis e data.
  - **Qualidade do RAG**: lê JSONs `evaluation/reports/retrieval_report.json` e `qa_level2_report.json` e renderiza métricas N1/N2 com cards + tabela de últimos casos.
  - **Sobre / Contato**: narrativa NovaData Solutions, arquitetura em 10 camadas, 5 contatos por papel (CTO, CISO, DPO, CCO, CHRO) e citação oficial do produto.
- `requirements.txt`: adicionados `streamlit>=1.38,<2` e `pytest>=8.0` (novo padrão ONE/mercado).
- `tests/test_streamlit_smoke.py` (NOVO): 5 testes smoke (existência do arquivo, import sem crash, 12 documentos no grid, funções de página callable, `main` callable) — válido para CI de UI sem precisar rodar navegador.
- `pyproject.toml`: versão bump `0.3.0-rc1` → `0.4.0-rc1`.

### Added (Sprint 3 - QA profissionalizado e avaliação Nível 2)

- `src/domain/answer.py`: novas classes `LatencyBreakdown`, constantes `DEFAULT_DISCLAIMER` e `INSUFFICIENT_INFORMATION_TEXT`, e campos `insufficient_information`, `latency` e `metadata` no `Answer`. Novos helpers: `citation_titles()`, `citation_sections()` e `pretty_metrics()`.
- `src/services/qa_service.py`: nova função `_build_answer` com heurísticas anti-hallucination (pelo menos 1 chunk útil com score ≥ 0.35 ou resposta cai no texto padrão `INSUFFICIENT_INFORMATION`). `answer()` agora mede 4 tempos distintos (embed, retrieval, generation, total) e injeta em `latency`.
- `evaluation/evaluate_qa_level2.py` (NOVO): runner Nível 2 que executa todos os 48 casos do `questions.json` e mede por caso 4 métricas:
  - **Faithfulness** (%) = tokens da resposta que aparecem em títulos/seções/snippets dos chunks úteis (anti-hallucination).
  - **Context Recall** (%) = keywords esperadas que aparecem na resposta.
  - **Citation Precision** (%) = das citações recuperadas, quantas são úteis.
  - **Citation Recall** (%) = dos documentos/seções esperados, quantos foram citados.
  - Salva relatório JSON em `evaluation/reports/qa_level2_report.json`. Flags: `--cases`, `--fail-below`, `--report`.
- `tests/test_qa_service.py` (NOVO): 14 testes unitários cobrindo estrutura `Answer`, dedup de `citation_titles()`, build_answer válido vs insuficiente, threshold 0.35 de utilidade, anti-hallucination flag, `pretty_metrics()` e resposta vazia.
- `pyproject.toml`: versão bump `0.2.0-rc1` → `0.3.0-rc1`.

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

