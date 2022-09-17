from flask import Flask, render_template
# from input_handling import get_news_from_nyt, return_poem_and_image
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    with open("news.json", "r") as file:
        news_list = json.load(file)
    
    return render_template("home.html", news_list=news_list)

"""
@app.route("/<string:nyt_section>", methods=["GET"])
def section(nyt_section):
    newest_news = get_news_from_nyt(0, nyt_section) # 0 is the first article
    print(newest_news.get('title'))
    news_poems = return_poem_and_image(newest_news.get("title"))
    print(news_poems)
    return render_template("section.html", newest_news=newest_news, list_of_news=news_poems)
"""

if __name__ == "__main__":
    app.run(debug=True)
