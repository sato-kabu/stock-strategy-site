import requests
from bs4 import BeautifulSoup
import json
import time
import os

# 1銘柄の財務指標をIR BANKから取得
def fetch_company_data(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        name_tag = soup.find("h1")
        name = name_tag.text.strip() if name_tag else f"{code}（名称取得失敗）"

        def extract(label):
            try:
                dls = soup.find_all("dl", class_="gdl")
                for dl in dls:
                    for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd")):
                        if label in dt.get_text(strip=True):
                            span = dd.find("span", class_="text")
                            if span:
                                return span.get_text(strip=True).replace("倍", "").replace("%", "")
            except Exception:
                return None

        return {
            "code": code,
            "name": name,
            "per": extract("PER（連）"),
            "pbr": extract("PBR（連）"),
            "roe": extract("ROE（連）")
        }

    except Exception as e:
        print(f"[ERROR] {code} 取得失敗: {e}")
        return {
            "code": code,
            "name": f"{code}（取得失敗）",
            "per": None,
            "pbr": None,
            "roe": None
        }

# メイン処理：全銘柄を読み込んで1件ずつ取得
def main():
    input_path = "static/data/autocomplete.json"
    output_path = "data/all_stocks.json"
    codes = []

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            for item in raw_data:
                if isinstance(item, dict) and "code" in item:
                    codes.append(item["code"])
                elif isinstance(item, str):
                    parts = item.split()
                    if parts and parts[0].isdigit():
                        codes.append(parts[0])
    except Exception as e:
        print(f"[ERROR] コード一覧の読み込みに失敗しました: {e}")
        return

    print(f"[INFO] 銘柄数: {len(codes)} 件")
    os.makedirs("data", exist_ok=True)

    results = []
    for idx, code in enumerate(codes):
        print(f"[{idx+1}/{len(codes)}] {code} 取得中...")
        data = fetch_company_data(code)
        results.append(data)
        time.sleep(1.5)  # IRBANKの負荷対策

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 取得完了 → {output_path} に保存しました")

if __name__ == "__main__":
    main()
