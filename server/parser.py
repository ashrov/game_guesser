from time import sleep
from bs4 import BeautifulSoup
import requests

from gamesdb.utils import Game
from gamesdb.parser_db import ParserDataBase


MAIN_URL = "https://store.steampowered.com/search/?category1=998&page={page_number}"
RESULT_GAMES_COUNT = 10000
START_PAGE = 1
CLEAR_DB = False


def get_urls(html) -> list:
    urls_html = html.findAll('a', class_='search_result_row')
    urls = [data['href'] for data in urls_html]
    return urls


def get_reviews_count(html) -> int:
    try:
        popularity_html = html.find('meta', itemprop='reviewCount')
        reviews_count = int(popularity_html["content"])
    except Exception as er:
        print(f"{er}. Cannot find reviews count. It was set to 0.")
        reviews_count = 0
    return reviews_count


def get_tags(html) -> list:
    all_tags = html.findAll('a', class_='app_tag')
    return [data.text.strip() for data in all_tags]


def get_game_name(html) -> str:
    name = html.find('div', id="appHubAppName", class_="apphub_AppName")
    return name.text if name else None


def get_game_from_game_url(game_page_url: str) -> Game | None:
    game_page = requests.get(game_page_url)
    game_html = BeautifulSoup(game_page.text, "html.parser")

    tags = get_tags(game_html)
    reviews_count = get_reviews_count(game_html)
    name = get_game_name(game_html)

    if name and tags:
        return Game(name=name, tags=tags, reviews_count=reviews_count, steam_url=game_page_url)
    else:
        return None


def parse_main_page(page: int, db: ParserDataBase) -> int:
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
        if game and db.add_game(game):
            games_count += 1
            print(f"Game added ({game.name})\n"
                  f"Page: {page}. Games on page: {games_count}\n")

        sleep(0.2)

    return games_count


def start_parsing(db: ParserDataBase):
    page_number = START_PAGE
    games_count = 0 if CLEAR_DB else db.get_games_count()
    while games_count < RESULT_GAMES_COUNT:
        print(f"{games_count=}")
        games_count += parse_main_page(page_number, db)
        page_number += 1


if __name__ == "__main__":
    database = ParserDataBase()
    savepoint_name = "parsing_start"

    try:
        database.set_savepoint(savepoint_name)
        if CLEAR_DB:
            database.delete_games()
        start_parsing(database)
        database.release_savepoint(savepoint_name)
    except Exception as er:
        print(f"{er}. Rollback db.")
        database.rollback_to_savepoint(savepoint_name)
    finally:
        database.disconnect()
