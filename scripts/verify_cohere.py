from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    embed_model = os.getenv("COHERE_EMBED_MODEL", "embed-multilingual-v3.0")
    chat_model = os.getenv("COHERE_CHAT_MODEL", "command-r7b-12-2024")
    chat_fallback = "command-r-08-2024"

    deprecated = {"command", "command-light", "command-r", "command-r-plus"}
    if (chat_model or "").strip().lower() in deprecated:
        print(
            f"[AVISO] modelo de chat '{chat_model}' faz parte de aliases descontinuados. "
            f"Tentando fallback para '{chat_fallback}'. Atualize COHERE_CHAT_MODEL no .env."
        )
        chat_model = chat_fallback

    if not api_key:
        print("[FALHA] COHERE_API_KEY nao encontrada no .env")
        return 1

    try:
        import cohere
    except ImportError:
        print("[FALHA] pacote 'cohere' nao instalado. Execute: pip install -r requirements.txt")
        return 1

    client = cohere.ClientV2(api_key=api_key)

    print(f"Testando embeddings (model={embed_model})...")
    try:
        text = "Dados pessoais sensiveis incluem origem racial, conviccao religiosa e dados de saude."
        emb = client.embed(texts=[text], model=embed_model, input_type="search_document")
        by_type = getattr(emb, "embeddings", None)
        vecs: list[list[float]] | None = None
        if by_type is not None:
            vecs = getattr(by_type, "float_", None)
            if vecs is None:
                try:
                    vecs = by_type.float if hasattr(by_type, "float") else None
                except Exception:
                    vecs = None
        if not vecs:
            raise ValueError(
                "Nao foi possivel extrair embeddings float da resposta do Cohere. "
                "Verifique a versao do SDK cohere e o modelo escolhido."
            )
        vec = vecs[0]
        print(f"[OK] embed_ok dimensoes={len(vec)}")
    except Exception as exc:
        print(f"[FALHA] embed: {type(exc).__name__}: {exc}")
        return 1

    print(f"Testando chat (model={chat_model})...")
    try:
        resp = client.chat(
            model=chat_model,
            messages=[{"role": "user", "content": "Explique em uma frase o que e dado pessoal sensivel."}],
        )
        content = ""
        message = getattr(resp, "message", None)
        if message:
            parts = getattr(message, "content", None) or []
            if parts:
                content = getattr(parts[0], "text", "") or str(parts[0])
        snippet = content.strip()[:220].replace("\n", " ")
        print(f"[OK] chat_ok resposta: {snippet}")
    except Exception as exc:
        print(f"[FALHA] chat: {type(exc).__name__}: {exc}")
        return 1

    print("\n[OK] Cohere configurado corretamente. Pronto para indexacao.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
