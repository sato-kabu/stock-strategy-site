import json
import openai
import os
import re


def analyze_with_ai(stock):
    prompt = (
        f"以下の株式情報をもとに、短期（1週間〜1ヶ月）および中期（1ヶ月〜3ヶ月）で"
        f"株価が10%以上上昇する可能性を、それぞれ0〜100%の確率で推定してください。\n\n"
        f"銘柄コード: {stock['code']}\n"
        f"企業名: {stock.get('name', '情報なし')}\n\n"
        f"【テクニカル指標】:\n{json.dumps(stock.get('yahoo', {}), indent=2, ensure_ascii=False)}\n\n"
        f"【IR情報】: {stock.get('ir', '情報なし')}\n\n"
        "回答は以下の形式でお願いします:\n"
        "短期: xx%\n中期: yy%"
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    ai_response = response.choices[0].message.content.strip()

    short_term_match = re.search(r"短期:\s*(\d+)%", ai_response)
    mid_term_match = re.search(r"中期:\s*(\d+)%", ai_response)

    short_term_prob = int(short_term_match.group(1)) if short_term_match else None
    mid_term_prob = int(mid_term_match.group(1)) if mid_term_match else None

    return short_term_prob, mid_term_prob

def main():
    input_path = "data/analysis_ready.json"
    output_path = "data/ai_predictions.json"

    with open(input_path, "r", encoding="utf-8") as f:
        stocks = json.load(f)

    results = []
    for stock in stocks:
        code = stock["code"]
        print(f"🔍 AI分析中: 銘柄コード {code}")

        try:
            short_term, mid_term = analyze_with_ai(stock)
            results.append({
                "code": code,
                "name": stock.get("name", "情報なし"),
                "short_term_probability": short_term,
                "mid_term_probability": mid_term
            })
            print(f"✅ 分析結果 - 短期: {short_term}%, 中期: {mid_term}%")
        except Exception as e:
            print(f"❌ AI分析エラー:\n{e}")
            results.append({
                "code": code,
                "name": stock.get("name", "情報なし"),
                "short_term_probability": None,
                "mid_term_probability": None,
                "error": str(e)
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"🎉 分析結果を保存しました → {output_path}")

if __name__ == "__main__":
    main()
