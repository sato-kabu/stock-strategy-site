import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_company_name(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        print(f"🔍 アクセス中: {url}")
        res = requests.get(url, headers=headers, timeout=10)
        print(f"➡️ ステータスコード: {res.status_code}")
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        return h1.text.strip() if h1 else None
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def main():
    codes = ["7203", "6758", "9432", "9984"]
    results = []

    for code in codes:
        print(f"\n🔽 処理開始：{code}")
        name = fetch_company_name(code)
        if name:
            print(f"✅ 銘柄名取得成功：{name}")
            results.append({"code": code, "name": name})
        else:
            print(f"⚠️ 銘柄名取得失敗：{code}")
        time.sleep(1)

    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n📁 ファイル出力完了 → data/stocks.json")

if __name__ == "__main__":
    main()
