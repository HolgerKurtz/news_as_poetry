from flask import Flask, render_template
from input_handling import get_news_from_nyt, return_poem_and_image

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    newest_news = get_news_from_nyt(0) # 0 is the first article
    news_poems = return_poem_and_image(newest_news.get("title"))
    return render_template("home.html", newest_news=newest_news, list_of_news=news_poems)

if __name__ == "__main__":
    app.run(debug=True)
