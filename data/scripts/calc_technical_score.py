import json

def calc_technical_score(stock):
    score = 50  # 基本値を50%とする

    # RSIの調整 (理想は40〜70程度)
    rsi = stock["rsi"]
    if 40 <= rsi <= 70:
        score += 20
    elif 30 <= rsi < 40 or 70 < rsi <= 80:
        score += 10
    else:
        score -= 10

    # 価格が5日移動平均線より上ならプラス
    price = stock["price"]
    ma5 = stock["ma5"]
    if price > ma5:
        score += 15
    else:
        score -= 15

    # 出来高が一定基準を超えているならプラス
    volume = stock["volume"]
    if volume > 100000:
        score += 15
    elif volume > 50000:
        score += 5
    else:
        score -= 5

    # 0〜100に収める
    return min(max(score, 0), 100)

def add_scores(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        stocks = json.load(f)

    for stock in stocks:
        stock["tech_score"] = calc_technical_score(stock)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

    print(f"[INFO] テクニカルスコアを追加しました → {output_file}")

if __name__ == "__main__":
    add_scores("data/ranked_short.json", "data/ranked_short_scored.json")
    add_scores("data/ranked_mid.json", "data/ranked_mid_scored.json")
