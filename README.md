# Wikipedia RAG Retrieval System

本專案是一個低成本、零付費 API 的中文 Wikipedia RAG 檢索系統練習專案。
專案重點不在於串接付費 LLM API，而是完整實作 RAG 系統中最核心的資料處理、向量索引、檢索策略與評估流程。

## 專案目標

本專案希望建立一套可重現、可維護、可評估的 RAG Retrieval Pipeline，流程包含：

```text
Wikipedia API
→ 文字清理
→ Section 切分
→ Chunk 切分
→ Embedding
→ FAISS 向量索引
→ Retrieval
→ Evaluation
```

目前專案聚焦於 Retrieval-first 架構，未使用 OpenAI API 或其他付費 LLM API。未來若有資源，可再接入本地 LLM 或雲端 LLM，形成完整的 Retrieval-Augmented Generation 問答系統。

---

## 專案特色

* 使用 MediaWiki API 自動抓取中文 Wikipedia 條目
* 支援多篇 Wikipedia 條目建立知識庫
* 依照 Wikipedia section 結構切分文章
* 使用 chunk size 與 overlap 建立檢索片段
* 使用 `BAAI/bge-m3` 建立中文語意向量
* 使用 FAISS 建立本地向量索引
* 加入 title-aware filtering，降低多實體查詢錯誤
* 加入 keyword bonus，補強 embedding 對關鍵詞的檢索能力
* 建立 50 題人工評估集
* 使用 Hit@K、Precision@K、Recall@K、MRR、MAP、nDCG 等指標評估 retrieval 表現
* 輸出錯誤案例，方便後續分析與優化

---

## 專案架構

```text
wikipedia-rag-retrieval-system/
│
├─ main.py
│  專案主要入口，啟動命令列互動查詢介面。
│
├─ requirements.txt
│  記錄專案需要安裝的 Python 套件。
│
├─ .gitignore
│  設定不需要上傳 GitHub 的檔案，例如 .venv、cache、index 檔。
│
├─ src/
│  ├─ config.py
│  │  集中管理專案參數，例如 Wikipedia 條目、chunk size、檔案路徑與 top_k。
│  │
│  ├─ wiki_fetcher.py
│  │  使用 MediaWiki API 抓取指定 Wikipedia 條目的純文字內容。
│  │
│  ├─ text_processor.py
│  │  負責文字清理、section 切分、chunk 切分，以及過濾不適合建索引的文字。
│  │
│  ├─ build_corpus.py
│  │  建立語料庫流程：抓 Wikipedia → 切 section → 切 chunk → 輸出 CSV。
│  │
│  ├─ build_index.py
│  │  將 chunk 轉成 embedding，建立 FAISS 向量索引，並儲存 metadata。
│  │
│  ├─ retriever.py
│  │  專案核心檢索模組，負責載入 FAISS、embedding model，並執行 dense retrieval、title filtering、keyword bonus 排序。
│  │
│  ├─ chat_cli.py
│  │  命令列互動查詢介面，讓使用者輸入問題並顯示 top-k 檢索結果與來源片段。
│  │
│  └─ evaluate.py
│     執行 retrieval 評估，計算 Hit@K、Precision@K、Recall@K、MRR、MAP、nDCG、Noise、Duplicate Rate，並輸出錯誤案例。
│
├─ data/
│  ├─ processed/
│  │  存放清理後的 section 和 chunk CSV。
│  │
│  └─ index/
│     存放 FAISS index 和 chunk metadata。
│
├─ outputs/
│  └─ eval/
│     存放評估結果、總表、錯誤案例與分主題績效。
│
└─ notebooks/
   保留原始 Jupyter 實驗紀錄。
```

---

## 使用技術

* Python
* Requests
* Pandas
* NumPy
* Sentence Transformers
* BAAI/bge-m3
* FAISS
* MediaWiki API

---

## 安裝方式

建議使用 Python 虛擬環境。

```bash
python -m venv .venv
```

Windows 啟動虛擬環境：

```bash
.venv\Scripts\activate
```

安裝套件：

```bash
pip install -r requirements.txt
```

---

## 執行流程

### 1. 建立 Wikipedia 語料庫

```bash
python -m src.build_corpus
```

此步驟會：

* 呼叫 Wikipedia API
* 取得指定條目內容
* 切分 section
* 切分 chunk
* 輸出處理後 CSV

輸出檔案：

```text
data/processed/wiki_sections_clean.csv
data/processed/wiki_chunks_clean.csv
```

---

### 2. 建立 FAISS 向量索引

```bash
python -m src.build_index
```

此步驟會：

* 載入 chunk CSV
* 使用 bge-m3 建立 embedding
* 建立 FAISS IndexFlatIP 索引
* 儲存 index 與 metadata

輸出檔案：

```text
data/index/wiki_clean.index
data/index/wiki_chunks_clean_meta.csv
```

---

### 3. 啟動命令列查詢介面

```bash
python main.py
```

或：

```bash
python -m src.chat_cli
```

使用者可以輸入問題，系統會回傳：

* Top-k 檢索結果
* 文章標題
* 章節
* chunk id
* dense score
* keyword score
* final score
* 來源內容片段

---

### 4. 執行 Retrieval 評估

```bash
python -m src.evaluate
```

此步驟會執行 50 題人工評估集，並輸出整體績效、分主題績效與錯誤案例。

輸出檔案：

