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

def get_news_from_nyt(number):
    response = requests.get(TOP_STORY_HOMEPAGE_URL, headers={
                            "Accept": "application/json"})
    data = response.json()

    return data['results'][number] # first --> 0


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

def return_list_of_poems(number):
    list_of_news = []
    for article_number in range(number):
        newest_news = get_news_from_nyt(article_number).get("title") # 0 is the first article
        news_poems = return_poem_and_image(newest_news)
        poem = news_poems.get("ai_text")
        image_url = news_poems.get("image_url")
        temp_dict = dict(title=newest_news, poem=poem, image_url=image_url)
        list_of_news.append(temp_dict)

    return list_of_news
    