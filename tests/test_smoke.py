from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_project_root_contains_core_files():
    expected = [
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
    ]
    for name in expected:
        assert (ROOT / name).exists(), f"arquivo esperado nao encontrado: {name}"


def test_source_structure_exists():
    src = ROOT / "src"
    expected = [
        "config",
        "domain",
        "providers",
        "ingestion",
        "retrieval",
        "services",
        "utils",
        "app",
        "cli",
    ]
    for name in expected:
        assert (src / name).exists(), f"pasta esperada em src/: {name}"


def test_scripts_exist():
    scripts = ROOT / "scripts"
    assert (scripts / "index_documents.py").exists()
    assert (scripts / "chat.py").exists()


def test_docs_structure_exists():
    docs = ROOT / "docs"
    assert (docs / "oficiais").exists()
    assert (docs / "empresa").exists()
    assert (docs / "adr").exists()
    assert (docs / "sample_questions.md").exists()


def test_imports_succeed():
    import sys

    sys.path.insert(0, str(ROOT))
    from src.config import get_settings  # noqa: F401
    from src.domain import Answer, Question, SourceCitation, Document  # noqa: F401
    from src.providers.base import ChatProvider, EmbeddingProvider  # noqa: F401
