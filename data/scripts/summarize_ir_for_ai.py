import json
import openai
import os
import sys

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "次のIR情報を株価予測に重要な要素に絞って200〜300字程度に要約してください。"},
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            temperature=0.2
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"❌ 要約エラー: {e}")
        return None

def main(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        ir_data = json.load(f)

    summarized_data = []
    for item in ir_data:
        summarized_body = summarize_text(item["body"])
        if summarized_body:
            summarized_data.append({
                "title": item["title"],
                "date": item["date"],
                "body": summarized_body
            })
            print(f"✅ 要約完了: {item['title']}")
        else:
            print(f"❌ 要約失敗: {item['title']}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summarized_data, f, ensure_ascii=False, indent=2)

    print(f"🎯 要約結果を保存しました: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用法: python summarize_ir_for_ai.py [入力JSON] [出力JSON]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
