from input_handling import get_news_from_nyt, return_poem_and_image
from random import choice
from instagram import post_insta_pic


def main():
    try:
        NYT_SECTIONS = ["home", "arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies", "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"]
        chosen_section = choice(NYT_SECTIONS)
        newest_news = get_news_from_nyt(0, chosen_section) # 0 is the first article
        headline = newest_news.get('title')
        news_poems = return_poem_and_image(newest_news.get("title"))

        recent_poem = news_poems[0] # {'ai_text': '\n\nThey were at work this day in the East,And work had commenced in the West,\n', 'image_url': 'images/7941d4b4-3510-11ed-9014-228e44f4b507.jpg'}
        CAPTION = f"{recent_poem.get('ai_text')}\n---\nIMAGE & POEM are created by AI.\nAnd based on this @nytimes HEADLINE:\n\n{headline}\n #AIimage #AIpoetry #nytimes #{chosen_section}"
        IMAGE = f"static/{recent_poem.get('image_url')}"
        post_insta_pic(IMAGE, CAPTION)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()