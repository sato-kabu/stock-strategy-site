import json
import argparse
import os
import math

def load_data():
    with open("data/yahoo_technicals.json", "r", encoding="utf-8") as f:
        return json.load(f)

def screen_short_term(data):
    screened = []
    for stock in data:
        try:
            if any(math.isnan(stock.get(k, float('nan'))) for k in ["price", "volume", "ma5", "ma25", "volume_5d_avg", "volume_20d_avg", "rsi"]):
                continue

            if stock["price"] < stock["ma25"]:
                continue
            if stock["ma5"] < stock["ma25"]:
                continue
            if stock["volume_5d_avg"] < stock["volume_20d_avg"] * 2:
                continue
            if stock["rsi"] < 70:
                continue

            screened.append(stock)
        except Exception:
            continue
    return screened

def screen_mid_term(data):
    screened = []
    for stock in data:
        try:
            if any(math.isnan(stock.get(k, float('nan'))) for k in ["price", "volume", "ma25", "ma75", "volume_20d_avg", "rsi"]):
                continue

            if stock["price"] < stock["ma75"]:
                continue
            if stock["ma25"] < stock["ma75"]:
                continue
            if stock["volume_20d_avg"] < stock["volume"] * 1.5:
                continue
            if not (50 <= stock["rsi"] <= 70):
                continue

            screened.append(stock)
        except Exception:
            continue
    return screened

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--term", choices=["short", "mid"], default="short", help="スクリーニング期間: shortまたはmid")
    args = parser.parse_args()

    data = load_data()
    if args.term == "short":
        screened = screen_short_term(data)
        output_path = "data/screened_yahoo_short.json"
    else:
        screened = screen_mid_term(data)
        output_path = "data/screened_yahoo_mid.json"

    os.makedirs("data", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(screened, f, ensure_ascii=False, indent=2, default=str)

    print(f"[INFO] {len(screened)} 件の銘柄を抽出 → {output_path}")

if __name__ == "__main__":
    main()
