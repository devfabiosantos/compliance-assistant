#Requires -Version 5.1
# deploy_oci.ps1 — Envia codigo + .env para OCI e roda o deploy via SSH
# USO (na sua maquina WINDOWS):
#   1. Tenha o .\scripts\deploy_oci.sh e .\.env em C:\ComplianceGPT
#   2. Preencha abaixo IP, usuario e caminho da chave SSH.
#   3. PowerShell como voce normal (nao Admin):
#      cd C:\ComplianceGPT ; .\scripts\deploy_oci.ps1

param(
    [string]$IpPublico = "150.136.1.1",
    [string]$Usuario  = "opc",
    [string]$ChavePrivada = "$env:USERPROFILE\.ssh\oci_rsa",
    [string]$PastaRemota = "/home/$Usuario/compliance-assistant"
)

$ErrorActionPreference = "Stop"

Write-Host "==> [1/4] Validando chave SSH e .env..." -ForegroundColor Cyan
if (-not (Test-Path $ChavePrivada)) { throw "Chave privada nao encontrada: $ChavePrivada" }
if (-not (Test-Path ".env")) { throw ".env nao encontrado na raiz do projeto." }
Get-Command scp -ErrorAction Stop | Out-Null
Get-Command ssh -ErrorAction Stop | Out-Null

Write-Host "==> [2/4] Enviando codigo (rsync via tar) para ${Usuario}@${IpPublico}:${PastaRemota} ..." -ForegroundColor Cyan
ssh -i $ChavePrivada -o StrictHostKeyChecking=accept-new "${Usuario}@${IpPublico}" "mkdir -p '${PastaRemota}' && sudo mkdir -p /opt/compliance-assistant && sudo chown -R '${Usuario}':'${Usuario}' /opt/compliance-assistant"

$TarLocal  = Join-Path $env:TEMP "compliance-assistant-src.tar"
$TarRemoto = "${PastaRemota}/compliance-assistant-src.tar"
tar --exclude='data\vector_store\*' --exclude='.git' --exclude='*.pyc' --exclude='__pycache__' --exclude='.venv' `
    --exclude='*.pkl' --exclude='index.faiss' -c -f $TarLocal `
    --transform 's,^\./,,' "." 2>&1 | Select-Object -First 3
scp -i $ChavePrivada -o StrictHostKeyChecking=accept-new $TarLocal "${Usuario}@${IpPublico}:${TarRemota}"
Remove-Item $TarLocal -ErrorAction SilentlyContinue

ssh -i $ChavePrivada "${Usuario}@${IpPublico}" @"
set -e
cd '${PastaRemota}'
rm -rf src scripts evaluation docs data tests .streamlit Dockerfile docker-compose.yml pyproject.toml README.md LICENSE streamlit_app.py CHANGELOG.md requirements.txt 2>/dev/null || true
tar -xf compliance-assistant-src.tar
rm compliance-assistant-src.tar
cp -f .env .env.bak-$(date +%Y%m%d%H%M%S) 2>/dev/null || true
"@

Write-Host "==> [3/4] Enviando .env (segredo via SCP, nunca no GitHub) ..." -ForegroundColor Cyan
scp -i $ChavePrivada .env "${Usuario}@${IpPublico}:${PastaRemota}/.env"

Write-Host "==> [4/4] Iniciando deploy remoto (bash deploy_oci.sh como sudo) ..." -ForegroundColor Cyan
ssh -i $ChavePrivada -t "${Usuario}@${IpPublico}" @"
set -e
sudo bash ${PastaRemota}/scripts/deploy_oci.sh
"@

Write-Host ""
Write-Host "==> PRONTO. Acesse: http://${IpPublico}:8501  (lembre-se de liberar porta 8501/TCP na Security List da sub-rede OCI)." -ForegroundColor Green
Write-Host "    Logs remotos: ssh -i $ChavePrivada ${Usuario}@${IpPublico} 'cd /opt/compliance-assistant && sudo docker compose logs -f --tail=200'"
Write-Host "    Rebuild    : ssh -i $ChavePrivada ${Usuario}@${IpPublico} 'cd /opt/compliance-assistant && sudo docker compose build --no-cache && sudo docker compose up -d'"
