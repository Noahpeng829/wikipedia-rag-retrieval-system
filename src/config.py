# src/config.py

TITLES = [
    "日本",
    "東京都",
    "神奈川縣",
    "京都市",
    "大阪市"
]

USER_AGENT = "NoahWikiRAG/0.1 (learning project)"

EMBED_MODEL_NAME = "BAAI/bge-m3"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 5

SECTION_CSV = "data/processed/wiki_sections_clean.csv"
CHUNK_CSV = "data/processed/wiki_chunks_clean.csv"
INDEX_FILE = "data/index/wiki_clean.index"
META_FILE = "data/index/wiki_chunks_clean_meta.csv"

EVAL_RESULT_CSV = "outputs/eval/rag_eval_results.csv"
EVAL_SUMMARY_CSV = "outputs/eval/rag_eval_summary.csv"
EVAL_ERROR_CSV = "outputs/eval/rag_eval_errors.csv"
EVAL_GROUP_CSV = "outputs/eval/rag_eval_group_summary.csv"