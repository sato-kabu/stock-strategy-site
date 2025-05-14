#!/bin/bash
source /root/stock-strategy-site/venv/bin/activate
cd /root/stock-strategy-site

python3 data/scripts/generate_yahoo_targets.py &&
python3 data/scripts/fetch_yahoo_technicals.py &&
python3 data/scripts/screen_yahoo_technicals.py &&
python3 data/scripts/merge_yahoo_irbank.py &&
python3 data/scripts/process_screened_stocks.py data/screened_yahoo_short.json data/screened_yahoo_mid.json
