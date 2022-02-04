from flask import Flask, render_template
from input_handling import return_list_of_poems

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    list_of_news = return_list_of_poems(3)
    return render_template("home.html", list_of_news=list_of_news)

if __name__ == "__main__":
    app.run(debug=True)
