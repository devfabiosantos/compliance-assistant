# Política de Segurança da Informação — NovaData Solutions
Documento nº PSI-ND-2026-001 | Versão 1.0
Aprovação: CISO + Diretoria Executiva | Data: 01/08/2026 | Próxima revisão: 01/2027

---

## 1. Objetivo e âmbito

### 1.1. Objetivo
Estabelecer as diretrizes, princípios, responsabilidades, controles e padrões mínimos de segurança da informação aplicáveis a todos os colaboradores, prestadores de serviço, parceiros e terceiros que acessem ou manipulem ativos de informação da NovaData Solutions, em conformidade com o **Código de Ética e Conduta** (Seção 9 — Segurança da Informação e Proteção de Dados), a **Política de Privacidade e LGPD**, o **Plano de Resposta a Incidentes**, a **Política de Controle de Acesso**, a **Política de Uso Aceitável** e a legislação aplicável (LGPD, Lei nº 12.965/2014, Lei nº 13.709/2018).

### 1.2. Âmbito
Aplica-se a todos os ativos de informação, físicos e lógicos, independentemente do suporte (papel, digital, nuvem, mídia removível), assim como a todos os ambientes corporativos (escritórios, home office, datacenters, nuvem e dispositivos de colaboradores e terceiros).

---

## 2. Classificação da Informação

### 2.1. Níveis de classificação
A NovaData Solutions classifica as informações em 4 níveis, conforme impacto à empresa e aos titulares dos dados:

| Nível | Rótulo | Exemplos típicos | Acesso mínimo permitido |
| --- | --- | --- | --- |
| 4 | **Pública** | Conteúdo do site institucional, releases oficiais, vagas abertas | Qualquer pessoa, inclusive externos |
| 3 | **Interna** | Manuais do colaborador não sensíveis, organograma público interno, FAQs internas gerais | Colaboradores ativos, mediante login |
| 2 | **Confidencial** | Contratos de clientes, dados financeiros operacionais, documentação de arquitetura de sistemas, dados de colaboradores | Áreas competentes e/ou por lista nominal de acesso |
| 1 | **Restrita / Crítica** | Dados pessoais sensíveis (art. 5º, II LGPD), segredos comerciais, credenciais administrativas, chaves criptográficas, resultados de auditorias de segurança | Mínimo de privilégio, lista nominal aprovada pelo gestor responsável + acompanhamento do CISO |

### 2.2. Obrigatoriedade de classificação
Todo ativo de informação novo (documento, planilha, compartilhamento, repositório, base de dados) deve ser classificado no momento de sua criação pelo gestor responsável ou proprietário do ativo.

---

## 3. Segurança Física e Ambiental

### 3.1. Áreas restritas
Datacenters, salas de rede, Cofre Digital e depósitos de mídia física são áreas restritas. O acesso é controlado por credencial nominal biométrica ou cartão-proximidade e registrado em log centralizado, com permanência de registros por pelo menos 24 meses, conforme Política de Backup e Retenção.

### 3.2. Segurança em home office
Colaboradores em home office observam as regras da **Política de Home Office**, incluindo:
- ambiente reservado e de preferência com tranca;
- vedação de tela em ambientes compartilhados;
- bloqueio automático após 5 minutos de inatividade;
- uso exclusivo de VPN corporativa em redes não confiáveis.

---

## 4. Controles Lógicos de Acesso

Os controles lógicos de acesso são regidos em detalhe pela **Política de Controle de Acesso**. A presente Política estabelece os princípios:
1. **Individualidade e intransferibilidade:** Toda credencial (usuário, senha, token, chave SSH) é pessoal e intransferível. Compartilhamento constitui infração disciplinar, conforme Código de Ética (Seção 9).
2. **Princípio do menor privilégio (least privilege):** Os acessos concedidos refletem o mínimo necessário para a função.
3. **MFA obrigatório:** Autenticação multifator é obrigatória para acessos administrativos, VPNs, consoles de nuvem, e-mail corporativo e painéis de cliente.
4. **Revogação imediata:** Desligamentos, desligamentos voluntários ou mudanças de cargo implicam revogação dos acessos em até **4 horas úteis**.
5. **Auditoria trimestral:** O CISO (via Equipe de Segurança) conduz revisão trimestral dos acessos aos ativos de classificação Confidencial e Restrita.

---

## 5. Senhas, Credenciais e Segredos

### 5.1. Padrão de senhas
As senhas dos sistemas corporativos devem ter, no mínimo, 14 caracteres, com combinação de letras maiúsculas, minúsculas, números e símbolos. Alternativamente, são aceitas frases-senha (passphrases) de pelo menos 5 palavras aleatórias.

