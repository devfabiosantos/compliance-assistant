# Guia de Aplicação da LGPD — Metodos e Boas Práticas
## Publicação ANPD (referência técnica)
Autoridade Nacional de Proteção de Dados (ANPD)
**Edição de referência — Stub com seções reais da ANPD**
Publicação atualizada em 01/2026. Para íntegra, vide publicação oficial no site da ANPD (gov.br/anpd).

---

## 1. Objetivo e abrangência

Este Guia tem como objetivo orientar agentes de tratamento (controladores e operadores), encarregados (DPOs), titulares de dados pessoais e autoridades, sobre os métodos de aplicação da Lei nº 13.709/2018 (LGPD) e as práticas recomendadas em conformidade com a disciplina da ANPD.

**Público-alvo:**
- Controladores de dados pessoais em ambiente corporativo (público e privado);
- Encarregados pela proteção de dados (DPO/Especialista LGPD);
- Equipes jurídicas, de compliance, segurança da informação e governança;
- Operadores de tratamento (prestadores de serviço contratados por controladores);
- Gestores de produtos digitais e engenheiros de software responsáveis por funcionalidades de tratamento de dados.

---

## 2. Conceitos-chave reforçados pela ANPD

### 2.1. Papéis no ecossistema LGPD

| Papel | Definição reforçada |
| --- | --- |
| Controlador | Decide *o quê*, *quando* e *para quê* tratar dados. Responsável pelas decisões de tratamento, prestação de contas e relação com a ANPD. |
| Operador | Executa as operações de tratamento em nome do controlador, seguindo instruções formais e contrato de prestação de serviços com cláusulas LGPD. |
| Encarregado / DPO | Presta contas internamente e ao titular; ligação com a ANPD. Recomenda-se formação técnica, independência funcional e relatório anual de atividade. |

### 2.2. Princípios essenciais para implementação prática

A ANPD recomenda adotar um framework de governança em LGPD que garanta, no mínimo, os dez princípios do art. 6º da LGPD. Na prática, o controlador deve demonstrar:

1. **Finalidade clara:** qualquer tratamento com finalidade genérica ("melhorar produtos") é considerado inadequado sem detalhamento.
2. **Necessidade e minimização:** tratar apenas o volume de dados estritamente necessário para a finalidade declarada.
3. **Livre acesso e transparência:** política de privacidade em linguagem clara, acessível e em português.
4. **Qualidade e atualização:** rotina de higienização (dados incorretos, desatualizados ou excessivos devem ser eliminados).
5. **Segurança técnica e organizacional:** controles lógicos (RBAC, MFA, criptografia), físicos e administrativos.
6. **Prevenção e resposta a incidentes:** plano documentado com papéis, prazos e comunicação a titulares e ANPD.

---

## 3. Governança de dados pessoais

### 3.1. Inventário de dados e mapeamento de fluxos

A ANPD recomenda fortemente que os controladores mantenham um **Inventário de Ativos de Dados Pessoais (IADP)** contendo:

- Finalidades de tratamento;
- Categorias de titulares (clientes, colaboradores, prestadores, candidatos a emprego);
- Categorias de dados (dados cadastrais, financeiros, de saúde, biométricos, de localização, logs);
- Bases legais invocadas (art. 7º LGPD);
- Fluxos internos e transferências internacionais;
- Medidas de segurança aplicadas;
- Prazos de retenção e critérios de eliminação;
- Responsáveis internos e terceiros envolvidos.

### 3.2. Registro de Operações de Tratamento (ROT)

O Registro de Operações de Tratamento é o documento que demonstra, em detalhe, cada atividade de tratamento realizada. A ANPD recomenda que o ROT contenha:

1. Identificação do controlador;
2. Finalidades da operação;
3. Descrição das categorias de titulares e de dados;
4. Categorias de destinatários (incluindo operadores e subcontratados);
5. Prazo de retenção aplicável e critérios de eliminação;
6. Medidas técnicas de segurança e de governança adotadas;
7. Avaliação de impacto à proteção de dados pessoais (AIPD), quando aplicável;
8. Transferências internacionais realizadas e respectivos mecanismos de salvaguarda.

