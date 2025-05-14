import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from pdf2image import convert_from_bytes
import pytesseract
import shutil

# HTMLページから最新3つのIRリンクを取得
def fetch_latest_ir_entries(code, count=3):
    url = f"https://irbank.net/{code}/ir"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    ir_entries = []
    for dt in soup.select("dl.sdl dt")[:count]:
        date_str = dt.get_text(strip=True).replace("/", "")
        dd = dt.find_next_sibling("dd")
        if dd and dd.a:
            href = dd.a["href"]
            title = dd.a.get_text(strip=True)
            ir_id_match = re.search(r'/(\d+)$', href)
            if ir_id_match:
                ir_id = ir_id_match.group(1)
                ir_entries.append({
                    "title": title,
                    "date": date_str,
                    "id": ir_id
                })
    return ir_entries

# PDFのURLを生成して内容を取得
def fetch_pdf_content(date, ir_id):
    pdf_url = f"https://f.irbank.net/pdf/{date}/{ir_id}.pdf"
    response = requests.get(pdf_url)
    if response.headers['Content-Type'] != 'application/pdf':
        print(f"⚠️ PDFではないレスポンス: {pdf_url}")
        return None
    return response.content

# OCR処理を実行
def perform_ocr(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    ocr_text = ""
    for image in images:
        ocr_text += pytesseract.image_to_string(image, lang='jpn')
    return ocr_text.strip()

# メイン処理
def main(code):
    ir_entries = fetch_latest_ir_entries(code)

    results = []
    for entry in ir_entries:
        print(f"📌 IRタイトル: {entry['title']}")
        pdf_bytes = fetch_pdf_content(entry['date'], entry['id'])

        if pdf_bytes:
            ocr_text = perform_ocr(pdf_bytes)
            if ocr_text:
                results.append({
                    "title": entry['title'],
                    "date": entry['date'],
                    "body": ocr_text
                })
                print("✅ OCR成功")
            else:
                print("❌ OCR失敗: 内容を取得できませんでした")
        else:
            print("❌ PDF取得失敗")

    # OCR結果を保存
    save_path = f"data/ocr_results/{code}.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ OCR結果を保存しました: {save_path}")

    # 最新結果をlatest.jsonとして常に上書き保存
    latest_output_path = "data/ocr_results/latest.json"
    shutil.copyfile(save_path, latest_output_path)
    print(f"✅ 最新結果を上書き保存しました: {latest_output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ocr_from_irbank.py <code>")
        sys.exit(1)
    main(sys.argv[1])
