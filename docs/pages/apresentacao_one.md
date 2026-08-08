# Apresentação ONE — Compliance Assistant (Roteiro 5 minutos exatos)

> **Tempo alvo:** 4min50s a 5min10s. Pratique 2 vezes e ajuste as falas do “Roteiro falado” para ficar natural.
>
> **URL do repositório:** https://github.com/devfabiosantos/compliance-assistant
> **Tags de entrega:** `v0.6.0-rc1` (freeze) e `v1.0.0-rc1` (release candidate final)
> **Build sugerido:** Build do Streamlit UI local com BUILD_TAG `v1.0.0-rc1`

---

## 1. Abertura (30s)

**Tela inicial:** Repositório GitHub `devfabiosantos/compliance-assistant` (README aberto, tag v1.0.0-rc1 no topo).

**Roteiro falado:**
> “Boa tarde/tarde. Meu nome é Fábio Santos, sou técnico de Segurança do Trabalho, desenvolvedor back-end Java/Go, participante do programa Oracle Next Education / Alura ONE Turma 7.
>
> O projeto que eu apresento hoje é o **Compliance Assistant**, um produto open-source da **NovaData Solutions** — empresa brasileira fictícia de governança e IA para compliance.
>
> Em 4 minutos e meio eu mostro: o problema, a arquitetura, 2 perguntas reais do RAG com fontes, 2 abas da UI Streamlit, avaliação Nível 1 100% e como fazer deploy no OCI Always Free.”

---

## 2. Problema + caso de uso (45s)

**Tela:** README seção “O problema” (4 itens) + Tabela casos de uso.

**Roteiro falado:**
> “O problema é simples e recorrente em qualquer empresa com mais de 50 colaboradores: centenas de páginas de políticas e leis, interpretações diferentes por área, e ninguém sabe de onde veio a resposta.
>
> Perguntas como *‘Posso enviar CPF por WhatsApp?’*, *‘Quem acessa dados financeiros?’* ou *‘Qual o SLA de incidente S0?’* demoram horas para serem respondidas — e ainda geram risco se a resposta está errada.
>
> O Compliance Assistant resolve isso com **RAG (Retrieval-Augmented Generation)** combinando 12 documentos reais: LGPD + ANPD e 9 políticas internas. Toda resposta tem **fonte, seção e score** — ou retorna ‘informação insuficiente’.”

---

## 3. Arquitetura (45s — 1 diagrama Mermaid)

**Tela:** README seção “Arquitetura (Mermaid)” renderizada no GitHub (8 blocos coloridos).

**Roteiro falado:**
> “A arquitetura é 10 camadas, provider-agnostic. Resumindo em 4 estágios:
>
> **1 — Fontes:** 12 documentos indexados (3 oficiais LGPD/ANPD + 9 corporativos).
> **2 — Ingestão:** Markdown/PDF → aliases por documento → chunker outline H2+ e seção herdada (não tem mais `section=None`).
> **3 — Retrieval:** Cohere `embed-multilingual-v3.0` com batching seguro de 96 textos por request → FAISS local versionado → busco top-5 por score threshold.
> **4 — Geração anti-hallucination:** Prompt com cabeçalhos por chunk + regras obrigatórias. Se não houver nenhum chunk útil (score <0.35), o assistente responde um texto padrão de ‘não tenho informação suficiente’ — nunca inventa.
>
> Interfaces: CLI, Streamlit 5 abas. Deploy: Dockerfile + Compose + OCI Always Free.”

---

## 4. UI 1 — Home + Base de Conhecimento (30s)

**Tela:** Streamlit rodando `http://localhost:8501`. BUILD_TAG `v1.0.0-rc1`.

**Roteiro falado:**
> “Primeiro a aba 🏠 Home. Aqui o usuário vê a versão, 8 diferenciais do produto e — na aba **📚 Base** — os 12 documentos organizados com categoria, versão, responsáveis e próxima revisão. O usuário entende imediatamente o ‘escopo’ do assistente antes de perguntar qualquer coisa.”

---

## 5. UI 2 — Pergunta 1 real (60s — principal)

**Tela:** Aba 💬 Compliance Assistant. Clica na pergunta sugerida:
> *“Em caso de incidente S0 na NovaData Solutions, quanto tempo de SLA e quem aciono?”*

**Roteiro falado:**
> “Eu clico em uma pergunta sugerida. Veja que a resposta — em português, natural — vem acompanhada de:
>
> **Primeiro:** O tempo correto: **SLA 1 hora**, responsáveis CISO + CTO.
> **Segundo:** Aqui embaixo, expander ‘📄 Fontes citadas (5)’ — Documento, Seção, Página e Score. Não inventa documento: todos os 5 chunks estão nos documentos que eu mostrei na Base.
> **Terceiro:** 5 colunas de métricas: Modelo `command-r7b-12-2024`, ~300ms embed, ~350ms busca total, ~1.8s de geração e ~2.5s total.
>
> Isso é rastreabilidade: auditoria, DPO, área de compliance — todo mundo consegue validar a origem. Nenhuma resposta ‘solta’.”

