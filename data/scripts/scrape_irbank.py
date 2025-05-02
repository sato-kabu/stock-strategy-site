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
            return None
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        return h1.text.strip() if h1 else None
    except Exception as e:
        print(f"Error fetching {code}: {e}")
        return None

def main():
    codes = ["7203", "6758", "9432", "9984"]
    results = []

    for code in codes:
        name = fetch_company_name(code)
        if name:
            results.append({"code": code, "name": name})
            print(f"取得成功: {code} → {name}")
        else:
            print(f"取得失敗: {code}")
        time.sleep(1)

    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