### 5.2. Gerenciadores de senha
É obrigatório o uso de gerenciador de senhas corporativo aprovado pela Diretoria de TI para senhas de sistemas, clientes e ambientes compartilhados. Senhas em bloco de notas, planilhas sem criptografia ou papéis são proibidas.

### 5.3. Chaves criptográficas e segredos na nuvem
Chaves de API, tokens de serviço, certificados e segredos são gerenciados em cofre de segredos aprovado (ex.: KMS/Vault), com rotação automática e trilhas de auditoria imutáveis. Nunca devem ser versionados em repositórios Git nem inseridos em scripts ou imagens de container.

---

## 6. Criptografia

### 6.1. Em trânsito
Todas as comunicações que trafeguem por redes não confiáveis devem empregar TLS 1.2 ou superior, com certificados válidos e atualizados. Protocolos inseguros como FTP, Telnet, HTTP e SMB não assinados são proibidos.

### 6.2. Em repouso
Discos de servidores, workstations corporativas, notebooks, backups e bancos de dados com dados de clientes ou colaboradores são criptografados em repouso com algoritmos aprovados (AES-256 ou superior), de acordo com a LGPD art. 37 e os controles recomendados na ANPD (vide Guia ANPD, Seção 5.1).

---

## 7. Segurança em Desenvolvimento de Software

### 7.1. Ciclo de vida seguro
A equipe de desenvolvimento segue o SSDLC definido pela Diretoria de Tecnologia, com:
- Análise de risco e requisitos de segurança em planning;
- SAST/DAST/SCA em CI/CD;
- SBOM para todos os produtos SaaS;
- Correção de vulnerabilidades em SLA:
  - **Crítica/CVSS ≥ 9,0:** 48 horas úteis;
  - **Alta/CVSS ≥ 7,0:** 7 dias úteis;
  - **Média/CVSS ≥ 4,0:** 30 dias úteis;
  - **Baixa:** resolvida em release seguinte.

### 7.2. Segurança em IA
O uso de modelos de inteligência artificial (incluindo o próprio **Compliance Assistant**) deve observar:
- Não envio de dados pessoais sensíveis sem anonimização prévia ou base legal;
- Política de aceite interno para cada ferramenta de IA;
- Registro de operações de tratamento no Registro de Operações de Tratamento (ROT), conforme diretrizes da ANPD.

---

## 8. Gestão de Terceiros

Todo prestador de serviço ou parceiro com acesso a ativos de informação passa por due diligence pré-contratual conduzida pelo Compliance em conjunto com o CISO. Os contratos devem conter, no mínimo:
- cláusulas de confidencialidade;
- cláusulas de LGPD (obrigações do operador);
- obrigação de adotar controles técnicos equivalentes aos da Política de Segurança;
- direito de auditoria pela NovaData Solutions;
- obrigação de notificar incidentes em até 24 horas corridas.

---

## 9. Conscientização e Treinamento

Todos os colaboradores participam de:
- **Onboarding de Segurança:** obrigatório, com aproveitamento ≥ 80%;
- **Refresh anual:** treinamento atualizado com foco em ameaças do período;
- **Simulações de phishing:** pelo menos 4 campanhas por ano, com reforço imediato para quem falhar.
- **Campanhas de conscientização:** mensagens curtas, frequentes e contextualizadas.

---

## 10. Resposta a Incidentes

A gestão de incidentes segue o **Plano de Resposta a Incidentes** da empresa. É obrigatória a comunicação imediata de todo incidente ou suspeita ao CISO e ao SOC, através dos canais oficiais. A comunicação à ANPD e aos titulares, quando aplicável, é coordenada pelo DPO com apoio do CISO, em observância aos prazos da LGPD.

---

## 11. Monitoramento, Logs e Auditoria

Todos os ativos críticos possuem log centralizado, com retenção mínima de 12 meses para logs gerais e 24 meses para eventos de segurança e acessos a dados pessoais sensíveis. O SOC realiza monitoramento 24x7, de acordo com o Organograma (CISO → SOC 24x7).

---

## 12. Conformidade Legal e Sanções

O descumprimento desta Política pode acarretar:
- advertência verbal ou escrita;
- suspensão ou revogação de acessos;
- aplicação de medidas disciplinares previstas no Código de Ética e na legislação trabalhista;
- comunicação a órgãos de fiscalização, quando aplicável;
- indenização por danos causados;
- comunicação ao DPO e, se necessário, à ANPD, em caso de incidente com dado pessoal.

---

Documento proprietário e confidencial da NovaData Solutions. Referências cruzadas: **Código de Ética (Seção 9)**, **Política de Privacidade e LGPD**, **Plano de Resposta a Incidentes**, **Política de Controle de Acesso**, **Política de Uso Aceitável**.
