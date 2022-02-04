import json
from poems_ai import ai_text
from create_image import generate_image
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


def return_poem_and_image(news):
    with open("news.json", "r") as file:
        news_list = json.load(file)

    if news in news_list:
        pass
    else:
        ai_poem = ai_text(news)
        image_url = generate_image(ai_poem).get('download_url')
        new_entry = dict(ai_text=ai_poem, image_url=image_url)
        news_list[news] = new_entry
        with open("news.json", "w+") as file:
            json.dump(news_list, file)

    return news_list.get(news)
