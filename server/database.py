import sqlite3
from sqlite3 import Connection, Cursor, connect

from utils import Game, Tag
import config


DB_TABLES = {
    "games": ("id INTEGER PRIMARY KEY",
              "game_name TEXT UNIQUE",
              "steam_url TEXT",
              "reviews_count INT"),
    "tags": ("id INTEGER PRIMARY KEY",
             "tag_name TEXT UNIQUE",
             "question TEXT",
             "usage_count INTEGER DEFAULT 0"),
    "game_to_tag": ("game_id INT",
                    "tag_id INT")
}


class DataBase:
    _connection: Connection
    _cursor: Cursor

    def __init__(self):
        self._connect()
        self._create_tables()

    def _create_tables(self):
        for table_name, columns in DB_TABLES.items():
            columns_sql = ", ".join(columns)
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            self._cursor.execute(sql)

    def delete_tables(self):
        for table_name in DB_TABLES.keys():
            sql = f"DROP TABLE {table_name}"
            self._cursor.execute(sql)

    def _connect(self):
        try:
            self._connection = connect(config.DATABASE_NAME)
        except Exception as er:
            print(f"unable to connect to {config.DATABASE_NAME}. {er}")
        else:
            print(f"{config.DATABASE_NAME} connected")
            self._cursor = self._connection.cursor()

    def execute(self, sql):
        self._connection.execute(sql)

    def set_savepoint(self, name):
        self._connection.execute(f"savepoint {name}")

    def release_savepoint(self, name):
        self._connection.execute(f"release savepoint {name}")

    def rollback_to_savepoint(self, name):
        self._connection.execute(f"rollback to savepoint {name}")

    def disconnect(self):
        self._cursor.close()
        self._connection.close()
        print(f"{config.DATABASE_NAME} disconnected")

    def delete_games(self):
        sqls = ("delete from games",
                "delete from game_to_tag",
                "update tags set usage_count = 0")
        for sql in sqls:
            self._cursor.execute(sql)

    def add_game(self, game: Game):
        self.set_savepoint("adding_game")

        sql = "insert into games (game_name, steam_url, reviews_count) values (?, ?, ?)"
        self._cursor.execute(sql, (game.name, game.steam_url, game.reviews_count))
        for tag_name in game.tags:
            self._link_tag_to_game(game, tag_name)

        self.release_savepoint("adding_game")

    def _link_tag_to_game(self, game: Game, tag_name: str):
        self._add_tag(tag_name)
        self.increment_usage(tag_name)
        sql = "insert into game_to_tag (game_id, tag_id) " \
              "select games.id, tags.id FROM games, tags where games.game_name = ? AND tags.tag_name = ?"
        self._cursor.execute(sql, (game.name, tag_name))

    def get_all_games(self) -> list[Game]:
        sql = "select * from games"
        self._cursor.execute(sql)
        return [Game().from_db_row(line, self._get_game_tags(line[0])) for line in self._cursor.fetchall()]

    def _get_game_tags(self, game_id: int) -> list[str]:
        sql = "select * from tags where id IN " \
              "(select tag_id FROM game_to_tag where game_id = ?)"
        self._cursor.execute(sql, (game_id, ))
        return [Tag().from_db_row(row) for row in self._cursor.fetchall()]

    def _get_tag_by_id(self, tag_id: int) -> Tag:
        sql = "select * from tags where id = ?"
        self._cursor.execute(sql, (tag_id, ))
        return Tag().from_db_row(self._cursor.fetchone())

    def get_all_tags(self) -> list[Tag]:
        sql = "select * from tags"
        self._cursor.execute(sql)
        return [Tag().from_db_row(line) for line in self._cursor.fetchall()]

    def _add_tag(self, tag_name: str):
        sql = f"insert into tags (tag_name) values (?)"
        try:
            self._cursor.execute(sql, (tag_name,))
        except sqlite3.IntegrityError:
            pass

    def increment_usage(self, tag):
        sql = f"update tags set usage_count = usage_count + 1 where tag_name = ?"
        self._cursor.execute(sql, (tag, ))

