# src/retriever.py

import re
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

from src.config import INDEX_FILE, META_FILE, EMBED_MODEL_NAME


class WikiRetriever:
    def __init__(self):
        print("Loading metadata...")
        self.df = pd.read_csv(META_FILE)

        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_FILE)

        print("Loading embedding model...")
        self.embed_model = SentenceTransformer(EMBED_MODEL_NAME)

        self.known_titles = sorted(
            self.df["title"].dropna().astype(str).unique().tolist()
        )

    def detect_title_in_query(self, query: str):
        for title in self.known_titles:
            if title in query:
                return title
        return None

    def keyword_score(self, query: str, text: str) -> int:
        score = 0
        q_tokens = re.findall(r"[\u4e00-\u9fffA-Za-z0-9]+", query)

        for tok in q_tokens:
            if tok and tok in text:
                score += 1

        return score

    def retrieve(self, query: str, top_k: int = 5) -> pd.DataFrame:
        q_emb = self.embed_model.encode(
            [query],
            normalize_embeddings=True
        )

        q_emb = np.array(q_emb, dtype="float32")

        search_k = min(20, len(self.df))
        scores, ids = self.index.search(q_emb, search_k)

        cand_df = self.df.iloc[ids[0]].copy().reset_index(drop=True)
        cand_df["dense_score"] = scores[0]

        target_title = self.detect_title_in_query(query)

        if target_title is not None:
            title_df = cand_df[cand_df["title"] == target_title].copy()
            if len(title_df) >= 2:
                cand_df = title_df.reset_index(drop=True)

        cand_df["keyword_score"] = cand_df["chunk_text"].apply(
            lambda x: self.keyword_score(query, str(x))
        )

        cand_df["final_score"] = (
            cand_df["dense_score"] + 0.05 * cand_df["keyword_score"]
        )

        cand_df = (
            cand_df
            .sort_values("final_score", ascending=False)
            .head(top_k)
            .reset_index(drop=True)
        )

        return cand_df