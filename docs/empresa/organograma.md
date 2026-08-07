# Organograma e Estrutura de Responsabilidades

**Empresa:** NovaData Solutions  
**Natureza:** Sociedade Anônima Fechada (S.A.)  
**Sede:** São Paulo / SP  
**Atuação:** Nacional — soluções de gestão empresarial em nuvem, governança, segurança, compliance e IA aplicada  
**Colaboradores (aproximadamente):** 250

**Versão:** 1.2  
**Atualização:** abril de 2026  
**Proprietário do documento:** Diretoria de Gente e Gestão, com apoio da Diretoria Jurídica e do DPO.

---

## 1. Visão Hierárquica

```
                           Conselho de Administração
                                    │
                                    ▼
                          Chief Executive Officer (CEO)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
Diretoria Financeira     Diretoria de Operações       Diretoria Jurídica
(CFO)                    (COO)                       (Diretor Jurídico)
        │                           │                           │
        │                    ┌──────┴───────┐             Comitê de Ética
        │                    │              │             ├── DPO
        │             Diretoria de TI    Diretoria        ├── Compliance
        │             (CTO)            Comercial          ├── Assessoria
        │                │             (CCO)              Jurídica
Controller/          ┌───┴───────┐
Tesouraria           │          │
              Segurança    Engenharia
              da Info.   de Software
              (CISO)     / Arquitetura
                 │
     ┌───────────┼────────────┐
     │           │            │
SOC / Blue   Red Team     Operações
Team / SIEM                de Infraestrutura
                          / SRE
```

---

## 2. Cargos e Responsabilidades Diretas

### 2.1. Chief Executive Officer (CEO)

- Representa a empresa perante o mercado, clientes, parceiros e autoridades.
- Define, com o Conselho e as Diretorias, a estratégia corporativa, de inovação e o roadmap de produtos.
- Aprova políticas de alto impacto (segurança, ética, LGPD) após deliberação do Comitê Executivo.
- É a instância final de recurso em decisões de medidas disciplinares relevantes.

### 2.2. Diretoria Financeira (CFO)

- Responsável pela integridade das demonstrações contábeis e pelo compliance fiscal e trabalhista.
- Aprova orçamentos anuais e investimentos de capital.
- Supervisiona Controladoria, Tesouraria, FP&A e compras estratégicas.
- Supervisiona o cumprimento das regras anticorrupção e de gestão de pagamentos suspeitos, em parceria com o Compliance e a Diretoria Jurídica.

### 2.3. Diretoria de Operações (COO)

- Supervisiona a execução operacional dos produtos e serviços contratados por clientes.
- É responsável por acordos de nível de serviço (SLAs) e por planos de continuidade do negócio.
- Coordena, junto ao CISO e ao DPO, os planos de resposta a incidentes de natureza operacional.

### 2.4. Diretoria Comercial (CCO)

- É responsável por vendas, pré-vendas, sucesso do cliente e relacionamento institucional com contas estratégicas.
- Garante a consistência ética nas negociações, alinhada ao **Código de Ética e Conduta**, Seção 5 (Relacionamento com Clientes, Parceiros e Fornecedores).
- Alinha com Jurídico e DPO cláusulas contratuais de privacidade e segurança.

### 2.5. Diretoria de Tecnologia (CTO)

- Define e executa a arquitetura tecnológica, padrões de engenharia, plataforma de dados e estratégia de IA.
- Garante a evolução sustentável dos softwares da NovaData Solutions, com foco em qualidade e segurança.
- É responsável, em conjunto com o CISO, pela adequada gestão de riscos tecnológicos.

### 2.6. Chief Information Security Officer (CISO)

- É o **executivo responsável pela segurança da informação** corporativa e de produtos.
- Detém a **responsabilidade executiva** pelo gerenciamento de incidentes de segurança cibernética, de acordo com o **Plano de Resposta a Incidentes**.
- Propõe e acompanha o cumprimento da **Política de Segurança da Informação**, da **Política de Controle de Acesso** e da **Política de Uso Aceitável dos Recursos de TI**.
- É, ao lado do DPO, **ponto de contato obrigatório** na ocorrência de incidentes que envolvam dados pessoais.

