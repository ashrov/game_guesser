import sqlite3
from time import sleep
from bs4 import BeautifulSoup
import requests

from utils import Game
from database import DataBase


MAIN_URL = "https://store.steampowered.com/search/?page={page_number}"
GAMES_COUNT_TO_PARSE = 1000


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
    name = html.find('div', id="appHubAppName", class_="apphub_AppName").text
    return name


def get_game_from_game_url(game_page_url: str) -> Game:
    game_page = requests.get(game_page_url)
    game_html = BeautifulSoup(game_page.text, "html.parser")

    tags = get_tags(game_html)
    try:
        reviews_count = get_reviews_count(game_html)
    except Exception as er:
        print(f"{er}. Cannot find reviews count. It was set to 0.")
        reviews_count = 0
    name = get_game_name(game_html)

    print("creating game...")
    return Game(name=name, tags=tags, reviews_count=reviews_count, steam_url=game_page_url)


def parse_main_page(page: int, db: DataBase) -> int:
    """ :return: count of parsed games """

    print(f"parsing {page} page...\n")
    url = MAIN_URL.format(page_number=page)
    main_page = requests.get(url)
    main_html = BeautifulSoup(main_page.text, "html.parser")
    games_urls = get_urls(main_html)

    games_count = 0
    for game_url in games_urls:
        print(f"parsing {game_url}")
        game = get_game_from_game_url(game_url)
        print(f"adding game ({game.name}) to db...")
        try:
            db.add_game(game)
        except sqlite3.IntegrityError:
            print("repeated games")
        else:
            games_count += 1
            print(f"Game added. Info:\n{game} added to db. \n"
                  f"Page: {page}. Games on page: {games_count}\n")
        sleep(0.5)

    return games_count


def start_parsing(db: DataBase):
    page_number = 1
    games_count = 0
    while games_count < GAMES_COUNT_TO_PARSE:
        games_count += parse_main_page(page_number, db)
        page_number += 1


if __name__ == "__main__":
    database = DataBase()
    savepoint_name = "parsing_start"
    try:
        database.set_savepoint(savepoint_name)
        database.delete_games()
        start_parsing(database)
        database.release_savepoint(savepoint_name)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: rollback db.")
        database.rollback_to_savepoint(savepoint_name)
    finally:
        database.disconnect()