---

## 4. Avaliação de Impacto à Proteção de Dados (AIPD)

A ANPD estabelece que o controlador deve realizar **AIPD** sempre que o tratamento:
- envolver **dados pessoais sensíveis** em larga escala;
- ocorrer em **novas tecnologias** (ex.: IA generativa, biometria, perfilamento automatizado);
- resultar em **risco elevado** aos direitos e liberdades do titular (ex.: decisões automatizadas que produzem efeitos jurídicos);
- envolver **crianças ou adolescentes** sem base legal robusta.

### 4.1. Etapas mínimas da AIPD

1. Descrição do contexto e do cenário de tratamento;
2. Mapeamento de fluxos de dados (entrada, processamento, saída, armazenamento, exclusão);
3. Identificação e classificação de riscos;
4. Medidas de mitigação e sua matriz de risco-residual;
5. Plano de remediação e validação pela alta gestão;
6. Aprovação final pelo DPO e pela Diretoria.

---

## 5. Segurança de dados pessoais

### 5.1. Controles recomendados pela ANPD

Os controles mínimos recomendados são:

| Camada | Medidas |
| --- | --- |
| Autenticação e controle de acesso | MFA obrigatório para contas administrativas; RBAC (least privilege); políticas de senha robustas; rotina de revogação de acessos. |
| Criptografia | Criptografia em repouso (AES-256) e em trânsito (TLS 1.2+); gestão de chaves segura; assinatura digital onde aplicável. |
| Detecção e resposta a incidentes | SOC 24x7; plano de resposta a incidentes com papéis, classificação, matriz de severidade; testes periódicos; registro centralizado. |
| Governança de software | SBOM, análise de vulnerabilidades, SAST/DAST, patching em SLA rigoroso. |
| Terceiros | Due diligence; contrato com cláusulas LGPD; auditorias; cláusulas de transferência internacional. |

### 5.2. Gestão de riscos

A ANPD recomenda a aplicação de ISO/IEC 27001, 27005, 27701 e a metodologia NIST SP 800-30 para gestão de riscos corporativos.

---

## 6. Resposta a incidentes de segurança (com LGPD)

A comunicação à ANPD e, eventualmente, aos titulares, deve ser avaliada com base em critérios como:
- Natureza, categoria, volume e sensibilidade dos dados pessoais afetados;
- Probabilidade de materialização do risco e gravidade do dano aos titulares;
- Existência de medidas de proteção pós-incidente;
- Facilidade para identificar os titulares afetados e comunicá-los individualmente.

**Prazos de comunicação à ANPD:** A ANPD recomenda a comunicação em até **24 a 72 horas úteis** após a ciência do incidente, dependendo da gravidade. Plano de Resposta a Incidentes documentado é obrigatório.

---

## 7. Perguntas frequentes no Guia ANPD

1. **Quem deve ter DPO/Encarregado?**
   Todo controlador que exerça atividade econômica, e sempre que a operação de tratamento seja de grande porte ou risco elevado. A ANPD pode, adicionalmente, exigir DPO por normativa específica.

2. **Transferências internacionais:** como adequar?
   Através de cláusulas-padrão, normas corporativas globais (BCRs), certificados, códigos de conduta ou decisão de adequação da ANPD.

3. **É permitido usar dados de clientes para marketing após o fim do contrato?**
   Apenas se houver base legal (consentimento específico e destacado ou interesse legítimo com mitigação de riscos).

4. **Os dados devem ser eliminados quando o titular pedir?**
   Em regra, sim (direito de exclusão, art. 17 LGPD). Existem exceções expressas em lei: cumprimento de obrigação legal, pesquisa, exercício regular de direito em processo etc.

---
*Referência: Guia da ANPD — Metodologia de aplicação prática da LGPD. Documento de referência interna da NovaData Solutions.*
