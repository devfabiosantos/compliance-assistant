# 0003 — Uso do LangChain como camada de orquestração RAG

- Data: 2026-08-05
- Status: Aceito

## Contexto

O Compliance Assistant é uma solução RAG (Retrieval-Augmented Generation). Seu fluxo envolve carregar documentos, particionar texto em chunks, gerar embeddings, recuperar trechos relevantes e passar contexto para um LLM sintetizar a resposta.

Em vez de implementar cada integração “na mão”, precisamos decidir se usamos um framework de orquestração e, se sim, qual.

## Decisão

Adotaremos o **LangChain** como camada de orquestração. Seu uso estará restrito a:
- Divisão de texto em chunks (`langchain-text-splitters`).
- (Opcional) integrações de loaders genéricos no futuro.
- Abstrações comuns de Chains quando agregarem valor.

Porém, **não vamos expor classes do LangChain diretamente para a aplicação.** Em vez disso, o LangChain será um detalhe interno das camadas de `ingestion/` e `retrieval/`, encapsulado pelas classes de serviço (`IndexService`, `QAService`, `Retriever`, `VectorStore`).

## Justificativa

1. **Produtividade:** `RecursiveCharacterTextSplitter` e loaders já existentes evitam reescrever código padrão.
2. **Ecossistema:** integração fácil com FAISS, Cohere e outros bancos vetoriais quando migrarmos.
3. **Reconhecimento de mercado:** o recrutador reconhece LangChain como stack de referência para RAG em Python.
4. **Baixo acoplamento:** mantendo os detalhes do LangChain nas camadas de implementação, evitamos que a aplicação fique travada no framework.

## Consequências

- Dependência adicionada (`langchain`, `langchain-core`, `langchain-community`, `langchain-text-splitters`).
- Atualizações de versão podem exigir ajustes pontuais (API do LangChain ainda muda).
- Se um dia substituirmos LangChain por LlamaIndex ou código manual, as interfaces centrais (`IndexService`, `QAService`, providers, `VectorStore`) continuam inalteradas.

## Alternativas Consideradas

- **Implementar tudo na mão (sem framework):** mais controle, porém maior esforço inicial e mais risco de bugs triviais.
- **LlamaIndex:** excelente para pipelines RAG complexos, mas com curva de aprendizado e abstrações diferentes do que planejamos inicialmente.

## Referências

- https://python.langchain.com/docs/concepts/
- https://python.langchain.com/docs/modules/data_connection/document_transformers/