---

## 6. UI 3 — Pergunta 2 anti-hallucination (30s — cross-doc)

**Tela:** Mesma aba Chat. Nova pergunta no campo:
> *“Posso usar IA generativa pública com dados de clientes da NovaData?”*

**Roteiro falado:**
> “Segunda pergunta — propositalmente ‘cinza’ para testar anti-hallucination. O sistema responde baseado em **Política Uso Aceitável Seção 12 (Inteligência Artificial Generativa)**. O resultado: proibido em IA generativa pública; **permitido em IA empresarial com DPO + CISO aprovando previamente + SSDLC + inventário**.
>
> Perfeito para a cultura de segurança: não é ‘sim/não’ mecânico; informa a regra + o caminho correto.”

---

## 7. Aba 📊 Qualidade (30s)

**Tela:** Aba 📊 Qualidade do RAG. Relatórios N1 e N2 carregados.

**Roteiro falado:**
> “Aqui a aba de qualidade. O sistema mede 2 níveis de avaliação automaticamente a cada release.
>
> **Nível 1 — Retrieval:** Documento correto, seção correta, keywords — **48 casos, 100% em tudo**. Esse número ‘perfeito’ eu não inventei: é o resultado do runner automático com aliases, normalização Unicode, stopwords, cross-documents e seção herdada.
>
> **Nível 2 — QA final:** Faithfulness anti-hallucination, Context Recall, Citation Precision e Citation Recall. Tudo JSON versionado em `evaluation/reports/`.”

---

## 8. Deploy OCI + Repo fechamento (30s — último slide)

**Tela:** README seção “Deploy OCI” (Passo A PowerShell).

**Roteiro falado:**
> “Para subir em produção no OCI Always Free (A1 AMPERE 4 OCPU / 24 GB / 200 GB volume — tudo sempre grátis), são só 2 arquivos:
>
> **PowerShell Windows:** `.\scripts\deploy_oci.ps1` envia código + `.env` por SSH, builda a imagem e sobe na porta 8501.
> **Oracle Linux manual:** `sudo bash scripts/deploy_oci.sh` — 10 passos documentados.
>
> Todo o código, changelog Keep a Changelog, licença MIT, CONTRIBUTING, ADRs — tudo versionado no GitHub: **github.com/devfabiosantos/compliance-assistant**, tags `v0.1.0` até `v1.0.0-rc1`.

---

## 9. Encerramento (10s)

**Tela:** Repositório GitHub v1.0.0-rc1. Nome do autor e email no README.

**Roteiro falado:**
> “Esse foi o Compliance Assistant, v1.0.0-rc1. Obrigado — dúvidas, comentários ou contribuições, issues e PRs são bem-vindos no repositório.”

---

### ⏱ Duração total planejada (falas + cliques): 4min55s ± 15s.

---

## 🎬 Dicas de gravação

1. **Prática 1 vez só sem gravar** → ajusta o texto das falas (elas são para ler, não decorar)
2. **Microfone USB / headset dedicado** (evita eco do notebook)
3. **Resolução 1920×1080, zoom 110% nos textos** (fica melhor no YouTube / plataforma ONE)
4. **Desliga notificações do Windows e navegador** (modo “não perturbe”)
5. **Feche tudo exceto:** Terminal PowerShell (para mostrar `docker compose up -d` se quiser um “bônus” de 10s), navegador com 2 abas: GitHub README e Streamlit.
6. **Se passar de 5min20s:** corte a pergunta 2 anti-hallucination e fique só com a pergunta 1 do incidente S0 (reduz ~30s).
7. **Se ficar curto (<4:40):** adicione no final um ‘bônus’ de 20s mostrando:
   ```powershell
   python evaluation\evaluate_retrieval.py --fail-on-zero
   ```
   e mostrando a linha `Acuracia (documento correto) : 100.0%`.

---

## 📝 Checklist do vídeo

- [ ] Tag v1.0.0-rc1 aparece no GitHub (README / Releases)
- [ ] BUILD_TAG `v1.0.0-rc1` aparece no canto da Home do Streamlit
- [ ] A pergunta 1 “incidente S0” mostra resposta com 1h + CISO/CTO + fontes dataframe com Seção 2 / 3.1
- [ ] 100% em Nível 1 aparece na aba Qualidade (ou pelo menos linha do evaluate_retrieval.py)
- [ ] Script deploy OCI aparece no README Passo A PowerShell
- [ ] Nome do autor / email / GitHub aparece no encerramento
