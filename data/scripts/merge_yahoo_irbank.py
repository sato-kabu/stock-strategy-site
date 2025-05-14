import json
import os

# ファイルパス
IRBANK_PATH = "data/all_stocks.json"
YAHOO_PATH = "data/yahoo_technicals.json"
SHORT_TERM_PATH = "data/screened_yahoo_short.json"
MID_TERM_PATH = "data/screened_yahoo_mid.json"

OUTPUT_SHORT = "data/merged_short.json"
OUTPUT_MID = "data/merged_mid.json"
OUTPUT_BOTH = "data/merged_both.json"

# IRBANKデータを読み込む（code をキーに辞書化）
def load_irbank_data():
    with open(IRBANK_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)
        return {item["code"]: item for item in items}

# Yahoo Financeテクニカルを読み込む（code をキーに辞書化）
def load_yahoo_data():
    with open(YAHOO_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)
        return {item["code"]: item for item in items}

# ターゲットファイルを読み込む
def load_screened_codes(path):
    with open(path, "r", encoding="utf-8") as f:
        return [item["code"] for item in json.load(f)]

# 統合処理
def merge_and_save(codes, irbank_data, yahoo_data, output_path):
    merged = []
    for code in codes:
        if code in irbank_data and code in yahoo_data:
            merged_item = {
                "code": code,
                **irbank_data[code],
                **yahoo_data[code]
            }
            merged.append(merged_item)

    os.makedirs("data", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"[INFO] {len(merged)} 件を統合 → {output_path}")

# メイン処理
def main():
    print("[INFO] データ統合を開始します...")
    irbank_data = load_irbank_data()
    yahoo_data = load_yahoo_data()

    short_codes = load_screened_codes(SHORT_TERM_PATH)
    mid_codes = load_screened_codes(MID_TERM_PATH)

    # 短期・中期を個別に統合
    merge_and_save(short_codes, irbank_data, yahoo_data, OUTPUT_SHORT)
    merge_and_save(mid_codes, irbank_data, yahoo_data, OUTPUT_MID)

    # 両方に含まれるコードを抽出
    common_codes = list(set(short_codes) & set(mid_codes))
    merge_and_save(common_codes, irbank_data, yahoo_data, OUTPUT_BOTH)

    print("[INFO] データ統合が完了しました。")

if __name__ == "__main__":
    main()
