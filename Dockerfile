FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY scripts ./scripts
COPY evaluation ./evaluation
COPY docs ./docs
COPY data ./data
COPY streamlit_app.py .streamlit ./

RUN mkdir -p /app/data/vector_store /app/data/logs && \
    chmod -R 777 /app/data /app/data/vector_store /app/data/logs && \
    chmod +x /app/scripts/*.py /app/scripts/*.sh 2>/dev/null || true

ARG BUILD_TAG=v1.0.0
ENV COMPLIANCE_BUILD_TAG=${BUILD_TAG}

HEALTHCHECK --interval=60s --timeout=10s --start-period=180s --retries=5 \
    CMD curl -f http://127.0.0.1:8501/_stcore/health || exit 1

EXPOSE 8501

CMD ["/app/scripts/entrypoint.sh"]
