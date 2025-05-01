import json

stocks = [
    {"code": "7203", "name": "トヨタ自動車"},
    {"code": "9432", "name": "NTT"},
    {"code": "6758", "name": "ソニーグループ"}
]

with open("data/stocks.json", "w", encoding="utf-8") as f:
    json.dump(stocks, f, ensure_ascii=False, indent=2)
