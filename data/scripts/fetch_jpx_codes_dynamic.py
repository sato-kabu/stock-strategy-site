# ファイル名: data/scripts/fetch_jpx_codes_dynamic.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

JPX_LISTING_PAGE = "https://www.jpx.co.jp/markets/statistics-equities/misc/01.html"
SAVE_EXCEL_PATH = "data/jpx_codes.xlsx"
SAVE_JSON_PATH = "data/codes.json"

def fetch_excel_url():
    print("[INFO] JPXページからExcelリンクを検索中...")
    res = requests.get(JPX_LISTING_PAGE)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")

    # .xlsリンクを探す
    link_tag = soup.find("a", href=lambda href: href and href.endswith(".xls"))
    if link_tag is None:
        raise Exception("Excelファイルのリンクが見つかりません")
    
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
    df = df.rename(columns={df.columns[1]: "コード"})
    codes = df["コード"].dropna().astype(int).astype(str).tolist()
    print(f"[SUCCESS] {len(codes)} 件の銘柄コードを抽出しました")
    return codes

def save_as_json(codes):
    with open(SAVE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 銘柄コードを {SAVE_JSON_PATH} に保存しました")

def main():
    os.makedirs("data", exist_ok=True)
    excel_url = fetch_excel_url()
    download_excel(excel_url)
    codes = extract_codes()
    save_as_json(codes)

if __name__ == "__main__":
    main()
