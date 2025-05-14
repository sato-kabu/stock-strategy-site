import os
import json
import requests
from bs4 import BeautifulSoup
import time

def fetch_irbank_links(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith(f"/{code}/") and href.count("/") == 2:
                full_url = "https://irbank.net" + href
                links.append(full_url)

        return links

    except Exception as e:
        print(f"[ERROR] {code} 一覧ページの取得に失敗: {e}")
        return []

def fetch_detail_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        title = soup.find("title").text.strip() if soup.find("title") else ""
        body = soup.get_text(separator="\n").strip()
        return {"url": url, "title": title, "body": body}

    except Exception as e:
        print(f"[ERROR] 詳細ページ取得失敗: {url} ({e})")
        return None

def main(code):
    print(f"[INFO] {code} のIR・開示情報を取得中...")
    links = fetch_irbank_links(code)
    print(f"[INFO] {code} の関連開示情報リンクを {len(links)} 件検出")

    results = []
    for url in links:
        detail = fetch_detail_page(url)
        if detail:
            results.append(detail)
        time.sleep(1)

    os.makedirs("data/irbank_full", exist_ok=True)
    output_path = f"data/irbank_full/{code}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[INFO] 保存完了: {output_path} （{len(results)}件）")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使い方: python3 fetch_irbank_full.py <銘柄コード>")
    else:
        main(sys.argv[1])
