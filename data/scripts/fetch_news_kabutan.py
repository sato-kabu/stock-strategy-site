def fetch_kabutan_news(code, max_items=5):
    url = f"https://kabutan.jp/stock/news?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        news_list = []

        # より柔軟にテーブルを取得
        tables = soup.find_all("table")
        for table in tables:
            if table.find("td", class_="datetime") and table.find("td", class_="news_title"):
                rows = table.find_all("tr")
                for row in rows:
                    date_td = row.find("td", class_="datetime")
                    title_td = row.find("td", class_="news_title")
                    if not date_td or not title_td:
                        continue
                    title_tag = title_td.find("a")
                    if not title_tag:
                        continue
                    news_list.append({
                        "date": date_td.get_text(strip=True),
                        "title": title_tag.get_text(strip=True),
                        "url": "https://kabutan.jp" + title_tag["href"]
                    })
                    if len(news_list) >= max_items:
                        break
                break  # 最初に該当したテーブルだけでOK

        if not news_list:
            print(f"[WARNING] ニュースが見つかりません: {code}")
        return news_list

    except Exception as e:
        print(f"[ERROR] ニュース取得失敗: {code} - {e}")
        return []
