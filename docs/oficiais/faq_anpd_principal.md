# FAQ — Perguntas Frequentes da ANPD sobre LGPD
**Autoridade Nacional de Proteção de Dados (ANPD)**
*Compilado atualizado em 01/2026 (versão de referência interna; íntegra oficial disponível em gov.br/anpd)*

---

## 1. Dados pessoais: conceitos básicos

**Q01. O que é dado pessoal segundo a LGPD?**
É toda informação relacionada a uma pessoa natural **identificada** (ex.: nome, CPF, RG, e-mail profissional vinculado ao colaborador) ou **identificável** (ex.: combinação de CEP, data de nascimento e profissão que, isolada ou cruzada, permita identificar uma pessoa natural). Vide art. 5º, I, da LGPD.

**Q02. O que é dado pessoal sensível?**
São dados pessoais que, se revelados, podem colocar a pessoa em risco de discriminação ou dano grave. São classificados como sensíveis, entre outros:
- origem racial ou étnica;
- convicções religiosas;
- opinião política;
- filiação a sindicato ou a organização de caráter religioso, filosófico ou político;
- dados de saúde ou vida sexual;
- dados genéticos ou biométricos, quando vinculados a uma pessoa natural.

Vide art. 5º, II, LGPD.

**Q03. O que é dado anonimizado?**
É dado tratado com técnicas de anonimização adequadas e controladas, de forma que o titular **não possa ser reidentificado** com razoabilidade (inclusive cruzamento com outros bancos de dados). Dados anonimizados **não são dados pessoais** para fins da LGPD — mas dados pseudonomizados continuam sendo dados pessoais.

---

## 2. Princípios e bases legais

**Q04. Quais são os princípios da LGPD?**
São 10, previstos no art. 6º da LGPD: finalidade, adequação, necessidade, livre acesso, qualidade dos dados, transparência, segurança, prevenção, não discriminação, responsabilização e prestação de contas.

**Q05. Quais as hipóteses (bases legais) para tratar dados pessoais?**
Previstas no art. 7º LGPD. As mais usadas em ambiente corporativo são:
- Consentimento (art. 7º, I);
- Cumprimento de obrigação legal ou regulatória (art. 7º, II);
- Execução de contrato (art. 7º, V);
- Exercício regular de direitos em processo (art. 7º, VI);
- Tutela da saúde (art. 7º, VIII);
- Interesse legítimo (art. 7º, X);
- Proteção de crédito (art. 7º, XI).

**Q06. O consentimento pode ser genérico?**
Não. O consentimento deve ser:
- específico por finalidade;
- fornecido de forma destacada (em cláusula própria, não escondido em texto longo);
- passível de revogação a qualquer tempo, de forma facilitada e gratuita;
- comprovado pelo controlador (documento, registro, trilha de auditoria, etc.).

---

## 3. Direitos do titular

**Q07. Quais são os principais direitos do titular na LGPD?**
Entre outros:
1. Confirmação da existência de tratamento (art. 17, I);
2. Acesso aos dados (art. 17, II);
3. Correção de dados incompletos, inexatos ou desatualizados (art. 17, III);
4. Anonimização, bloqueio ou eliminação de dados excessivos ou tratados em desconformidade com a LGPD (art. 17, IV);
5. Portabilidade dos dados a outro fornecedor de serviço ou produto (art. 17, V);
6. Eliminação dos dados pessoais tratados com base no consentimento (art. 17, VI);
7. Informação sobre as entidades públicas e privadas com as quais o controlador realizou uso compartilhado de dados (art. 17, VII);
8. Informação sobre a possibilidade de não fornecer consentimento e sobre as consequências da negativa (art. 17, VIII);
9. Revogação do consentimento (art. 17, IX);
10. Revisão de decisões automatizadas (art. 20).

**Q08. O titular tem direito a portabilidade de dados mesmo quando o contrato já acabou?**
Sim. A portabilidade se aplica sempre que o tratamento tiver sido baseado em consentimento ou em contrato.

---

## 4. Controlador, operador, DPO

**Q09. Quem é o controlador? Quem é o operador?**
**Controlador** é quem decide as regras do tratamento (finalidades, bases, prazos). **Operador** é quem executa o tratamento em nome do controlador (ex.: fornecedor de hospedagem, call center terceirizado). As responsabilidades são complementares, mas o controlador permanece responsável perante titulares e ANPD.

**Q10. O que é DPO / Encarregado? É obrigatório?**
Encarregado é a pessoa indicada pelo controlador e pelo operador como canal de comunicação entre os agentes, os titulares dos dados e a ANPD. Sua obrigatoriedade decorre da natureza e do porte das operações, com base em critérios adicionais a serem fixados pela ANPD. Em ambiente corporativo de médio/grande porte (como a NovaData Solutions), recomenda-se designação formal desde a implantação do programa de governança LGPD.

---

## 5. Segurança e incidentes

**Q11. Quais as medidas de segurança mínimas que a LGPD exige?**
A LGPD não elenca exaustivamente, mas estabelece no art. 37 medidas de segurança, técnicas e administrativas aptas a proteger os dados contra acessos não autorizados, destruição, perda, alteração, comunicação ou difusão. Na prática: controles de acesso (MFA, RBAC), criptografia, plano de resposta a incidentes, gestão de vulnerabilidades, cláusulas contratuais com terceiros e auditoria.

**Q12. Em caso de incidente de segurança com dados pessoais, preciso comunicar a ANPD e os titulares?**
A comunicação à ANPD é obrigatória quando o incidente **puder acarretar risco ou dano relevante aos titulares**. A comunicação deve ocorrer em **prazo razoável**, tipicamente em até **24 a 72 horas úteis** após a ciência do evento, dependendo da complexidade. A decisão de comunicar titulares individualmente depende da análise de gravidade e mitigações possíveis.

---

## 6. Transferência internacional

**Q13. Posso enviar dados pessoais de titulares brasileiros para fora do país?**
Sim, desde que amparada por uma das hipóteses legais de transferência internacional. Exemplos comuns:
- País com grau de proteção adequado (decisão ANPD);
- Cláusulas-padrão aprovadas pela ANPD;
- Regras corporativas globais (BCRs) aprovadas;
- Certificações, códigos de conduta adotados.

**Q14. Posso usar serviços em nuvem hospedados fora do Brasil?**
Sim, desde que as condições da transferência internacional sejam observadas. O controlador permanece responsável. Recomenda-se contrato com SLA, criptografia, territorialidade de dados, e, se possível, escolher região Brasil na nuvem.

---

## 7. Sanções

**Q15. Qual o valor máximo de multa por infração à LGPD?**
A multa simples pode chegar a **2% do faturamento da pessoa jurídica (grupo ou conglomerado) no Brasil no último exercício (excluídos impostos)**, com teto máximo de **R$ 50 milhões por infração**. Outras sanções: bloqueio/eliminação de dados, suspensão de atividades e proibição de exercer tratamento por até 10 anos. Vide art. 48º LGPD.

---
*FAQ de referência interna da NovaData Solutions. Fonte primária: publicações oficiais da ANPD.*
