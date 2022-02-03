import json
from poems_ai import ai_text


def return_ai_result(news):
    with open("news.json", "r") as file:
        news_list = json.load(file)

    if news in news_list:
        print(f"{news} is in der json-Datei")
    else:
        news_list[news] = ai_text(news)
        with open("news.json", "w+") as file:
            json.dump(news_list, file)

    return news_list.get(news)


if "__main__" == "__main__":
    print(return_ai_result("What is the capital of France?"))
