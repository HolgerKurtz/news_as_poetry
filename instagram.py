from instagrapi import Client
from dotenv import load_dotenv
import os

load_dotenv()

def post_insta_pic(pic, caption):
    cl = Client()
    cl.login("news_as_poetry", os.getenv("INSTAGRAM_PW"))
    try:
        media = cl.photo_upload(pic,caption)
        print(f"{pic} uploaded to insta")
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    post_insta_pic("/Users/holgerkurtz/Documents/news_as_poems/static/images/a-bestseller-book,-digital-art.jpg", "test")
