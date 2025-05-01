import requests
from bs4 import BeautifulSoup
import json

def main():
    url = "https://irbank.net/code"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ ステータスコード: {res.status_code}")
        return

    soup = BeautifulSoup(res.content, "html.parser")
    links = soup.select("a[href^='/']")

    results = []
    for link in links:
        href = link.get("href")
        if href and href.count("/") == 1 and href[1:].isdigit():
            code = href[1:]
            name = link.text.strip()
            results.append({"code": code, "name": name})

    print(f"✅ 銘柄数: {len(results)}")

    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
