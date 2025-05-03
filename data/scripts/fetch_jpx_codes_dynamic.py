import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import datetime

JPX_LISTING_PAGE = "https://www.jpx.co.jp/markets/statistics-equities/misc/01.html"
SAVE_EXCEL_PATH = "data/jpx_codes.xlsx"
SAVE_JSON_PATH = "data/codes.json"
FLAG_FIRST_RUN_PATH = "data/.jpx_codes_first_run.flag"

def fetch_excel_url():
    print("[INFO] JPXページからExcelリンクを検索中...")
    res = requests.get(JPX_LISTING_PAGE)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")

    # 「data_j.xls」を含むリンクを探す
    link_tag = soup.find("a", href=lambda href: href and "data_j.xls" in href)
    if link_tag is None:
        raise Exception("目的のExcelファイル（data_j.xls）のリンクが見つかりません")
    
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

    # B列を「コード」、C列を「銘柄名」として認識
    df = df.rename(columns={df.columns[1]: "コード", df.columns[2]: "銘柄名"})

    # 形式が130Aなどを含むため、strに変換
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

def is_third_business_day(today=None):
    if today is None:
        today = datetime.date.today()

    # 今日までのカレンダー作成（平日のみ）
    date = today.replace(day=1)
    business_days = []
    while date.month == today.month:
        if date.weekday() < 5:
            business_days.append(date)
        date += datetime.timedelta(days=1)

    return today == business_days[2]  # 第3営業日

def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(FLAG_FIRST_RUN_PATH):
        print("[INFO] 初回実行のため、第3営業日でなくても実行します。")
        with open(FLAG_FIRST_RUN_PATH, "w") as f:
            f.write("初回実行済み")
    else:
        if not is_third_business_day():
            print("[SKIP] 本日は第3営業日ではありません。スキップします。")
            return

    excel_url = fetch_excel_url()
    download_excel(excel_url)
    records = extract_codes()
    save_as_json(records)

if __name__ == "__main__":
    main()
