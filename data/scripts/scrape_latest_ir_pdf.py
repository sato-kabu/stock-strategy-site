import sys
import os
import json
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from datetime import datetime

def get_latest_ir_list(code, max_items=3):
    base_url = f"https://irbank.net/{code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(base_url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    a_tags = soup.select(f"a[href^='/{code}/1401']")

    ir_list = []
    for a in a_tags[:max_items]:
        title = a.text.strip()
        ir_url = "https://irbank.net" + a["href"]
        ir_list.append({"title": title, "ir_url": ir_url})

    if not ir_list:
        raise Exception("IR情報が見つかりません")

    return ir_list

def get_pdf_url(ir_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(ir_url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    a_tag = soup.select_one("a[href$='.pdf']")
    if not a_tag:
        raise Exception("PDFリンクが見つかりません")

    return a_tag["href"]

def extract_pdf_text(pdf_url):
    res = requests.get(pdf_url)
    res.raise_for_status()

    with open("/tmp/temp_ir.pdf", "wb") as f:
        f.write(res.content)

    doc = fitz.open("/tmp/temp_ir.pdf")
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text.strip()

def extract_date_from_url(pdf_url):
    try:
        date_str = pdf_url.split("/")[-1].split(".")[0][8:16]  # 例: 140120250424xxxxx → 20250424
        return datetime.strptime(date_str, "%Y%m%d").isoformat() + "T15:00:00"
    except:
        return datetime.now().isoformat()

def save_ir_data(code, items):
    os.makedirs("data/irbank", exist_ok=True)
    save_path = f"data/irbank/{code}.json"

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"✅ 最新IR3件を保存しました: {save_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrape_latest_ir_pdf.py <code>")
        sys.exit(1)

    code = sys.argv[1]
    ir_list = get_latest_ir_list(code, max_items=3)
    result = []

    for ir in ir_list:
        print(f"🔗 {ir['title']} → {ir['ir_url']}")
        try:
            pdf_url = get_pdf_url(ir['ir_url'])
            body = extract_pdf_text(pdf_url)
            timestamp = extract_date_from_url(pdf_url)
            result.append({
                "code": code,
                "timestamp": timestamp,
                "title": ir["title"],
                "pdf_url": pdf_url,
                "body": body
            })
        except Exception as e:
            print(f"⚠️ 取得失敗: {ir['title']} ({e})")

    save_ir_data(code, result)

if __name__ == "__main__":
    main()