### 2.7. Diretoria Jurídica (Diretor Jurídico)

- Assessora juridicamente a empresa em contratos, litígios, propriedade intelectual, regulatório e societário.
- Coordena o **Comitê de Ética**, o **Compliance** e a atuação do **DPO**.
- Representa a empresa perante autoridades de controle, quando designado.
- Garante conformidade com a LGPD e demais leis setoriais aplicáveis.

---

## 3. Instâncias de Governança e Papéis Especiais

### 3.1. Comitê de Ética

- Composição mínima: representantes da Diretoria Jurídica, de RH, de TI e do Compliance, além de convidados, sempre em número ímpar.
- Atribuições:
  - interpretar o **Código de Ética e Conduta**;
  - coordenar o **Canal de Denúncias**;
  - apurar denúncias e propor medidas disciplinares;
  - recomendar revisões periódicas do Código.
- Relatórios consolidados são enviados à Diretoria Executiva e, em casos relevantes, ao Conselho de Administração.

### 3.2. DPO — Encarregado pelo Tratamento de Dados Pessoais

- Papel conforme art. 41 da LGPD.
- Responsabilidades principais:
  - receber e orientar solicitações de titulares de dados;
  - orientar colaboradores e fornecedores sobre boas práticas de privacidade;
  - interagir com a ANPD e demais autoridades de proteção de dados;
  - ser acionado em qualquer incidente que envolva dados pessoais;
  - apoiar o Compliance nas revisões da **Política de Privacidade e LGPD**.
- **Em incidentes de segurança com impacto a dados pessoais, o DPO é uma das primeiras autoridades a ser acionada**, simultaneamente ao CISO e ao Diretor Jurídico.

### 3.3. Compliance

- Executa programas de integridade, treinamentos éticos, anticorrupção e LGPD.
- Mantém matrizes de risco e controles de conformidade.
- Acompanha o registro e a evolução das denúncias recebidas pelo Canal de Denúncias.

### 3.4. Diretoria de Gente e Gestão (RH)

- Garante aderência às normas trabalhistas e de relacionamento.
- Participa de apurações de conduta junto ao Comitê de Ética.
- Coordenar admissões, desligamentos, cargos e salários, avaliações e cultura organizacional.

---

## 4. Resumo de Responsabilidades por Tema

Para consulta rápida:

| Tema | Responsável Primário | Co-responsáveis |
| --- | --- | --- |
| Segurança da Informação e incidentes cibernéticos | CISO | CTO, DPO, Diretor Jurídico |
| Proteção de dados pessoais (LGPD) | DPO | Diretor Jurídico, Compliance, CISO |
| Conduta ética e Canal de Denúncias | Comitê de Ética | RH, Diretor Jurídico, Compliance |
| Políticas de acesso corporativo | CISO | CTO, RH |
| Políticas de segurança e backup | CISO / Infraestrutura reporta à CTO | CISO, COO |
| Comunicação com a ANPD em incidentes | DPO | Diretor Jurídico, CISO, CEO |
| Apresentação de resultados de integridade anual | Compliance | CFO, Diretor Jurídico, CEO |
| Treinamentos anual de Ética e LGPD | RH + Compliance | DPO, CISO, Jurídico |
| Gestão de fornecedores e conflitos de interesse | Compliance / Compras | CFO, Diretor Jurídico |
| Assédio, diversidade e inclusão | RH | Comitê de Ética, Jurídico |

---

## 5. Como usar este documento com o Compliance Assistant

Este documento habilita perguntas do tipo:

- "Quem é responsável por incidentes de LGPD na NovaData Solutions?"
- "Qual diretoria cuida do Canal de Denúncias?"
- "O CISO responde para quem?"
- "Quem aprova políticas de alto impacto como Segurança e Ética?"
- "Se houver incidente com dados pessoais, quem deve ser comunicado primeiro?"

Combinado com o **Código de Ética e Conduta**, o RAG pode devolver respostas multi-documento que associam regras de conduta aos responsáveis por sua aplicação.
