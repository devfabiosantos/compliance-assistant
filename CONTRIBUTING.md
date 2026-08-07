# Contribuindo com o Compliance Assistant

Obrigado pelo interesse em contribuir com o Compliance Assistant. Este documento descreve o processo e as diretrizes adotadas pelo projeto.

## Fluxo de desenvolvimento

- O projeto segue o modelo de versionamento semântico (SemVer) para releases.
- Todo desenvolvimento é feito em branches curtas, que são revisadas via Pull Request.
- As branches são nomeadas com o prefixo correspondente ao tipo de alteração:
  - `feat/<descricao>` para novas funcionalidades
  - `fix/<descricao>` para correções de defeitos
  - `docs/<descricao>` para alterações exclusivas em documentação
  - `refactor/<descricao>` para refatorações sem mudança de comportamento
  - `chore/<descricao>` para tarefas de manutenção (dependências, configuração etc.)

## Commits convencionais

Utilizamos Conventional Commits em português ou inglês. Exemplos válidos:

```
feat: implementa pipeline de indexacao de documentos
fix: corrige quebra em chunks com acentos
docs: atualiza README com requisitos do Cohere
refactor: isola provider Cohere em camada propria
chore: atualiza versao do langchain
```

## Criando um Pull Request

1. Abra uma issue descrevendo o problema ou proposta.
2. Crie uma branch a partir de `main`.
3. Implemente a alteração com commits atômicos.
4. Adicione ou atualize testes quando aplicável.
5. Garanta que `pytest` e a validação local passam.
6. Abra o PR e preencha o template, se disponível.

## Padrões de código Python

- Versão alvo: Python 3.12
- Nomenclatura: `snake_case` para arquivos e funções; `PascalCase` para classes.
- Todas as novas camadas devem expor abstrações (interfaces/base) antes de implementações concretas.
- Não dependa de detalhes de framework (LangChain, Cohere) diretamente nas camadas de serviço.

## Relatando problemas

Ao abrir uma issue, descreva:

1. Passos para reproduzir o problema.
2. Comportamento esperado e comportamento observado.
3. Versão do Python, sistema operacional e dependências (pip freeze).
4. Logs ou stacktrace, se houver.

## Dúvidas gerais

Para questões de arquitetura ou uso do produto, abra uma issue com a label `question`.
