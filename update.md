# Updating Isaac Physics Expert

## Git installation

From your existing repository:

```bash
git pull --ff-only
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If `.venv` is missing, create it with `python3 -m venv .venv` before activating it.

## Legacy ZIP upgrade

If you have `isaac-physics-expert-cli-update.zip`, back up any locally edited project files before extracting. The archive overwrites matching files.

```bash
unzip -o ~/Downloads/isaac-physics-expert-cli-update.zip -d ~
cd ~/isaac-physics-expert
```

Activate the virtual environment and reinstall the Python dependencies as shown above. The CLI runs with `./isaac-expert` and no longer requires Streamlit.

## Refresh the local documentation index

To refresh your local copy, run this with Ollama running and the virtual environment active:

```bash
python -m expert.ingest --docs --refresh --max-pages 100
```

`--max-pages` sets the limit per source group. Use `--list-sources` to find group IDs and `--only` to refresh selected groups.

## Package an updated index

Maintainers can export the official documentation from their local index using the existing embeddings:

```bash
python -m scripts.build_docs_index
```

Include the resulting `assets/docs-index.tar.xz` when publishing. Keep `chroma_db/` local. Existing installations continue using their local index.
