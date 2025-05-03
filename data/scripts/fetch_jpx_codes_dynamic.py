import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import datetime
import json

JPX_URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/index.html"
SAVE_EXCEL_PATH = "data/jpx_codes.xlsx"
OUTPUT_JSON_PATH = "data/jpx_codes.json"

def find_excel_link():
    print("[INFO] JPXページからExcelリンクを検索中...")
    res = requests.get(JPX_URL)
    soup = BeautifulSoup(res.content, "html.parser")
    link_tag = soup.find("a", href=True, string=lambda x: x and "xls" in x)
    if not link_tag:
        raise Exception("Excelリンクが見つかりませんでした")
    href = link_tag["href"]
    if not href.startswith("http"):
        href = "https://www.jpx.co.jp" + href
    print(f"[SUCCESS] Excelリンク発見: {href}")
    return href

def download_excel(url):
    print("[INFO] Excelファイルをダウンロード中...")
    res = requests.get(url)
    with open(SAVE_EXCEL_PATH, "wb") as f:
        f.write(res.content)
    print(f"[SUCCESS] Excelを保存: {SAVE_EXCEL_PATH}")

def extract_codes():
    print("[INFO] Excelから銘柄コードを抽出中...")
    df = pd.read_excel(SAVE_EXCEL_PATH, header=1)  # 2行目がヘッダー
    if "コード" not in df.columns or "銘柄名" not in df.columns:
        raise Exception("列 'コード' または '銘柄名' が見つかりません")
    df = df[["コード", "銘柄名"]].dropna()
    df["コード"] = df["コード"].astype(str).str.zfill(4)
    return df.to_dict(orient="records")

def should_run_today_or_first_time():
    if not os.path.exists(OUTPUT_JSON_PATH):
        print("[INFO] 初回実行のため、第3営業日でなくても実行します。")
        return True

    JST = datetime.timezone(datetime.timedelta(hours=9))
    today = datetime.datetime.now(JST).date()
    month_dates = pd.date_range(start=today.replace(day=1), end=today + pd.Timedelta(days=31), freq="B")
    third_business_day = month_dates[2].date()
    return today == third_business_day

def main():
    if not should_run_today_or_first_time():
        print("[SKIP] 本日は第3営業日ではありません。スキップします。")
        return

    excel_url = find_excel_link()
    download_excel(excel_url)
    codes = extract_codes()

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)
    print(f"[SUCCESS] {len(codes)} 件の銘柄を {OUTPUT_JSON_PATH} に保存しました。")

if __name__ == "__main__":
    main()
