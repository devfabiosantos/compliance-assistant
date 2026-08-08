# Política de Backup e Retenção de Dados — NovaData Solutions
Documento nº PBR-ND-2026-001 | Versão 1.0
Aprovação: CTO + CISO + Diretoria Executiva | Data: 01/08/2026 | Próxima revisão: 01/2027

---

## 1. Objetivo

Estabelecer diretrizes, arquitetura e responsabilidades para a realização de backups, restaurações e retenção de dados e ativos de informação da NovaData Solutions, visando garantir a disponibilidade, integridade e confidencialidade em conformidade com a **Política de Segurança da Informação**, o **Plano de Resposta a Incidentes**, a **Política de Privacidade e LGPD**, a legislação aplicável (LGPD, normas fiscais, trabalhistas e contábeis) e os SLAs com clientes.

---

## 2. Princípios

1. **3-2-1-1-0 como padrão:** 3 cópias, em 2 mídias distintas, 1 cópia off-site, 1 cópia imutável (ou air-gapped, quando aplicável) e 0 erros em restaurações testadas.
2. **Criptografia em repouso e trânsito:** sempre, usando algoritmos e tamanhos de chave aprovados (AES-256 em repouso, TLS 1.2+ em trânsito).
3. **Regra do menor privilégio:** equipe mínima com acesso a console e restauração. Uso de MFA e trilhas de auditoria imutáveis.
4. **Testes de restauração periódicos e documentados.**
5. **Retenção mínima obrigatória por categoria de dado, conforme legislação.**
6. **Eliminação segura ao término da retenção.**
7. **Backup imutável e protegido contra ransomware (WORM/object lock, quando aplicável).**

---

## 3. Arquitetura de backup

### 3.1. Camadas de backup (exemplos)
| Camada | Mídia / destino | Frequência | Retenção padrão | Observação |
| --- | --- | --- | --- | --- |
| **Tier 0 — Snapshots locais (produção)** | Storage local / snapshots em nuvem | Incremental a cada 4h; full diário | Snapshots curtos: até 14 dias | Rápida recuperação operacional |
| **Tier 1 — Backup diário (nuvem)** | Object storage em região primária | Diário (full semanal + incremental diário) | 90 dias | Recuperação operacional e análises |
| **Tier 2 — Off-site e/ou imutável** | Object storage em região secundária + object lock imutável | 1x por semana (full) + logs diários | 12 meses | Resiliência geográfica e proteção antiransomware |
| **Tier 3 — Retenção regulatória** | Arquivamento imutável / fria | Mensal ou conforme evento | Ver matriz de retenção (Seção 6) | Obrigações legais e LGPD |

### 3.2. RTO e RPO alvo

| Categoria de ativo | RTO alvo | RPO alvo |
| --- | --- | --- |
| Sistemas SaaS críticos, faturamento, autenticação, bases de dados de clientes | ≤ 4h | ≤ 1h |
| Sistemas administrativos (RH, finanças, ERP interno) | ≤ 8h | ≤ 4h |
| Sistemas internos de suporte, wikis, documentação | ≤ 24h | ≤ 24h |
| Ambientes de homologação/dev | ≤ 48h | ≤ 24h |

---

## 4. Escopo do backup

Entram no escopo:
1. Bases de dados, schemas, logs transacionais e arquivos de auditoria;
2. Repositórios de arquivos, compartilhamentos, documentação corporativa;
3. VMs, containers (imagens), configurações de infraestrutura como código, chaves criptográficas de backups;
4. Logs de segurança, eventos de rede e auditoria;
5. Configurações de rede, firewall, IAM/SSO;
6. Dados de colaboradores e clientes sob obrigação de retenção legal.

Não entram no escopo:
- Dados temporários, caches, builds descartáveis de pipeline;
- Cópias locais em workstations de colaboradores (estas seguem política de endpoint e DLP).

---

## 5. Responsabilidades

