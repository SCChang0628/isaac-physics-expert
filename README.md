# Isaac Physics Expert

Ask physics questions about Isaac Sim, Isaac Lab, PhysX, and OpenUSD from your terminal. The tool runs locally with Ollama and cites the documentation it retrieves.

## 1. Download and install on Ubuntu 24.04

```bash
sudo apt update
sudo apt install -y git curl python3-venv
git clone https://github.com/SCChang0628/isaac-physics-expert.git
cd isaac-physics-expert
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If needed, install Ollama using the [Ollama Linux guide](https://docs.ollama.com/linux).

```bash
sudo systemctl start ollama
ollama pull qwen3.5:9b
ollama pull bge-m3
```

## 2. Ask a question

The bundled documentation index is unpacked automatically on first use.

```bash
./isaac-expert
```

Type a question and press Enter. Use `/version 6.2.0` to switch versions, `/stats` to check the local index, or `/quit` to exit. Responses are in Traditional Chinese.

For a single question:

```bash
./isaac-expert --version 5.1.0 "How can I troubleshoot unstable contacts?"
```

Supported Isaac Sim versions are `5.1.0` (default), `6.0.0`, `6.0.1`, `6.1.0`, and `6.2.0`.

## 3. Ask about engineering examples

The repo includes [Isaac Sim 5.1.0 engineering examples](notes/isaac-examples/5.1.0) on Fabric and USD writeback, live transforms, rigid-body readiness, payload handling, ROS 2 telemetry, and runtime performance. The CLI automatically indexes the examples for the selected Isaac Sim version on the first question and refreshes changed examples after updates. You can read the Markdown files directly on GitHub. The [Fabric writeback test](notes/isaac-examples/5.1.0/fabric-writeback-test.md) runs in Isaac Sim 5.1.0 using an in-memory scene.

```bash
./isaac-expert --version 5.1.0 "如何用自由落體測試確認 Fabric 的姿態有變，而 USD root layer 沒改變？請給完整測試程式。"
```

To include your own notes, run `python -m expert.ingest --notes /path/to/notes`. Run `python -m expert.ingest --help` for more indexing options.

## Updates

See [update.md](update.md) for upgrade and documentation refresh instructions.
