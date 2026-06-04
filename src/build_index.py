# src/build_index.py

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.config import CHUNK_CSV, INDEX_FILE, META_FILE, EMBED_MODEL_NAME


def build_index():
    df = pd.read_csv(CHUNK_CSV)

    required_cols = ["title", "section", "chunk_text"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"缺少必要欄位: {col}")

    df["chunk_text"] = df["chunk_text"].fillna("").astype(str)
    df = df[df["chunk_text"].str.strip() != ""].reset_index(drop=True)

    print("Loaded chunks:", df.shape)

    print("Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL_NAME)

    texts = df["chunk_text"].tolist()

    print("Encoding texts...")
    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    embeddings = np.array(embeddings, dtype="float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    df.to_csv(META_FILE, index=False, encoding="utf-8-sig")

    print(f"Saved index -> {INDEX_FILE}")
    print(f"Saved meta  -> {META_FILE}")


if __name__ == "__main__":
    build_index()