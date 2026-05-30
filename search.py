import os
from serpapi import GoogleSearch

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def web_search(query: str):
    params = {
        "q": query,
        "hl": "ru",
        "gl": "kz",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" not in results:
        return "ничего не нашёл"

    items = results["organic_results"][:3]

    output = []

    for item in items:
        title = item.get("title")
        snippet = item.get("snippet")
        output.append(f"{title} — {snippet}")

    return "\n".join(output)
