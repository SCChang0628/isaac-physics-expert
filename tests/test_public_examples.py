from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

import chromadb

from expert import ingest
from expert.common import chunks


class PublicExampleTests(TestCase):
    def test_sync_is_versioned_and_updates_only_public_examples(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            examples = root / "notes" / "isaac-examples"
            folder = examples / "5.1.0"
            folder.mkdir(parents=True)
            note = folder / "fabric.md"
            note.write_text("# Fabric\n\nOriginal public example.", encoding="utf-8")
            collection = chromadb.EphemeralClient().create_collection("test_public_examples")
            collection.add(ids=["private"], documents=["Private example"], embeddings=[[1, 0]],
                           metadatas=[{"family": "user_note", "version": "all"}])
            self.addCleanup(chromadb.EphemeralClient().delete_collection, collection.name)

            def embed(*, model, input):
                return SimpleNamespace(embeddings=[[1, 0] for _ in input])

            with (patch.object(ingest, "ROOT", root),
                  patch.object(ingest, "PUBLIC_EXAMPLES", examples),
                  patch.object(ingest.ollama, "embed", side_effect=embed) as embedding):
                self.assertFalse(ingest.sync_public_examples(collection, "6.0.0"))
                embedding.assert_not_called()
                self.assertTrue(ingest.sync_public_examples(collection, "5.1.0"))
                self.assertTrue(ingest.sync_public_examples(collection, "5.1.0"))
                embedding.assert_called_once()
                public = collection.get(where={"family": ingest.PUBLIC_EXAMPLE_FAMILY})
                self.assertEqual(public["metadatas"][0]["source"], note.relative_to(root).as_posix())
                self.assertEqual(public["metadatas"][0]["version"], "5.1.0")

                note.write_text("# Fabric\n\nRevised public example.", encoding="utf-8")
                self.assertTrue(ingest.sync_public_examples(collection, "5.1.0"))
                public = collection.get(where={"family": ingest.PUBLIC_EXAMPLE_FAMILY})
                self.assertEqual(public["documents"], ["# Fabric\n\nRevised public example."])

                note.unlink()
                self.assertFalse(ingest.sync_public_examples(collection, "5.1.0"))
                self.assertEqual(collection.get()["ids"], ["private"])

    def test_writeback_example_stays_whole_in_the_index(self):
        note = ingest.PUBLIC_EXAMPLES / "5.1.0" / "fabric-writeback-test.md"
        parts = chunks(note.read_text(encoding="utf-8"))
        self.assertEqual(len(parts), 1)
        _, script, _ = parts[0].split("```")
        compile(script.removeprefix("python\n"), str(note), "exec")
