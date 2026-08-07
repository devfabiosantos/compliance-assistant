# Avaliação do RAG

Este diretório contém casos de teste usados para validar a qualidade do **retrieval** e, no futuro, a qualidade das respostas.

## Níveis de avaliação

### Nível 1 — Recuperação correta da fonte

- Verifica se o sistema recuperou o documento certo.
- Verifica se a página está entre as esperadas, quando conhecida.
- Métricas futuras: `accuracy@k`, `hit_rate`, `MRR`.

Arquivo: `questions.json`.

### Nível 2 — Qualidade da resposta (Sprint posterior)

- Faithfulness (resposta fundamentada nos chunks recuperados).
- Relevância (resposta atende diretamente à pergunta).
- Groundedness (tudo na resposta tem origem nos documentos).

## Como usar

Na Sprint 6 será implementado um runner em `tests/evaluation_test.py` que executa cada questão contra o índice e compara o documento esperado com os recuperados.
