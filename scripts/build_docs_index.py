"""Package a ChromaDB snapshot containing only configured official sources."""

from __future__ import annotations

import json
from pathlib import Path
import tarfile
from tempfile import TemporaryDirectory

import chromadb

from expert.common import (
    COLLECTION, DB_DIR, DOCS_ARCHIVE, DOCS_COLLECTION, DOCS_EMBED_MODEL, EMBED_MODEL, ROOT,
)
from expert.ingest import in_source


def main():
    if EMBED_MODEL != DOCS_EMBED_MODEL:
        raise ValueError(f"The starter index requires {DOCS_EMBED_MODEL} embeddings.")
    sources = json.loads((ROOT / "config" / "sources.json").read_text(encoding="utf-8"))
    source = chromadb.PersistentClient(path=str(DB_DIR)).get_collection(COLLECTION)
    DOCS_ARCHIVE.parent.mkdir(exist_ok=True)

    with TemporaryDirectory(dir=DOCS_ARCHIVE.parent) as temp:
        snapshot = Path(temp) / "snapshot"
        target = chromadb.PersistentClient(path=str(snapshot)).create_collection(
            name=DOCS_COLLECTION, metadata={"hnsw:space": "cosine"}
        )
        offset = 0
        while True:
            batch = source.get(
                where={"kind": "official_docs"}, limit=250, offset=offset,
                include=["documents", "embeddings", "metadatas"],
            )
            if not batch["ids"]:
                break
            for metadata in batch["metadatas"]:
                if not any(
                    all(metadata[key] == group[key] for key in ("version", "product", "family"))
                    and in_source(metadata["source"], group["base"])
                    for group in sources
                ):
                    raise ValueError("An indexed document does not match the official source catalog.")
            target.add(
                ids=batch["ids"], documents=batch["documents"],
                embeddings=batch["embeddings"], metadatas=batch["metadatas"],
            )
            offset += len(batch["ids"])

        if not offset:
            raise ValueError("The local index has no official documents to package.")

        archive_file = Path(temp) / DOCS_ARCHIVE.name
        with tarfile.open(archive_file, "w:xz", preset=8) as archive:
            for path in sorted(snapshot.iterdir()):
                archive.add(path, arcname=path.name)
        archive_file.replace(DOCS_ARCHIVE)
    print(f"Packaged {offset:,} official documentation chunks in {DOCS_ARCHIVE}.")


if __name__ == "__main__":
    main()
