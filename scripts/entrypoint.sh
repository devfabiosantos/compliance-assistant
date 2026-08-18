#!/bin/bash
set -e

echo "[$(date)] Entrypoint Compliance Assistant (Docker) iniciado..."
echo "[$(date)] Verificando indice vetorial FAISS em data/vector_store/..."

INDICE_FAISS="data/vector_store/index.faiss"
DOCS_DIR="docs"

if [ ! -d "$DOCS_DIR" ]; then
    echo "[$(date)] ERRO CRITICO: Diretorio $DOCS_DIR nao encontrado! Abortando."
    exit 1
fi

if [ -f "$INDICE_FAISS" ]; then
    echo "[$(date)] Indice FAISS ja existe ($INDICE_FAISS). Pulando indexacao (ligacao rapida)."
else
    echo "[$(date)] Indice FAISS NAO ENCONTRADO. Iniciando indexacao automatica (198 chunks)..."
    echo "[$(date)] Comando: python scripts/index_documents.py"

    if [ -z "${COHERE_API_KEY}" ]; then
        echo "[$(date)] ERRO CRITICO: Variavel COHERE_API_KEY vazia no ambiente!"
        echo "[$(date)] Acao: Adicione COHERE_API_KEY nas Environment Variables do Render e faca Manual Deploy."
        exit 1
    fi

    python scripts/index_documents.py
    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "[$(date)] ERRO CRITICO: index_documents.py retornou exit_code=$EXIT_CODE"
        exit 1
    fi

    if [ ! -f "$INDICE_FAISS" ]; then
        echo "[$(date)] ERRO CRITICO: Apos indexacao $INDICE_FAISS ainda nao existe!"
        exit 1
    fi
    echo "[$(date)] Indexacao automatica CONCLUIDA. Indice $INDICE_FAISS criado com sucesso."
fi

echo "[$(date)] Iniciando Streamlit UI (porta 8501)..."
exec streamlit run streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.enableCORS=true \
    --server.enableXsrfProtection=true
