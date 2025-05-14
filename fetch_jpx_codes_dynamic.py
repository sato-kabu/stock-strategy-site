import requests 
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import datetime
import sys
import unicodedata

JPX_LISTING_PAGE = "https://www.jpx.co.jp/markets/statistics-equities/misc/01.html"
SAVE_EXCEL_PATH = "data/jpx_codes.xlsx"
SAVE_JSON_PATH = "data/codes.json"
AUTOCOMPLETE_JSON_PATH = "static/data/autocomplete.json"
FLAG_FIRST_RUN_PATH = "data/.jpx_codes_first_run.flag"

def fetch_excel_url():
    print("[INFO] JPXページからExcelリンクを検索中...")
    res = requests.get(JPX_LISTING_PAGE)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")
    link_tag = soup.find("a", href=lambda href: href and "data_j.xls" in href)
    if link_tag is None:
        raise Exception("目的のExcelファイルのリンクが見つかりません")
    excel_url = "https://www.jpx.co.jp" + link_tag["href"]
    print(f"[SUCCESS] Excelリンク発見: {excel_url}")
    return excel_url

def download_excel(url):
    print("[INFO] Excelファイルをダウンロード中...")
    response = requests.get(url)
    response.raise_for_status()
    with open(SAVE_EXCEL_PATH, "wb") as f:
        f.write(response.content)
    print(f"[SUCCESS] Excelを保存: {SAVE_EXCEL_PATH}")

def extract_codes():
    print("[INFO] Excelから銘柄コードを抽出中...")
    df = pd.read_excel(SAVE_EXCEL_PATH, skiprows=1)
    df = df.rename(columns={df.columns[1]: "コード", df.columns[2]: "銘柄名"})
    df = df[["コード", "銘柄名"]].dropna()
    df["コード"] = df["コード"].astype(str).str.strip()
    df["銘柄名"] = df["銘柄名"].astype(str).str.strip()
    records = df.to_dict(orient="records")
    print(f"[SUCCESS] {len(records)} 件の企業コードを抽出しました")
    return records

def save_as_json(records):
    with open(SAVE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 銘柄コードを {SAVE_JSON_PATH} に保存しました")

def convert_codes_to_autocomplete_format(records, output_path):
    seen = set()
    unique_list = []
    for row in records:
        # 正規化して、重複をより確実に除去
        code = unicodedata.normalize('NFKC', row["コード"]).strip()
        name = unicodedata.normalize('NFKC', row["銘柄名"]).strip()
        combined = f"{code} {name}"
        if combined not in seen:
            seen.add(combined)
            unique_list.append(combined)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_list, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Autocomplete候補を {output_path} に保存しました")

def is_third_business_day(today=None):
    if today is None:
        today = datetime.date.today()
    date = today.replace(day=1)
    business_days = []
    while date.month == today.month:
        if date.weekday() < 5:
            business_days.append(date)
        date += datetime.timedelta(days=1)
    return today == business_days[2]

def main(force=False):
    os.makedirs("data", exist_ok=True)
    os.makedirs("static/data", exist_ok=True)

    if not force:
        if not os.path.exists(FLAG_FIRST_RUN_PATH):
            print("[INFO] 初回実行のため、第3営業日でなくても実行します。")
            with open(FLAG_FIRST_RUN_PATH, "w") as f:
                f.write("初回実行済み")
        elif not is_third_business_day():
            print("[SKIP] 本日は第3営業日ではありません。スキップします。")
            return
    else:
        print("[FORCE] 強制実行モードです")

    excel_url = fetch_excel_url()
    download_excel(excel_url)
    records = extract_codes()
    save_as_json(records)
    convert_codes_to_autocomplete_format(records, AUTOCOMPLETE_JSON_PATH)

if __name__ == "__main__":
    force = "--force" in sys.argv
    main(force=force)
