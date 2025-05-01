import requests
import json

def fetch_stock(code):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={code}.T"
    res = requests.get(url)

    # ✅ デバッグ用ログ出力
    print("✅ ステータスコード:", res.status_code)
    print("📦 レスポンス本文（JSON）:", res.text[:300])  # 長すぎるので最初の300文字だけ表示

    if res.status_code != 200:
        return None

    data = res.json()

    if not data['quoteResponse']['result']:
        print("⚠️ 結果が空です")
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
    code = "7203"
    data = fetch_stock(code)

    if data:
        with open("data/stock_7203.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        print("❌ データ取得に失敗しました")

if __name__ == "__main__":
    main()
