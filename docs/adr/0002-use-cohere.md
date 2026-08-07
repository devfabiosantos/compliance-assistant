# 0002 — Uso do Cohere como provedor de LLM e Embeddings

- Data: 2026-08-05
- Status: Aceito

## Contexto

O Compliance Assistant depende de dois serviços de IA:
1. **Modelo de chat** para sintetizar respostas a partir de trechos recuperados.
2. **Modelo de embeddings** para indexar documentos e transformar perguntas em vetores para busca semântica.

O projeto de portfólio precisa:
- Suportar português do Brasil de forma robusta.
- Custar pouco ou nada em ambiente de demonstração.
- Ser simples de integrar via SDK oficial.

## Decisão

Adotaremos a **plataforma Cohere** para ambos os papéis:
- **Chat:** modelo `command-r` ou variante disponível em conta free-tier.
- **Embeddings:** modelo `embed-multilingual-v3.0` (suporta múltiplos idiomas, incluindo PT-BR).

A comunicação com Cohere será confinada à camada `src/providers/`, por trás das interfaces abstratas `ChatProvider` e `EmbeddingProvider`.

## Justificativa

1. **Suporte a PT-BR:** o `embed-multilingual-v3.0` é treinado para vários idiomas, reduzindo perda de qualidade em textos jurídicos/corporativos em português.
2. **Fácil integração:** SDK Python oficial (`cohere`) bem documentado.
3. **Free-tier disponível:** permite executar o MVP sem custo inicial.
4. **RAG nativo:** o Cohere já oferece recursos úteis para chat com contexto e documentos.
5. **Testabilidade:** manter os providers por trás de interfaces facilita trocar para OpenAI, Anthropic, Groq ou OCI Generative AI no futuro.

## Consequências

- Toda resposta e todo embedding passam por chamadas de rede para a API da Cohere.
- Precisamos gerenciar chaves de API com segurança (`.env` e não commitados no Git).
- Limites de cota do free-tier podem requerer cache ou batch menor durante indexação.
- A troca futura de provedor exige apenas uma nova classe em `src/providers/` sem afetar serviços e camadas superiores.

## Alternativas Consideradas

- **Google Gemini:** boa qualidade, mas o free-tier do projeto se esgotou.
- **OpenAI GPT + text-embedding-3:** muito maduro, porém sem free-tier generoso no momento da avaliação.
- **Modelos locais (Ollama):** ideal para privacidade, porém requer recursos de CPU/RAM/GPU maiores do que uma instância pequena da OCI oferece confortavelmente.
- **OCI Generative AI:** opção de deploy final, mas complica a rodagem local no MVP.

## Referências

- https://docs.cohere.com/reference/chat
- https://docs.cohere.com/reference/embed
