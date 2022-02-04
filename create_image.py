import requests, json
from dotenv import load_dotenv
import os

load_dotenv()
TEMPLATE_API_KEY = os.getenv("TEMPLATE_API_KEY")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")

def generate_image(text):
    data = {
        "overrides": [
            {
                "name": "background-color",
                "stroke": "grey",
                "backgroundColor": "#FFE100"
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

if __name__ == "__main__":
    url = generate_image("Test").get('download_url')
    print(url)

