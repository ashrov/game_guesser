from logging import getLogger

from sqlite3 import IntegrityError

from .utils import Game, Tag, User
from .basic_db import BasicDataBase


logger = getLogger(__name__)


class ParserDataBase(BasicDataBase):
    def delete_games(self):
        sqls = ("delete from games",
                "delete from game_to_tag",
                "update tags set usage_count = 0")
        for sql in sqls:
            self._cursor.execute(sql)

    def add_game(self, game: Game) -> int:
        self.set_savepoint("adding_game")

        sql = "insert into games (game_name, steam_url, reviews_count) values (?, ?, ?)"
        try:
            self._cursor.execute(sql, (game.name, game.steam_url, game.reviews_count))
        except IntegrityError:
            print("repeated game")
            return 0
        else:
            for tag_name in game.tags:
                self._link_tag_to_game(game.name, tag_name)
            self.release_savepoint("adding_game")
            return 1

    def _link_tag_to_game(self, game_name: str, tag_name: str):
        self._add_tag(tag_name)
        self.increment_usage(tag_name)
        sql = "insert into game_to_tag (game_id, tag_id) " \
              "select games.id, tags.id FROM games, tags where games.game_name = ? AND tags.tag_name = ?"
        self._cursor.execute(sql, (game_name, tag_name))

    def get_games_count(self):
        sql = "select count() from games"
        self._cursor.execute(sql)
        return self._cursor.fetchone()[0]

    def _add_tag(self, tag_name: str):
        sql = f"insert into tags (tag_name) values (?)"
        try:
            self._cursor.execute(sql, (tag_name,))
        except IntegrityError:
            pass

    def increment_usage(self, tag):
        sql = f"update tags set usage_count = usage_count + 1 where tag_name = ?"
        self._cursor.execute(sql, (tag, ))
