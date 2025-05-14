import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_data():
    base_url = "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm={}"
    all_data = []

    for page_num in range(1, 6):  # 5ページ分取得
        url = base_url.format(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        rows = soup.select('.m-tableType01_table tbody tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                name = cols[0].text.strip()
                value = cols[1].text.strip()
                change = cols[2].text.strip()
                all_data.append({
                    "name": name,
                    "value": value,
                    "change": change
                })

    return all_data

def save_data(data):
    save_path = "/root/stock-strategy-site/data/ticker_data.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    data = fetch_data()
    save_data(data)
