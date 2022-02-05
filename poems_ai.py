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
    
    multiple_choices = openai.Completion.create(
        engine="text-davinci-001",
        temperature=0.9,
        prompt=input_with_context,
        stop="\n---\n",
        n=4,
        max_tokens=100
    )
    list_of_choices = []
    for text in multiple_choices.get('choices'):
        list_of_choices.append(text.get('text'))
    
    return list_of_choices


if __name__ == "__main__":
    print(ai_text("Paris"))
