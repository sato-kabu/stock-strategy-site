import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
import subprocess

# 使用可能な英字（JPX定義に基づく：B,E,I,O,Q,V,Z を除外）
ALLOWED_LETTERS = set("ACDFGHJKLMNPRSTUWX Y")

# JPXコードのバリデーション（英数字4桁まで）
def is_valid_jpx_code(code):
    if not isinstance(code, str):
        return False
    code = code.upper()
    if re.fullmatch(r"\d{4}", code):
        return True
    if re.fullmatch(r"[0-9A-DF-HJ-NP-UWXY]{4}", code):
        return True
    return False

# ラベルに対応する値を抽出
def extract_value_by_label(soup, label):
    try:
        dls = soup.find_all("dl", class_="gdl")
        for dl in dls:
            dt_tags = dl.find_all("dt")
            dd_tags = dl.find_all("dd")
            for dt, dd in zip(dt_tags, dd_tags):
                if label in dt.get_text(strip=True):
                    span = dd.find("span", class_="text")
                    if span:
                        return span.get_text(strip=True)
    except Exception as e:
        print(f"[ERROR] ラベル取得失敗（{label}）: {e}")
    return None

# 個別企業データを取得
def fetch_company_data(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        name_tag = soup.find("h1")
        name = name_tag.text.strip() if name_tag else None
        return {
            "code": code,
            "name": name,
            "per": extract_value_by_label(soup, "PER（連）"),
            "pbr": extract_value_by_label(soup, "PBR（連）"),
            "roe": extract_value_by_label(soup, "ROE（連）"),
            "roa": extract_value_by_label(soup, "ROA（連）"),
            "eps": extract_value_by_label(soup, "EPS（連）"),
            "bps": extract_value_by_label(soup, "BPS（連）"),
            "capital_ratio": extract_value_by_label(soup, "株主資本比率（連）"),
            "credit_ratio": extract_value_by_label(soup, "信用倍率"),
            "market_cap": extract_value_by_label(soup, "時価総額"),
            "volume": extract_value_by_label(soup, "出来高")
        }
    except Exception as e:
        print(f"[ERROR] {code} 取得失敗: {e}")
        return {"code": code, "name": None}

# メイン処理
def main():
    with open("data/codes.json", "r", encoding="utf-8") as f:
        stock_list = json.load(f)

    results = []
    total = len(stock_list)

    for idx, stock in enumerate(stock_list):
        code = stock.get("コード")
        if not is_valid_jpx_code(code):
            continue
        print(f"[{idx+1}/{total}] {code} を取得中...")
        data = fetch_company_data(code)
        if data["name"]:
            results.append(data)
        else:
            print(f"[WARNING] データ取得失敗: {code}")
        time.sleep(1)

    os.makedirs("data", exist_ok=True)
    with open("data/all_stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[INFO] {len(results)} 件の企業データを保存しました: data/all_stocks.json")

    # ▼ 以下、自動パイプラインの実行
    try:
        print("[INFO] IRBANK取得完了 → スクリーニング開始")
        subprocess.run(["python3", "data/scripts/screen_candidates.py"], check=True)

        print("[INFO] 候補コード生成 → Yahooターゲット生成開始")
        subprocess.run(["python3", "data/scripts/generate_yahoo_targets.py"], check=True)

        print("[INFO] Yahoo Finance API → テクニカル取得開始")
        subprocess.run(["python3", "data/scripts/fetch_yahoo_technicals.py"], check=True)

        print("[INFO] テクニカルスクリーニング（短期）実行中...")
        subprocess.run(["python3", "data/scripts/screen_yahoo_technicals.py", "--term", "short"], check=True)

        print("[INFO] テクニカルスクリーニング（中期）実行中...")
        subprocess.run(["python3", "data/scripts/screen_yahoo_technicals.py", "--term", "mid"], check=True)

        print("[INFO] Yahoo×IRBANKの統合処理実行中...")
        subprocess.run(["python3", "data/scripts/merge_yahoo_irbank.py"], check=True)

        print("[✅ 完了] IRBANK + Yahooパイプライン全体処理が完了しました。")

    except Exception as e:
        print(f"[ERROR] パイプライン自動処理に失敗: {e}")

if __name__ == "__main__":
    main()
