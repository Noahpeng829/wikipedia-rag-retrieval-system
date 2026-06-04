# src/chat_cli.py

from src.config import TOP_K, EMBED_MODEL_NAME
from src.retriever import WikiRetriever


def format_retrieval_answer(query, result_df):
    if result_df.empty:
        return "找不到相關資料。"

    lines = []
    lines.append(f"問題：{query}")
    lines.append("")
    lines.append("以下是系統檢索到的相關資料：")
    lines.append("")

    for i, row in result_df.head(3).iterrows():
        lines.append(f"[參考 {i + 1}] {row['title']} / {row['section']}")
        lines.append(str(row["chunk_text"])[:500])
        lines.append("")

    return "\n".join(lines)


def pretty_print_results(result_df):
    if result_df.empty:
        print("No retrieval results.")
        return

    show_cols = [
        "title",
        "section",
        "chunk_id",
        "dense_score",
        "keyword_score",
        "final_score"
    ]

    print(result_df[show_cols])


def chat():
    retriever = WikiRetriever()

    print("\n=== Local Wikipedia RAG Retrieval Demo ===")
    print(f"Embedding model: {EMBED_MODEL_NAME}")
    print("模式：不使用付費 LLM，只展示本地檢索與來源引用")
    print("輸入 q / quit 離開\n")

    while True:
        query = input("你問：").strip()

        if query.lower() in ["q", "quit", "exit"]:
            print("結束對話。")
            break

        if not query:
            continue

        result_df = retriever.retrieve(query, top_k=TOP_K)

        print("\n--- Top Retrieved Chunks ---")
        pretty_print_results(result_df)

        print("\n=== 回答 / 檢索摘要 ===")
        print(format_retrieval_answer(query, result_df))

        print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    chat()