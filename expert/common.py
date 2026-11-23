from __future__ import annotations
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DB_DIR = Path(os.getenv("ISAAC_EXPERT_DB", str(ROOT / "chroma_db")))
# v2 uses new metadata fields for strict multi-version retrieval.
COLLECTION = os.getenv("ISAAC_EXPERT_COLLECTION", "isaac_expert_bgem3_v2")
EMBED_MODEL = os.getenv("ISAAC_EXPERT_EMBED_MODEL", "bge-m3")
CHAT_MODEL = os.getenv("ISAAC_EXPERT_CHAT_MODEL", "qwen3.5:9b")


def chunks(text: str, size: int = 1900, overlap: int = 220) -> list[str]:
    text = text.strip()
    if not text:
        return []
    output = []
    cursor = 0
    while cursor < len(text):
        end = min(len(text), cursor + size)
        if end < len(text):
            cut = text.rfind("\n", cursor + size // 2, end)
            if cut > cursor:
                end = cut + 1
        output.append(text[cursor:end].strip())
        if end >= len(text):
            break
        cursor = max(cursor + 1, end - overlap)
    return [s for s in output if len(s) >= 15]
