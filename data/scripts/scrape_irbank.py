import requests
from bs4 import BeautifulSoup
import json
import os
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}
CODES = ["7203", "6758", "9432", "9984"]  # トヨタ、ソニー、NTT、ソフトバンクG
OUTPUT_DIR = "data"

def fetch_company_name(code):
    url = f"https://irbank.net/{code}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        return h1.text.strip() if h1 else None
    except Exception as e:
        print(f"[ERROR] {code} - 名前取得失敗: {e}")
        return None

def fetch_company_details(code):
    url = f"https://irbank.net/{code}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.content, "html.parser")

        # 簡易的に table をすべて取得して保存（必要に応じてカスタム可能）
        tables = soup.find_all("table")
        details = {}
        for idx, table in enumerate(tables):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
                if cells:
                    rows.append(cells)
            details[f"table_{idx}"] = rows
        return details
    except Exception as e:
        print(f"[ERROR] {code} - 詳細取得失敗: {e}")
        return None

def main():
    results = []

    for code in CODES:
        print(f"🔍 処理中: {code}")
        name = fetch_company_name(code)
        if name:
            results.append({"code": code, "name": name})

            details = fetch_company_details(code)
            if details:
                file_path = os.path.join(OUTPUT_DIR, f"stock_{code}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(details, f, ensure_ascii=False, indent=2)
        time.sleep(1)  # アクセス間隔を空けて負荷軽減

    # 銘柄一覧を保存
    with open(os.path.join(OUTPUT_DIR, "stocks.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
