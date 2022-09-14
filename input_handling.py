import json
from poems_ai import ai_text
from create_image import generate_image, create_ai_image
import requests
from dotenv import load_dotenv
import os
from pprint import pprint
import random

load_dotenv()
# Get most popular articles from NYT API
# https://developer.nytimes.com/

API_KEY = os.getenv("NYT_API_KEY")

def get_news_from_nyt(number, section="home"):
    NYT_SECTIONS = ["home", "arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies", "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"]

    # check if section is valid
    if section in NYT_SECTIONS:
        pass
    else:
        section = "home" # default

    TOP_STORY_HOMEPAGE_URL = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={API_KEY}"
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
        # create a dict like this
        """
            {
                "news": [
                            {
                                "ai_text": "test_1",
                                "image_url": "test_url_1"
                            },
                            {
                                "ai_text": "test_2",
                                "image_url": "test_url_2"
                            }
                        ]
            }
        """
        ai_poem = ai_text(news) # ai_poems = list of strings
        random_color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        list_of_choices = [] # list of ai choices
        for poem in ai_poem:
            poem_and_url_dict = dict(ai_text=poem, image_url=create_ai_image(news)) # create_ai_image("a bestseller book, digital art") or generate_image(poem, random_color).get('download_url'))
            print(poem_and_url_dict)
            list_of_choices.append(poem_and_url_dict)
        news_list[news] =list_of_choices

        with open("news.json", "w+") as file:
            json.dump(news_list, file)

    return news_list.get(news) # returns list 

if __name__ == "__main__":
    test = return_poem_and_image("a wonderful christmas day in new york")
    print(test)