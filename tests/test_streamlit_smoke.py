from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_PATH = ROOT / "streamlit_app.py"


def _import_app():
    assert APP_PATH.exists(), f"streamlit_app.py nao encontrado em {APP_PATH}"
    spec = importlib.util.spec_from_file_location("streamlit_app_module", str(APP_PATH))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["streamlit_app_module"] = module
    spec.loader.exec_module(module)
    return module


class TestStreamlitAppSmoke:
    def test_file_exists(self):
        assert APP_PATH.is_file()

    def test_imports_without_crash(self):
        module = _import_app()
        for name in ["APP_TITLE", "COMPANY", "BUILD_TAG", "page_home", "page_chat", "page_base", "page_quality", "page_about", "main", "_doc_cards"]:
            assert hasattr(module, name), name

    def test_doc_cards_have_twelve_docs(self):
        module = _import_app()
        cards = module._doc_cards()
        assert len(cards) == 12
        titles = {c.title for c in cards}
        assert any("LGPD" in t for t in titles), cards
        assert any("Seguranca" in t or "Segurança" in t or "Segurança da Informação" in t or "Seguranca da Informacao" in t for t in titles), cards
        assert any("Incidentes" in t or "Resposta" in t for t in titles), cards

    def test_page_functions_are_callable(self):
        module = _import_app()
        for fn in [module.page_home, module.page_base, module.page_quality, module.page_about]:
            assert callable(fn)

    def test_main_callable(self):
        module = _import_app()
        assert callable(module.main)
