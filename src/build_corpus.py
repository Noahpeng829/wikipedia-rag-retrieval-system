# src/build_corpus.py

import time
import pandas as pd

from src.config import TITLES, SECTION_CSV, CHUNK_CSV
from src.wiki_fetcher import get_wiki_extract
from src.text_processor import split_into_sections, chunk_text, is_bad_text


def build_corpus():
    section_rows = []

    for title in TITLES:
        try:
            result = get_wiki_extract(title)
            rows = split_into_sections(
                raw_text=result["extract"],
                title=result["title"],
                pageid=result["pageid"]
            )

            section_rows.extend(rows)
            print(f"[OK] {title} -> {len(rows)} sections")
            time.sleep(1.0)

        except Exception as e:
            print(f"[FAIL] {title}: {e}")

    df_sections = pd.DataFrame(section_rows)

    if df_sections.empty:
        raise ValueError("沒有成功取得任何 section 資料")

    df_sections.to_csv(SECTION_CSV, index=False, encoding="utf-8-sig")
    print(f"Saved sections -> {SECTION_CSV}")

    chunk_rows = []

    for _, row in df_sections.iterrows():
        chunks = chunk_text(row["text"])

        for i, ch in enumerate(chunks):
            if is_bad_text(ch):
                continue

            chunk_rows.append({
                "pageid": row["pageid"],
                "title": row["title"],
                "section": row["section"],
                "chunk_id": i,
                "chunk_text": ch
            })

    df_chunks = pd.DataFrame(chunk_rows)
    df_chunks.to_csv(CHUNK_CSV, index=False, encoding="utf-8-sig")

    print(f"Saved chunks -> {CHUNK_CSV}")
    print("Chunks shape:", df_chunks.shape)


if __name__ == "__main__":
    build_corpus()