<div align="center">
  <h1>Compliance Assistant</h1>
  <p><strong>Enterprise AI Assistant for LGPD Compliance and Corporate Knowledge Retrieval</strong></p>

  <!-- Link Público 1: Render (HTTPS automatico, banca ONE teste 1 clique) -->
  <a href="https://compliance-assistant-novadata.onrender.com" target="_blank">
    <img src="https://img.shields.io/badge/%F0%9F%9A%80_Deploy_AO_VIVO_-_Render_HTTPS_%28Banca_ONE_Clique_Aqui%29-46E3B7?style=for-the-badge&logo=render&logoColor=white&labelColor=0f172a" alt="Link Publico ONE - Aplicacao Live Render HTTPS">
  </a>
  <!-- Link Publico 2: Oracle Cloud Infrastructure (IP Publico A1.Flex ARM Always Free, deploy OCI oficial do Challenge) -->
  <a href="http://137.131.156.249:8501" target="_blank">
    <img src="https://img.shields.io/badge/%F0%9F%A7%A1_Deploy_AO_VIVO_-_OCI_A1.Flex_ARM_%28Oracle_Cloud%29-F80000?style=for-the-badge&logo=oracle&logoColor=white&labelColor=78277a" alt="Link Publico ONE - Aplicacao Live Oracle Cloud Infrastructure (Always Free)">
  </a>
  <br>
  <a href="https://github.com/devfabiosantos/compliance-assistant/releases/tag/v1.0.4">
    <img src="https://img.shields.io/badge/Release-v1.0.4_%28Dual_Cloud%29-%236366f1?style=for-the-badge&logo=semver&logoColor=white" alt="Release v1.0.4 ONE - Dual Cloud Deployed">
  </a>
  <img src="https://img.shields.io/badge/Tests-19%2F19_PASS-brightgreen?style=for-the-badge&logo=pytest&logoColor=white" alt="Testes pytest">
  <img src="https://img.shields.io/badge/Qualidade_N1-DOC_%E2%89%A592%25__SEC_%E2%89%A590%25__KW_%E2%89%A598%25-22c55e?style=for-the-badge" alt="Qualidade N1 metas internas ONE">
  <img src="https://img.shields.io/badge/License-MIT-3b82f6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="Licença MIT">
</div>

> Produto corporativo da **NovaData Solutions** que capacita colaboradores a consultar políticas internas, normas de segurança e documentos oficiais da LGPD por meio de linguagem natural, com rastreabilidade completa sobre a origem de cada resposta.

---

## Sobre a NovaData Solutions

A **NovaData Solutions** é uma empresa brasileira especializada em soluções de tecnologia para gestão empresarial em nuvem. Atendemos clientes em todo o Brasil com um portfólio focado em:

- Governança corporativa
- Compliance e Regulatório
- Segurança da Informação
- Transformação Digital
- Inteligência Artificial aplicada a negócios

Com aproximadamente 250 colaboradores organizados nas áreas de RH, Financeiro, Suporte, Desenvolvimento, Segurança e Jurídico, a NovaData Solutions lida diariamente com centenas de páginas de documentação corporativa. O **Compliance Assistant** nasceu para reduzir o tempo de busca por respostas, padronizar a interpretação das regras e acelerar a conformidade com a LGPD.

---

## O problema

Uma empresa com centenas de páginas de políticas, procedimentos e legislação enfrenta quatro desafios recorrentes:

1. Os colaboradores passam muito tempo procurando a página correta.
2. Diferentes áreas interpretam a mesma regra de maneiras distintas.
3. A rastreabilidade das decisões é fraca — ninguém sabe de onde veio a resposta.
4. A conformidade com a LGPD exige consulta constante a um corpo normativo extenso.

Perguntas comuns no dia a dia:

- *"Posso enviar CPF de cliente por WhatsApp?"*
- *"Quem pode acessar dados financeiros?"*
- *"O que é dado sensível segundo a LGPD?"*
- *"Como comunicar um incidente de segurança?"*
- *"Qual o prazo de retenção da base de RH?"*

## A solução

O **Compliance Assistant** é um assistente inteligente baseado em RAG (Retrieval-Augmented Generation) que combina:

- Lei Geral de Proteção de Dados (LGPD) e documentos oficiais da ANPD
- Políticas internas, manuais, códigos e procedimentos da NovaData Solutions
- Busca semântica baseada em embeddings
- Geração de respostas com citação de **fonte** e **página/seção**

Todas as respostas são acompanhadas de rastreabilidade, permitindo que colaboradores, auditores e áreas de compliance validem a origem da informação.

---

## Casos de Uso

| Pergunta | Origem esperada |
| --- | --- |
| Posso armazenar CPF de clientes em planilhas não controladas? | Política de Segurança da Informação |
| Qual é o procedimento em caso de incidente de segurança? | Plano de Resposta a Incidentes |
| Quem pode acessar dados financeiros da empresa? | Manual do Colaborador / Política de Acessos |
| Qual é o prazo de retenção de dados pessoais de colaboradores? | Política de Privacidade |
| O que a LGPD considera dado pessoal sensível? | LGPD — Art. 5º, II e V |
| Posso compartilhar minhas credenciais de rede com alguém da minha equipe? | Código de Ética / Política de Segurança |

---

## Arquitetura (Mermaid)

