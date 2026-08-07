# Compliance Assistant

> Enterprise AI Assistant for LGPD Compliance and Corporate Knowledge Retrieval

Produto corporativo da **NovaData Solutions** que capacita colaboradores a consultar políticas internas, normas de segurança e documentos oficiais da LGPD por meio de linguagem natural, com rastreabilidade completa sobre a origem de cada resposta.

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

## Arquitetura

```
 Documentos                           (fontes oficiais + políticas internas)
        │
        ▼
  Carregamento (PyPDF / Markdown)
        │
        ▼
  Normalização & Chunking             (tamanho controlado, com sobreposição)
        │
        ▼
  Embeddings (Cohere)                 (embed-multilingual-v3.0)
        │
        ▼
  FAISS Vector Store                  (índice local com versionamento)
        │
        ▼
  Retriever Semântico                 (top-k + score threshold)
        │
        ▼
  LLM Cohere (Command-R)             (RAG com prompt de auditoria)
        │
        ▼
  Resposta + Fontes + Páginas        (rastreabilidade completa)
```

## Stack Tecnológico

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.12 |
| Orquestração RAG | LangChain |
| Provedor de IA | Cohere (Chat + Embeddings) |
| Banco Vetorial | FAISS |
| Carregamento PDF | PyPDF |
| Interface MVP | CLI (Click) |
| Interface Web | Streamlit (Sprint posterior) |
| Deploy | Oracle Cloud Infrastructure (OCI) |
| Versionamento | Git + Conventional Commits |

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
├── evaluation/                  # casos de teste do RAG
├── scripts/
│   ├── index_documents.py       # pipeline de ingestão
│   └── chat.py                  # CLI de consulta
├── src/
│   ├── app/                     # entrypoints / wiring
│   ├── cli/                     # comandos Click
│   ├── config/                  # carregamento de settings
│   ├── domain/                  # modelos centrais (Question, Answer, ...)
│   ├── ingestion/               # load, split, normalização
│   ├── providers/               # abstração LLM/embeddings
│   │   ├── base.py
│   │   ├── cohere_chat.py
│   │   └── cohere_embeddings.py
│   ├── retrieval/               # FAISS / retrievers
│   ├── services/                # faixas de uso (QAService, IndexService)
│   └── utils/                   # logging, formatação, textos
├── tests/
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

## Como executar localmente

### 1. Requisitos

- Python 3.12+
- Chave de API da Cohere (`COHERE_API_KEY`)

### 2. Instalação

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell
# source .venv/bin/activate   # Linux/Mac

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 3. Configuração

```bash
cp .env.example .env
# Edite .env e preencha COHERE_API_KEY
```

### 4. Indexar os documentos

```bash
python scripts/index_documents.py
```

### 5. Consultar o assistente (CLI)

```bash
python scripts/chat.py "O que caracteriza um dado pessoal sensível?"
```

---

## Avaliação da qualidade do RAG

A qualidade do sistema é medida em **níveis** para evitar retrabalho: primeiro valida-se a recuperação semântica, só depois a qualidade da resposta.

### Nível 1 — Retrieval (documento / seção / palavras-chave)

O runner `evaluation/evaluate_retrieval.py` executa automaticamente os casos definidos em `evaluation/questions.json` e gera relatório em texto + JSON.

**Como rodar:**

```bash
# 1) Garanta que o indice existe
python scripts/index_documents.py

# 2) Executa avaliacao Nivel 1 com top_k do .env
python evaluation/evaluate_retrieval.py

# 3) Sobrescrevendo k para comparar impactos
python evaluation/evaluate_retrieval.py --k 3

# 4) Falhar o processo se houver casos reprovados (ideal para CI)
python evaluation/evaluate_retrieval.py --fail-on-zero
```

O relatório JSON é salvo em `evaluation/reports/retrieval_report.json` e contém:
- acurácia de **documento correto**
- acurácia de **seção correta** (quando aplicável)
- recall de **palavras-chave** esperadas
- top-k chunks retornados por caso, com score, página e snippet

### Nível 2 — Qualidade da resposta (Sprint posterior)

Depois do retrieval estável, avalia-se:
- groundedness / faithfulness (resposta fiel aos chunks)
- relevância semântica
- completude vs. esperado

---

## Limitações e Uso Responsável

- O **Compliance Assistant não substitui parecer jurídico** ou decisão de área competente.
- Respostas são geradas exclusivamente a partir dos documentos indexados. Informação ausente na base resultará em respostas incompletas ou declaração de não conhecimento.
- Não envie dados pessoais reais (CPF, e-mails, números de documentos) ao usar ambientes públicos ou de demonstração.
- Índices locais gerados em `data/vector_store/` são artefatos transitórios e não devem ser versionados.

---

## Roadmap

| Versão | Sprint | Conteúdo |
| --- | --- | --- |
| `v0.1.0` | 1 | Arquitetura, estrutura do repositório e documentação inicial |
| `v0.2.0` | 2 | Base documental da NovaData Solutions (MDs corporativos) |
| `v0.3.0` | 3 | Pipeline de ingestão completo e indexação FAISS |
| `v0.4.0` | 4 | Motor de perguntas e respostas com rastreabilidade |
| `v0.5.0` | 5 | Interface Web (Streamlit multipágina com site institucional) |
| `v0.6.0` | 6 | Testes de qualidade e validação do RAG |
| `v0.9.0` | 7 | Deploy na Oracle Cloud Infrastructure |
| `v1.0.0` | 8 | README final, apresentação e ajustes de lançamento |

Evoluções futuras pós `v1.0.0`:

- Upload de documentos com processamento assíncrono
- pgvector / Qdrant como banco vetorial em produção
- API REST (FastAPI) + frontend React
- Autenticação JWT e controle de perfis
- Auditoria com histórico completo de perguntas e respostas
- RAG híbrido (semântico + palavras-chave)
- Avaliação automática (faithfulness, groundedness, relevância)
- Observabilidade (logs estruturados, métricas, tracing)

---

## Contexto Educacional

Este projeto foi desenvolvido como desafio prático do programa **Oracle Next Education (ONE)**, combinando os requisitos do Challenge com uma arquitetura de produto real, boas práticas de engenharia e documentação profissional.

O objetivo educacional é demonstrar a aplicação prática de IA Generativa (RAG) em um cenário realista de conformidade corporativa e LGPD, com controle sobre a arquitetura, governança, rastreabilidade e evolução incremental do produto.

---

## Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](./LICENSE).

## Contribuindo

Siga as orientações do [CONTRIBUTING.md](./CONTRIBUTING.md) para submeter alterações, relatar problemas ou propor funcionalidades.
