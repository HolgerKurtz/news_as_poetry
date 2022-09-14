from cgitb import text
import requests
from dotenv import load_dotenv
import os
import warnings

# AI IMAGE PART
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io
import uuid

load_dotenv()
TEMPLATE_API_KEY = os.getenv("TEMPLATE_API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")

# POSTKIT
POSTKIT_TOKEN = os.getenv("POSTKIT_TOKEN")
POSTKIT_TEMPLATE_ID = os.getenv("POSTKIT_TEMPLATE_ID")

def generate_image(text, color):
    data = {
        "overrides": [
            {
            "name": "background-color",
            "stroke": "grey",
            "backgroundColor": color
            },
            {
            "name": "rect_content",
            "stroke": "grey",
            "backgroundColor": "#FFFFFF"
            },
            {
            "name": "poetry",
            "text": text,
            "textBackgroundColor": "rgba(246, 243, 243, 0)",
            "color": "#3D3D3D"
            },
            {
            "name": "line_1",
            "stroke": "grey",
            "strokeWidth": 3
            },
            {
            "name": "credits",
            "text": "more news as poetry @news_as_poetry (Instagram)",
            "textBackgroundColor": "rgba(246, 243, 243, 0)",
            "color": "#3D3D3D"
            }
        ]
        }

    response = requests.post(
        f"https://rest.apitemplate.io/v2/create-image?template_id={TEMPLATE_ID}",
        headers = {
            "X-API-KEY": f"{TEMPLATE_API_KEY}"
            },
        json= data
    )
    return response.json()

def generate_image_postkit(text):
    post_url = "https://api.postkit.co/make"
    data = {
        "id": POSTKIT_TEMPLATE_ID,
        "token": POSTKIT_TOKEN,
        "size": "1080x1080",
        "params": {
            "text_background": {
                "content":text
            },
        }
        }
    response = requests.post(
        post_url,
        json=data
    )
    if response.status_code == 200:
        with open(f"{text}.png", "wb") as file:
            file.write(response.content)
        return f"{text}.png"
    else:
        print("Error: ", response.status_code)
        print(response.text)
        return None

def create_ai_image(text_prompt, additional_info=None): # for ideas like ', digital art'
    """
    Takes Prompt and uses stability sdk / API to create an image
    """
    image_folder = "images/"
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'], 
        verbose=True,
    )
    # the object returned is a python generator
    answers = stability_api.generate(
        prompt=f"{text_prompt}, {additional_info}"
        # seed=34567, # if provided, specifying a random seed makes results deterministic
        # steps=30, # defaults to 50 if not specified
    )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img_name = str(uuid.uuid1())
                image_path = f"{image_folder}{img_name}.jpg" # images/text_prompt.jpg # for flask 
                img.save(f"static/{image_path}") #static/images/text_prompt.jpg 
    return image_path
if __name__ == "__main__":
    # generate_image_postkit("This is a test") 
    # generate_image("Test", "#dfb857").get('download_url')
    print(create_ai_image("a bestseller book, digital art"))