```text
outputs/eval/rag_eval_results.csv
outputs/eval/rag_eval_summary.csv
outputs/eval/rag_eval_errors.csv
outputs/eval/rag_eval_group_summary.csv
```

---

## Retrieval 策略

本專案目前使用以下檢索策略：

### 1. Dense Retrieval

使用 `BAAI/bge-m3` 將 query 與 chunk 轉換為 embedding，並使用 FAISS 進行向量相似度搜尋。

### 2. Title-aware Filtering

若使用者問題中包含已知 Wikipedia 條目名稱，例如「東京都」，系統會優先保留該 title 對應的 chunk，降低檢索焦點偏移。

### 3. Keyword Bonus

系統會計算 query 中的關鍵詞是否出現在 chunk 內，並將 keyword score 加入 final score。

目前 final score 計算方式：

```text
final_score = dense_score + 0.05 * keyword_score
```

---

## 評估方法

本專案建立 50 題人工評估問題，並以 section-level relevance 作為判斷標準。
也就是說，系統不只要找對文章 title，也要找對對應 section。

評估指標包含：

| 指標             | 說明                          |
| -------------- | --------------------------- |
| Hit@K          | Top-K 內是否命中正確答案             |
| Precision@K    | Top-K 中相關結果比例               |
| Recall@K       | 是否在 Top-K 中找到正確目標           |
| MRR            | 第一個正確結果排名的倒數                |
| MAP            | 平均精準率                       |
| nDCG@K         | 考慮排名位置的檢索品質                 |
| Noise@K        | Top-K 中不相關內容比例              |
| Duplicate Rate | Top-K 中重複 title/section 的比例 |

---

## 評估結果

目前使用 50 題 section-level retrieval benchmark 進行測試。

| Scope            | Hit@1 | Hit@3 | Hit@5 |  MRR |   MAP | nDCG@5 |
| ---------------- | ----: | ----: | ----: | ---: | ----: | -----: |
| Overall          |  0.68 |  0.72 |  0.72 | 0.70 | 0.621 |  0.666 |
| Japan            |  0.92 |  0.96 |  0.96 | 0.94 | 0.861 |  0.906 |
| Tokyo Metropolis |  0.44 |  0.48 |  0.48 | 0.46 | 0.380 |  0.426 |

---

## 錯誤分析

從錯誤案例可以觀察到，系統主要錯誤集中在多實體查詢，例如：

```text
東京都是不是日本的首都所在地？
東京都屬於日本的哪一級行政區？
東京都位於日本本州嗎？
東京都在日本的政治與行政上有何地位？
```

這些問題同時包含「東京都」與「日本」，系統容易將查詢焦點偏移到較上位的「日本」條目，導致檢索到：

```text
日本 / 主要城市
日本 / 行政區劃
日本 / Introduction
```

而不是：

```text
東京都 / Introduction
東京都 / 行政區劃
```

此現象反映目前系統仍存在 entity focus drift 問題，也就是多實體查詢時，retriever 可能無法正確辨識主要查詢對象。

---

## 專案限制

目前專案仍有以下限制：

1. 尚未接入付費 LLM API 或本地 LLM 生成答案。
2. 目前主要展示 retrieval pipeline，而非完整生成式問答系統。
3. 多實體查詢時仍可能發生查詢主體偏移。
4. 評估集規模仍小，且部分問題屬於關係推論題，對純 retrieval 任務較嚴格。
5. 目前尚未加入 BM25、Cross-Encoder Reranker 或 Query Rewrite。

---

## 未來優化方向

後續可優化方向包含：

### 1. Hybrid Retrieval

加入 BM25 sparse retrieval，與 FAISS dense retrieval 結合。

```text
final_score = α * dense_score + β * bm25_score
```

### 2. Query Rewrite

針對多實體查詢做 query expansion，例如：

```text
東京都是不是日本的一級行政區？
→ 東京都 行政區劃 一級行政區 首都所在地
```

### 3. Entity / Title Boosting

當 query 中明確出現某個 title 時，提高該 title chunk 的排序權重。

### 4. Section-aware Boosting

根據 query 關鍵字提升對應 section 權重，例如：

* 人口 → 人口 section
* 行政 → 行政區劃 section
* 地理 / 位於 → 地理 section
* 首都 → Introduction / 主要城市 section

### 5. Reranker

加入 Cross-Encoder Reranker，對 FAISS 取回的 top-20 chunk 重新排序。

### 6. Web Demo

使用 Streamlit 或 FastAPI 建立簡易展示頁面，支援：

* 問題輸入
* Top-k chunk 顯示
* 來源引用
* 檢索分數顯示
* 錯誤案例分析

---

## 專案定位

本專案不是完整商業級 RAG 問答系統，而是一個 retrieval-first 的 RAG 學習專案。
重點在於展示：

* 如何建立知識庫
* 如何進行 chunking
* 如何建立向量索引
* 如何設計檢索策略
* 如何用指標評估 retrieval 品質
* 如何分析錯誤案例並提出改善方向

在有限資源下，本專案不依賴付費 API，而是專注於 RAG 系統中可維護、可重現、可評估的核心流程。

---

## 執行指令總整理

```bash
# 建立語料庫
python -m src.build_corpus

# 建立 FAISS index
python -m src.build_index

# 啟動互動查詢
python main.py

# 執行評估
python -m src.evaluate
```

---

## Author

Noah Peng
Wikipedia RAG Retrieval System Practice Project
