# Wikipedia RAG 檢索系統

[English](README.md) | [繁體中文](README_zh.md)

## 專案概述

本專案實作了一套以檢索為核心（Retrieval-first）的 Retrieval-Augmented Generation（RAG）流程，資料來源為中文 Wikipedia。

與許多僅著重於串接大型語言模型（LLM）API 的 RAG 範例不同，本專案聚焦於 RAG 系統最核心且最關鍵的檢索層（Retrieval Layer），包含：

* 知識庫建置
* 文字前處理
* Section-aware Chunking
* Embedding 向量生成
* 向量搜尋
* 檢索策略優化
* 檢索績效評估
* 錯誤案例分析

整個系統設計目標為：

* 可重現（Reproducible）
* 可維護（Maintainable）
* 可部署（Deployable）
* 不依賴任何付費 API

### 專案重點

* Retrieval Pipeline 設計
* Retrieval 評估框架
* Retrieval 錯誤分析
* Retrieval 策略優化
* FastAPI 應用封裝
---

## Demo

![Demo](docs/demo.png)

## 專案成果

* 建立完整 Wikipedia Retrieval Pipeline
* 使用 FAISS 建立本地語意向量搜尋系統
* 使用 BGE-M3 建立中文語意檢索向量
* 建立 50 題 Section-level Benchmark Dataset
* 實作 Retrieval Evaluation Framework
* 使用 FastAPI 與簡易 Web UI 封裝成可操作的展示系統

主要結果：

| 指標 | 分數 |
|------|-----:|
| Hit@1 | 0.68 |
| Hit@3 | 0.72 |
| MRR | 0.70 |
| MAP | 0.621 |
| nDCG@5 | 0.666 |
---

## 專案動機

許多 RAG 初學者專案往往只專注於串接 OpenAI 或其他大型語言模型 API。

然而在實務上：

> Retrieval Quality 決定了 RAG 系統能力的上限。

如果檢索不到正確資訊，即使使用再強大的 LLM，也無法產生正確答案。

因此本專案希望深入研究：

* 如何建立知識庫
* Chunking 策略如何影響檢索品質
* Embedding 檢索的運作方式
* 如何客觀評估檢索效能
* 如何分析檢索失敗案例並持續改善

---

## 為什麼這個專案重要

在 Retrieval-Augmented Generation 系統中，語言模型負責生成答案，而檢索層負責提供可參考的知識來源。

如果檢索到的內容錯誤或不完整，即使使用強大的大型語言模型，也可能產生錯誤答案或幻覺內容。

因此，本專案先聚焦於 Retrieval Quality 的設計、評估與錯誤分析，再保留未來整合生成層的擴充空間。

這讓本專案不只是單純串接 LLM API，而是更接近實際 RAG 系統開發時會遇到的核心工程問題。

---

## 系統架構

![Architecture](docs/architecture.png)

系統主要分為兩條流程：

### 離線知識庫建置流程（Offline Knowledge Base Construction）

負責：

* 擷取 Wikipedia 條目
* 文字清理與切分
* 建立 Embedding
* 建立 FAISS 向量索引

### 線上檢索流程（Online Retrieval Pipeline）

負責：

* 接收使用者查詢
* 搜尋相關 Chunk
* 套用 Title-aware Filtering
* 套用 Keyword Bonus Ranking
* 回傳 Top-K 檢索結果

---

## 評估結果

本專案建立了 50 題人工設計的 Benchmark 問題，用於評估 Section-level Retrieval 效能。

![Evaluation Result](docs/evaluation_result.png)

主要指標如下：

| 指標     |    分數 |
| ------ | ----: |
| Hit@1  |  0.68 |
| Hit@3  |  0.72 |
| Hit@5  |  0.72 |
| MRR    |  0.70 |
| MAP    | 0.621 |
| nDCG@5 | 0.666 |

評估結果顯示：

* 單實體查詢（Single Entity Query）具有良好的檢索能力
* 多實體查詢（Multi-Entity Query）仍存在改善空間
* 提供了明確的優化方向與後續研究議題

---

## 主要功能

### 知識庫建置

* 使用 MediaWiki API 抓取中文 Wikipedia 條目
* 支援多篇文章建立知識庫
* 自動移除低品質段落與噪音內容
* 清理 Wikipedia 特有格式與標記

### 文字處理

* Section-based 文件切分
* Chunk Overlap 重疊切分
* 可調整 Chunk Size 與 Overlap

### 檢索系統

* Embedding Dense Retrieval
* BGE-M3 多語言向量模型
* FAISS 本地向量搜尋
* Title-aware Filtering
* Keyword-enhanced Ranking

### 評估系統

* 自建 Benchmark Dataset
* Section-level Relevance 評估
* 支援以下指標：

  * Hit@K
  * Precision@K
  * Recall@K
  * MRR
  * MAP
  * nDCG
  * Noise Rate
  * Duplicate Rate

### 部署

