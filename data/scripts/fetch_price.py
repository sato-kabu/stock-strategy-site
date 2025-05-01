import requests
import json

def fetch_stock(code):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={code}.T"
    res = requests.get(url)
    data = res.json()

    if not data['quoteResponse']['result']:
        return None

    item = data['quoteResponse']['result'][0]
    return {
        "code": code,
        "name": item.get("longName"),
        "price": item.get("regularMarketPrice"),
        "change": item.get("regularMarketChangePercent"),
        "volume": item.get("regularMarketVolume"),
        "marketCap": item.get("marketCap"),
        "peRatio": item.get("trailingPE"),
        "pbr": item.get("priceToBook")
    }

def main():
    code = "7203"  # トヨタでテスト
    data = fetch_stock(code)
    if data:
        with open("data/stock_7203.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        print("データ取得失敗")

if __name__ == "__main__":
    main()
