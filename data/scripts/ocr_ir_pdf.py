import os
import sys
import json
import pytesseract
from pdf2image import convert_from_path
from datetime import datetime

# OCRで使うTesseract言語
OCR_LANG = "jpn"  # 日本語

def pdf_to_text(pdf_path):
    try:
        # PDFを画像に変換（300dpiで高精度）
        images = convert_from_path(pdf_path, dpi=300)
        all_text = ""
        for idx, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=OCR_LANG)
            all_text += f"\n\n--- Page {idx+1} ---\n\n{text.strip()}"
        return all_text.strip()
    except Exception as e:
        print(f"⚠️ OCR失敗: {pdf_path} - {e}")
        return ""

def save_text(code, pdf_path, text):
    out_dir = f"data/ocr/{code}"
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.now().isoformat()
    out_path = os.path.join(out_dir, os.path.basename(pdf_path).replace(".pdf", ".json"))
    data = {
        "code": code,
        "timestamp": timestamp,
        "pdf": pdf_path,
        "text": text
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ OCR結果を保存しました: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使い方: python ocr_ir_pdf.py <証券コード> <PDFファイルパス>")
        sys.exit(1)

    code = sys.argv[1]
    pdf_path = sys.argv[2]

    text = pdf_to_text(pdf_path)
    save_text(code, pdf_path, text)
