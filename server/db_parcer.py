import time
from bs4 import BeautifulSoup
import requests

from utils import TagsList, Game
from database import DataBase


MAIN_URL = "https://store.steampowered.com/search/?page={page_number}&count=100"
PAGES_COUNT = 10  # games count is (pages_count * 100)


def get_urls(html) -> list:
    urls_html = html.findAll('a', class_='search_result_row')
    urls = [data['href'] for data in urls_html]
    return urls


def get_reviews_count(html) -> int:
    popularity_html = html.find('meta', itemprop='reviewCount')
    reviews_count = popularity_html["content"]
    return int(reviews_count)


def get_tags(html) -> list:
    all_tags = html.findAll('a', class_='app_tag')
    return [data.text.strip() for data in all_tags]


def get_game_name(html) -> str:
    all_names = html.findAll('div', class_="apphub_AppName")
    filtered_names = [name.text for name in all_names]
    return filtered_names[0]


def get_game_from_game_url(url: str) -> Game:
    game_page = requests.get(game_url)
    game_html = BeautifulSoup(game_page.text, "html.parser")

    tags = get_tags(game_html)
    reviews_count = get_reviews_count(game_html)
    name = get_game_name(game_html)

    print("creating game...")
    game = Game(name=name, tags=tags, reviews_count=reviews_count, steam_url=game_url)

    return game


db = DataBase()
db.drop_games()

for page_number in range(1, PAGES_COUNT + 1):
    print(f"parsing {page_number} / {PAGES_COUNT} page...\n")
    url = MAIN_URL.format(page_number=page_number)
    main_page = requests.get(url)
    main_html = BeautifulSoup(main_page.text, "html.parser")
    games_urls = get_urls(main_html)

    for game_url in games_urls:
        game = None
        while not game:
            try:
                game = get_game_from_game_url(game_url)
            except:
                print("Error while parsing game. Trying parse again...")

        print("adding game to db...")
        db.add_game(game)
        print(f"Game added. Info:\n{game} added to db\n")

db.disconnect()
