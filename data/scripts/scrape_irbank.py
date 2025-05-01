import requests
from bs4 import BeautifulSoup
import json

def scrape_irbank_stock_list():
    url = "https://irbank.net/code"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    print("✅ レスポンス取得成功")

    links = soup.select("a[href^='/']")
    print(f"🔍 該当リンク数: {len(links)}")

    stocks = []
    for a in links:
        text = a.text.strip()
        href = a["href"]
        if href.count("/") == 1 and href[1:].isdigit() and len(href[1:]) >= 4:
            stocks.append({
                "code": href[1:],
                "name": text
            })

    print(f"✅ 銘柄数抽出: {len(stocks)}")

    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_irbank_stock_list()
