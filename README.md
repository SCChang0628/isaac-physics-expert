# Isaac Physics Expert — CLI / RAG / 多版本官方文件

**純終端機、唯讀、在本機 Ollama 運行**的 Isaac Sim / Isaac Lab / USD / PhysX 專家推薦系統。
不會啟動 Isaac Sim、不會幫你跑實驗、不會改動 USD 或原始碼。

## 0. 更新舊版本

從 `isaac-physics-expert-cli-update.zip` 覆蓋到家目錄：

```bash
unzip -o ~/Downloads/isaac-physics-expert-cli-update.zip -d ~
cd ~/isaac-physics-expert
source .venv/bin/activate
python -m pip install -r requirements.txt
```

> 若在專案中找不到 `.venv`，先用 `python3 -m venv .venv` 建立。新版不需要 Streamlit；舊套件留在虛擬環境也不影響 CLI。

## 1. 初始化（Ubuntu 24.04）

```bash
sudo apt update
sudo apt install -y git curl python3-venv
# 尚未安裝 Ollama 才需要執行：
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
ollama pull qwen3.5:9b
ollama pull bge-m3
cd ~/isaac-physics-expert
python3 -m venv .venv    # 已存在可以略過
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 2. 建立官方文件 RAG（重要）

先查看索引清單：

```bash
python -m expert.ingest --list-sources
```

先小批量驗證網路、Embedding、資料庫功能，每個版本／資料庫來源最多 15 頁：

```bash
python -m expert.ingest --docs --max-pages 15
```

若成功，再擴充至每組最多 100 頁（可能耗時較久，請保持網路連線）：

```bash
python -m expert.ingest --docs --max-pages 100
```

下載和索引不使用 Isaac Sim 物理引擎。重新執行會略過已索引的網址；加 `--refresh` 才會重建舊內容。若官方 API 已修改，應加 `--refresh` 更新。

特定版本增量擴充：

```bash
python -m expert.ingest --docs --only isaac-sim-5.1.0 isaac-lab-2.3 --max-pages 120
python -m expert.ingest --docs --only isaac-sim-6.2.0 isaac-lab-3.0-ga --max-pages 120
```

註：官方網站有時會移動頁面或回傳 404，出現 `[warn]` 不表示所有文件都成功。請檢查索引成功頁數和警告。`--max-pages 100` 表示**每來源最多 100 頁，不是抓取整站所有文件**；HTML sidebar 與官方 `llms.txt` 是本工具的版本化文件探索入口，支援逐步擴充。

## 3. 加入自己的工程專案（唯讀）

```bash
python -m expert.ingest --oht ~/OHT_Project_ros --oht-version 5.1.0
python -m expert.ingest --dog ~/jetson_dog --dog-version 6.1.0
python -m expert.ingest --notes ./notes
```

ASCII USDA 僅使用文字段落擷取，不代表 USD 全部 References 已解析。完整 Stage 讀取可用原專案附帶的 `scripts/export_usd_physics.py` 搭配 Isaac Sim 的 Python 執行，再將擷取結果索引至 private notes。請勿將專案中敏感資訊推上公開 GitHub。

## 4. 終端機互動問答

```bash
./isaac-expert
```

範例：

```text
Isaac[5.1.0] > 高速過彎時 OHT 彈飛，應優先調整哪些 PhysX 參數？
Isaac[5.1.0] > /version 6.2.0
Isaac[6.2.0] > Isaac Lab 3.0 GA 的 PhysxCfg 如何設定？
Isaac[6.2.0] > /model qwen3.5:4b
Isaac[6.2.0] > /stats
Isaac[6.2.0] > /quit
```

單次問題：

```bash
./isaac-expert --version 5.1.0 "Triangle Mesh 與 SDF 接觸時如何排查不穩定？"
./isaac-expert --version 6.2.0 "Isaac Lab PhysX 與 Newton 有什麼差異？"
```

`/version` 可選 `5.1.0`、`6.0.0`、`6.0.1`、`6.1.0`、`6.2.0`。

## 5. 官方知識庫版本規劃

| Isaac Sim | Isaac Lab 文件 | 備註 |
|---|---|---|
| 5.1.0 | 2.3.x | 2.3 系列主要針對 5.1 |
| 6.0.0 | 3.0.0 beta | 歷史 EA/beta 文件，須核對實際安裝版 |
| 6.0.1 | 3.0.0 beta2 | 歷史 beta 文件，須核對實際安裝版 |
| 6.1.0 | 3.0.0 EA | NVIDIA 相容性表列示 |
| 6.2.0 | 3.0.0 GA | NVIDIA 相容性表列示 |

除此之外還索引 OpenUSD Physics API、Omniverse Physics 107.3/110.1、PhysX SDK 5.6.1 和 SDK 5.8.0 參考資料。PhysX SDK 與 USD API 不代表 Isaac Sim 所有版本行為完全一致；推薦時以版本指定的 Isaac Sim 文檔為優先。

官方相容性表：https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/compatibility.html

官方 Lab 版本文件：https://docs.nvidia.com/isaaclab/3.0/llms.txt 、https://docs.nvidia.com/isaaclab/2.3/llms.txt

完整來源及頁數配額可自行修改 `config/sources.json`。

## 6. 同步 GitHub

確保 `.gitignore` 已排除 `chroma_db/`, `data/`, `.venv/` 等：

```bash
cd ~/isaac-physics-expert
git status
git add README.md requirements.txt .gitignore config/ expert/ isaac-expert tests/
git commit -m "Add terminal-only Isaac expert and multi-version RAG"
git push
```

**GitHub 只存程式碼和文件來源清單**；索引資料庫、模型權重以及私人 OHT/機器狗檔案留在本機。

## 7. 錯誤排查

- `Connection refused`：`sudo systemctl status ollama`。
- `model not found`：`ollama pull qwen3.5:9b && ollama pull bge-m3`。
- `知識庫尚未建立`：`python -m expert.ingest --docs --max-pages 15`。
- `404/403`：文件網址可能改變；依印出的 `[warn]` 檢查 `config/sources.json`。
- `CUDA out of memory`：改用 `./isaac-expert --model qwen3.5:4b`，並避免與大型 Isaac Sim 場景同時運行。
- `python: module not found`：在專案根目錄執行 `source .venv/bin/activate` 並 `pip install -r requirements.txt`。

這是可擴充的推薦系統，不是自行訓練的新 LLM 權重。未來可收集人工確認的問答，另行進行 LoRA 微調。
