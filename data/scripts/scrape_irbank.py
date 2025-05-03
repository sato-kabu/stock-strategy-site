import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_company_name(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        print(f"[INFO] アクセス中: {url}")
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        if h1:
            print(f"[SUCCESS] 取得成功: {code} → {h1.text.strip()}")
        else:
            print(f"[WARNING] タイトルが見つかりません: {code}")
        return h1.text.strip() if h1 else None
    except Exception as e:
        print(f"[ERROR] {code} の取得に失敗: {e}")
        return None

def main():
    codes = ["7203", "6758", "9432", "9984"]  # トヨタ、ソニー、NTT、SBG
    results = []

    for code in codes:
        name = fetch_company_name(code)
        if name:
            results.append({"code": code, "name": name})
        time.sleep(1)

    print(f"[INFO] {len(results)} 件の企業情報を取得しました")
    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("[INFO] data/stocks.json に保存しました")

if __name__ == "__main__":
    main()