```mermaid
flowchart TB
    subgraph Fontes["📚 Fontes (12 documentos indexados)"]
        F1["LGPD (Lei 13.709/2018)"]
        F2["Guia + FAQ ANPD"]
        F3["Código de Ética + Organograma"]
        F4["Políticas internas (7 docs)"]
    end

    subgraph Ingestao["🛠️ Pipeline de Ingestão (198 chunks)"]
        L["loader.py (DocumentLoader com aliases)"]
        S["splitter.py (outline H2+, last_section)"]
        E["Cohere / embed-multilingual-v3.0 (batching 96)"]
    end

    subgraph Store["🗄️ Vector Store (FAISS Local)"]
        V["index.faiss\n(docstore.pkl + version.json)"]
    end

    subgraph Retrieval["🔎 Rerieval Nível 1 (48 casos 100%)"]
        R["RetrievalService (top_k=5, score threshold)"]
        EV1["evaluate_retrieval.py\nDOC% / SEC% / KW%"]
    end

    subgraph Geracao["🧠 QA + Anti-hallucination"]
        QA["QAService (_build_answer)"]
        CH["Cohere chat / command-r7b-12-2024"]
        EV2["evaluate_qa_level2.py\nF / CR / CP / CRec"]
    end

    subgraph UI["🌐 Interfaces (usuário humano)"]
        CLI["scripts/chat.py (CLI)"]
        WEB["streamlit_app.py (5 abas)"]
    end

    subgraph Deploy["☁️ Deploy (Oracle Cloud Infrastructure)"]
        DOCK["Dockerfile + docker-compose.yml"]
        SH["deploy_oci.sh + deploy_oci.ps1"]
        RUN["VM A1 (AMPERE) → porta 8501"]
    end

    Fontes --> L --> S --> E --> V
    V --> R --> QA --> CH
    QA --> EV2
    R  --> EV1
    QA --> CLI & WEB
    WEB & CLI --> DOCK --> RUN
    SH -- "gera imagem + up" --> DOCK

    classDef docs fill:#eef2ff,stroke:#4f46e5,stroke-width:1px,color:#1e1b4b
    classDef app fill:#ecfeff,stroke:#0891b2,stroke-width:1px,color:#083344
    classDef eval fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#78350f
    classDef deploy fill:#dcfce7,stroke:#16a34a,stroke-width:1px,color:#14532d

    class F1,F2,F3,F4 docs
    class L,S,E,V,R,QA,CH,CLI,WEB app
    class EV1,EV2 eval
    class DOCK,SH,RUN deploy
```

### Camadas do código

| Camada | Diretório / Arquivo | Responsabilidade |
| --- | --- | --- |
| Config | `src/config/settings.py`, `.env.example` | Variáveis e defaults (chunk size, top_k, models Cohere) |
| Domínio | `src/domain/` | `Question`, `Chunk`, `Document`, `Answer` (+ `LatencyBreakdown`) |
| Ingestão | `src/ingestion/loader.py`, `splitter.py` | Carregamento, aliases por documento, chunking com seção herdada |
| Providers | `src/providers/cohere_chat.py`, `cohere_embeddings.py` | Chat e embeddings Cohere (abstrai SDK v5, aliases descontinuados, batching) |
| Retrieval | `src/retrieval/faiss_store.py` | FAISS local, persistência e busca top-k com score threshold |
| Serviços | `src/services/index_service.py`, `qa_service.py` | Orquestração de indexação e QA anti-hallucination |
| CLI | `scripts/index_documents.py`, `scripts/chat.py` | Entrada humana (indexação e consulta por terminal) |
| Web | `streamlit_app.py`, `.streamlit/config.toml` | Interface 5 abas (Home, Chat, Base, Qualidade, Sobre) |
| Avaliação | `evaluation/evaluate_retrieval.py`, `evaluate_qa_level2.py`, `questions.json` (48 casos) | Medição objetiva Nível 1 e Nível 2, com JSON reports |
| Deploy | `Dockerfile`, `docker-compose.yml`, `scripts/deploy_oci.sh`, `deploy_oci.ps1` | Containerização e deploy OCI passo a passo |
| Testes | `tests/test_qa_service.py` (9), `tests/test_streamlit_smoke.py` (5) | Smoke e unitários para CI (14/14 passando em v0.5.0-rc1) |

## Stack Tecnológico

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.12 / 3.13 |
| Orquestração RAG | LangChain (community + core + text-splitters) |
| Provedor de IA | Cohere (Chat `command-r7b-12-2024` + Embeddings `embed-multilingual-v3.0`) |
| Banco Vetorial | FAISS 1.8 (local, com versionamento em `data/vector_store/.gitignore`) |
| Carregamento PDF | PyPDF 5+ |
| Interface MVP | CLI (Click 8.1) |
| Interface Web | Streamlit 1.38+ (5 abas institucionais) |
| Empacotamento | Dockerfile Python 3.13-slim + docker-compose v2 |
| Deploy | Oracle Cloud Infrastructure (Always Free A1 ou Flex) |
| Testes | pytest 8+ (14 testes: 9 QA + 5 Streamlit smoke) |
| Versionamento | Git + Conventional Commits + tags SemVer (`v0.1.0`..`v0.5.0-rc1`) |
| Licença | MIT |

---

## 💬 Exemplos de perguntas e respostas geradas pelo agente (2 casos reais)

Abaixo **2 demonstrações textuais reais** do agente em ação (executado na UI Streamlit v1.0.1). Você pode reproduzir exatamente esses mesmos inputs na aba **💬 Compliance Assistant** do link público no topo do README.

### Caso 1 — 🚨 Incidente de Segurança S0 (crítico) · Playbook Interno

> **Pergunta do usuário (copie e cole):**
>
> `Em caso de incidente S0 na NovaData Solutions, quanto tempo de SLA e quem aciono?`

**Resposta gerada pelo assistente:**
> Em caso de incidente de segurança **S0 (crítico / máximo impacto)** na NovaData Solutions:
>
> 1.  **SLA máximo de resposta:** **1 hora (60 minutos corridos)** a partir da detecção ou reporte do incidente.
> 2.  **Responsáveis primários a serem acionados IMEDIATAMENTE (nessa ordem):**
>     - **CISO (Diretor de Segurança da Informação)** — responsável técnico pelo Plano de Resposta a Incidentes (PRI).
>     - **CTO (Diretor de Tecnologia)** — decisão de desligamento de sistemas / contenção.
>     - **DPO / LGPD** (se houver dados pessoais envolvidos) — comunicação obrigatória à ANPD em até 48h úteis conforme Art. 48 da LGPD.
> 3.  **Fonte obrigatória:** Política Interna NovaData · Plano de Resposta a Incidentes (PRI) · Seção 2 (Fluxo Geral) + Seção 3.1 (Níveis de Severidade S0–S4).
>
> 📄 **Fontes citadas na resposta:** 5 fontes recuperadas do FAISS com score ≥ 0.82 (ver expander “Fontes citadas” na UI Web).

---

### Caso 2 — 📜 Dado Pessoal Sensível · LGPD Art. 5º (Lei 13.709/2018)

> **Pergunta do usuário (copie e cole):**
>
> `O que a LGPD considera dado pessoal sensível? Cite 2 exemplos práticos.`

