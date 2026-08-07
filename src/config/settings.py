from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppPath:
    docs_official_dir: Path
    docs_company_dir: Path
    vector_store_dir: Path
    log_dir: Path


@dataclass(frozen=True)
class Settings:
    cohere_api_key: Optional[str]
    cohere_chat_model: str
    cohere_embed_model: str

    chunk_size: int
    chunk_overlap: int

    retriever_top_k: int
    retriever_score_threshold: float

    log_level: str
    log_format: str

    paths: AppPath

    @staticmethod
    def _read_int(key: str, default: int) -> int:
        value = os.getenv(key)
        if value is None or value.strip() == "":
            return default
        return int(value)

    @staticmethod
    def _read_float(key: str, default: float) -> float:
        value = os.getenv(key)
        if value is None or value.strip() == "":
            return default
        return float(value)

    @staticmethod
    def _read_str(key: str, default: str) -> str:
        value = os.getenv(key)
        if value is None or value.strip() == "":
            return default
        return value.strip()

    @staticmethod
    def _resolve_path(value: str) -> Path:
        return Path(value).expanduser().resolve()


def get_settings(env_file: Optional[str] = None) -> Settings:
    if env_file:
        load_dotenv(env_file, override=False)
    else:
        load_dotenv(override=False)

    paths = AppPath(
        docs_official_dir=Settings._resolve_path(
            Settings._read_str("DOCS_OFFICIAL_DIR", "./docs/oficiais")
        ),
        docs_company_dir=Settings._resolve_path(
            Settings._read_str("DOCS_COMPANY_DIR", "./docs/empresa")
        ),
        vector_store_dir=Settings._resolve_path(
            Settings._read_str("VECTOR_STORE_DIR", "./data/vector_store")
        ),
        log_dir=Settings._resolve_path(
            Settings._read_str("LOG_DIR", "./data/logs")
        ),
    )

    return Settings(
        cohere_api_key=os.getenv("COHERE_API_KEY"),
        cohere_chat_model=Settings._read_str("COHERE_CHAT_MODEL", "command-r7b-12-2024"),
        cohere_embed_model=Settings._read_str("COHERE_EMBED_MODEL", "embed-multilingual-v3.0"),
        chunk_size=Settings._read_int("CHUNK_SIZE", 800),
        chunk_overlap=Settings._read_int("CHUNK_OVERLAP", 120),
        retriever_top_k=Settings._read_int("RETRIEVER_TOP_K", 5),
        retriever_score_threshold=Settings._read_float("RETRIEVER_SCORE_THRESHOLD", 0.5),
        log_level=Settings._read_str("LOG_LEVEL", "INFO"),
        log_format=Settings._read_str("LOG_FORMAT", "json"),
        paths=paths,
    )
