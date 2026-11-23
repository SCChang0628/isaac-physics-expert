from __future__ import annotations
import errno
import os
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_DIR = ROOT / "chroma_db"
# v2 uses new metadata fields for strict multi-version retrieval.
DOCS_COLLECTION = "isaac_expert_bgem3_v2"
DOCS_EMBED_MODEL = "bge-m3"
DOCS_ARCHIVE = ROOT / "assets" / "docs-index.tar.xz"
DB_DIR = Path(os.getenv("ISAAC_EXPERT_DB", str(DEFAULT_DB_DIR)))
COLLECTION = os.getenv("ISAAC_EXPERT_COLLECTION", DOCS_COLLECTION)
EMBED_MODEL = os.getenv("ISAAC_EXPERT_EMBED_MODEL", DOCS_EMBED_MODEL)
CHAT_MODEL = os.getenv("ISAAC_EXPERT_CHAT_MODEL", "qwen3.5:9b")


def prepare_docs_index() -> None:
    if (DB_DIR != DEFAULT_DB_DIR or COLLECTION != DOCS_COLLECTION
            or EMBED_MODEL != DOCS_EMBED_MODEL or DB_DIR.exists()
            or not DOCS_ARCHIVE.is_file()):
        return

    with TemporaryDirectory(dir=DB_DIR.parent) as temp:
        with tarfile.open(DOCS_ARCHIVE, "r:xz") as archive:
            archive.extractall(temp, filter="data")
        try:
            Path(temp).rename(DB_DIR)
        except OSError as error:
            # Another process may have installed the index while we extracted it.
            if error.errno not in (errno.EEXIST, errno.ENOTEMPTY) or not DB_DIR.is_dir():
                raise


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
