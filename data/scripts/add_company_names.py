import json

# 正しいJPX銘柄一覧から会社名を読み込む関数（エラー処理追加版）
def load_stock_names():
    with open("data/all_stocks.json", "r", encoding="utf-8") as f:
        stock_names = {}
        for stock in json.load(f):
            name_parts = stock["name"].split(" ", 1)
            if len(name_parts) > 1:
                stock_names[stock["code"]] = name_parts[1]
            else:
                stock_names[stock["code"]] = stock["name"]  # 空白がない場合そのまま使う
        return stock_names

# ランキングデータに会社名を追加する関数
def add_company_names(input_file, output_file, stock_names):
    with open(input_file, "r", encoding="utf-8") as f:
        ranked_stocks = json.load(f)

    for stock in ranked_stocks:
        stock["company"] = stock_names.get(stock["code"], "不明")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ranked_stocks, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 会社名を追加完了: {output_file}")

if __name__ == "__main__":
    stock_names = load_stock_names()

    add_company_names(
        "data/ranked_short.json",
        "data/ranked_short.json",
        stock_names
    )

    add_company_names(
        "data/ranked_mid.json",
        "data/ranked_mid.json",
        stock_names
    )
