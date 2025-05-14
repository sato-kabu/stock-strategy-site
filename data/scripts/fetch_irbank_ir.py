import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import time

def fetch_ir_info(code):
    url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        ir_data = []
        ir_section = soup.find("section", id="ir")
        if not ir_section:
            print(f"[WARNING] IR情報が見つかりません: {code}")
            return []

        for row in ir_section.find_all("li"):
            a_tag = row.find("a")
            if not a_tag:
                continue
            link = "https://irbank.net" + a_tag.get("href")
            title = a_tag.text.strip()
            date_tag = row.find("time")
            date = date_tag.text.strip() if date_tag else None

            # 詳細本文を取得（リンク先）
            detail_text = None
            try:
                detail_res = requests.get(link, headers=headers, timeout=10)
                detail_res.raise_for_status()
                detail_soup = BeautifulSoup(detail_res.content, "html.parser")
                text_block = detail_soup.find("div", class_="content")
                detail_text = text_block.get_text(strip=True) if text_block else None
            except Exception as e:
                print(f"[WARNING] 詳細取得失敗: {link} ({e})")

            ir_data.append({
                "title": title,
                "link": link,
                "date": date,
                "detail": detail_text
            })
            time.sleep(0.5)  # サーバーに優しく

        return ir_data

    except Exception as e:
        print(f"[ERROR] IR取得失敗: {code} ({e})")
        return []

def main():
    if len(sys.argv) < 2:
        print("使い方: python fetch_irbank_ir.py <銘柄コード>")
        return

    code = sys.argv[1]
    print(f"[INFO] {code} のIR情報を取得中...")
    ir_data = fetch_ir_info(code)

    os.makedirs("data/irbank_ir", exist_ok=True)
    outpath = f"data/irbank_ir/{code}.json"
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(ir_data, f, ensure_ascii=False, indent=2)

    print(f"[INFO] 保存完了: {outpath} （{len(ir_data)}件）")

if __name__ == "__main__":
    main()
