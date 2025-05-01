import json

def main():
    # 仮のデータを出力
    stock_data = {
        "7203": { "name": "トヨタ自動車", "price": 2800 },
        "6758": { "name": "ソニーグループ", "price": 13000 }
    }

    with open("data/stock_prices.json", "w", encoding="utf-8") as f:
        json.dump(stock_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
