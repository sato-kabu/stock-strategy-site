import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

JPX_URL = "https://www.jpx.co.jp/markets/statistics-equities/misc/01.html"
BASE_URL = "https://www.jpx.co.jp"
SAVE_EXCEL_PATH = "data/jpx_codes.xlsx"
SAVE_JSON_PATH = "data/codes.json"

def fetch_excel_url():
    print("[INFO] JPXページからExcelリンクを検索中...")
    res = requests.get(JPX_URL)
    soup = BeautifulSoup(res.content, "html.parser")
    link_tag = soup.select_one('a[href$=".xls"]')
    if link_tag:
        href = link_tag.get("href")
        full_url = BASE_URL + href
        print(f"[SUCCESS] Excelリンク発見: {full_url}")
        return full_url
    else:
        raise RuntimeError("Excelリンクが見つかりませんでした")

def download_excel(url):
    print("[INFO] Excelファイルをダウンロード中...")
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError("Excelファイルのダウンロードに失敗しました")
    os.makedirs(os.path.dirname(SAVE_EXCEL_PATH), exist_ok=True)
    with open(SAVE_EXCEL_PATH, "wb") as f:
        f.write(res.content)
    print(f"[SUCCESS] Excelを保存: {SAVE_EXCEL_PATH}")

def extract_codes():
    print("[INFO] Excelから銘柄コードを抽出中...")
    df = pd.read_excel(SAVE_EXCEL_PATH, skiprows=1)

    # 'コード'列から空でない値を取り出し、文字列化（例：130Aなど対応）
    codes = df["コード"].dropna().astype(str).str.strip().tolist()

    print(f"[INFO] {len(codes)} 件のコードを取得しました")
    return codes

def save_codes_as_json(codes):
    import json
    with open(SAVE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)
    print(f"[INFO] コード一覧を保存: {SAVE_JSON_PATH}")

def main():
    excel_url = fetch_excel_url()
    download_excel(excel_url)
    codes = extract_codes()
    save_codes_as_json(codes)

if __name__ == "__main__":
    main()
