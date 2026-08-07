# 0001 — Uso do FAISS como banco vetorial no MVP

- Data: 2026-08-05
- Status: Aceito

## Contexto

O Compliance Assistant precisa de um componente para armazenar vetores de embeddings e executar buscas por similaridade de forma eficiente. O MVP roda localmente em ambiente de desenvolvimento e posteriormente será implantado em uma única instância na Oracle Cloud Infrastructure (OCI).

Neste estágio, os requisitos são:
- Indexar até ~100 páginas de documentação.
- Suportar busca por similaridade com embeddings Cohere.
- Ser de fácil instalação, sem dependência de serviço externo.

## Decisão

Adotaremos o **FAISS (Facebook AI Similarity Search)** na CPU como banco vetorial da versão inicial.

O índice será persistido em arquivos locais (`index.faiss` + `chunks.json` + `version.json`) dentro de `data/vector_store/`, e a pasta será ignorada no Git, com exceção dos metadados de versão.

## Justificativa

1. Simplicidade: o FAISS-CPU pode ser instalado via `pip` e não exige servidor, container ou serviço gerenciado.
2. Performance suficiente para a escala do MVP (~dezenas de milhares de chunks).
3. Integração madura no ecossistema Python/IA.
4. Baixa fricção para começar: uma instalação e duas chamadas (build / search) já são suficientes.
5. Custos zero em ambiente local ou de demonstração.

## Consequências

- A busca vetorial fica acoplada ao disco local da instância.
- Para escalar horizontalmente ou compartilhar estado entre múltiplas réplicas, precisaremos migrar para pgvector, Qdrant ou Milvus.
- O índice é regenerado pelo pipeline `scripts/index_documents.py` sempre que a documentação mudar.
- Precisamos de um procedimento de backup caso o índice seja destruído.

## Alternativas Consideradas

- **pgvector (PostgreSQL):** excelente para produção, mas exige instância PG e mais configuração; custo alto para começar.
- **Qdrant / Milvus:** bancos vetoriais maduros, porém trazem complexidade operacional e de deployment (container ou cluster).
- **ChromaDB:** alternativa popular e simples; porém FAISS tem melhor desempenho bruto para buscas puramente vetoriais.

## Referências

- https://github.com/facebookresearch/faiss
- https://python.langchain.com/docs/integrations/vectorstores/faiss/