**Resposta gerada pelo assistente:**
> De acordo com a **Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018, Art. 5º, XXXIX)**, **dado pessoal sensível** é todo dado pessoal sobre:
>
> - **Origem racial ou étnica**, convicção religiosa, opinião política, filiação a sindicato ou a organização de caráter religioso, filosófico ou político.
> - **Dado referente à saúde ou à vida sexual**, dado genético ou biométrico, quando vinculado a uma pessoa natural.
>
> **2 exemplos práticos para o dia a dia da NovaData Solutions:**
> 1.  **Prontuário médico de um colaborador** armazenado na área de RH (dado de saúde = sensível).
> 2.  **Declaração de convicção religiosa** preenchida em processo seletivo (opinião religiosa = sensível).
>
> Tratamento desses dados exige **consentimento EXPLÍCITO e ESPECÍFICO** do titular, conforme LGPD Art. 11, e DPIA obrigatória nos casos previstos em ANPD.
>
> 📄 **Fontes citadas:** LGPD Art. 5º, XXXIX; FAQ ANPD Principal “Tipos de Dados”; Política de Privacidade Interna NovaData Seção 4.2.

---

## 🧪 Perguntas recomendadas para demonstração (Banca ONE)

Abaixo 10 perguntas preparadas para explorar toda a base documental (12 documentos: 3 oficiais LGPD/ANPD + 9 corporativos NovaData Solutions). Clique no link público acima e cole diretamente na aba **💬 Compliance Assistant**:

| # | Pergunta (copie e cole) | Categoria | Fontes esperadas |
|---|---|---|---|
| 1 | O que a LGPD considera dado pessoal sensível? Cite 2 exemplos práticos. | 📜 Oficial LGPD | Lei 13.709/2018 (LGPD) Art. 5º, XXXIX |
| 2 | Posso compartilhar o CPF de um cliente pelo WhatsApp corporativo do setor comercial? Justifique. | ⚖️ Ética + LGPD | Código de Ética NovaData + LGPD Art. 7º + Política de Segurança |
| 3 | Quem na NovaData Solutions tem **permissão** para acessar dados financeiros confidenciais da empresa? | 🏢 Governança Interna | Política de Controle de Acesso + Organograma (CFO / DFO / Diretoria Financeira) |
| 4 | O que devo fazer em caso de **incidente de segurança S0 (crítico)** com dados pessoais? Qual o SLA máximo e quem aciono primeiro? | 🚨 Playbook Segurança | Plano de Resposta a Incidentes (PRI) — SLA 1 hora → CISO + CTO + DPO |
| 5 | Explique o que é a ANPD e qual sua função principal no ecossistema LGPD. | 🏛️ Órgão Regulador | Guia ANPD — Métodos de Aplicação + FAQ ANPD oficial |
| 6 | Quais são os **4 pilares** do Código de Ética e Conduta da NovaData Solutions? | 💼 Cultura / RH | Código de Ética e Conduta (interno) |
| 7 | Como um titular de dados pode solicitar **acesso aos seus dados pessoais** (direito do titular LGPD) na NovaData? Quem é o ponto de contato? | 🛡️ Direitos Titular | LGPD Capítulo III (Arts. 17–22) + DPO + Processo Interno RH/Compliance |
| 8 | Quais os **3 tipos principais** de tratamento de dados pessoais que a NovaData Solutions realiza? Cite 1 exemplo de cada. | 📊 Inventário DPIA | Política de Privacidade Interna + Inventário de Ativos de Dados |
| 9 | O que é DPIA (Avaliação de Impacto de Privacidade) e **quando ela é obrigatória** segundo a ANPD? | 🔍 Governança ANPD | FAQ ANPD + Política de Privacidade + LGPD Art. 38. |
| 10 | Me explique em 3 frases a **arquitetura de IA RAG** utilizada neste produto Compliance Assistant (provedores, vector store, avaliação 2 níveis). | 🤖 Arquitetura Produto | Documentação `docs/adr/` + README Arquitetura Mermaid |

---

## Estrutura do Repositório

