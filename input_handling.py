import json
from poems_ai import ai_text
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# Get most popular articles from NYT API
# https://developer.nytimes.com/

API_KEY = os.getenv("NYT_API_KEY")
TOP_STORY_HOMEPAGE_URL = f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={API_KEY}"

def get_news_from_nyt():
    response = requests.get(TOP_STORY_HOMEPAGE_URL, headers={
                            "Accept": "application/json"})
    data = response.json()

    return data['results'][0]


def return_ai_result(news):
    with open("news.json", "r") as file:
        news_list = json.load(file)

    if news in news_list:
        pass
    else:
        news_list[news] = ai_text(news)
        with open("news.json", "w+") as file:
            json.dump(news_list, file)

    return news_list.get(news)


if "__main__" == "__main__":
    newest_news = get_news_from_nyt()
    print(return_ai_result(newest_news.get("title")))
