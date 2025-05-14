import json

# 銘柄コードから会社名を取得する関数
def load_company_names():
    with open("data/all_stocks.json", "r", encoding="utf-8") as f:
        stocks = json.load(f)
        company_names = {}
        for stock in stocks:
            parts = stock["name"].split(" ", 1)
            if len(parts) > 1:
                company_names[stock["code"]] = parts[1]
            else:
                company_names[stock["code"]] = stock["name"]
        return company_names

# テクニカルスコアを算出する関数（より詳細なロジック）
def calc_technical_score(stock, term):
    score = 50  # ベースは50%

    if term == "short":
        ma_diff = (stock["price"] - stock["ma5"]) / stock["ma5"]
        score += ma_diff * 100
        score += (stock["rsi"] - 50) * 0.5
    else:
        ma_diff = (stock["price"] - stock["ma25"]) / stock["ma25"]
        score += ma_diff * 100 * 0.8
        score += (stock["rsi"] - 50) * 0.3

    # スコアを0～100に制限
    score = min(max(score, 0), 100)
    return round(score, 1)

# ランキングを作成する関数
def create_ranking(input_file, output_file, term):
    with open(input_file, "r", encoding="utf-8") as f:
        stocks = json.load(f)

    company_names = load_company_names()

    for stock in stocks:
        stock["probability"] = calc_technical_score(stock, term)
        stock["company_name"] = company_names.get(stock["code"], "不明")

    # 上昇確率順にソート
    stocks.sort(key=lambda x: x["probability"], reverse=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

    print(f"[INFO] ランキング保存完了: {output_file}")

# 短期ランキング
create_ranking("data/screened_yahoo_short.json", "data/ranked_short.json", "short")

# 中期ランキング
create_ranking("data/screened_yahoo_mid.json", "data/ranked_mid.json", "mid")
