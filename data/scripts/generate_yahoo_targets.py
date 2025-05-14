# data/scripts/generate_yahoo_targets.py

import json
import os

def main():
    with open("data/screened_candidates.json", "r", encoding="utf-8") as f:
        screened = json.load(f)

    results = []
    for item in screened:
        code = item.get("code")
        if isinstance(code, str) and len(code) >= 4:
            results.append({"code": code})

    os.makedirs("data", exist_ok=True)
    with open("data/yahoo_targets.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[INFO] {len(results)} 件のコードを保存 → data/yahoo_targets.json")

if __name__ == "__main__":
    main()
