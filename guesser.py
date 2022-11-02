from database import DataBase
from utils import Game, Tag


db = DataBase()
all_tags = db.get_all_tags()


def search_games(tmp_game: Game) -> list[Game]:
    pass


def get_tag(tmp_game: Game) -> Tag:
    return Tag("", "")


def close():
    db.disconnect()


close()
