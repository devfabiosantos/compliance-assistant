# Política de Controle de Acesso — NovaData Solutions
Documento nº PCA-ND-2026-001 | Versão 1.0
Aprovação: CTO + CISO + Diretoria Executiva | Data: 01/08/2026 | Próxima revisão: 01/2027

---

## 1. Objetivo

Estabelecer diretrizes e regras para gestão de identidades, credenciais e acessos aos ativos de informação, sistemas, aplicações, ambientes de nuvem, redes e instalações físicas da NovaData Solutions, em conformidade com:
- **Código de Ética e Conduta** (Seção 9 — Segurança da Informação e Proteção de Dados);
- **Política de Segurança da Informação** (Seção 4 — Controles Lógicos de Acesso);
- **Política de Privacidade e LGPD** (princípio da necessidade e livre acesso);
- **Plano de Resposta a Incidentes** (revogação de acessos em incidentes);
- requisitos legais (LGPD art. 37, Lei Geral de Informática, normas ISO/IEC 27001 e 27002).

---

## 2. Princípios fundamentais

São princípios desta política:
1. **Individualidade e intransferibilidade:** Toda conta de acesso é pessoal e intransferível. Nenhum colaborador pode compartilhar senhas, tokens, biometria ou qualquer credencial com terceiros, colegas ou prestadores, conforme proibição do Código de Ética;
2. **Menor privilégio (least privilege):** Acesso concedido apenas aos recursos estritamente necessários para a execução da função;
3. **Separação de funções (segregation of duties):** O mesmo colaborador não acumula funções conflitantes (ex.: aprovar pagamento e lançar pagamento, alterar banco e auditar alterações);
4. **Need-to-know:** Acesso a informações sensíveis apenas por colaboradores que necessitam conhecer, com base em suas atribuições;
5. **Rastreabilidade:** Toda ação relevante (criação de conta, concessão de privilégio, revogação, acesso a dados sensíveis) é registrada em log centralizado com retenção mínima de 12 meses (24 meses para eventos de segurança e dados pessoais sensíveis, conforme Política de Backup e Retenção);
6. **Revisão periódica:** Acessos privilegiados, perfis de administrador, acessos a clientes e a bases de dados pessoais são revisados trimestralmente pelo CISO e gestores competentes;
7. **MFA obrigatório:** Autenticação multifator para acessos administrativos, consoles de nuvem, VPN, e-mail corporativo e painéis com dados de clientes;
8. **Justificativa e aprovação:** Toda concessão ou ampliação de acesso requer justificativa documentada e aprovação de, no mínimo, o gestor imediato e, para privilégios administrativos, aprovação adicional do proprietário do ativo e do CISO.

---

## 3. Ciclo de vida da identidade

### 3.1. Provisionamento
O provisionamento segue os fluxos:
1. **Solicitação de acesso:** por meio de sistema de chamados/fluxo formal;
2. **Validação:** justificativa e necessidade são validadas pela área competente;
3. **Aprovação:** gestor imediato, proprietário do sistema e, para privilégios administrativos, CISO;
4. **Implementação:** pela Diretoria de TI/Segurança;
5. **Comunicação:** de posse de credencial para o colaborador em canal seguro.

### 3.2. Modificação de acesso
Alterações de cargo, função, transferência interna ou necessidade de nova atribuição implicam revisão de acessos em até **3 dias úteis** e a aplicação do princípio do menor privilégio.

### 3.3. Revogação
A revogação de acessos ocorre em, no máximo:
- **4 horas úteis** em caso de desligamento voluntário, demissão, rescisão ou suspeita de desvio;
- **Imediata** em caso de incidente de segurança ou suspeita de comprometimento de credencial, conforme Plano de Resposta a Incidentes;
- Em até 3 dias úteis para mudanças de cargo/função e em fim de projetos temporários;
- Em até 2 dias úteis após término de contrato de prestador/parceiro.

