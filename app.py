from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# JSONファイルからautocomplete用データ読み込み
autocomplete_data = []
json_path = "static/data/autocomplete.json"
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            autocomplete_data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ JSONファイルの読み込みに失敗しました")

@app.route("/")
def index():
    market_summary = {}
    last_updated = "不明"
    try:
        with open("data/market_summary.json", "r", encoding="utf-8") as f:
            market_summary = json.load(f)
            last_updated = datetime.fromtimestamp(
                os.path.getmtime("data/market_summary.json")
            ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print("[ERROR] market_summary.json 読み込み失敗:", e)

    return render_template("index.html", market_summary=market_summary, last_updated=last_updated)

@app.route("/recommend")
def recommendations():
    short_ranked, mid_ranked = [], []
    short_updated, mid_updated = "不明", "不明"

    try:
        short_path = "data/ranked_short.json"
        with open(short_path, "r", encoding="utf-8") as f:
            short_ranked = json.load(f)
            short_ranked.sort(key=lambda x: x.get('probability', 0), reverse=True)
            short_updated = datetime.fromtimestamp(
                os.path.getmtime(short_path)
            ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print("[ERROR] 短期ランキング読み込み失敗", e)

    try:
        mid_path = "data/ranked_mid.json"
        with open(mid_path, "r", encoding="utf-8") as f:
            mid_ranked = json.load(f)
            mid_ranked.sort(key=lambda x: x.get('probability', 0), reverse=True)
            mid_updated = datetime.fromtimestamp(
                os.path.getmtime(mid_path)
            ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print("[ERROR] 中期ランキング読み込み失敗", e)

    last_updated = max(short_updated, mid_updated)

    return render_template(
        "recommendations.html",
        short_ranked=short_ranked,
        mid_ranked=mid_ranked,
        last_updated=last_updated
    )

@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    advice, analysis_comment, current_price, stock_info = None, None, None, None
    code, price, quantity, cash = "", 0, 0, 0

    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            price = float(request.form.get("price", 0))
            quantity = int(request.form.get("quantity", 0))
            cash = float(request.form.get("cash", 0))
        except ValueError:
            advice = "⚠️ 数値入力が正しくありません。"

    return render_template("portfolio.html",
                           code=code,
                           price=price,
                           quantity=quantity,
                           cash=cash,
                           current_price=current_price,
                           advice=advice,
                           analysis_comment=analysis_comment,
                           stock_info=stock_info,
                           stocks=json.dumps(autocomplete_data, ensure_ascii=False))

@app.context_processor
def inject_ticker_data():
    try:
        with open("data/market_summary.json", "r", encoding="utf-8") as f:
            ticker_data = json.load(f)
    except Exception as e:
        print("[ERROR] Tickerデータ読み込み失敗:", e)
        ticker_data = {}

    return {"ticker_data": ticker_data}

if __name__ == "__main__":
    print(">>> Flask 起動中...")
    app.run(host="0.0.0.0", port=5000, debug=False)
