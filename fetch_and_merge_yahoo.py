# ✅ fetch_and_merge_yahoo.py
# Yahoo Finance API の取得 → スクリーニング → IRBANKとの統合 までを実行するスクリプト

import subprocess

def run_pipeline():
    print("[INFO] fetch_yahoo_technicals.py を実行中...")
    subprocess.run(["python3", "data/scripts/fetch_yahoo_technicals.py"], check=True)

    print("[INFO] screen_yahoo_technicals.py を実行中...")
    subprocess.run(["python3", "data/scripts/screen_yahoo_technicals.py", "--term", "short"], check=True)
    subprocess.run(["python3", "data/scripts/screen_yahoo_technicals.py", "--term", "mid"], check=True)

    print("[INFO] merge_yahoo_irbank.py を実行中...")
    subprocess.run(["python3", "data/scripts/merge_yahoo_irbank.py"], check=True)

    print("[INFO] 完了: fetch_and_merge_yahoo.py 全処理が終了しました")

if __name__ == "__main__":
    run_pipeline()