* FastAPI Backend
* Web 互動介面
* REST API
* 完全本地部署

---

## 技術架構

### Backend

* Python
* FastAPI

### Data Processing

* Pandas
* NumPy

### Retrieval

* Sentence Transformers
* BAAI/bge-m3
* FAISS

### Data Source

* MediaWiki API

### Frontend

* HTML
* CSS
* JavaScript

---

## 專案結構

```text
wikipedia-rag-retrieval-system/
│
├── main.py
├── requirements.txt
├── README.md
├── README_zh.md
│
├── src/
│   ├── api.py
│   ├── config.py
│   ├── wiki_fetcher.py
│   ├── text_processor.py
│   ├── build_corpus.py
│   ├── build_index.py
│   ├── retriever.py
│   ├── chat_cli.py
│   └── evaluate.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── data/
│   ├── processed/
│   └── index/
│
├── outputs/
│   └── eval/
│
└── docs/
    ├── architecture.png
    ├── demo.png
    └── evaluation_result.png
```

---

## 安裝方式

建立虛擬環境：

```bash
python -m venv .venv
```

Windows 啟用：

```bash
.venv\Scripts\activate
```

安裝套件：

```bash
pip install -r requirements.txt
```

---

## 使用方式

### Step 1：建立語料庫

```bash
python -m src.build_corpus
```

功能：

* 下載 Wikipedia 條目
* 切分 Section
* 建立 Chunk
* 輸出處理後 CSV

輸出：

```text
data/processed/wiki_sections_clean.csv
data/processed/wiki_chunks_clean.csv
```

---

### Step 2：建立向量索引

```bash
python -m src.build_index
```

功能：

* 建立 Embedding
* 建立 FAISS Index
* 儲存 Metadata

輸出：

```text
data/index/wiki_clean.index
data/index/wiki_chunks_clean_meta.csv
```

---

### Step 3：啟動 Web 系統

```bash
uvicorn src.api:app --reload
```

開啟：

```text
http://127.0.0.1:8000
```

Swagger API 文件：

```text
http://127.0.0.1:8000/docs
```

---

### Step 4：執行評估

```bash
python -m src.evaluate
```

輸出：

```text
outputs/eval/rag_eval_results.csv
outputs/eval/rag_eval_summary.csv
outputs/eval/rag_eval_errors.csv
outputs/eval/rag_eval_group_summary.csv
```

---

## 檢索策略

### Dense Retrieval

使用 BGE-M3 將 Query 與 Chunk 轉換為向量，並透過 FAISS 進行相似度搜尋。

### Title-aware Filtering

若 Query 中出現已知 Wikipedia 條目名稱，系統會優先保留該條目的 Chunk。

例如：

```text
東京都是不是日本的一級行政區？
```

系統將優先檢索：

```text
東京都
```

而非其他無關文章。

### Keyword Bonus Ranking

系統會根據 Query 關鍵詞與 Chunk 的匹配程度額外加分。

```text
final_score = dense_score + 0.05 × keyword_score
```

可提升實體名稱相關問題的穩定性。

---

## 詳細評估結果

| 主題  | Hit@1 | Hit@3 | Hit@5 |  MRR |   MAP | nDCG@5 |
| --- | ----: | ----: | ----: | ---: | ----: | -----: |
| 整體  |  0.68 |  0.72 |  0.72 | 0.70 | 0.621 |  0.666 |
| 日本  |  0.92 |  0.96 |  0.96 | 0.94 | 0.861 |  0.906 |
| 東京都 |  0.44 |  0.48 |  0.48 | 0.46 | 0.380 |  0.426 |

---

## 錯誤分析

大部分錯誤發生於多實體查詢。

例如：

```text
東京都是不是日本的首都所在地？
東京都屬於日本的哪一級行政區？
東京都在日本的政治與行政上有何地位？
```

系統有時會將焦點從：

```text
東京都
```

偏移到：

```text
日本
```

這種現象稱為：

```text
Entity Focus Drift（實體焦點漂移）
```

也是未來優化的重要方向。

---

## 目前限制

* 以 Retrieval 為核心，尚未整合完整生成式問答
* 尚未接入本地或雲端 LLM
* Benchmark 規模有限
* 尚未加入 BM25
* 尚未加入 Reranker
* 尚未加入 Query Rewrite

---

## 未來優化方向

### Retrieval

* BM25 Sparse Retrieval
* Hybrid Retrieval
* Query Rewrite
* Entity Boosting
* Section-aware Ranking

### Ranking

* Cross-Encoder Reranker
* Reciprocal Rank Fusion（RRF）

### Generation

* 本地 LLM 整合
* Ollama 部署
* Citation-based Answer Generation

### Engineering

* Docker 容器化
* CI/CD Pipeline
* Cloud Deployment

---

## 作者

**Noah Peng（彭伊宏）**

AI 與資料分析師

國立臺北大學（National Taipei University）

Wikipedia RAG Retrieval Practice Project