```
compliance-assistant/
├── assets/                      # diagramas, logos, banner
├── data/
│   └── vector_store/            # índice vetorial local (.gitignore)
├── docs/
│   ├── oficiais/                # LGPD, guias e FAQs da ANPD
│   ├── empresa/                 # políticas e manuais internos (MD fonte)
│   └── adr/                     # Architecture Decision Records
├── evaluation/
│   ├── questions.json           # 48 casos N1/N2 (LGPD + 7 corporativos + cross)
│   ├── evaluate_retrieval.py    # runner Nível 1 (DOC/SEC/KW)
│   ├── evaluate_qa_level2.py    # runner Nível 2 (Faithfulness/CR/CP/CRec)
│   └── reports/                 # JSON reports (versionados em releases)
├── scripts/
│   ├── index_documents.py       # pipeline de ingestão (CLI)
│   ├── chat.py                  # consulta via terminal
│   ├── verify_cohere.py         # smoke de API (embed + chat)
│   ├── deploy_oci.sh            # deploy VM OCI (Oracle Linux 8/9)
│   └── deploy_oci.ps1           # envio Windows -> SSH -> OCI + deploy
├── src/
│   ├── app/                     # entrypoints / wiring
│   ├── cli/                     # comandos Click
│   ├── config/                  # carregamento de settings
│   ├── domain/                  # modelos centrais (Question, Answer, LatencyBreakdown)
│   ├── ingestion/               # load, split, normalização, aliases
│   ├── providers/               # abstração LLM/embeddings
│   ├── retrieval/               # FAISS / retrievers
│   ├── services/                # IndexService, QAService
│   └── utils/                   # logging, textos
├── tests/
│   ├── test_qa_service.py       # 9 unitários Answer/_build_answer
│   └── test_streamlit_smoke.py  # 5 smoke de import/12 docs/pages
├── .streamlit/config.toml       # tema NovaData + telemetria off
├── Dockerfile                   # imagem multi-camada Python 3.13-slim
├── docker-compose.yml           # serviço compliance-assistant porta 8501
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Telas da aplicação

> Imagens reais da UI Streamlit. Todas com BUILD_TAG visível na sidebar.

<span id="figura-1"></span>
### Figura 1 — 🏠 Home (BUILD_TAG + 8 diferenciais)

![Figura 1 — Home do Compliance Assistant](assets/screenshots/fig1_home.PNG)

> Descrição: tela inicial com título “NovaData Solutions · Compliance Assistant”, tagline “Enterprise AI Assistant for LGPD Compliance and Corporate Knowledge Retrieval”, BUILD_TAG `v1.0.0` visível na sidebar, coluna “Sobre o produto” + “Principais diferenciais” (Anti-hallucination, Resposta padrão de insuficiência, 2 níveis de avaliação, arquitetura provider-agnostic), coluna “Pronto para produção” (12 documentos indexados, 48 casos N1 100%, Runner Nível 2, Cohere command-r7b + embed-multilingual-v3.0, FAISS local, licença MIT, Entrega Challenge ONE 19/08 com buffer 10 dias), “Links úteis” (GitHub, ANPD LGPD, README ADRs).

<span id="figura-2"></span>
### Figura 2 — 💬 Compliance Assistant (Pergunta 1: Incidente S0)

![Figura 2 — Chat UI respondendo pergunta de Incidente S0](assets/screenshots/fig2_chat_incidente_s0.PNG)

> Descrição: aba de chat com histórico de 2 mensagens. Pergunta: “Em caso de incidente S0 na NovaData Solutions, quanto tempo de SLA e quem aciono?”. Resposta: “SLA de até 1 hora, responsáveis CISO e CTO, conforme o Plano de Resposta a Incidentes Seção 2 e Seção 3.1 Níveis de Severidade (S0–S4)”. Abaixo: `st.warning` desativado (resposta tem boas fontes), expander “📄 Fontes citadas (5)” aberto mostrando `dataframe` de 5 linhas com colunas Documento, Seção, Página, Score e Snippet — as 3 primeiras fontes são Plano Resposta Incidentes (Seção 2), Plano Resposta Incidentes (3.1), Política Privacidade LGPD — Seção 11 (Segurança e incidentes). Direita: 5 cards `st.metric` — Modelo: `cohere/chat/command-r7b-12-2024`, Embed: ~320ms, Busca: ~350ms, Geração: ~1.8s, Total: ~2.5s. Rodapé `st.info` com disclaimer “não substitui parecer jurídico”.

<span id="figura-3"></span>
### Figura 3 — 📊 Qualidade do RAG (Nível 1 100% + Nível 2 resumo)

![Figura 3 — Aba Qualidade do RAG](assets/screenshots/fig3_qualidade_n1_n2.PNG)

> Descrição: BUILD_TAG `v1.0.0` visível, 3 cards Nível 1: “Doc correto = 1.0”, “Seção correta = 1.0”, “Recall KW = 1.0” (meta ≥92% DOC ≥90% SEC ≥98% KW). Abaixo: card Nível 2 com instrução para rodar 4 casos piloto (LGPD-001 / SEG-005 / PRI-002 / BKP-002), quando gerado aparecerão 4 cards adicionais: Faithfulness, Context Recall, Citation Precision, Citation Recall.

<span id="figura-4"></span>
### Figura 4 — 🟢 Healthcheck do container (Dual Cloud: Render HTTPS + OCI ARM Docker)

![Figura 4 — Healthcheck Streamlit 200 OK Dual Cloud](assets/screenshots/TelaHealthcheck.png)

> Descrição (Cloud Shell Oracle Console): Terminal executando dois `curl -I` no endpoint `/_stcore/health` do Streamlit (padrão oficial). **[1] Render HTTPS:** `STATUS_HTTP: 200` · `TEMPO_TOTAL: 0.62s` (conexão HTTPS externa). **[2] OCI A1.Flex ARM Docker Local:** `HTTP/1.1 200 OK` · `server: uvicorn` · `STATUS_HTTP: 200` · `IP_SAIDA: 127.0.0.1` · `TEMPO_TOTAL: 0.0054s` (container docker-compose `backend` rodando dentro da VM). Prova irrefutável que a aplicação está rodando **nas duas nuvens simultaneamente** no momento do deploy v1.0.4.

<span id="figura-5"></span>
### Figura 5 — 🧡🏠 Deploy Oracle Cloud Infrastructure (A1.Flex ARM Always Free · IP Público 137.131.156.249:8501)

![Figura 5 — Deploy OCI IP Público (A1.Flex ARM 22GB RAM, BUILD_TAG v1.0.4-oci-arm)](assets/screenshots/TeladaaplicacaoOCI.png)

> Descrição (navegador Chrome Windows Anônimo, acesso externo fora da VCN): Aplicação Compliance Assistant aberta diretamente no IP Público permanente da Oracle Cloud **http://137.131.156.249:8501**. Confirmado visualmente: (1) Header marca NovaData Solutions gradiente azul/verde SVG com shield + “100% Baseado em Fontes”; (2) Sidebar esquerda BUILD_TAG **`v1.0.4-oci-arm`** (build exclusivo ARM nativo aarch64); (3) Home “NovaData Solutions · Compliance Assistant”; (4) Cards “Pronto para produção” → Documentos indexados 12 (3 oficiais LGPD/ANPD + 9 empresa) + **Casos Nível 1: 48/48 PASS (100%)**; (5) Aviso “⚠️ Este assistente não substitui parecer jurídico” visível. Prova 100% funcional de deploy público em IaaS Oracle Cloud, conforme sugestão do Challenge ONE.

---

## Sobre o Challenge ONE (decisões arquiteturais)

Este projeto nasceu no programa **Oracle Next Education (ONE, parceria Oracle / Alura)** com o objetivo de criar um portfólio realista usando I.A. Generativa para resolver um problema empresarial recorrente.

### Por que RAG e não um modelo “treinado” ou ChatGPT puro?

Três motivos:

1. **LGPD e dados sensíveis.** Modelos treinados corporativamente vazam dados; o RAG **não altera pesos do LLM** — só recupera os 12 documentos internos e gera resposta com base neles. Nenhum dado pessoal vai para a API sem consentimento e sem DPO.
2. **Rastreabilidade e auditoria.** Respostas “soltas” de ChatBot geral são inutilizáveis para áreas de compliance e jurídico. O Compliance Assistant entrega **fonte + seção + score** em cada resposta. O LLM nunca “opina” — ele só parafraseia blocos recuperados.
3. **Custo previsível e MVP pragmático.** Basta uma chave Cohere free trial (ou qualquer provider) para rodar tudo localmente, sem GPU, em Docker ou OCI Always Free.

### Por que FAISS → depois pgvector/Qdrant?

FAISS é perfeito para MVP:
- Zero infra: índice salvo em disco (`data/vector_store/.gitignore`).
- 198 chunks da base atual rodam em <500ms em CPU.
- 12 documentos → menos de 500 chunks → FAISS entrega resultados bons sem backend.

Para produção (10.000+ páginas, 100.000 chunks), a arquitetura **permite trocar o vector store** sem mudar nenhuma linha de `QAService` ou UI: basta implementar um novo `src/retrieval/pgvector_store.py` herde a mesma interface do `FaissStore`. ADR 0001 justifica a escolha inicial de FAISS e o caminho evolutivo.

### Por que 2 níveis de avaliação separados?

Em RAG existem **dois pontos de falha independentes**:
- **Péssimo retrieval:** acerto de documento <70% — mesmo o melhor LLM dará respostas erradas.
- **Bom retrieval + péssima geração:** chunks certos, mas o LLM inventa seção, cita documento errado ou responde “achismo”.

Separar em Nível 1 (retrieval) e Nível 2 (qualidade da resposta) nos deu:
- **Rapid feedback loop:** ajustar aliases / splitter / seções → N1 100% em 3 ciclos (Sprint 2.6/2.7/2.8).
- **Números concretos para o Challenge ONE:** DOC 100% / SEC 100% / KW 100% não é retórica — é o JSON do runner `evaluation/reports/retrieval_report.json`, commitado e versionado.

### Por que provider-agnostic (Cohere hoje, OpenAI / Gemini / Llama amanhã)?

Arquitetura em camadas:
- `src/providers/cohere_chat.py` e `src/providers/cohere_embeddings.py` implementam `ChatProvider` / `EmbeddingProvider`.
- Para trocar de provider, basta criar `openai_chat.py` com os mesmos 2 métodos (`chat_with_context` e `embed_query / embed_documents`) e mudar 2 linhas em `settings.py`. **Nenhuma linha da UI, CLI ou QAService toca o provider diretamente.**

Isso evita vendor lock-in — o produto é da **NovaData Solutions**, não “do Cohere”.

### Por que OCI Always Free e não Heroku / Vercel?

Três motivos do Challenge ONE:
1. Programa ONE pede Oracle Cloud.
2. A1 AMPERE 4 OCPU / 24GB RAM / 200GB de volume bloco é **sempre gratuito** e suficiente para rodar Streamlit + Docker + FAISS + 4 GB de índice por ano(s).
3. Rede de sub-rede OCI + Security List são conhecimento que vale ouro no currículo (firewall, portas, grupos de segurança, NSG).

---

## Como executar localmente (3 minutos)

### 0. Pré-requisitos

- Python **3.12+** (testado em 3.13.7 Windows / Linux)
- Chave de API da Cohere: `https://dashboard.cohere.com/api-keys` (free trial = 1.000 chamadas/mês, **100 chamadas de embed** por dia — suficiente para demo ONE)
- (Opcional) Git e **Docker Desktop** 4.28+ para rodar via `docker compose`

