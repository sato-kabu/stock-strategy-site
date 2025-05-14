import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pypdf import PdfReader
from io import BytesIO

def fetch_latest_ir_list(code, count=3):
    url = f"https://irbank.net/{code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select("a[href^='/" + code + "/1']")

    ir_items = []
    for a in links[:count]:
        title = a.get_text(strip=True)
        href = a.get("href")
        date_span = a.find_previous("td", class_="date")
        date_str = date_span.get_text(strip=True) if date_span else "2025-01-01"

        # 日付の形式を変換
        try:
            if "/" in date_str:
                timestamp = datetime.strptime(date_str, "%Y/%m/%d").isoformat()
            elif "-" in date_str:
                timestamp = datetime.strptime(date_str, "%Y-%m-%d").isoformat()
            else:
                timestamp = "2025-01-01T00:00:00"
        except Exception:
            timestamp = "2025-01-01T00:00:00"

        # 正しいPDF URL（企業コードを含まない）
        doc_id = href.split("/")[-1]
        pdf_url = f"https://f.irbank.net/pdf/{doc_id}.pdf"

        ir_items.append({
            "title": title,
            "url": f"https://irbank.net{href}",
            "pdf_url": pdf_url,
            "timestamp": timestamp,
        })

    return ir_items

def extract_pdf_text(pdf_url):
    try:
        response = requests.get(pdf_url)
        if not response.content.startswith(b"%PDF"):
            raise ValueError("PDFではないレスポンス")
        reader = PdfReader(BytesIO(response.content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        print(f"⚠️ PDF読み取り失敗: {pdf_url} - {e}")
        return ""

def classify_text(text):
    if "決算" in text and "短信" in text:
        return "決算発表"
    elif "配当" in text:
        return "配当関連"
    elif "自己株式" in text:
        return "自社株買い"
    elif "設立" in text or "子会社" in text:
        return "子会社・関連会社"
    elif "上方修正" in text or "下方修正" in text:
        return "業績修正"
    else:
        return "その他"

def main(code):
    ir_items = fetch_latest_ir_list(code)
    result = []

    for item in ir_items:
        body_text = extract_pdf_text(item["pdf_url"])
        label = classify_text(body_text)
        result.append({
            "text": item["title"],
            "label": label,
            "timestamp": item["timestamp"],
            "body": body_text
        })
        item["body"] = body_text

    # 保存（本文付きIR一覧）
    ir_save_path = f"data/irbank/{code}.json"
    os.makedirs(os.path.dirname(ir_save_path), exist_ok=True)
    with open(ir_save_path, "w", encoding="utf-8") as f:
        json.dump(ir_items, f, ensure_ascii=False, indent=2)

    # 保存（分類結果）
    event_save_path = f"data/events/{code}.json"
    os.makedirs(os.path.dirname(event_save_path), exist_ok=True)
    with open(event_save_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 分類済みIRイベントを保存しました: {event_save_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python classify_ir_events.py <code>")
        sys.exit(1)

    code = sys.argv[1]
    main(code)
