import json
import os

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def merge_data():
    yahoo_data = load_json("data/screened_merged_both.json")
    analysis_data = []

    print("🔍 読み込み開始")
    for stock in yahoo_data:
        code = stock["code"]
        ir_path = f"data/clean_results/{code}.json"
        print(f"📌 銘柄 {code} のIRデータパス: {ir_path}")

        try:
            ir_data = load_json(ir_path)
            stock["ir"] = ir_data
            analysis_data.append(stock)
            print(f"✅ 銘柄 {code} IRデータを読み込み成功")
        except FileNotFoundError:
            print(f"⚠️ IRデータが見つかりません: {code}")

    save_json("data/analysis_ready.json", analysis_data)
    print("🎉 統合データ保存完了")

if __name__ == "__main__":
    merge_data()
