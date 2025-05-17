import os
from openai import OpenAI
import subprocess
import datetime

# OpenAI APIキーの読み込み
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=api_key)

# ChatGPTで提案を生成する関数（新API対応）
def generate_ai_suggestion(task_description):
    prompt = f"以下の依頼に従って、サイトの修正をするための具体的なコードを提案してください。\n\n依頼: {task_description}\n\n### 提案内容:"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3
    )

    return response.choices[0].message.content

# Gitブランチ作成＆PR作成
def create_branch_and_push(suggestion):
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    branch_name = f"ai-update-{timestamp}"

    subprocess.run(["git", "checkout", "-b", branch_name])

    # 提案内容をHTMLファイルとして保存
    filename = "templates/latest_news.html"
    with open(filename, "w") as f:
        f.write(suggestion)

    subprocess.run(["git", "add", filename])
    subprocess.run(["git", "commit", "-m", f"AI自動提案: {timestamp}"])
    subprocess.run(["git", "push", "--set-upstream", "origin", branch_name])

    subprocess.run([
        "gh", "pr", "create", "--title", f"AI自動提案: {timestamp}",
        "--body", suggestion
    ])

# メイン関数
if __name__ == "__main__":
    task = input("AIに依頼したい内容を入力してください: ")
    suggestion = generate_ai_suggestion(task)
    print("[INFO] AIの提案内容を生成しました。\n")
    print(suggestion)

    proceed = input("\nこの提案をGitHubに送信してPRを作成しますか？ (y/n): ")
    if proceed.lower() == 'y':
        create_branch_and_push(suggestion)
        print("[INFO] GitHubにブランチを作成し、PRを作成しました。")
    else:
        print("[INFO] PR作成を中止しました。")
