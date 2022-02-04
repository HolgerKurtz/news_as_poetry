# Simple Flask Web Server

# Import Flask
from flask import Flask, render_template

from input_handling import return_poem_and_image, get_news_from_nyt

# Create an instance of Flask
app = Flask(__name__)
# Create a route that renders index.html template


@app.route("/", methods=["GET", "POST"])
def index():
    newest_news = get_news_from_nyt()
    news_poems = return_poem_and_image(newest_news.get("title"))
    poem = news_poems.get("ai_text")
    image_url = news_poems.get("image_url")
    return render_template("index.html", newest_news=newest_news, poem=poem, image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
