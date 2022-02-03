# Simple Flask Web Server

# Import Flask
from flask import Flask, render_template, request, redirect, url_for

from input_handling import return_ai_result

# Create an instance of Flask
app = Flask(__name__)
# Create a route that renders index.html template


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        news = "test"  # get_nyt_news()
        news_poems = return_ai_result(user_input)
        return render_template("index.html", news=news, news_poems=news_poems)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