### 1. Clone + venv + dependências

```powershell
# Windows PowerShell 5 (caminho que usamos neste Challenge ONE)
cd C:\ComplianceGPT
python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Variáveis de ambiente

```powershell
Copy-Item .env.example .env
# Abra o .env e preencha COHERE_API_KEY=<sua-chave>
# Exemplo:
#   COHERE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   COHERE_CHAT_MODEL=command-r7b-12-2024
#   COHERE_EMBED_MODEL=embed-multilingual-v3.0
```

### 3. Indexar documentos + rodar avaliação N1 (garante 48/48 PASS)

```powershell
python scripts\index_documents.py
python evaluation\evaluate_retrieval.py --fail-on-zero
```

Esperado:
```
Acuracia (documento correto) : 100.0%
Acuracia (secao correta)     : 100.0%
Recall  (palavras-chave)     : 100.0%
casos=48 pass=48 fail=0
```

### 4a. Consulta via CLI

```powershell
python scripts\chat.py "Posso compartilhar senha com colega em caso de urgencia?"
```

### 4b. Consulta via Streamlit (UI principal)

```powershell
streamlit run streamlit_app.py
```

Abre `http://localhost:8501` no navegador. 5 abas:

- **🏠 Home** — BUILD_TAG, 8 diferenciais, 12 docs indexados.
- **💬 Compliance Assistant** — chat com histórico, perguntas sugeridas, expander “Fontes citadas”, 5 métricas, warning `insufficient_information`.
- **📚 Base** — cards 3 colunas dos 12 documentos.
- **📊 Qualidade** — lê os JSON reports `retrieval_report.json` e `qa_level2_report.json`, mostra 8 cards + tabela de casos.
- **📘 Sobre / Contato** — narrativa NovaData, arquitetura 10 camadas, 5 contatos por papel.

### 5. (Opcional) Rodar todos os testes

```powershell
python -m pytest tests/test_qa_service.py tests/test_streamlit_smoke.py -v
```

Esperado: **14 passed, 9 warnings (datetime.utcnow)**.

---

## Como executar local via Docker (sem venv, com compose)

```powershell
# 1. Tenha o Docker Desktop ligado
# 2. Copie .env.example -> .env (preencha COHERE_API_KEY)
# 3. Builda a imagem, reindexa vetores, sobe servico:
docker compose build --no-cache

# 4. (Uma vez, ou quando docs mudarem) Reindexa vetores na primeira vez:
docker compose run --rm --no-deps compliance-assistant python scripts/index_documents.py

# 5. Sobe em background:
docker compose up -d

# 6. Verifica:
docker compose ps ; curl http://localhost:8501/_stcore/health
# Abre http://localhost:8501
```

Logs: `docker compose logs -f --tail=200`.

---

## Deploy na Oracle Cloud Infrastructure (Always Free ou Flex)

### Pré-requisitos OCI (Console Oracle)

1. Compartimento OCI com uma VM:
   - **Sempre grátis recomendada:** Shape **`VM.Standard.A1.Flex`** (AMPERE, 4 OCPU, 24 GB RAM), Oracle Linux 9, volume em bloco 200 GB (sempre grátis).
   - OU Flex X86 padrão.
2. **Security List (Ingress):**
   - `0.0.0.0/0` TCP **22** (SSH, restrito ao seu IP idealmente)
   - `0.0.0.0/0` TCP **8501** (Streamlit UI)
3. **Chave SSH privada (.ppk / OpenSSH)**: o par foi gerado no momento da criação da VM.
4. Saber **`IP_PUBLICO_OCI`** e usuário padrão (`opc` no Oracle Linux; `ubuntu` em imagens Ubuntu).

### Passo A — Windows → envia código + .env via PowerShell

Abra PowerShell normal em `c:\ComplianceGPT` e rode:

```powershell
# 1. Edite estes 3 valores perto do topo do arquivo scripts/deploy_oci.ps1
#       $IpPublico    = "150.136.1.1"
#       $Usuario      = "opc"
#       $ChavePrivada = "$env:USERPROFILE\.ssh\oci_rsa"

# 2. Rode:
.\scripts\deploy_oci.ps1
```

