import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

# CSVから銘柄コード読み込み
df = pd.read_csv("data/jpx.csv", encoding="utf-8-sig")
codes = df["コード"].dropna().astype(str).str.zfill(4).tolist()

# 結果格納
results = []

for i, code in enumerate(codes[:50]):  # 🔸最初はテスト的に50件だけ
    url = f"https://irbank.net/{code}"
    headers = { "User-Agent": "Mozilla/5.0" }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.content, "html.parser")
        h1 = soup.find("h1")
        name = h1.text.strip() if h1 else ""
        if name:
            results.append({ "code": code, "name": name })
            print(f"{code}: {name}")
    except Exception as e:
        print(f"⚠️ {code} エラー: {e}")
    
    time.sleep(1)  # アクセス間隔制御

# 保存
with open("data/stocks.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
