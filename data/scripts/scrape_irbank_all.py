# data/scripts/scrape_irbank_all.py

import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://irbank.net"

def get_all_codes():
    print("[INFO] 銘柄コード一覧を取得中...")
    url = f"{BASE_URL}/code"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print("[ERROR] コード一覧取得失敗")
            return []
        soup = BeautifulSoup(res.content, "html.parser")
        codes = []
        for a in soup.select("table a[href^='/']"):
            href = a.get("href", "")
            code = href.strip("/").split("/")[0]
            if code.isdigit() and len(code) == 4:
                codes.append(code)
        print(f"[INFO] 銘柄コード {len(codes)} 件取得")
        return list(set(codes))  # 重複排除
    except Exception as e:
        print(f"[ERROR] 例外発生: {e}")
        return []

def fetch_company_name(code):
    url = f"{BASE_URL}/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        print(f"[INFO] アクセス中: {url}")
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"[WARNING] {code}: ステータスコード {res.status_code}")
            return None
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        return h1.text.strip() if h1 else None
    except Exception:
        return None

def main():
    codes = get_all_codes()
    results = []

    for i, code in enumerate(codes):
        name = fetch_company_name(code)
        if name:
            print(f"[SUCCESS] 取得成功: {code} → {name}")
            results.append({"code": code, "name": name})
        else:
            print(f"[FAIL] 取得失敗: {code}")
        time.sleep(0.5)  # 負荷軽減のため

    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[INFO] {len(results)} 件の企業情報を取得しました")
    print("[INFO] data/stocks.json に保存しました")

if __name__ == "__main__":
    main()
