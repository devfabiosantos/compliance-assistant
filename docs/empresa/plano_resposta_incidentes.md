# Plano de Resposta a Incidentes de Segurança da Informação e LGPD — NovaData Solutions
Documento nº PRI-ND-2026-001 | Versão 1.0
Aprovação: CISO + DPO + CTO + Diretoria Executiva | Data: 01/08/2026 | Próxima revisão: 01/2027

---

## 1. Objetivo e âmbito

O presente Plano de Resposta a Incidentes (PRI) define papéis, processos, fluxos e responsabilidades para a detecção, classificação, contenção, erradicação, recuperação e comunicação de incidentes de segurança da informação e incidentes com dados pessoais, visando:
1. Minimizar o impacto para a NovaData Solutions, seus colaboradores, clientes e parceiros;
2. Cumprir as obrigações legais da LGPD (art. 48), da Lei Geral de Informática e das normas aplicáveis;
3. Garantir comunicação tempestiva à ANPD e aos titulares de dados, quando aplicável, segundo critérios da ANPD;
4. Facilitar a análise de causa raiz e as ações de melhoria contínua;
5. Alinhar a resposta aos incidentes com a **Política de Segurança**, a **Política de Controle de Acesso**, a **Política de Privacidade e LGPD** e a **Política de Backup e Retenção**.

O PRI aplica-se a todos os ativos, instalações físicas, sistemas, aplicações, nuvem, dados e colaboradores da NovaData, inclusive em home office. Prestadores de serviços e parceiros observam, em seus contratos, obrigações de notificar a NovaData em até 24 horas corridas sobre incidentes que afetem ativos de propriedade ou sob responsabilidade da empresa.

---

## 2. Definições, papéis e responsabilidades

### 2.1. Definições operacionais
- **Evento de segurança:** ocorrência observável relevante para a segurança de ativos;
- **Incidente:** qualquer evento adverso que comprometa ou suspeite de comprometer a confidencialidade, integridade ou disponibilidade de um ativo;
- **Incidente de segurança (LGPD):** incidente com dados pessoais que acarrete risco ou dano relevante aos titulares (art. 48 LGPD);
- **Vazamento:** acesso, cópia, transmissão ou divulgação não autorizada de informação;
- **Ransomware:** ataque por criptoextorsão que compromete disponibilidade de ativos;
- **Falso positivo:** alerta analisado e descartado como incidente real.

### 2.2. Comitê Gestor de Incidentes (CGI)
São membros permanentes do CGI:
| Papel (Organograma) | Responsabilidade no PRI |
| --- | --- |
| **CISO** | Executivo responsável pelo PRI; aciona os demais membros; valida decisões de contenção; comunica à Diretoria |
| **DPO** | Avalia impacto LGPD; coordena comunicação à ANPD e titulares; articula com jurídico |
| **CTO** | Responsável pela recuperação de ambientes, validação de backup, mitigação de vulnerabilidades |
| **Diretor Jurídico** | Avalia riscos legais, contratuais e processuais; aprova comunicações oficiais |
| **CCO / Diretor de Comunicação** | Comunicação externa com clientes, mercado e imprensa; comunicação interna aos colaboradores |
| **Líder do SOC** | Conduz operacionalmente a resposta, a investigação e a documentação forense |
| **Representante do RH** | Suporte a envolvimento de colaboradores, medidas disciplinares e comunicação interna |

Sempre que relevante, integram o CGI os gestores das áreas envolvidas, o time de arquitetura e os proprietários dos ativos afetados.

### 2.3. Equipe de Resposta a Incidentes (CSIRT)
A CSIRT é operacionalmente liderada pelo CISO, com apoio direto do SOC 24x7 e do time de Segurança, Infraestrutura e Plataformas. Prestadores de segurança contratados e apoio forense externo são acionados em incidentes de alta gravidade.

---

## 3. Linhas do tempo, severidade e classificação

### 3.1. Níveis de severidade (S0–S4)
| Nível | Rótulo | Tempo de resposta SLA | Exemplos típicos |
| --- | --- | --- | --- |
| S0 | Crítico | Resposta em até 1h | Ransomware em produção, vazamento massivo de dados de clientes, ataque ativo com exfiltração, comprometimento de credenciais administrativas globais |
| S1 | Alto | Resposta em até 2h | Acesso não autorizado a base de clientes com dados pessoais, sequestro de conta administrativa, ataque DDoS grave com indisponibilidade de SaaS |
| S2 | Médio | Resposta em até 8h úteis | Comprometimento de uma estação de trabalho sem propagação, phishing exitoso que exfiltrasse dados de uma área restrita, vulnerabilidade explorável sem evidência de exploração em ativo crítico |
| S3 | Baixo | Resposta em até 24h úteis | Evento isolado sem impacto, phishing sem clique, compartilhamento acidental de arquivo com cancelamento imediato, falha sem impacto em produção |
| S4 | Informativo | Resposta em até 3 dias úteis | Evento de segurança sem impacto real mas com potencial de melhoria (falso positivo com alta taxa, ruído de alertas etc.) |

