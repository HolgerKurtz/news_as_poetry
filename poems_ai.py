# load the API_KEY from the token.json file and set the API_KEY variable
# https://beta.openai.com/docs/guides/answers
from dotenv import load_dotenv
import os
import openai

load_dotenv()


openai.api_key = os.getenv("API_KEY")
openai.organization = os.getenv("ORGANIZATION")


def ai_text(news):
    with open("context.txt", "r") as file:
        context = file.read()
    input_with_context = context.replace("++NEWS++", news)
    
    result = openai.Completion.create(
        engine="text-davinci-001",
        temperature=0.9,
        prompt=input_with_context,
        max_tokens=200
    )
    return result['choices'][0]['text']


if __name__ == "__main__":
    print(ai_text("Paris"))