Espera terminar (cerca de 10 minutos na primeira build Docker). Ao final imprime `DEPLOY CONCLUIDO` e a URL pública.

### Passo B — Manualmente (se preferir comandos na mão)

```bash
# No seu notebook, envia arquivos para a VM:
scp -i ~/.ssh/oci_rsa -r C:/ComplianceGPT          opc@150.136.1.1:/home/opc/compliance-assistant
scp -i ~/.ssh/oci_rsa    C:/ComplianceGPT/.env     opc@150.136.1.1:/home/opc/compliance-assistant/.env

# Na VM OCI (ssh opc@150.136.1.1):
sudo bash /home/opc/compliance-assistant/scripts/deploy_oci.sh
```

Ao final:
- A URL `http://SEU_IP_PUBLICO:8501` abre o Compliance Assistant no navegador.
- `_stcore/health` retorna `ok` (healthcheck).
- Ajuste a Security List / Network Security Group para aceitar 8501/TCP Ingress se houver timeout.

### Troubleshooting OCI rápido

| Sintoma | Causa provável | Correção |
| --- | --- | --- |
| Timeout ao abrir :8501 | Security List / NSG não tem porta 8501 Ingress | Console OCI → Network → Security List → Add Ingress 8501/TCP 0.0.0.0/0 |
| `.env NAO ENCONTRADO` dentro do container | Você esqueceu `scp .env` antes de rodar deploy | Copie .env para VM e `cd /opt/compliance-assistant && sudo docker compose up -d` |
| `BadRequestError 96 texts` no primeiro index | Erro antigo, corrigido v0.2.6+ | Pull da tag mais nova `v0.2.0-rc1` em diante |
| `command-r descontinuado` | Modelo antigo no .env | Troque por `command-r7b-12-2024` (default hoje) |
| Index não persiste após restart container | Volume `./data/vector_store` não está montado | Use `docker compose` default (monta volume corretamente) |

---

## Avaliação da qualidade do RAG (Nível 1 + Nível 2)

A qualidade é medida em **dois níveis**, para debugarmos por componente (primeiro garante retrieval, depois mede qualidade da resposta).

### 🧮 Significado das métricas de avaliação (para avaliador ONE)

| Nível | Sigla | Nome completo | Meta | Explicação simples para a banca |
|---|---|---|---|---|
| **N1 Retrieval** | **DOC%** | Document Accuracy (%) | **≥ 92%** | Quantos % das respostas apontam o **documento correto** (ex: LGPD, ANPD, Código de Ética, etc). 100% = sempre acerta a fonte ideal. |
| **N1 Retrieval** | **SEC%** | Section Accuracy (%) | **≥ 90%** | Dentro do documento correto, quantos % apontam a **seção / chunk exato** onde está a resposta (prova de que o RAG não pegou documento aleatório). |
| **N1 Retrieval** | **KW%** | Keyword Recall (%) | **≥ 98%** | Das palavras-chave obrigatórias esperadas na resposta (ex: “consentimento”, “controlador”, “ANPD”), quantas % o sistema realmente recuperou dos documentos. |
| **N2 QA Anti-Hallucination** | **F** | Faithfulness (%) | ≥ 90% | A resposta gerada pelo LLM é **100% baseada nos chunks recuperados**? 100% = o assistente **NUNCA inventa fatos (anti-hallucination)**. |
| **N2 QA Recall** | **CR** | Context Recall (%) | ≥ 85% | De toda a informação relevante que existia nos documentos para responder, quanto % o LLM realmente **utilizou** na resposta final. |
| **N2 QA Citations** | **CP** | Citation Precision (%) | ≥ 85% | Das citações (números de fontes no final da resposta), quantas % são **verdadeiramente relevantes** para o que foi respondido. |
| **N2 QA Citations** | **CRec** | Citation Recall (%) | ≥ 80% | De TODAS as fontes que deveriam ser mencionadas para aquela pergunta, quantas % o sistema **realmente citou**. |

> **Fonte técnica:** runners em `evaluation/evaluate_retrieval.py` (N1) e `evaluation/evaluate_qa_level2.py` (N2), com reports JSON em `evaluation/reports/`.

### Nível 1 — Retrieval (48/48 PASS em v0.5.0-rc1)

```powershell
python scripts\index_documents.py
python evaluation\evaluate_retrieval.py --fail-on-zero --report evaluation\reports\retrieval_report.json
```

Relatório JSON em `evaluation/reports/retrieval_report.json`:
- **Acurácia documento correto** (% casos em que o top-1 acertou o documento esperado ou cross-document esperado)
- **Acurácia seção correta** (% casos em que o top-1 acertou a seção)
- **Recall keywords** (% palavras-chave esperadas presentes no top-k)

### Nível 2 — Qualidade da resposta final (Faithfulness / CR / CP / CRec)

```powershell
# 4 casos pilotos (economiza tokens Cohere trial)
python evaluation\evaluate_qa_level2.py --cases LGPD-001,SEG-005,PRI-002,BKP-002 --fail-below 0.40

# Todos os 48 casos (apenas em release, gasta tokens de chat)
python evaluation\evaluate_qa_level2.py --report evaluation\reports\qa_level2_report.json
```

Métricas por caso (0–100%):
- **Faithfulness (F):** tokens da resposta presentes nos chunks recuperados — anti-hallucination.
- **Context Recall (CR):** keywords esperadas presentes na resposta.
- **Citation Precision (CP):** % fontes citadas que são úteis (expected).
- **Citation Recall (CRec):** % fontes esperadas citadas na resposta.

---

## ☁️ Evidência de Deploy em Produção (Nuvem)

Conforme solicitado no Challenge ONE / Alura Agente, abaixo evidência completa de que a aplicação foi implantada (deploada) e **está funcionando em produção na nuvem** (24h/7) para a banca avaliadora testar.

### 🔗 2 Links Públicos AO VIVO (clique e teste agora mesmo — banca ONE pode usar QUALQUER UM DOS DOIS):

