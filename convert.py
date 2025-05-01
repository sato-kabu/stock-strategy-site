import pandas as pd

# JPXの.xlsファイルを読み込み
df = pd.read_excel("data/data_j.xls", dtype=str)

# 必要な列だけを抽出して整形
df = df[["コード", "銘柄名"]].dropna()
df.columns = ["code", "name"]
df["code"] = df["code"].str.zfill(4)

# JSON出力
df.to_json("data/stocks.json", orient="records", force_ascii=False, indent=2)
