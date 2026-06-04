# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import json
from src.config import TOP_K, EVAL_RESULT_CSV, EVAL_SUMMARY_CSV, EVAL_ERROR_CSV, EVAL_GROUP_CSV
from src.retriever import WikiRetriever

# =========================================================
# 0) 基本設定
# =========================================================
TOP_K = 5
K_LIST = [1, 3, 5]

# 如果你有生成答案函式，可改成 True
# 例如：USE_ANSWER_EVAL = True，並提供 answer_question(question, retrieved_df)
USE_ANSWER_EVAL = False
retriever = WikiRetriever()
# =========================================================
# 1) 建立評估題庫
#    新增 gold_answer，未來可做生成答案評估
#    gold_section 不知道可以先設 None
# =========================================================

eval_questions = [
    # =========================
    # 日本（1~25）
    # =========================
    {"question": "日本是什麼國家？", "gold_title": "日本", "gold_section": "Introduction", "gold_answer": "日本是位於東亞的島國。", "question_type": "definition"},
    {"question": "日本的首都是哪裡？", "gold_title": "日本", "gold_section": "主要城市", "gold_answer": "日本的首都是東京。", "question_type": "capital"},
    {"question": "日本位於哪個地區？", "gold_title": "日本", "gold_section": "地理", "gold_answer": "日本位於東亞。", "question_type": "location"},
    {"question": "日本的面積大約是多少？", "gold_title": "日本", "gold_section": "地理", "gold_answer": None, "question_type": "area"},
    {"question": "日本的行政區劃是怎麼分的？", "gold_title": "日本", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative"},
    {"question": "日本的地理位置在哪裡？", "gold_title": "日本", "gold_section": "地理", "gold_answer": "日本位於東亞。", "question_type": "location"},
    {"question": "日本屬於哪一洲或區域？", "gold_title": "日本", "gold_section": "Introduction", "gold_answer": "日本屬於東亞。", "question_type": "location"},
    {"question": "日本是島國嗎？", "gold_title": "日本", "gold_section": "Introduction", "gold_answer": "是，日本是島國。", "question_type": "definition"},
    {"question": "日本由哪些主要島嶼組成？", "gold_title": "日本", "gold_section": "地理", "gold_answer": None, "question_type": "geography"},
    {"question": "日本的官方首都通常被認為是哪裡？", "gold_title": "日本", "gold_section": "主要城市", "gold_answer": "日本的首都是東京。", "question_type": "capital"},
    {"question": "日本的國土面積有多大？", "gold_title": "日本", "gold_section": "地理", "gold_answer": None, "question_type": "area"},
    {"question": "日本總共有幾個都道府縣？", "gold_title": "日本", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative"},
    {"question": "日本的行政區單位包含哪些類型？", "gold_title": "日本", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative"},
    {"question": "日本在亞洲的哪個位置？", "gold_title": "日本", "gold_section": "地理", "gold_answer": "日本位於東亞。", "question_type": "location"},
    {"question": "日本的首都東京位於哪個國家？", "gold_title": "日本", "gold_section": "主要城市", "gold_answer": "東京位於日本。", "question_type": "capital"},
    {"question": "日本和東京都之間是什麼關係？", "gold_title": "日本", "gold_section": "行政區劃", "gold_answer": "東京都是日本的一級行政區，且為首都所在地。", "question_type": "administrative_relation"},
    {"question": "日本是亞洲國家嗎？", "gold_title": "日本", "gold_section": "Introduction", "gold_answer": "是，日本是亞洲的東亞國家。", "question_type": "definition"},
    {"question": "日本位於太平洋的哪一側？", "gold_title": "日本", "gold_section": "地理", "gold_answer": None, "question_type": "location"},
    {"question": "日本有什麼樣的行政劃分制度？", "gold_title": "日本", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative"},
    {"question": "日本屬於哪一個地理區域？", "gold_title": "日本", "gold_section": "地理", "gold_answer": "日本屬於東亞。", "question_type": "location"},
    {"question": "日本的首都城市叫什麼名字？", "gold_title": "日本", "gold_section": "主要城市", "gold_answer": "日本的首都城市是東京。", "question_type": "capital"},
    {"question": "日本的國家性質是什麼？", "gold_title": "日本", "gold_section": "Introduction", "gold_answer": "日本是東亞的島國。", "question_type": "definition"},
    {"question": "日本有哪些主要行政區類別？", "gold_title": "日本", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative"},
    {"question": "日本在世界地圖上的大致位置在哪裡？", "gold_title": "日本", "gold_section": "地理", "gold_answer": "日本位於東亞。", "question_type": "location"},
    {"question": "日本的首都是否為東京？", "gold_title": "日本", "gold_section": "主要城市", "gold_answer": "是，日本的首都是東京。", "question_type": "capital"},

    # =========================
    # 東京都（26~50）
    # =========================
    {"question": "東京都是什麼？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": "東京都是日本的都，也是首都所在地。", "question_type": "definition"},
    {"question": "東京都位於日本的哪裡？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "location"},
    {"question": "東京都的人口大約有多少？", "gold_title": "東京都", "gold_section": "人口", "gold_answer": None, "question_type": "population"},
    {"question": "東京都的行政地位是什麼？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "東京都是日本的一級行政區。", "question_type": "administrative"},
    {"question": "東京都和日本的關係是什麼？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "東京都是日本的一級行政區，且為首都所在地。", "question_type": "administrative_relation"},
    {"question": "東京都是不是日本的首都所在地？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": "是，東京都是日本的首都所在地。", "question_type": "capital_relation"},
    {"question": "東京都屬於日本的哪一級行政區？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "東京都屬於日本的一級行政區。", "question_type": "administrative"},
    {"question": "東京都位於哪個地方？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "location"},
    {"question": "東京都大約有多少人口？", "gold_title": "東京都", "gold_section": "人口", "gold_answer": None, "question_type": "population"},
    {"question": "東京都在日本的地位是什麼？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "東京都是日本的一級行政區，也是首都所在地。", "question_type": "administrative_relation"},
    {"question": "東京都是日本的哪一種行政區？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "東京都是日本的都。", "question_type": "administrative"},
    {"question": "東京都是不是都道府縣之一？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": "是，東京都是都道府縣之一。", "question_type": "administrative"},
    {"question": "東京都位於日本的哪個區域？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "location"},
    {"question": "東京都的人口規模如何？", "gold_title": "東京都", "gold_section": "人口", "gold_answer": None, "question_type": "population"},
    {"question": "東京都和東京有什麼關係？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "definition"},
    {"question": "東京都是不是日本的一級行政區？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "是，東京都是日本的一級行政區。", "question_type": "administrative"},
    {"question": "東京都在日本行政區劃中的角色是什麼？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative_relation"},
    {"question": "東京都位於日本本州嗎？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "location"},
    {"question": "東京都的行政層級如何描述？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": "東京都是日本的一級行政區。", "question_type": "administrative"},
    {"question": "東京都有什麼行政上的特殊性？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "administrative_relation"},
    {"question": "東京都是否為日本首都圈核心？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "capital_relation"},
    {"question": "東京都與日本中央政府有什麼關聯？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "administrative_relation"},
    {"question": "東京都的首都功能代表什麼？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": None, "question_type": "capital_relation"},
    {"question": "東京都在日本的政治與行政上有何地位？", "gold_title": "東京都", "gold_section": "行政區劃", "gold_answer": None, "question_type": "administrative_relation"},
    {"question": "東京都是否可視為東京這座首都的行政區名稱？", "gold_title": "東京都", "gold_section": "Introduction", "gold_answer": "是，東京都可視為東京首都所在地的行政區名稱。", "question_type": "definition"},
]
eval_df = pd.DataFrame(eval_questions)
print("評估題數:", len(eval_df))
print(eval_df.head())


# =========================================================
# 2) 文字正規化與輔助函式
# =========================================================
def normalize_text(text):
    """簡單文字正規化，用於答案比對"""
    if text is None or pd.isna(text):
        return ""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。、「」；：！？,.!?()（）\[\]{}\"'`~\-_/]", "", text)
    return text


def safe_get(row, col, default=None):
    """避免欄位不存在報錯"""
    return row[col] if col in row.index else default


def is_relevant(row, gold_title, gold_section=None):
    """
    判斷 retrieval 結果是否 relevant
    若 gold_section=None，僅檢查 title
    """
    row_title = str(safe_get(row, "title", ""))
    row_section = str(safe_get(row, "section", ""))

    if gold_section is None or pd.isna(gold_section):
        return row_title == str(gold_title)
    else:
        return (row_title == str(gold_title)) and (row_section == str(gold_section))


def get_relevance_list(retrieved_df, gold_title, gold_section=None):
    """
    回傳每個 rank 是否 relevant 的 0/1 list
    """
    rel_list = []
    for _, row in retrieved_df.iterrows():
        rel_list.append(1 if is_relevant(row, gold_title, gold_section) else 0)
    return rel_list


# =========================================================
# 3) 單題檢索指標
#    加入：
#    - Hit@K
#    - Precision@K
#    - Recall@K
#    - RR / MRR
#    - AP (Average Precision)
#    - nDCG@K
#    - duplicate_rate@K
#    - noise@K
# =========================================================
def calc_single_metrics(retrieved_df, gold_title, gold_section=None, k_list=[1, 3, 5]):
    result = {}

    if retrieved_df is None or len(retrieved_df) == 0:
        for k in k_list:
            result[f"hit@{k}"] = 0
            result[f"precision@{k}"] = 0.0
            result[f"recall@{k}"] = 0.0
            result[f"ndcg@{k}"] = 0.0
            result[f"noise@{k}"] = 1.0
            result[f"duplicate_rate@{k}"] = np.nan
        result["rr"] = 0.0
        result["ap"] = 0.0
        result["first_relevant_rank"] = np.nan
        result["num_relevant_retrieved"] = 0
        return result

    rel_list = get_relevance_list(retrieved_df, gold_title, gold_section)
    rel_ranks = [i + 1 for i, rel in enumerate(rel_list) if rel == 1]

    # 這裡目前每題通常只有 1 個 gold document

    # RR
    result["rr"] = 1.0 / min(rel_ranks) if len(rel_ranks) > 0 else 0.0
    result["first_relevant_rank"] = min(rel_ranks) if len(rel_ranks) > 0 else np.nan
    result["num_relevant_retrieved"] = 1 if sum(rel_list) > 0 else 0

    # AP
    # Average Precision = relevant 出現位置上的 precision 平均
    if len(rel_ranks) > 0:
        precisions_at_rel = []
        for r in rel_ranks:
            precisions_at_rel.append(sum(rel_list[:r]) / r)
        result["ap"] = float(np.mean(precisions_at_rel))
    else:
        result["ap"] = 0.0

    # 各種 @K 指標
    for k in k_list:
        topk_rel = rel_list[:k]
        relevant_in_topk = sum(topk_rel)
    
        # Hit@K
        result[f"hit@{k}"] = 1 if relevant_in_topk > 0 else 0
    
        # Precision@K
        result[f"precision@{k}"] = relevant_in_topk / k if k > 0 else 0.0
    
        # Recall@K
        # 目前每題只有 1 個 gold target，所以 recall 只應該是 0 或 1
        result[f"recall@{k}"] = 1.0 if relevant_in_topk > 0 else 0.0
    
        # noise@K = top-k 中不相關比例
        result[f"noise@{k}"] = 1 - result[f"precision@{k}"]
    
        # nDCG@K
        dcg = 0.0
        for i, rel in enumerate(topk_rel, start=1):
            dcg += rel / np.log2(i + 1)
    
        ideal_rel = sorted(rel_list, reverse=True)[:k]
        idcg = 0.0
        for i, rel in enumerate(ideal_rel, start=1):
            idcg += rel / np.log2(i + 1)
    
        result[f"ndcg@{k}"] = dcg / idcg if idcg > 0 else 0.0
    
        # duplicate_rate@K
        seen = []
        for _, row in retrieved_df.head(k).iterrows():
            key = (safe_get(row, "title", None), safe_get(row, "section", None))
            seen.append(key)
    
        if len(seen) > 0:
            unique_count = len(set(seen))
            result[f"duplicate_rate@{k}"] = 1 - (unique_count / len(seen))
        else:
            result[f"duplicate_rate@{k}"] = np.nan

    return result


# =========================================================
# 4) 生成答案評估（可選）
#    如果你有 answer_question(question, retrieved_df) 可啟用
#    指標：
#    - exact match (EM)
#    - token/char overlap F1
# =========================================================
def calc_answer_f1(pred, gold):
    pred_norm = normalize_text(pred)
    gold_norm = normalize_text(gold)

    if pred_norm == "" or gold_norm == "":
        return 0.0

    # 中文這裡用字元級 overlap，簡單且穩
    pred_chars = list(pred_norm)
    gold_chars = list(gold_norm)

    pred_count = {}
    gold_count = {}

    for ch in pred_chars:
        pred_count[ch] = pred_count.get(ch, 0) + 1
    for ch in gold_chars:
        gold_count[ch] = gold_count.get(ch, 0) + 1

    common = 0
    for ch in pred_count:
        if ch in gold_count:
            common += min(pred_count[ch], gold_count[ch])

    if common == 0:
        return 0.0

    precision = common / len(pred_chars)
    recall = common / len(gold_chars)

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def calc_answer_metrics(pred_answer, gold_answer):
    if gold_answer is None or pd.isna(gold_answer):
        return {
            "pred_answer": pred_answer,
            "answer_em": np.nan,
            "answer_f1": np.nan
        }

    pred_norm = normalize_text(pred_answer)
    gold_norm = normalize_text(gold_answer)

    em = 1 if pred_norm == gold_norm else 0
    f1 = calc_answer_f1(pred_answer, gold_answer)

    return {
        "pred_answer": pred_answer,
        "answer_em": em,
        "answer_f1": f1
    }


# =========================================================
# 5) 檢索結果摘要
#    方便 debug / 分析
# =========================================================
def extract_topk_info(retrieved_df, top_k=5):
    info = {}

    for i in range(top_k):
        idx = i + 1
        if retrieved_df is not None and len(retrieved_df) > i:
            row = retrieved_df.iloc[i]
            info[f"top{idx}_title"] = safe_get(row, "title", None)
            info[f"top{idx}_section"] = safe_get(row, "section", None)
            info[f"top{idx}_score"] = safe_get(row, "final_score", None)
            info[f"top{idx}_content_preview"] = str(safe_get(row, "chunk_text", ""))[:120]
        else:
            info[f"top{idx}_title"] = None
            info[f"top{idx}_section"] = None
            info[f"top{idx}_score"] = None
            info[f"top{idx}_content_preview"] = None

    return info


# =========================================================
# 6) 可選：你自己的回答函式
#    若 USE_ANSWER_EVAL = True，請自行補這個函式
# =========================================================
def answer_question(question, retrieved_df):
    """
    這裡只是佔位函式
    如果你已有 LLM 回答函式，請替換這裡
    """
    raise NotImplementedError("請將 answer_question(question, retrieved_df) 改成你的實際回答函式")


# =========================================================
# 7) 主評估流程
#    直接沿用你現有的 retrieve()
# =========================================================
all_results = []

for _, row in eval_df.iterrows():
    question = row["question"]
    gold_title = row["gold_title"]
    gold_section = row["gold_section"]
    gold_answer = row["gold_answer"]

    # 你的既有 retrieval
    retrieved = retriever.retrieve(question, top_k=TOP_K)

    # 單題檢索評估
    metrics = calc_single_metrics(
        retrieved_df=retrieved,
        gold_title=gold_title,
        gold_section=gold_section,
        k_list=K_LIST
    )

    # top-k 詳細內容
    topk_info = extract_topk_info(retrieved, top_k=TOP_K)

    # 可選：答案評估
    answer_metrics = {
        "pred_answer": None,
        "answer_em": np.nan,
        "answer_f1": np.nan
    }

    if USE_ANSWER_EVAL:
        try:
            pred_answer = answer_question(question, retrieved)
            answer_metrics = calc_answer_metrics(pred_answer, gold_answer)
        except Exception as e:
            answer_metrics = {
                "pred_answer": f"[ERROR] {str(e)}",
                "answer_em": np.nan,
                "answer_f1": np.nan
            }

    out = {
        "question": question,
        "gold_title": gold_title,
        "gold_section": gold_section,
        "gold_answer": gold_answer,
        "question_type": row.get("question_type", None),
        **metrics,
        **topk_info,
        **answer_metrics
    }

    all_results.append(out)

result_df = pd.DataFrame(all_results)


# =========================================================
# 8) 顯示單題結果
# =========================================================
print("\n================ 單題評估結果 ================\n")
show_cols = [
    "question", "gold_title",
    "top1_title", "top1_section", "top1_score",
    "hit@1", "hit@3", "hit@5",
    "precision@1", "precision@3", "precision@5",
    "recall@1", "recall@3", "recall@5",
    "rr", "ap", "ndcg@3", "ndcg@5",
    "noise@3", "duplicate_rate@3",
    "first_relevant_rank",
    "answer_em", "answer_f1"
]

show_cols = [c for c in show_cols if c in result_df.columns]
print(result_df[show_cols].to_string(index=False))


# =========================================================
# 9) 整體平均績效
# =========================================================
summary = {
    "num_questions": len(result_df),

    "Hit@1": result_df["hit@1"].mean(),
    "Hit@3": result_df["hit@3"].mean(),
    "Hit@5": result_df["hit@5"].mean(),

    "Precision@1": result_df["precision@1"].mean(),
    "Precision@3": result_df["precision@3"].mean(),
    "Precision@5": result_df["precision@5"].mean(),

    "Recall@1": result_df["recall@1"].mean(),
    "Recall@3": result_df["recall@3"].mean(),
    "Recall@5": result_df["recall@5"].mean(),

    "MRR": result_df["rr"].mean(),
    "MAP": result_df["ap"].mean(),

    "nDCG@3": result_df["ndcg@3"].mean(),
    "nDCG@5": result_df["ndcg@5"].mean(),

    "Noise@3": result_df["noise@3"].mean(),
    "Noise@5": result_df["noise@5"].mean(),

    "DuplicateRate@3": result_df["duplicate_rate@3"].mean(),
    "DuplicateRate@5": result_df["duplicate_rate@5"].mean(),
}

if "answer_em" in result_df.columns:
    summary["Answer_EM"] = result_df["answer_em"].mean(skipna=True)
if "answer_f1" in result_df.columns:
    summary["Answer_F1"] = result_df["answer_f1"].mean(skipna=True)

summary_df = pd.DataFrame([summary])

# =========================================================
# 9-1) 分 title 統計績效
# =========================================================
group_summary_df = (
    result_df.groupby("gold_title")[["hit@1", "hit@3", "hit@5", "precision@1", "precision@3", "precision@5", "rr", "ap", "ndcg@3", "ndcg@5"]]
    .mean()
    .reset_index()
)

print("\n================ 分主題績效 ================\n")
print(group_summary_df.to_string(index=False))    
print("\n================ 整體績效 ================\n")
print(summary_df.to_string(index=False))


# =========================================================
# 10) 錯誤案例分析（很重要）
#     方便你之後調 chunk / hybrid / reranker
# =========================================================
error_df = result_df[result_df["hit@1"] == 0].copy()

print("\n================ Top1 未命中題目 ================\n")
if len(error_df) > 0:
    err_cols = [
        "question", "gold_title",
        "top1_title", "top1_section", "top1_score",
        "top1_content_preview",
        "top2_title", "top2_section", "top2_score",
        "top3_title", "top3_section", "top3_score"
    ]
    err_cols = [c for c in err_cols if c in error_df.columns]
    print(error_df[err_cols].to_string(index=False))
else:
    print("所有題目 Top1 都有命中。")


# =========================================================
# 11) 存檔
# =========================================================
result_df.to_csv(EVAL_RESULT_CSV, index=False, encoding="utf-8-sig")
summary_df.to_csv(EVAL_SUMMARY_CSV, index=False, encoding="utf-8-sig")
error_df.to_csv(EVAL_ERROR_CSV, index=False, encoding="utf-8-sig")
group_summary_df.to_csv(EVAL_GROUP_CSV, index=False, encoding="utf-8-sig")

print("\n已輸出：")
print("- rag_eval_results_japan_tokyo_v2.csv")
print("- rag_eval_summary_japan_tokyo_v2.csv")
print("- rag_eval_errors_japan_tokyo_v2.csv")
print("- rag_eval_group_summary_japan_tokyo_v2.csv")