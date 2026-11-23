"""Terminal-first, interactive Isaac Sim/Isaac Lab expert recommender."""
from __future__ import annotations
import argparse
import sys
import chromadb
from expert.common import CHAT_MODEL, COLLECTION, DB_DIR, prepare_docs_index
from expert.recommend import LAB_FOR_SIM, SIM_VERSIONS, recommend


def show_stats():
    prepare_docs_index()
    client = chromadb.PersistentClient(path=str(DB_DIR))
    try:
        coll = client.get_collection(COLLECTION)
        print(f"知識庫：{coll.count()} 個文字片段 ({DB_DIR})")
    except Exception:
        print("知識庫尚未建立。請執行 python -m expert.ingest --docs --max-pages 15")


def answer(question, version, model):
    def show_generation_start():
        print("模型正在產生回答…", file=sys.stderr, flush=True)

    print(f"\n[Isaac Sim {version} | Isaac Lab {LAB_FOR_SIM[version]} | {model}]\n", flush=True)
    print("正在搜尋知識庫…", file=sys.stderr, flush=True)
    try:
        r = recommend(question, version, model=model, on_generation_start=show_generation_start)
    except Exception as exc:
        print(f"[錯誤] {exc}")
        print("確認 Ollama 已啟動、模型已下載、知識庫已索引。")
        return
    print(r.answer)
    if r.sources:
        print("\n--- 本次參考來源 ---")
        for i, s in enumerate(r.sources, 1):
            print(f"[{i}] {s['product']} ({s['version']}) {s['title']}\n    {s['source']}")
    print()


def main():
    p = argparse.ArgumentParser(description="純終端機 Isaac Physics Expert")
    p.add_argument("question", nargs="?", help="單次問題；省略則啟動互動模式")
    p.add_argument("--version", choices=SIM_VERSIONS, default="5.1.0", help="目標 Isaac Sim 版本")
    p.add_argument("--model", default=CHAT_MODEL, help="Ollama 模型，例如 qwen3.5:9b")
    p.add_argument("--stats", action="store_true", help="顯示資料庫大小")
    args = p.parse_args()
    if args.stats:
        show_stats()
        if not args.question:
            return
    if args.question:
        answer(args.question, args.version, args.model)
        return
    version = args.version
    model = args.model
    print("Isaac Physics Expert｜純終端機推薦系統（唯讀）")
    print(f"Isaac Sim {version}｜Isaac Lab {LAB_FOR_SIM[version]}｜{model}")
    print("輸入問題；/version 6.2.0 切換版本；/model qwen3.5:4b 切換模型；/stats；/help；/quit")
    while True:
        try:
            q = input(f"\nIsaac[{version}] > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再見")
            return
        if not q:
            continue
        if q in ("/quit", "/exit", "quit", "exit", "q"):
            print("再見")
            return
        if q in ("/help", "help"):
            print("輸入問題直接提問；/version <5.1.0|6.0.0|6.0.1|6.1.0|6.2.0>；/model <Ollama 名稱>；/stats；/quit")
            continue
        if q == "/stats":
            show_stats()
            continue
        if q.startswith("/version "):
            v = q.split(maxsplit=1)[1].strip()
            if v in SIM_VERSIONS:
                version = v
                print(f"已切換 Isaac Sim {v} / Isaac Lab {LAB_FOR_SIM[v]}")
            else:
                print(f"不支援版本 {v}；可用：{', '.join(SIM_VERSIONS)}")
            continue
        if q.startswith("/model "):
            model = q.split(maxsplit=1)[1].strip()
            print(f"已切換本機模型 {model}")
            continue
        if q.startswith("/"):
            print("未知指令；輸入 /help")
            continue
        answer(q, version, model)


if __name__ == "__main__":
    main()
