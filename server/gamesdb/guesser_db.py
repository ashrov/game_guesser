from logging import getLogger
from sqlite3 import Connection, Cursor, connect, IntegrityError

from .utils import Game, Tag
from .basic_db import BasicDataBase


logger = getLogger(__name__)


class GuesserDataBase(BasicDataBase):
    def __init__(self):
        super().__init__()

        self._all_tags = self._get_all_tags()
        self._all_games = self._get_all_games()

    @property
    def all_tags(self):
        return self._all_tags

    @property
    def all_games(self):
        return self._all_games

    @property
    def games_count(self):
        return len(self._all_games)

    def get_game_tags(self, game_id: int) -> set[Tag]:
        sql = "select * from tags where id in " \
              "(select tag_id FROM game_to_tag where game_id = ?)"
        self._cursor.execute(sql, (game_id, ))
        return {Tag().from_db_row(row) for row in self._cursor.fetchall()}

    def get_adjacent_tags(self, game) -> set[Tag]:
        sql = "select * from tags where question not null and id in " \
              "(select tag_id from game_to_tag where game_id = ?)"
        self._cursor.execute(sql, (game.id, ))
        return {Tag().from_db_row(row) for row in self._cursor.fetchall()}

    def get_games_with_tag(self, tag: Tag) -> set[Game]:
        if tag.id > 0:
            game_id_select_sql = "select game_id from game_to_tag where tag_id = ?"
            params = (tag.id, )
        else:
            game_id_select_sql = "select game_id from game_to_tag WHERE tag_id in " \
                                 "(select id from tags where tag_name = ?)"
            params = (tag.name, )

        sql = f"select * from games where id in ({game_id_select_sql})"
        self._cursor.execute(sql, params)

        return {Game().from_db_row(row, []) for row in self._cursor.fetchall()}

    def _get_all_tags(self) -> set[Tag]:
        sql = "select * from tags where question is not null"
        self._cursor.execute(sql)
        return {Tag().from_db_row(line) for line in self._cursor.fetchall()}

    def _get_all_games(self) -> set[Game]:
        sql = "select * from games"
        self._cursor.execute(sql)
        return {Game().from_db_row(line, []) for line in self._cursor.fetchall()}
