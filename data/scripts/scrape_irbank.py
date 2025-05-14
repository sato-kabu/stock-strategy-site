import requests
from bs4 import BeautifulSoup
import json
import os
import time

# ラベルに対応する値を抽出する共通関数
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
                        return span.get_text(strip=True).replace("倍", "").replace("%", "")
    except Exception as e:
        print(f"[ERROR] ラベル取得失敗（{label}）: {e}")
    return None

# 個別銘柄ページから企業データを取得
def fetch_company_data(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        # 企業名取得
        name_tag = soup.find("h1")
        name = name_tag.text.strip() if name_tag else None

        # 指標取得（PER（連）、PBR（連）、ROE（連））
        per = extract_value_by_label(soup, "PER（連）")
        pbr = extract_value_by_label(soup, "PBR（連）")
        roe = extract_value_by_label(soup, "ROE（連）")

        return {
            "code": code,
            "name": name,
            "per": per,
            "pbr": pbr,
            "roe": roe
        }

    except Exception as e:
        print(f"[ERROR] {code} 取得失敗: {e}")
        return {
            "code": code,
            "name": None,
            "per": None,
            "pbr": None,
            "roe": None
        }

# メイン処理（複数銘柄のデータ取得）
def main():
    codes = ["7203", "6758", "9432", "9984"]  # 必要に応じて変更可
    results = []

    for code in codes:
        print(f"[INFO] {code} を取得中...")
        data = fetch_company_data(code)
        results.append(data)
        time.sleep(1)  # 負荷対策のウェイト

    os.makedirs("data", exist_ok=True)
    with open("data/stocks.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("[INFO] data/stocks.json に保存しました")

if __name__ == "__main__":
    main()
