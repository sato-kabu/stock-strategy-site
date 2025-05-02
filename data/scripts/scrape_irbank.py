import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_company_name(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"[{code}] HTTPエラー: {res.status_code}")
            return None
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        if h1:
            print(f"[{code}] 取得成功: {h1.text.strip()}")
        else:
            print(f"[{code}] 企業名が取得できませんでした")
        return h1.text.strip() if h1 else None
    except Exception as e:
        print(f"[{code}] エラー発生: {e}")
        return None

def main():
    codes = ["7203", "6758", "9432", "9984"]  # テスト用：トヨタ、ソニー、NTT、SBG
    results = []

    for code in codes:
        name = fetch_company_name(code)
        if name:
            results.append({"code": code, "name": name})
        time.sleep(1)

    print(f"最終的な結果: {results}")
    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("保存完了 → data/stocks.json")

if __name__ == "__main__":
    main()
