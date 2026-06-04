# src/text_processor.py

import re
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

BAD_SECTIONS = {
    "外部連結", "外部链接",
    "參考資料", "参考资料",
    "延伸閱讀", "延伸阅读",
    "相關作品", "相关作品",
    "註釋", "注释",
    "参考文献", "參考文獻"
}

BAD_PATTERNS = [
    "页面存档备份",
    "頁面存檔備份",
    "互联网档案馆",
    "網際網路檔案館",
    "官方網站",
    "官方网站",
    "X（前Twitter）",
    "爱奇艺",
    "愛奇藝",
    "ISBN"
]


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.replace("\xa0", " ")
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_bad_text(text: str) -> bool:
    if not text or len(text.strip()) < 20:
        return True

    for p in BAD_PATTERNS:
        if p in text:
            return True

    return False


def split_into_sections(raw_text: str, title: str, pageid=None):
    lines = raw_text.splitlines()

    rows = []
    current_section = "Introduction"
    buffer_lines = []

    def flush_buffer():
        nonlocal buffer_lines, current_section, rows
        text = clean_text("\n".join(buffer_lines))

        if text and current_section not in BAD_SECTIONS and not is_bad_text(text):
            rows.append({
                "pageid": pageid,
                "title": title,
                "section": current_section,
                "text": text
            })

        buffer_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        m = re.match(r"^=+\s*(.*?)\s*=+$", line)
        if m:
            flush_buffer()
            sec = m.group(1).strip()
            if sec:
                current_section = sec
            continue

        buffer_lines.append(line)

    flush_buffer()
    return rows


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    if not isinstance(text, str) or not text.strip():
        return []

    text = text.strip()
    chunks = []

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start += chunk_size - overlap

    return chunks