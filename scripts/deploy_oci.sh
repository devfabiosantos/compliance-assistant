#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# deploy_oci.sh — Deploy passo a passo do Compliance Assistant em Oracle Linux 8/9 (OCI Always Free A1 ou Flex)
#
# USO (na VM OCI, como usuario 'opc' ou 'ubuntu'):
#   sudo su -
#   bash deploy_oci.sh
#
# IMPORTANTE: antes de rodar este script na VM, envie o codigo e o .env PARA A VM:
#   Na sua maquina Windows local:
#     scp -i ~/.ssh/chave_privada_oci.key -r C:\ComplianceGPT opc@IP_PUBLICO_OCI:/home/opc/compliance-assistant
#     scp -i ~/.ssh/chave_privada_oci.key   C:\ComplianceGPT\.env opc@IP_PUBLICO_OCI:/home/opc/compliance-assistant/.env
#
# Na VM, crie um softlink de /home/opc/compliance-assistant para /opt/compliance-assistant (opcional).

set -euo pipefail

APP_DIR="/opt/compliance-assistant"
APP_USER="compliance"
SVC_NAME="compliance-assistant"

echo "[1/10] Atualizando sistema..."
dnf -y upgrade --refresh || yum -y upgrade --refresh
dnf -y install --setopt=install_weak_deps=False dnf-plugins-core ca-certificates curl tar jq firewalld || \
yum -y install dnf-plugins-core ca-certificates curl tar jq firewalld

echo "[2/10] Configurando firewall para porta 8501 TCP..."
systemctl enable --now firewalld 2>/dev/null || true
firewall-cmd --permanent --add-port=8501/tcp 2>/dev/null || true
firewall-cmd --permanent --add-service=http         2>/dev/null || true
firewall-cmd --reload 2>/dev/null || true

echo "[3/10] Instalando Docker (Engine + Compose v2 plugin)..."
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo 2>/dev/null || true
dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin 2>/dev/null || \
yum -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
systemctl enable --now docker
docker --version
docker compose version

echo "[4/10] Criando usuario ${APP_USER} e grupos docker..."
id -u "${APP_USER}" >/dev/null 2>&1 || useradd -r -m -s /sbin/nologin "${APP_USER}"
usermod -aG docker "${APP_USER}" 2>/dev/null || true
usermod -aG docker "${USER}" 2>/dev/null || true
mkdir -p "${APP_DIR}" "${APP_DIR}/data/vector_store" "${APP_DIR}/evaluation/reports" "${APP_DIR}/logs"

echo "[5/10] Copiando codigo para ${APP_DIR} (se estiver em /home/opc)..."
if [ -d /home/opc/compliance-assistant/src ]; then
  rsync -a --delete --exclude='data/vector_store/*' --exclude='.git/' \
        /home/opc/compliance-assistant/ "${APP_DIR}/"
fi
chown -R root:root "${APP_DIR}"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}/data" "${APP_DIR}/evaluation/reports" "${APP_DIR}/logs" 2>/dev/null || true
chmod -R 750 "${APP_DIR}" 2>/dev/null || true

echo "[6/10] Verificando .env..."
if [ ! -f "${APP_DIR}/.env" ]; then
  echo "ERRO: ${APP_DIR}/.env NAO ENCONTRADO."
  echo "Copie da sua maquina local com SCP e rode novamente:"
  echo "  scp -i CHAVE.key C:\\ComplianceGPT\\.env opc@IP_OCI:${APP_DIR}/.env"
  exit 1
fi
chmod 600 "${APP_DIR}/.env"

echo "[7/10] Verificando BUILD_TAG e ajustando VECTOR_STORE_DIR..."
grep -qE "^VECTOR_STORE_DIR=/app/data/vector_store$" "${APP_DIR}/.env" 2>/dev/null || \
  echo "VECTOR_STORE_DIR=/app/data/vector_store" >> "${APP_DIR}/.env"
grep -qE "^VECTOR_STORE_DOCSTORE_PATH=" "${APP_DIR}/.env" 2>/dev/null || \
  echo "VECTOR_STORE_DOCSTORE_PATH=/app/data/vector_store/docstore.pkl" >> "${APP_DIR}/.env"
grep -qE "^BUILD_TAG=" "${APP_DIR}/.env" || echo "BUILD_TAG=v0.5.0-rc1" >> "${APP_DIR}/.env"

echo "[8/10] Build da imagem Docker..."
cd "${APP_DIR}"
. ./.env 2>/dev/null || true
export BUILD_TAG="${BUILD_TAG:-v0.5.0-rc1}"
docker compose build --no-cache

echo "[9/10] Reindexando vetores na primeira inicializacao (uma vez, gasta tokens Cohere)..."
mkdir -p data/vector_store && docker compose run --rm --no-deps compliance-assistant \
  /bin/sh -c "cd /app && python scripts/index_documents.py" 2>&1 | tail -n 25

echo "[10/10] Sobe servico em background e verifica healthcheck..."
docker compose up -d
echo "Esperando 90s do Streamlit inicializar..."
sleep 90
docker compose ps
echo
echo "Healthcheck raw:"
curl -fsS http://127.0.0.1:8501/_stcore/health 2>&1 || echo "  (ainda nao pronto, re-teste em 30s)"
echo
echo "================================================================================"
echo "DEPLOY CONCLUIDO."
echo "Acesse no navegador (LIBERE a regra Ingress 8501/TCP na Console OCI Security List):"
echo "   http://$(curl -s ifconfig.me 2>/dev/null || echo '<IP_PUBLICO_OCI>'):8501"
echo
echo "Logs ao vivo:   cd ${APP_DIR} ; docker compose logs -f --tail=200"
echo "Parar servico:  cd ${APP_DIR} ; docker compose down"
echo "Rebuild release:cd ${APP_DIR} ; docker compose build --no-cache ; docker compose up -d"
echo "Reindexar dados:cd ${APP_DIR} ; docker compose run --rm compliance-assistant python scripts/index_documents.py"
echo "================================================================================"
