import requests
from requests.exceptions import HTTPError
import json
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(filename="gpt-j.log",filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv()

class News:
    """Creates a News and adds context"""

    def __init__(self, news: str) -> None:
        self.news = news
        self.context = self.get_context()

    def get_context(self):
        with open("context.txt", "r") as file:
            context = file.read()
        input_with_context = context.replace("++NEWS++", self.news)
        
        return input_with_context

    def __repr__(self) -> str:
        return f"{self.context}"


class TextGen():
    """Creates a TextGen with parameters via huggingface API"""
    def __init__(self):
        self.HUG_API = os.environ.get('HUGGINGFACE_API')
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
        self.headers = {"Authorization": f"Bearer {self.HUG_API}"}
        self.parameters = {
            "max_new_tokens": 200,
            "return_full_text": False,
            "end_sequence" : "---"
        }
        self.options = {'use_cache': False}
         
    def query(self, news):
        info = "Es gab ein technisches Problem. Bitte kontaktieren Sie hk@holgerkurtz.de"
        
        body = {
            "inputs": news,
            "parameters": self.parameters,
            "options": self.options
        }
        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=json.dumps(body)
            )
        response.raise_for_status()
        try:
            if response.status_code == 200:
                output = response.json()[0]['generated_text']
                cleaned = output.replace("---", "")
                return cleaned
            else:
                return info
       
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
            return info
      
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  # Python 3.6
            return info
    
def ai_text(news_headline):
    news = News(news_headline).context
    text = TextGen().query(news)
    return [text] # return as list because gpt-3 could return multiple texts