import requests
from bs4 import BeautifulSoup
import json

def scrape_irbank_stock_list():
    url = "https://irbank.net/code"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    stocks = []
    for a in soup.select("a[href^='/']"):
        text = a.text.strip()
        href = a["href"]
        if href.count("/") == 1 and href[1:].isdigit():
            stocks.append({
                "code": href[1:],
                "name": text
            })

    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_irbank_stock_list()