### 3.4. Desativação de contas inativas
Contas inativas por mais de **45 dias consecutivos** são desativadas automaticamente, com notificação ao gestor e reativação por novo processo de solicitação/aprovação.

---

## 4. Perfis e privilégios

### 4.1. Tipos de perfis
A política classifica perfis em:
- **Usuário padrão:** acesso a ferramentas operacionais de sua função;
- **Usuário privilegiado:** acesso a sistemas, bancos, consoles ou redes com capacidades administrativas;
- **Usuário de serviço:** contas máquina para integrações e automações. Possuem senhas fortes, rotação periódica e auditoria especial;
- **Usuário de emergência (break-glass):** credenciais de último recurso, para uso exclusivo em incidentes críticos, sob monitoramento rigoroso, com uso justificado e validação pós-incidente pelo CISO.

### 4.2. Privilégios de administração
Privilégios administrativos são concedidos a número mínimo e estritamente necessário de colaboradores. Todo acesso privilegiado utiliza MFA, é monitorado pelo SOC 24x7 e está sujeito a revisão trimestral formal.

---

## 5. Gestão de senhas, tokens e segredos

Regras complementares à Política de Segurança (Seção 5):
1. As senhas não podem ser compartilhadas, armazenadas em papel ou em arquivos sem criptografia;
2. Use gerenciador de senhas corporativo;
3. Bloqueio de conta após 5 tentativas inválidas sucessivas;
4. Proibição de reuso das últimas 12 senhas para contas privilegiadas;
5. Senhas de contas de serviço são rotacionadas a cada 90 dias, pelo menos;
6. Tokens OATH/TOTP, hardware keys (FIDO2/U2F) e biometria são preferíveis a senhas como segundo fator.

---

## 6. Controles adicionais em ambientes críticos

Para bases de dados com dados pessoais sensíveis e ambientes produtivos:
- Acesso restrito e lista nominal aprovada pelo proprietário + CISO;
- Rastreamento de sessões (log de comandos quando aplicável);
- Política de “acesso just-in-time” para ambientes de produção, com concessão temporária de privilégios e auditoria;
- Auditoria mensal de acessos realizados;
- Monitoramento de anomalias pelo SOC.

---

## 7. Controles físicos

Os controles de acesso físico seguem a Política de Segurança (Seção 3) e incluem:
- cadastro de biometria/crachá nominal;
- revogação imediata de crachá em caso de desligamento;
- registros de acessos a áreas restritas com retenção mínima de 24 meses;
- visitação com identificação, crachá de visitante, lista pré-aprovada e acompanhamento permanente.

---

## 8. Terceiros, prestadores e parceiros

Acessos por terceiros seguem:
- due diligence prévia e contrato com cláusulas de segurança e LGPD (vide Política de Segurança, Seção 8);
- contas individuais e não compartilhadas;
- período de acesso alinhado ao contrato e às entregas, com data de expiração pré-definida;
- revogação automática em caso de término ou incidente de segurança.

---

## 9. Monitoramento, log e auditoria

A auditoria dos acessos compreende:
- logs centralizados e coletados diariamente;
- revisão periódica pelo CISO e Compliance;
- investigação de anomalias pelo SOC;
- apresentação de relatórios à Diretoria Executiva com frequência trimestral;
- participação, quando necessário, em auditorias internas e externas.

---

## 10. Incumprimento

O descumprimento a esta política pode acarretar:
- revogação temporária ou definitiva de acessos;
- medidas disciplinares trabalhistas;
- comunicação ao Comitê de Ética;
- comunicação a órgãos de fiscalização;
- indenização por danos materiais ou morais, inclusive à titulares de dados pessoais, quando cabível.

---

Cross-references: **Código de Ética (Seção 9)**, **Política de Segurança da Informação**, **Política de Privacidade e LGPD**, **Plano de Resposta a Incidentes**, **Política de Backup e Retenção**.
