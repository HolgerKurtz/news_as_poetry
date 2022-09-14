import requests
from dotenv import load_dotenv
import os

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

if __name__ == "__main__":
    generate_image_postkit("This is a test") 
    generate_image("Test", "#dfb857").get('download_url')