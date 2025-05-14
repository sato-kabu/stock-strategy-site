import json
import subprocess
import os
import sys

# 銘柄リストを読み込む
def load_screened_stocks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# OCR処理を呼び出す関数
def run_ocr(stock_code):
    subprocess.run(["python3", "data/scripts/ocr_from_irbank.py", str(stock_code)], check=True)

# OCR後の前処理を呼び出す関数
def run_preprocess(stock_code):
    input_path = f"data/ocr_results/{stock_code}.json"
    output_path = f"data/clean_results/{stock_code}.json"
    subprocess.run(["python3", "data/scripts/preprocess_ocr_text.py", input_path, output_path], check=True)

# メイン処理関数
def main(short_screened_json, mid_screened_json):
    short_stocks = load_screened_stocks(short_screened_json)
    mid_stocks = load_screened_stocks(mid_screened_json)

    # 短期・中期の銘柄を結合（重複排除なし）
    all_stocks = short_stocks + mid_stocks

    for stock in all_stocks:
        code = stock['code']
        print(f"🔍 銘柄コード {code} を処理開始します...")

        # OCR処理を実行
        try:
            run_ocr(code)
            print(f"✅ OCR完了 - {code}")
        except subprocess.CalledProcessError:
            print(f"❌ OCR失敗 - {code}")
            continue

        # OCR結果を前処理
        try:
            run_preprocess(code)
            print(f"✅ 前処理完了 - {code}")
        except subprocess.CalledProcessError:
            print(f"❌ 前処理失敗 - {code}")
            continue

        print(f"🎯 銘柄コード {code} のIR処理を正常に終了しました。\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用法: python process_screened_stocks.py [short_screened_json] [mid_screened_json]")
        sys.exit(1)

    short_screened_json = sys.argv[1]
    mid_screened_json = sys.argv[2]
    main(short_screened_json, mid_screened_json)
