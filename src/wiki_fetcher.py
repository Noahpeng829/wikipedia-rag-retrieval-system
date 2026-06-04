# src/wiki_fetcher.py

import requests
from src.config import USER_AGENT

def get_wiki_extract(title: str, lang: str = "zh") -> dict:
    api_url = f"https://{lang}.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": USER_AGENT
    }

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
        "titles": title
    }

    resp = requests.get(api_url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    return {
        "pageid": page.get("pageid"),
        "title": page.get("title", title),
        "extract": page.get("extract", "")
    }