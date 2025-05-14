import sys
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def fetch_irbank_html(code):
    url = f"https://irbank.net/{code}"
    response = requests.get(url)
    response.encoding = "utf-8"
    if response.status_code != 200:
        raise Exception(f"Failed to fetch IRBANK page for {code}")
    return response.text

def extract_ir_links_and_bodies(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("a[href^='/" + code + "/']")

    output = []
    for row in rows[:5]:  # 最新5件に絞る
        href = row.get("href")
        text = row.get_text(strip=True)
        link_url = f"https://irbank.net{href}"

        # 各リンク先ページを取得し本文を取得
        res = requests.get(link_url)
        res.encoding = "utf-8"
        if res.status_code != 200:
            continue
        sub_soup = BeautifulSoup(res.text, "html.parser")
        body_tag = sub_soup.find("div", class_="edn") or sub_soup.find("div", class_="document") or sub_soup.find("body")
        body_text = body_tag.get_text(separator="\n", strip=True) if body_tag else ""

        output.append({
            "code": code,
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "body": body_text
        })

    return output

def save_ir_data(code, output):
    os.makedirs("data/irbank", exist_ok=True)
    save_path = f"data/irbank/{code}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)  # ← ✅ 辞書ではなくリストを保存
    print(f"✅ Saved {len(output)} IR items for {code} to {save_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_irbank_body.py <code>")
        sys.exit(1)

    code = sys.argv[1]
    html = fetch_irbank_html(code)
    output = extract_ir_links_and_bodies(html)
    save_ir_data(code, output)
