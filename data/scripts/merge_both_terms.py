import json
import sys

def merge_files(file1, file2, output):
    with open(file1, 'r', encoding='utf-8') as f1, \
         open(file2, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    merged = data1 + data2

    with open(output, 'w', encoding='utf-8') as out_f:
        json.dump(merged, out_f, ensure_ascii=False, indent=2)

    print(f"[INFO] {len(merged)} 件を統合 → {output}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_both_terms.py file1.json file2.json output.json")
        sys.exit(1)

    merge_files(sys.argv[1], sys.argv[2], sys.argv[3])
