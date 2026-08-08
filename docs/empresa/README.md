# Documentos da empresa (NovaData Solutions)

Pasta reservada aos documentos corporativos internos da NovaData Solutions. Eles serão a fonte primária para respostas sobre políticas internas, segurança, ética, RH e procedimentos.

## Formato

Os documentos são escritos em **Markdown** e versionados no Git. Se, no futuro, você gerar PDFs a partir deles, os `.pdf` gerados serão ignorados no Git (ver `.gitignore`).

## Documentos esperados (Sprint 1.5 e Sprint 2)

### Sprint 1.5 — Validação do pipeline RAG

Documentos piloto para validar chunking, embeddings, indexação e recuperação.

| Arquivo | Área | Páginas aproximadas | Observação |
| --- | --- | --- | --- |
| `codigo_etica_conduta.md` | Compliance / Jurídico | ~10 | Primeiro documento piloto com cross-references |
| `organograma.md` | Governança | ~2 | Diagrama de responsabilidades; habilita perguntas multi-documento |

### Sprint 2 — Base documental completa

Estes documentos compõem a base corporativa da NovaData Solutions, com cross-references consistentes entre si e com o Código de Ética e o Organograma:

| Arquivo | Área | Versão | Aprovação | Próxima revisão |
| --- | --- | --- | --- | --- |
| `politica_seguranca_informacao.md` | TI / Segurança | 1.0 | CISO / Diretoria | 01/2027 |
| `politica_privacidade_lgpd.md` | Jurídico / Compliance | 1.0 | Diretor Jurídico / DPO | 01/2027 |
| `manual_colaborador.md` | RH | 1.0 | Diretor de Pessoas | 01/2027 |
| `politica_controle_acesso.md` | TI | 1.0 | CTO / CISO | 01/2027 |
| `plano_resposta_incidentes.md` | Segurança / Operações | 1.0 | CISO / CTO / DPO | 01/2027 |
| `politica_backup_retenção.md` | Infraestrutura | 1.0 | CTO / Diretoria | 01/2027 |
| `politica_uso_aceitavel.md` | Governança / TI | 1.0 | CISO / Compliance | 01/2027 |

Total alvo (Sprint 1.5 + Sprint 2): **8 documentos corporativos + organograma** (~80–90 páginas de conteúdo denso, conectado e com rastreabilidade de regras).

## Diretrizes de escrita

- Adote tom profissional, como em um documento corporativo real.
- Prefira seções numeradas (`1.`, `1.1.`, `4.2.` etc.) — o splitter e o usuário aproveitam a estrutura.
- Sempre que citar uma regra, justifique-a: *"Conforme a Política de Controle de Acessos da NovaData Solutions..."*.
- **Faça os documentos "conversarem"**: cruze referências sempre que possível. Ex.: no Código de Ética, cite "Consulte também a Política de Segurança da Informação (Seção 4.2)". Na Política de Segurança, retorne ao Código de Ética.
- Evite texto genérico. Descreva como a NovaData Solutions efetivamente opera.
- Não inclua dados pessoais reais de colaboradores. Use exemplos fictícios (CPF 000.000.000-00, e-mails @novadatatech.br fictícios etc.).
- Ao mencionar papéis, use nomes consistentes com `organograma.md` (DPO, CISO, CTO, Diretor Jurídico etc.).

## Como gerar PDF (futuro)

```bash
# Exemplo com pandoc (instalar pandoc + latex)
pandoc docs/empresa/politica_seguranca.md -o docs/empresa/politica_seguranca.pdf \
    --template=eisvogel --pdf-engine=xelatex -V lang=pt-BR
```
