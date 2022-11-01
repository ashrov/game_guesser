import sqlite3
from sqlite3 import Connection, Cursor

from utils import Game, Tag
import config


class DataBase:
    _db: Connection
    _cursor: Cursor
    _connected: bool

    def __init__(self):
        self.connect()
        if not self._connected:
            raise ConnectionError

        self._create_tables()

    def _create_tables(self):
        for table_name, columns in config.DB_TABLES.items():
            columns_sql = ""
            for column in columns:
                columns_sql += f"{column}{', ' if column != columns[-1] else ''}"

            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            self._cursor.execute(sql)

    def connect(self):
        try:
            self._db = sqlite3.connect(config.DATABASE_NAME)
        except ConnectionError:
            print(f"unable to connect to {config.DATABASE_NAME}")
            self._connected = False
        else:
            print(f"{config.DATABASE_NAME} connected")
            self._connected = True
            self._cursor = self._db.cursor()

    def disconnect(self):
        self._cursor.close()
        self._db.close()
        self._connected = False
        print(f"{config.DATABASE_NAME} disconnected")

    def add_game(self, game: Game):
        sql = "INSERT INTO games (game_name, tags) VALUES (?, ?)"
        self._cursor.execute(sql, (game.name, game.tags))
        self._db.commit()

    def get_tags(self) -> list[Tag]:
        sql = "SELECT * from tags"
        self._cursor.execute(sql)
        tags = [Tag(*line) for line in self._cursor.fetchall()]
        return tags

    def add_tag(self, tag: Tag):
        sql = f"INSERT INTO tags (tag_name, question) VALUES (?, ?)"
        self._cursor.execute(sql, (tag.name, tag.question))
        self._db.commit()

    def increment_usage(self, tag: Tag):
        sql = f"UPDATE tags SET usage_count = usage_count + 1 WHERE tag_name = '{tag.name}'"
        self._cursor.execute(sql)
        self._db.commit()

