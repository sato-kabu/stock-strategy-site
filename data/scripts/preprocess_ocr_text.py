import json
import sys
import re
import os

def load_ocr_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_clean_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 簡易置換辞書
REPLACEMENTS = {
    'ョョクタ自動車株式会社': 'トヨタ自動車株式会社',
    '日時自動車株式会社': '日野自動車株式会社',
    '人へ': '△',
    'ムA': '△',
    'ム': '△',
    '選': '～',
    'ご': '～',
    '人A': '△',
    'A': '△',
    '則': '',
    '自動還': '自動車',
    '間還胃': '売上高',
    '楽利益': '営業利益',
    '条会竹主に授属する': '親会社株主に帰属する当期純利益',
}

# 表データをCSV形式に変換（任意で拡張可能）
def format_tables(text):
    # 数値が並んでいる表部分を認識しCSVフォーマットに整理
    table_pattern = re.compile(r'(\d{4}年\s*\d{1,2}月期.*?)(?:\n\n|\Z)', re.DOTALL)
    tables = table_pattern.findall(text)
    formatted_tables = []
    for table in tables:
        # 余計な改行を取り除く
        table_clean = re.sub(r'\n+', '\n', table.strip())
        formatted_tables.append(table_clean)
    return formatted_tables

def preprocess_text(text):
    # 置換辞書で簡易修正
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    # 不自然な改行・空白を削除
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\n\s+', '\n', text)

    # 表データを抽出し、CSV向けに加工
    tables = format_tables(text)

    return text.strip(), tables

def main(input_json, output_json):
    data = load_ocr_json(input_json)
    clean_data = []

    for entry in data:
        body_text = entry.get("body", "")
        clean_text, tables = preprocess_text(body_text)

        clean_entry = {
            "title": entry.get("title", ""),
            "timestamp": entry.get("timestamp", ""),
            "clean_body": clean_text,
            "tables": tables
        }
        clean_data.append(clean_entry)

    save_clean_json(output_json, clean_data)
    print(f"✅ 前処理済みテキストを保存しました: {output_json}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用法: python preprocess_ocr_text.py [input_json] [output_json]")
        sys.exit(1)

    input_json = sys.argv[1]
    output_json = sys.argv[2]
    main(input_json, output_json)