| Papel | Responsabilidade |
| --- | --- |
| **CTO** | Aprova arquitetura e investimentos; valida prazos e BCDR; |
| **CISO** | Garante segurança, criptografia, acesso least privilege, trilhas, imutabilidade e antiransomware; |
| **Líder de Infra / CloudOps** | Operacionaliza a política, agenda jobs, monitora e executa testes periódicos; |
| **DPO / Jurídico** | Valida prazos de retenção e eliminação em conformidade com LGPD e leis específicas; |
| **Gestores das áreas** | Validação das categorias de dados e prazos aplicáveis à sua área; |
| **Auditoria interna/externa** | Confere cumprimento e amostragens de teste. |

---

## 6. Matriz mínima de retenção (exemplos, por categoria)

| Categoria de dado | Prazo mínimo de retenção | Base legal / razão |
| --- | --- | --- |
| Documentos fiscais e contábeis | 5 anos + adicional prescricional | Lei do Imposto de Renda, CPC, Código Tributário |
| Documentos trabalhistas e de pessoal | Até 30 anos após desligamento | CLT, FGTS, previdência |
| Contratos com clientes e fornecedores | Duração do contrato + prazo prescricional aplicável (até 10 anos, em regra) | Código Civil e obrigações contratuais |
| Dados de marketing baseados em consentimento | Até revogação + inatividade de 24 meses | LGPD art. 7º, I, e transparência com titulares |
| Currículos de não selecionados | 2 anos, salvo banco de talentos com manifestação explícita | LGPD, minimização |
| Logs de segurança e de acesso a dados pessoais sensíveis | 24 meses | Política de Segurança, ANPD e auditoria |
| Logs gerais de TI e infraestrutura | 12 meses | Melhores práticas e PRI |
| Backups de produção (Tier 1) | 90 dias (padrão) | Operacionalidade |
| Backups de retenção regulatória (Tier 3) | Conforme categoria acima (máx. típico: 10 anos; documentos trabalhistas até 30 anos se aplicável) | Obrigações legais |

Quando houver conflito entre prazos, prevalece o prazo maior.

---

## 7. Monitoramento e alertas

São monitorados de forma contínua:
- Taxa de sucesso de jobs de backup (meta ≥ 99,5% ao mês);
- Conclusão no tempo, tamanho, crescimento e latência;
- Restaurações de amostra;
- Integridade e checksums;
- Consumo e projeção de custos;
- Tentativas de acesso, permissões e ações de restauração/eliminação (log imutável).

---

## 8. Testes de recuperação

| Tipo de teste | Frequência mínima |
| --- | --- |
| Teste de arquivo individual (aleatório) | 1x por semana |
| Teste de restore de banco de dados crítico | 1x por mês |
| Teste de sistema completo (aplicação + banco + rede) | 1x por trimestre |
| Simulação de ransomware / BCDR completo | 2x por ano (uma em conjunto com o PRI) |

Todo teste é registrado com data, responsável, resultado, evidências e plano de correção em caso de falha. Falhas são corrigidas em prazo máximo de 7 dias úteis.

---

## 9. Eliminação segura

Ao término do prazo de retenção, os dados são eliminados de forma segura e irreversível, respeitando-se:
- **Em mídia magnética/estado sólido (SSD/disco):** apagamento criptográfico, degaussing ou destruição física, conforme caso;
- **Em nuvem / object storage:** exclusão lógica seguida de exclusão física, com confirmação pelo provedor, quando aplicável;
- **Backups imutáveis:** aguardam o término do período de retenção e são removidos em processo automatizado com auditoria.

Toda eliminação relevante é registrada em log, com período de retenção do registro por, no mínimo, 5 anos.

---

## 10. Terceiros e subcontratados

Provedores de nuvem, BaaS e backup terceirizado seguem:
- due diligence pré-contratual;
- cláusulas de segurança e LGPD;
- direito de auditoria pela NovaData;
- SLA de recuperação contratualizado com penalidades;
- obrigação de notificar incidentes em até 24 horas corridas, alinhado ao PRI.

---

## 11. Incumprimento e incidentes

Falhas identificadas no processo de backup, restauração ou retenção são comunicadas imediatamente ao CISO e ao CTO, entrando no fluxo do Plano de Resposta a Incidentes. Descumprimento repetido ou intencional sujeita os responsáveis às medidas disciplinares do Código de Ética.

---

Cross-references: **Política de Segurança**, **Plano de Resposta a Incidentes**, **Política de Privacidade e LGPD**, **Política de Controle de Acesso**.