### 3.2. Prazo de comunicação à ANPD e aos titulares
Conforme critérios da ANPD e da LGPD:
- **S0 e S1 com envolvimento de dados pessoais sensíveis ou massa crítica de titulares:** comunicação preliminar à ANPD em até **24 horas úteis** após a ciência do incidente;
- **Outros níveis S2 em diante, com potencial de risco ou dano relevante:** comunicação em até **72 horas úteis**, dependendo da análise do DPO em conjunto com o Diretor Jurídico;
- Comunicação individual a titulares é decidida em conjunto pelo CGI, considerando gravidade, probabilidade do dano e mitigações disponíveis.

---

## 4. Ciclo de resposta ao incidente

O ciclo segue 7 fases, podendo ser executadas de forma concorrente quando necessário:

### 4.1. Fase 1 — Preparação
Controles permanentes:
- SOC 24x7 com SIEM, EDR/XDR, SOAR e feeds de inteligência de ameaças;
- Simulações (table-top) semestrais de incidentes críticos (Ransomware, vazamento LGPD);
- Treinamentos obrigatórios de conscientização e phishing;
- Inventário, mapas de fluxo de dados e ROT atualizados;
- Plano de continuidade de negócios e plano de backup atualizados e testados trimestralmente.

### 4.2. Fase 2 — Detecção e relato
Qualquer colaborador, prestador ou terceiro deve comunicar suspeita ou evidência de incidente por meio dos canais oficiais:
- E-mail: incidentes@novadatatech.br (fictício)
- Aplicativo interno do SOC / portal de segurança
- Em emergência, ligação direta para o CISO e DPO

### 4.3. Fase 3 — Análise inicial e classificação
O SOC analisa, classifica em S0–S4 e confere se o evento é incidente real. Caso positivo, aciona o CGI de acordo com o nível. Toda evidência inicial é preservada para análise forense.

### 4.4. Fase 4 — Contenção
Ações rápidas para impedir propagação e ampliação do impacto:
- isolamento de hosts, contas e redes suspeitas;
- revogação imediata de credenciais potencialmente comprometidas;
- bloqueios em perímetro (firewall/WAF/IDS);
- habilitação de medidas de contingência e BCDR, se necessário.

### 4.5. Fase 5 — Erradicação
Remoção da causa raiz: eliminação de malware, patching de vulnerabilidades, endurecimento de controles, desativação de backdoors, limpeza de artefatos maliciosos.

### 4.6. Fase 6 — Recuperação e retorno à normalidade
Restauração dos sistemas e dados a partir de backups validados, em ordem de criticidade definida no BCDR. Testes de integridade e segurança são executados antes de cada sistema retornar à produção. Prazos de recuperação (RTO/RPO) seguem o Plano de Backup e Retenção.

### 4.7. Fase 7 — Pós-incidente, análise e lições aprendidas
- **Análise de Causa Raiz (RCA):** documentada e apresentada em até 10 dias úteis após o fechamento do incidente;
- **Plano de Ação Corretiva (PAC):** com responsáveis e prazos;
- **Relatório Executivo:** à Diretoria;
- **Registro de ocorrência e documentação de notificações:** arquivados por 10 anos, com acesso restrito ao CGI, jurídico e auditorias;
- **Atualização de políticas e controles:** com foco em evitar reincidência.

---

## 5. Comunicação com órgãos, titulares e mercado

- **Comunicação à ANPD:** de responsabilidade do DPO, com validado jurídico; segue prazos da LGPD.
- **Comunicação a titulares:** decidida pelo CGI, considerando gravidade, risco e requisitos legais.
- **Comunicação a clientes e mercado:** conduzida pelo CCO/CEO, com apoio jurídico e CISO, evitando detalhes técnicos sensíveis.
- **Confidencialidade preliminar:** Nenhum colaborador, à exceção do CGI, pode pronunciar-se publicamente sobre incidentes em andamento. Declarações públicas só são autorizadas após validação do comitê.

---

## 6. Evidências, cadeia de custódia e preservação

A coleta e preservação de evidências seguem rigorosa cadeia de custódia, com registro de horários, responsáveis e ações realizadas. Equipes de resposta não realizam alterações em artefatos forenses críticos sem o devido registro.

---

## 7. Simulações, testes e exercícios

- **Table-top (simulação):** pelo menos 1 semestral com cenários distintos (ex.: ransomware em ERP, vazamento de base de clientes, ataque de credencial phishing em RH);
- **Simulações de Ransomware:** validação do restore de backup e dos SLAs de recuperação em pelo menos 1x por trimestre;
- **Red Team interno/externo:** pelo menos 1 exercício anual para validar PRI, SOC e equipes.

---

## 8. Disposições finais

A não observância a este PRI por colaboradores ou prestadores sujeita aos envolvidos às medidas do Código de Ética e, em caso de conduta dolosa ou grave culposa, às medidas legais cabíveis. O CGI revisa e atualiza o PRI anualmente ou após qualquer incidente de alto impacto.

---

Cross-references: **Política de Segurança**, **Política de Controle de Acesso**, **Política de Privacidade e LGPD**, **Política de Backup e Retenção**, **Código de Ética**.