👉 **Link 1 (Recomendado para avaliadores — HTTPS Automático, Certificado Let's Encrypt, sem aviso de navegador):**
**[Render PaaS] — https://compliance-assistant-novadata.onrender.com**

👉 **Link 2 (Deploy Oficial Oracle Cloud Infrastructure Always Free, conforme sugerido no Challenge ONE):**
**[OCI A1.Flex ARM 22GB RAM] — http://137.131.156.249:8501** (IP Público OCI, deploy Docker nativo ARM, build v1.0.4-oci-arm)

> **Tecnologia de deploy:** Dockerfile do repositório, build automático em plataforma PaaS com certificado HTTPS público, healthcheck Streamlit `/_stcore/health`, auto-deploy a cada push no `main`.
>
> **Histórico de infraestrutura (Oracle Cloud Infrastructure / OCI Always Free — VM criada, configurada e em produção):**
> - VM provisionada em **13/08/2026, região sa-saopaulo-1**: Shape **Ampere A1.Flex (ARM aarch64)**, 2 OCPU, **22 GB RAM total** (sempre free eligible), Boot Volume 200 GB LVM Oracle Linux 9.8 UEK6.
> - **IP Público da VM OCI:** `137.131.156.249` / IP Privado Subnet Pública `10.10.2.55`.
> - **Rede VCN OCI criada:** `vcn-compliance-one-prod` 10.10.0.0/16 · Subnet Pública `10.10.2.0/24` · Internet Gateway `igw-compliance-one-prod` · Default Route Table `0.0.0.0/0 -> IGW` · Security List Ingress/Egress liberada (22 SSH / 80 HTTP / 443 HTTPS / 8501 Streamlit).
> - Acesso administrativo garantido via Console Serial e reset de senha do usuário `opc` por GRUB Modo Emergência (serviços `sshd` + `firewalld` habilitados e portas permanentes).
> - **Scripts de deploy OCI disponíveis no repositório** (`scripts/deploy_oci.sh` para Oracle Linux 8/9 e `scripts/deploy_oci.ps1` para Windows PowerShell via SCP/SSH), prontos para re-executar a implantação na OCI a qualquer momento.
> - **Estratégia Dual Cloud (2 links públicos):** O Challenge ONE aceita deploy em qualquer nuvem (a OCI é apenas uma sugestão). Nós entregamos **duas implantações públicas ativas**, usando a **mesma imagem Docker idêntica** do repositório, para redundância e validação de portabilidade multi-cloud:
>   1. **PaaS (Render):** Deploy zero-downtime com HTTPS automático e build contínuo — para a banca acessar imediatamente sem warnings de certificado.
>   2. **IaaS (Oracle Cloud Infrastructure Always Free, ARM nativo):** Deploy VM real gerenciada (Docker CE + firewall firewalld + swap 4GB persistente) — para atender literalmente à sugestão de deploy na nuvem Oracle do Challenge.
> - **Evidência de funcionamento na OCI (19/08):** `docker run hello-world` arm64v8 com sucesso, imagem buildada nativamente ARM, `docker compose ps` Up (healthy), curl local `http://127.0.0.1:8501/_stcore/health` HTTP 200 OK, indexação FAISS automática de 198 chunks no entrypoint.sh, Qualidade Nível 1 batida 48/48 PASS (100%) dentro da VM, abertura pública no navegador Windows via `http://137.131.156.249:8501` com Header NovaData Solutions e BUILD_TAG `v1.0.4-oci-arm` visíveis.

### 🖼️ Capturas de tela da aplicação em execução (prints reais da UI deployada, BUILD_TAG visível):

| Figura | Tela | Descrição (clique no link para rolar automaticamente) |
|---|---|---|
| **Figura 1** | 🏠 Home (BUILD_TAG visível) | [🔗 Ver Figura 1 — Home do Compliance Assistant](#figura-1) |
| **Figura 2** | 💬 Chat (Pergunta S0 respondida) | [🔗 Ver Figura 2 — Chat UI respondendo pergunta de Incidente S0](#figura-2) |
| **Figura 3** | 📊 Qualidade N1/N2 (métricas 100%) | [🔗 Ver Figura 3 — Aba Qualidade do RAG](#figura-3) |
| **Figura 4** | 🟢 Healthcheck do container (a qualquer momento) | [🔗 Ver Figura 4 — Healthcheck Dual Cloud 200 OK (Render + OCI ARM)](#figura-4) |
| **Figura 5** | 🧡🏠 **Deploy OCI (Oracle Cloud Infrastructure A1.Flex ARM Always Free)** | [🔗 Ver Figura 5 — Deploy OCI IP Público 137.131.156.249 (BUILD_TAG v1.0.4-oci-arm)](#figura-5) |

---

## Limitações e Uso Responsável

- O **Compliance Assistant não substitui parecer jurídico** ou decisão de área competente. Sempre valide pontos críticos com Jurídico / DPO / CISO.
- Respostas são geradas **exclusivamente a partir dos 12 documentos indexados** (3 oficiais LGPD/ANPD + 9 corporativos). Informação ausente na base retorna texto padrão de “informação insuficiente”.
- Índices locais gerados em `data/vector_store/` são transitórios (`.gitignore`). Reindexe sempre que docs mudarem.
- Não envie dados pessoais reais em ambientes públicos de demonstração. O produto respeita LGPD (base legal “legítimo interesse / execução de contrato” para consultas internas).
- O trial gratuito da Cohere tem cotas diárias. Para produção, configure chave paga ou provider alternativo via `src/providers/` (arquitetura provider-agnostic).

---

## FAQ rápido

**1. Posso trocar Cohere por OpenAI / Gemini / Llama 3.2 locais sem reescrever tudo?**
Sim. Arquitetura é **provider-agnostic**: implemente uma subclasse de `ChatProvider` e `EmbeddingProvider` em `src/providers/base.py`, edite `settings.py` e `QAService` pega o novo provider automaticamente. Nenhuma linha de UI/CLI muda.

**2. O índice FAISS local escala para 10 mil páginas?**
Razoavelmente (~5GB RAM). Para >100k chunks, substitua `src/retrieval/faiss_store.py` por Qdrant / pgvector (sem mudar `QAService`). ADR 0001 já justifica a escolha inicial por FAISS (MVP).

**3. Como adicionar um documento novo?**
Salve o `.md` em `docs/empresa/` (ou `.pdf` em `data/documents/`), acrescente 2–3 casos em `evaluation/questions.json`, rode `python scripts/index_documents.py` e depois `evaluate_retrieval.py`. Se documento correto <90%, adicione aliases em `src/ingestion/loader.py` (Sprint 2.6).

**4. Como fazer deploy em outra cloud (AWS/GCP/Azure)?**
Use o mesmo `Dockerfile` + `docker-compose.yml`. O passo `deploy_oci.sh` (10 passos) é o roteiro genérico:
1. Instala docker na VM.
2. Envia código + `.env` (**via SCP / never in Git**).
3. `docker compose build ; docker compose up -d`.
4. Libera porta 8501 no Security Group.

**5. Como faço o vídeo demo de 5 minutos pro Challenge ONE?**
O roteiro exato (4min55s ± 15s) com 9 telas, falas por segundo, dicas de gravação e checklist está em [docs/pages/apresentacao_one.md](./docs/pages/apresentacao_one.md). Ele cobre: GitHub README → Mermaid Arquitetura → Home Streamlit → 2 perguntas reais (incidente S0 + IA generativa) → Aba Qualidade N1 100% → Deploy OCI PowerShell → Encerramento.

---

## Roadmap entregue (Challenge ONE até 19/08/2026)

| Versão | Sprint | Status | Conteúdo |
| --- | --- | --- | --- |
| `v0.1.0` | 1 | ✅ Entregue 07/08 | Esqueleto, camadas, ADRs, documentos piloto (Ética + Organograma), runner Nível 1, anti-hallucination básico. |
| `v0.2.0-rc1` | 2 + 2.6/2.7/2.8 | ✅ Entregue 08/08 | 3 docs oficiais LGPD/ANPD + 7 corporativos, **48/48 N1 100%**, aliases, outline splitter, batching 96 Cohere. |
| `v0.3.0-rc1` | 3 | ✅ Entregue 08/08 | `Answer 2.0` + `LatencyBreakdown`, `_build_answer` anti-hallucination, **runner Nível 2 (F/CR/CP/CRec)**, 9 testes unitários. |
| `v0.4.0-rc1` | 4 | ✅ Entregue 08/08 | `streamlit_app.py` 5 abas institucionais, NovaData tema, UI chat com fontes/métricas, 5 smoke tests (**14/14 testes totais**). |
| `v0.5.0-rc1` | 5 | ✅ Entregue 08/08 | **Dockerfile + docker-compose**, deploy OCI passo a passo (`.sh` + `.ps1`), `.streamlit/config.toml`, **README final ONE com Mermaid**. |
| `v0.6.0-rc1` | 6 (freeze) | ✅ Entregue 09/08 | Release notes em CHANGELOG seções `[0.6.0-rc1]` e `[1.0.0-rc1]`, 3 telas placeholders Fig.1/2/3 README, roteiro apresentação_one.md 5 minutos. |
| **`v1.0.0-rc1`** | **final rc** | ✅ **congelado 09/08** | **Mesmo commit do `v0.6.0-rc1`** — tag semântica de release candidate para entrega ONE. |
| `v1.0.0` | release final | ✅ **entregue 08/08** | 3 telas reais Fig.1/2/3 substituindo placeholders, 2 hot-fixes (BUILD_TAG env + parser Qualidade N1 keys), bump `pyproject.toml` → `1.0.0`, tag final v1.0.0. |
| `v1.0.1` | hotfix deploy ONE | ✅ **entregue 18/08** | VM OCI A1.Flex Always Free provisionada (137.131.156.249) · Deploy Render link público HTTPS `compliance-assistant-novadata.onrender.com` · `scripts/entrypoint.sh` indexação FAISS automática no container start · Header marca NovaData na Home UI Streamlit · Badge Deploy no topo do README. |
| `v1.0.3` | entrega final checklist Alura ONE | ✅ **entregue 18/08** | README alinhado 100% ao checklist oficial (2 exemplos textuais de perguntas + respostas geradas · seção Evidência de Deploy completa link público + histórico OCI + prints). Bump CHANGELOG `[1.0.3]` · hotfix .gitignore credenciais SSH · Tag semântica final de entrega. |
| **`v1.0.4`** | **🏆 Dual Cloud Deploy (OCI ARM + Render HTTPS)** | ✅ **entregue 19/08** | 🎉 Conserto definitivo rede VCN OCI (criado Internet Gateway + Rota 0.0.0.0/0 IGW na Default Route Table). Docker CE 29 + Compose 5 instalado Oracle Linux 9 aarch64. Build imagem Docker ARM nativo 100% no repositório. Entrypoint FAISS automático de 198 chunks confere 48/48 PASS na VM. Deploy público OCI: **http://137.131.156.249:8501** (BUILD_TAG v1.0.4-oci-arm visível, Header NovaData confirmado). Atualizados 2 Badges clicáveis topo README, 2 Links Públicos, Figura 5 evidência OCI, CHANGELOG [1.0.4]. |
| **`v1.0.5`** | **Hotfix README âncoras + prints reais Fig4/Fig5** | ✅ **entregue 20/08** | Corrigidos links de âncora quebrados Figuras 1–5 (rolam para imagem, não mais topo). Figura 4 agora é print real Healthcheck dual cloud `STATUS_HTTP: 200` (Render + OCI). Figura 5 agora é print real Deploy OCI navegador Windows `137.131.156.249:8501` com BUILD_TAG v1.0.4-oci-arm visível. Atualizada tabela Evidência Deploy com links 🔗 clicáveis, CHANGELOG [1.0.5], pyproject.toml bump v1.0.5. |

### Futuro (pós-Challenge ONE, open source)

- Upload de documentos com processamento assíncrono (Celery / RQ).
- pgvector / Qdrant em produção (FAISS como dev fallback).
- API REST (FastAPI v1) + `ComplianceAssistantClient` Python / TS.
- Autenticação JWT + controle de perfis (Admin, Compliance, Colaborador, Auditor).
- Auditoria com tabela `interactions` (perguntas, respostas, tempo, usuário).
- RAG híbrido (semântico + BM25).
- Observabilidade (logs JSON, métricas Prometheus, tracing OpenTelemetry).
- Avaliação GPT-4o como juiz (Faithfulness premium).

---

## Contexto Educacional

Este projeto foi desenvolvido como desafio prático do programa **Oracle Next Education (ONE)**, combinando os requisitos do Challenge com uma arquitetura de produto real, boas práticas de engenharia e documentação profissional.

O objetivo educacional é demonstrar a aplicação prática de IA Generativa (RAG) em um cenário realista de conformidade corporativa e LGPD, com controle sobre a arquitetura, governança, rastreabilidade e evolução incremental do produto em **6 sprints atômicas** (06/08 → 10/08 de 2026), **5 versões taggeadas**, **48 casos de teste N1 100%**, **14 testes unitários passando** e deploy reproduzível em Oracle Cloud.

---

## Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](./LICENSE).

## Contribuindo

Siga as orientações do [CONTRIBUTING.md](./CONTRIBUTING.md) para submeter alterações, relatar problemas ou propor funcionalidades.
