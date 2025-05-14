
import json

def parse_number(value):
    try:
        if value is None:
            return None
        if '兆' in value:
            return float(value.replace('兆', '').replace('億', '')) * 10000
        elif '億' in value:
            return float(value.replace('億', ''))
        elif '万' in value:
            return float(value.replace('万', '')) / 10000
        return float(value.replace(',', '').replace('倍', '').replace('%', ''))
    except:
        return None

def main():
    with open("data/all_stocks.json", "r", encoding="utf-8") as f:
        stocks = json.load(f)

    screened = []

    for stock in stocks:
        try:
            volume = parse_number(stock.get("volume"))
            per = parse_number(stock.get("per"))
            market_cap = parse_number(stock.get("market_cap"))

            if volume is None or volume < 100000:  # 出来高が明らかに少ないものは除外
                continue
            if per is None or per < 5 or per > 50:  # PERが極端なものは除外
                continue
            if market_cap is not None and market_cap > 30000:  # 超大手（3兆円超）を除外
                continue

            screened.append(stock)
        except Exception as e:
            print(f"[WARNING] スクリーニング中にエラー: {e}")
            continue

    with open("data/screened_candidates.json", "w", encoding="utf-8") as f:
        json.dump(screened, f, ensure_ascii=False, indent=2)

    print(f"[INFO] {len(screened)} 件の候補を抽出 → data/screened_candidates.json")

if __name__ == "__main__":
    main()
