#!/bin/bash
echo "[1] スタート：IRバンク全銘柄データ取得"
python3 data/scripts/scrape_irbank_all.py

echo "[2] スクリーニング開始"
python3 data/scripts/screen_candidates.py

echo "[3] Yahooファイナンス検索用コード抽出"
python3 data/scripts/generate_yahoo_targets.py

echo "[4] Yahooファイナンステクニカル取得開始"
python3 data/scripts/fetch_yahoo_technicals.py

echo "[完了] 自動処理が正常に終了しました"
