import yfinance as yf
import json
import os
import time

# テクニカル指標を取得する関数
def fetch_technical_data(code):
    try:
        ticker = yf.Ticker(f"{code}.T")
        hist = ticker.history(period="6mo")

        if hist.empty or len(hist) < 20:
            return {}

        hist["5d_ma"] = hist["Close"].rolling(window=5).mean()
        hist["25d_ma"] = hist["Close"].rolling(window=25).mean()
        hist["75d_ma"] = hist["Close"].rolling(window=75).mean()

        hist["volume_5d_avg"] = hist["Volume"].rolling(window=5).mean()
        hist["volume_20d_avg"] = hist["Volume"].rolling(window=20).mean()

        delta = hist["Close"].diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        roll_up = up.rolling(14).mean()
        roll_down = down.rolling(14).mean()
        rs = roll_up / roll_down
        rsi = 100 - (100 / (1 + rs))

        latest = hist.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        return {
            "price": latest["Close"],
            "volume": latest["Volume"],
            "ma5": latest["5d_ma"],
            "ma25": latest["25d_ma"],
            "ma75": latest["75d_ma"],
            "volume_5d_avg": latest["volume_5d_avg"],
            "volume_20d_avg": latest["volume_20d_avg"],
            "rsi": latest_rsi
        }

    except Exception as e:
        print(f"[ERROR] {code}: {e}")
        return {}

def main():
    with open("data/yahoo_targets.json", "r", encoding="utf-8") as f:
        targets = json.load(f)

    results = []

    for item in targets:
        if isinstance(item, dict):
            code = item.get("code")
        else:
            code = item  # 文字列形式でも対応

        print(f"[INFO] {code} を取得中...")
        data = fetch_technical_data(code)
        if data:
            results.append({"code": code, **data})
        time.sleep(1)

    os.makedirs("data", exist_ok=True)
    output_path = "data/yahoo_technicals.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print(f"[INFO] 完了: {output_path} に保存しました")

if __name__ == "__main__":
    main()
