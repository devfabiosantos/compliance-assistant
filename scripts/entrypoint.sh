#!/bin/bash
set +e

echo "[$(date)] Entrypoint Compliance Assistant (Docker) iniciado..."
echo "[$(date)] Verificando indice vetorial FAISS em data/vector_store/..."

INDICE_FAISS="data/vector_store/index.faiss"
DOCS_DIR="docs"
FALTA_CHAVE_COHERE=0
FALTA_INDICE_FAISS=0

if [ ! -d "$DOCS_DIR" ]; then
    echo "[$(date)] AVISO: Diretorio $DOCS_DIR nao encontrado! Vamos tentar ligar Streamlit mesmo assim..."
fi

if [ -f "$INDICE_FAISS" ]; then
    echo "[$(date)] Indice FAISS ja existe ($INDICE_FAISS). Pulando indexacao (ligacao rapida)."
else
    FALTA_INDICE_FAISS=1
    echo "[$(date)] Indice FAISS NAO ENCONTRADO. Vamos tentar indexacao automatica (198 chunks)..."
    echo "[$(date)] Comando (tentativa): python scripts/index_documents.py"

    if [ -z "${COHERE_API_KEY}" ]; then
        FALTA_CHAVE_COHERE=1
        echo "[$(date)] AVISO: Variavel COHERE_API_KEY vazia no ambiente!"
        echo "[$(date)] Acao: Adicione COHERE_API_KEY nas Environment Variables do Render Dashboard e faca Manual Deploy."
        echo "[$(date)] Contingencia: Vamos LIGAR STREAMLIT MESMO ASSIM para mostrar ERRO AMIGAVEL na UI. Deploy NAO sera marcado como Failed."
    else
        python scripts/index_documents.py
        EXIT_CODE=$?

        if [ $EXIT_CODE -ne 0 ]; then
            echo "[$(date)] AVISO: index_documents.py retornou exit_code=$EXIT_CODE"
            echo "[$(date)] Contingencia: Ligando Streamlit mesmo assim para UI amigavel."
        else
            if [ ! -f "$INDICE_FAISS" ]; then
                echo "[$(date)] AVISO: Apos indexacao $INDICE_FAISS ainda nao existe!"
            else
                FALTA_INDICE_FAISS=0
                echo "[$(date)] Indexacao automatica CONCLUIDA. Indice $INDICE_FAISS criado com sucesso."
            fi
        fi
    fi
fi

export DEPLOY_FALTA_CHAVE_COHERE="${FALTA_CHAVE_COHERE}"
export DEPLOY_FALTA_INDICE_FAISS="${FALTA_INDICE_FAISS}"

echo "[$(date)] Iniciando Streamlit UI (porta 8501)..."
echo "[$(date)] DEPLOY_FALTA_CHAVE_COHERE=${DEPLOY_FALTA_CHAVE_COHERE} | DEPLOY_FALTA_INDICE_FAISS=${DEPLOY_FALTA_INDICE_FAISS}"
exec streamlit run streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.enableCORS=true \
    --server.enableXsrfProtection=true
