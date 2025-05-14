import requests
from bs4 import BeautifulSoup
import json

urls = [
    "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=1",
    "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=2",
    "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=3",
    "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=4",
    "https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=NAVE&Gcode=00&hm=5",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

market_summary = {
    "日経平均株価": "",
    "日経平均前日比": "",
    "銘柄情報": []
}

for idx, url in enumerate(urls):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    if idx == 0:
        nikkei_avg = soup.select_one(".font-m .font-lll").text.strip()
        nikkei_diff = soup.select_one(".font-m .colorRed, .font-m .colorGreen").text.strip()
        market_summary["日経平均株価"] = nikkei_avg
        market_summary["日経平均前日比"] = nikkei_diff

    rows = soup.select("table.tblModel-1 tbody tr")
    for row in rows:
        cols = row.select("td")
        if len(cols) == 8:
            code = cols[0].text.strip()
            name = cols[1].text.strip()
            price_open = cols[2].text.strip().split("（")[0]
            price_high = cols[3].text.strip().split("（")[0]
            price_low = cols[4].text.strip().split("（")[0]
            current_price = cols[5].text.strip().split("（")[0]
            diff = cols[6].text.strip()
            volume = cols[7].text.strip()

            market_summary["銘柄情報"].append({
                "銘柄コード": code,
                "銘柄名": name,
                "始値": price_open,
                "高値": price_high,
                "安値": price_low,
                "現在値": current_price,
                "前日比": diff,
                "売買高": volume
            })

with open("data/market_summary.json", "w", encoding="utf-8") as f:
    json.dump(market_summary, f, ensure_ascii=False, indent=2)

print("マーケット情報を取得しました。")
