# Simple Flask Web Server

# Import Flask
from flask import Flask, render_template, request, redirect, url_for

from input_handling import return_ai_result, get_news_from_nyt

# Create an instance of Flask
app = Flask(__name__)
# Create a route that renders index.html template


@app.route("/", methods=["GET", "POST"])
def index():
    newest_news = get_news_from_nyt()
    news_poems = return_ai_result(newest_news.get("title"))
    return render_template("index.html", newest_news=newest_news, news_poems=news_poems)


if __name__ == "__main__":
    app.run(debug=True)
